from flask.views import MethodView
from flask import jsonify, request
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
import uuid
from app.decorators import admin_access, login_required
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.orm.attributes import flag_modified
from datetime import timedelta, datetime
from app.extensions import db
from app.models.auth import User, Address
from app.utils import *

class RegistrationView(MethodView):

    def post(self):
        body = request.get_json()
        try:
            name = body.get('name')
            mobileNumber = body.get('mobileNumber')
            email = body.get('email')
            password = body.get('password')

            if not name:
                return jsonify({"error": "Name is required"}), 401

            if len(password) < 6:
                return jsonify({"error": "Password must be at least 6 characters long"}), 401

            if not email and not mobileNumber:
                return jsonify({"error": "Either email address or mobile number is required"}), 401

            if email:
                if not validate_email(email):
                    return jsonify({"error": "Please enter a valid email address"}), 401
                user = User.query.filter_by(email=email).first()
                if user:
                    return jsonify({"error": "User with this email already exists, please login"}), 400

            if mobileNumber:
                phoneNum = f'+91{str(mobileNumber)}'
                if not validate_number(phoneNum):
                    return jsonify({"error": "Invalid phone number"}), 401
                user = User.query.filter_by(mobileNumber=mobileNumber).first()
                if user:
                    return jsonify({"error": "User with this mobile number already exists, please login"}), 400

            # Create the public id
            public_id = str(uuid.uuid4())

            # Create new user object
            if mobileNumber:
                new_user = User(name=name.capitalize(), password=password, mobileNumber=mobileNumber, email=None, public_id=public_id)
            else:
                new_user = User(name=name.capitalize(), password=password, mobileNumber=None, email=email, public_id=public_id)
                message = f'Hi {name.capitalize()}, welcome to popscape.'
                send_email_to_user(email, message)
            
            # Add new user to the database
            db.session.add(new_user)
            db.session.commit()

            # Generate access and refresh tokens
            access_token_expires = timedelta(minutes=30) # Shorter expiry
            refresh_token_expires = timedelta(days=1) # Longer expiry
            access_token = create_access_token(identity=new_user.public_id, expires_delta=access_token_expires)
            refresh_token = create_refresh_token(identity=new_user.public_id, expires_delta=refresh_token_expires)

            return jsonify(
                {
                    "message": "User created successfully. Please check your inbox.",
                    "tokens": {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                }), 200

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"error": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Unexpected error", "message": str(e)}), 500

    @admin_access
    def delete(self):
        id = request.args.get('id')
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify("User deleted successfully", 204)
    
class LoginView(MethodView):

    def post(self):
        body = request.form
        try:
            name = body.get('name')
            mobileNumber = body.get('mobileNumber')
            email = body.get('email')
            password = body.get('password')

            if not name:
                return jsonify({"error": "Name is required"}), 401

            if len(password) < 6:
                return jsonify({"error": "Password must be at least 6 characters long"}), 401

            if not email and not mobileNumber:
                return jsonify({"error": "Either email address or mobile number is required"}), 401
            
            if email:
                user = User.query.filter_by(email = email).first()
                if not user:
                    return jsonify({"error": "User does not exist, please register"}), 401
            
            if mobileNumber:
                user = User.query.filter_by(mobileNumber=mobileNumber).first()
                if not user:
                    return jsonify({"error": "User doest not exist, please register"}), 401
            
            if (user.name == name.capitalize()):
                if check_password_hash(user.password, password):
                    
                    # This block will prevent from generating new token if the old one is still valid.
                    if 'token' in request.headers:
                        token = request.headers['token']
                        try:
                            data = decode_token(token)

                            # Calculate expiry based on header's 'exp' claim if present
                            token_expiry = datetime.utcfromtimestamp(data['exp'])
                            remaining_time = token_expiry - datetime.utcnow()

                            # If remaining time is sufficient (e.g., 1 minute buffer), reuse token
                            buffer_time = timedelta(minutes=1)  # Adjust buffer time as needed
                            if remaining_time > buffer_time:
                                return jsonify(
                                {   
                                    'message': 'Valid token, using existing one',
                                    'tokens': {
                                        'access_token': token,
                                    }
                                }), 201
                        except:
                            pass 

                    # Generate access and refresh tokens
                    access_token_expires = timedelta(minutes=30) # Shorter expiry
                    refresh_token_expires = timedelta(days=1) # Longer expiry
                    access_token = create_access_token(identity=user.public_id, expires_delta=access_token_expires)
                    refresh_token = create_refresh_token(identity=user.public_id, expires_delta=refresh_token_expires)
                    
                    return jsonify(
                    {   
                        'message': f'You are successfully logged in as {user.name}',
                        'tokens': {
                            'access_token': access_token,
                            'refresh_token': refresh_token
                        }
                    }), 201

                return jsonify({"error": "Wrong password entered"}), 401
            
            return jsonify({"error": "User name didn't match"}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500
                
class ChangeAdminAccess(MethodView):
    
    decorators = [admin_access]

    def post(self):
        body = request.form
        try:
            mobileNumber = body.get('mobileNumber')
            email = body.get('email')
            accessFlag = body.get('accessFlag')                
            
            if accessFlag == "True":
                accessFlag = True
            elif accessFlag == "False":
                accessFlag = False
            else:
                return jsonify({"error": "Wrong flag is being sent"})
            if mobileNumber: 
                user = User.query.filter_by(mobileNumber=mobileNumber).first()
            else:
                user = User.query.filter_by(email=email).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 401
            
            if accessFlag:
                if user.is_admin:
                    return jsonify({'error': f'{user.name} is already marked as admin'})
    
                user.is_admin = True
                db.session.commit()
                return jsonify({'succes': f'{user.name} is marked as admin'})
            
            if not accessFlag:
                if not user.is_admin:
                    return jsonify({'error': f'{user.name} is already revoked as admin'})
                
                user.is_admin = False
                db.session.commit()
                return jsonify({'succes': f'{user.name} is revoked as admin'})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
class AddressView(MethodView):

    decorators = [login_required]

    def get(self): 
        # Decoding the token to fetch the user
        token = request.headers['token']
        user_id = get_user_id(token)

        address_list = Address.query.filter_by(user_id=user_id).all()
        return jsonify([item.serialize() for item in address_list]), 200
    
    def post(self):
        try:
            # Decoding the token to fetch the user
            token = request.headers.get('token')
            if not token:
                return jsonify({"error": "Token is missing"}), 400

            user_id = get_user_id(token)
            if not user_id:
                return jsonify({"error": "Invalid token"}), 401

            body = request.get_json()
            if not body:
                return jsonify({"error": "Request body is missing"}), 400

            street = body.get("street")
            city = body.get("city")
            state = body.get("state")
            pincode = body.get("pincode")
            country = body.get("country")
            houseNo = body.get("houseNo")
            phone_number = body.get("phone_number")

            # Required fields validation
            if not street:
                return jsonify({"error": "Street is required"}), 400
            if not city:
                return jsonify({"error": "City is required"}), 400
            if not state:
                return jsonify({"error": "State is required"}), 400
            if not pincode:
                return jsonify({"error": "Pincode is required"}), 400
            if not country:
                return jsonify({"error": "Country is required"}), 400
            if not houseNo:
                return jsonify({"error": "House No is required"}), 400
            if not phone_number:
                return jsonify({"error": "Phone No is required"}), 400

            address_type = body.get("address_type", "home")
            isPrimary = body.get("isPrimary", False)

            address_details = {
                "street": street,
                "houseNo": houseNo,
                "city": city,
                "state": state,
                "pincode": pincode,
                "country": country,
                "address_type": address_type,
                "phone_number": phone_number,
                "isPrimary": isPrimary
            }

            address_list = Address.query.filter_by(user_id=user_id).all()
            if len(address_list) >= 10:
                return jsonify({"error": "Max 10 addresses are allowed"}), 400
            
            # Check if another primary address exists
            if isPrimary:
                primary_address = Address.query.filter(
                    Address.user_id == user_id,
                    func.json_extract(Address.meta_details, '$.isPrimary') == True
                ).first()
                if primary_address:
                    """ flag_modified: This function is used to notify SQLAlchemy that the JSON field has been modified. """
                    primary_address_details = primary_address.meta_details
                    primary_address_details['isPrimary'] = False
                    primary_address.meta_details = primary_address_details
                    flag_modified(primary_address, "meta_details")
                    db.session.commit()

            new_address = Address(user_id=user_id, meta_details=address_details)
            db.session.add(new_address)
            db.session.commit()
            return jsonify({"message": "Address added successfully"}), 201

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")
            # Return a 500 error with the error message
            return jsonify({"error": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Unexpected error", "message": str(e)}), 500
        
    def put(self):
        try:
            address_id = request.args.get("address_id")
            # Decoding the token to fetch the user
            token = request.headers.get('token')
            user_id = get_user_id(token)
            if not user_id:
                return jsonify({"error": "Invalid token"}), 401
            
            old_address = Address.query.filter_by(id=address_id).first()
            if not old_address:
                return jsonify({"error": "Address not found"}), 400
            old_address_details = old_address.meta_details

            body = request.get_json()
            if not body:
                return jsonify({"error": "Request body is missing"}), 400

            street = body.get("street", old_address_details.get('street'))
            city = body.get("city", old_address_details.get('city'))
            state = body.get("state", old_address_details.get('state'))
            pincode = body.get("pincode", old_address_details.get('pincode'))
            country = body.get("country", old_address_details.get('country'))
            houseNo = body.get("houseNo", old_address_details.get('houseNo'))
            phone_number = body.get("phone_number", old_address_details.get('phone_number'))
            address_type = body.get("address_type", old_address_details.get('address_type'))
            isPrimary = body.get("isPrimary", old_address_details.get('isPrimary', False))

            if old_address_details.get('isPrimary') != isPrimary and isPrimary == True:
                primary_address = Address.query.filter(
                    Address.user_id == user_id,
                    func.json_extract(Address.meta_details, '$.isPrimary') == True
                )
                if len(primary_address) > 1:
                    return jsonify({"error": "You have alredy one primary address"}), 400

            address_details = {
                "street": street,
                "houseNo": houseNo,
                "city": city,
                "state": state,
                "pincode": pincode,
                "country": country,
                "address_type": address_type,
                "phone_number": phone_number,
                "isPrimary": isPrimary
            }

            old_address.meta_details = address_details
            # flag_modified: This function is used to notify SQLAlchemy that the JSON field has been modified.
            flag_modified(old_address, "meta_details")
            db.session.commit()
            
            return jsonify({"message": "Address edited successfully"}), 201

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")
            # Return a 500 error with the error message
            return jsonify({"error": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Unexpected error", "message": str(e)}), 500
        
    def delete(self):
        try:
            address_id = request.args.get("address_id")
            # Decoding the token to fetch the user
            token = request.headers.get('token')
            user_id = get_user_id(token)
            if not user_id:
                return jsonify({"error": "Invalid token"}), 401
            old_address = Address.query.filter_by(id=address_id).first()
            if not old_address:
                return jsonify({"error": "Address not found"}), 400
            
            db.session.delete(old_address)
            db.session.commit()
            return jsonify({"message": "Address deleted successfully"}), 200
        
        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")
            # Return a 500 error with the error message
            return jsonify({"error": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "Unexpected error", "message": str(e)}), 500