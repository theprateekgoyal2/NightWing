from functools import wraps
from flask import request, jsonify
from app.models.auth import User
from flask_jwt_extended import decode_token
import jwt

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # Decoding the payload to fetch the stored details
            data = decode_token(token)

            # Fetch user from the database using public_id
            current_user = User.query.filter_by(public_id=data['sub']).first()

            if not current_user:
                return jsonify({'message': 'User not found'}), 401

            # Pass the current user to the decorated function
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired !!'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token !!'}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return decorated

def admin_access(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'token' in request.headers:
            token = request.headers['token']

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # Decoding the payload to fetch the stored details
            data = decode_token(token)

            # Fetch user from the database using public_id
            current_user = User.query.filter_by(public_id=data['sub']).first()

            if not current_user:
                return jsonify({'message': 'User not found'}), 401
            
            if not current_user.is_admin: 
                return jsonify({'message': 'You do not have access !!'}), 401

            # Pass the current user to the decorated function
            return f(*args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired !!'}), 401

        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token !!'}), 401

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    return decorated