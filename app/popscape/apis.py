from flask.views import MethodView
from flask import jsonify, request
from app.models.popscape import Category, SubCategory, Products
from app.extensions import db
from app.utils import abbreviationFunc, generate_filename, sanitize_category, sanitize_name, sanitize_subProd
from app.misc import UPLOAD_FOLDER
from app.decorators import login_required, admin_access
from sqlalchemy.exc import SQLAlchemyError
import os

class CategoryView(MethodView):
    
    # To view all the categories present
    def get(self):
        try:
            categories = Category.query.all()
            if not categories:
                return jsonify({"message": "No categories found"}), 404
            categories_json = [category.serialize() for category in categories if category is not None]
            return jsonify(categories_json), 200

        except SQLAlchemyError as e:
            # Log the error message
            # log.error(f"Database error: {str(e)}")
            return jsonify({"message": "Database error", "message": str(e)}), 500

    # To add a new category
    # @admin_access
    def post(self):
        if not request.is_json:
            return jsonify({"message": "Invalid JSON"}), 400

        body = request.get_json()
        if not body:
            return jsonify({"message": "Request body is missing"}), 400

        try:
            name = body.get('name')
            
            if name == "":
                return jsonify({"message": "Name field can't be empty."}), 400

            if not name:
                return jsonify({"message": "Name field missing."}), 400
            
            name = sanitize_category(name)
            existing_categories = [category.name for category in Category.query.all()]
            if name in existing_categories:
                return jsonify({"message": "Category already exists."}), 400

            new_category = Category(name=name)
            db.session.add(new_category)
            db.session.commit()

            return jsonify({"message": "Category created successfully"}), 201
        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500
        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500
        
    # To edit a category
    # @login_required
    def put(self):
        id = request.args.get('id')
        if not id:
            return jsonify({"message": "ID parameter is missing"}), 400

        try:
            item = Category.query.get(id)
            if not item:
                return jsonify({"message": "No item found"}), 404

            if not request.is_json:
                return jsonify({"message": "Invalid JSON"}), 400

            data = request.get_json()
            if not data:
                return jsonify({"message": "Request body is missing"}), 400

            name = data.get('name')
            
            if name == "":
                return jsonify({"message": "Name field can't be empty."}), 400

            if not name:
                return jsonify({"message": "Name field missing."}), 400

            name = sanitize_category(name)
            # item.totalItems = data['totalItems']

            existing_categories = [category.name for category in Category.query.all() if category.id != id]
            if name in existing_categories:
                return jsonify({"message": "Category already exists."}), 400

            item.name = name
            db.session.commit() 
            return jsonify({"message":"Item edited successfully"}), 202

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500
        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500

    # To delete a category
    # @admin_access
    def delete(self):
        id = request.args.get('id')
        if not id:
            return jsonify({"message": "ID parameter is missing"}), 400

        try:
            item = Category.query.get(id)
            if not item:
                return jsonify({"message": "No item found"}), 404

            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Item deleted successfully"}), 204

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500
        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500
        
class SubCategoryView(MethodView):

    # To retrieve all sub-categorie(s) from a category
    def get(self):
        id = request.args.get('id')
        if not id:
            return jsonify({"message": "ID parameter is missing"}), 400
    
        try:
            category = Category.query.get(id)
            if not category:
                return jsonify({"message": "Category does not exist"}), 404
            
            subcategories = SubCategory.query.filter_by(category_id=id).all()
            if not subcategories:
                return jsonify({"message": "No Sub-Categories found"}), 404
            
            subcategories_json = [item.serialize() for item in subcategories if item is not None]
            return jsonify(subcategories_json), 200
        
        except SQLAlchemyError as e:
            # Log the error message
            # log.error(f"Database error: {str(e)}")
            return jsonify({"message": "Database error", "message": str(e)}), 500
    
    # To add sub-categorie(s) to a category
    # @admin_access
    def post(self):
        id = request.args.get('id')
        if not id:
            return jsonify({"message": "ID parameter is missing"}), 400
        try:
            body = request.get_json()
            if not body:
                return jsonify({"message": "Request body is missing"}), 400
            
            name = body.get('name')
            if name == "":
                return jsonify({"message": "Name field can't be empty."}), 400

            if not name:
                return jsonify({"message": "Name field missing."}), 400

            name = sanitize_name(name)

            release_year = body.get('releaseYear')
            if release_year == "":
                return jsonify({"message": "releaseYear field can't be empty."}), 400

            if not release_year:
                return jsonify({"message": "releaseYear field missing."}), 400

            category = Category.query.get(id)
            if not category:
                return jsonify({"message": "Category does not exist"}), 404

            if SubCategory.query.filter_by(category_id=id, name=name, releaseYear=release_year).first():
                return jsonify({"message": "Sub-Category already exists"}), 400

            abbreviation = abbreviationFunc(name, release_year)
            new_item = SubCategory(name=name, releaseYear=release_year, category_id=id, abbreviation=abbreviation)
            db.session.add(new_item)

            category.totalItems += 1
            db.session.commit()
            return jsonify({"message": "Sub-Category added successfully"}), 201

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500
        
    # To edit any sub-categorie(s)
    # @login_required
    def put(self):
        s_id = request.args.get('sid')
        if not s_id:
            return jsonify({"message": "S-ID parameter is missing."}), 400
        
        item = SubCategory.query.get(s_id)
        if not item:
            return jsonify({"message": "No Sub-Category found."}), 404

        try:
            body = request.get_json()
            if not body:
                return jsonify({"message": "Request body is missing."}), 400

            name = body.get('name', item.name)
            if name == "":
                return jsonify({"message": "Name field can't be empty."}), 400
            name = sanitize_name(name)

            releaseYear = body.get('releaseYear', item.releaseYear)
            if releaseYear == "":
                return jsonify({"message": "releaseYear field can't be empty."}), 400
            
            if SubCategory.query.filter_by(name=name, releaseYear=releaseYear).first():
                return jsonify({"message": "Sub-Category already exists."}), 400
            
            abbreviation = abbreviationFunc(name, releaseYear)

            if name is None or not isinstance(name, str):
                return jsonify({"message": "Invalid or missing 'name'"}), 400
            if releaseYear is None or not isinstance(releaseYear, int):
                return jsonify({"message": "Invalid or missing 'releaseYear'"}), 400

            item.name = name
            item.releaseYear = releaseYear
            item.abbreviation = abbreviation

            # if totalProducts is not None:
            #     item.totalProducts = totalProducts

            db.session.commit()
            return jsonify({"message": "Sub-Category edited successfully."}), 202
        
        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500
        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500
    
    # To delete any sub-categorie(s)
    # @admin_access
    def delete(self):
        id = request.args.get('id')
        s_id = request.args.get('sid')
        if not id:
            return jsonify({"message": "ID parameter is missing."}), 400
        if not s_id:
            return jsonify({"message": "SID parameter is missing."}), 400
        try:
            sub_item = SubCategory.query.get(s_id)
            item = Category.query.get(id)
            
            if not sub_item:
                return jsonify({"message": "No sub-item found."}), 404
            if not item:
                return jsonify({"message": "No item found."}), 404
            
            db.session.delete(sub_item)

            item.totalItems = item.totalItems-1

            db.session.commit()
            return jsonify("Item deleted successfully", 204)
        
        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500
        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500
     
class ProductsView(MethodView):
    
    # To retrieve all products form sub-category
    def get(self):
        # Get the 'id' parameter from the request arguments
        id = request.args.get('sid')
        if not id:
            return jsonify({"message": "ID parameter is missing"}), 400
        
        try:
            # Query the products that belong to the given subcategory ID
            ProductList = Products.query.filter_by(subCategory_id=id).all()
            # Check if there are no products for this sub-category
            if not ProductList:
                return jsonify({"message": "There are no product(s) for this sub-category"}), 404
            
            # Serialize the list of products
            ProductList_json = [item.serialize() for item in ProductList]
            
            # Query the subcategory to get additional information
            item = SubCategory.query.get(id)
            if not item:
                return jsonify({"message": "Sub-Category does not exist"}), 404
            
            # Get the names of the subcategory and category
            subcategory = item.name
            category = item.category.name
            
            # Define the path to store the file and add it to each product
            for subProd in ProductList_json:
                path = f'{UPLOAD_FOLDER}/{category}/{subProd["subProduct"]}/{subcategory}/{subProd["name"]}.png'
                subProd['url'] = path

            # Return the list of products with their URLs
            return jsonify(ProductList_json), 200
        
        except SQLAlchemyError as e:
            # Rollback in case of a database error and log it
            # log.error(f"Database error: {str(e)}")
            return jsonify({"message": "Database error", "message": str(e)}), 500
        
    # To add product(s) to sub-category
    @admin_access
    def post(self):
        # Check if 'id' parameter is provided in the request
        id = request.args.get('sid')
        if not id:
            return jsonify({"message": "ID parameter is missing"}), 400
        
        try:
            # Check if SubCategory with the given 'id' exists
            item = SubCategory.query.get(id)
            if not item:
                return jsonify({"message": "Sub-Category does not exist"}), 404

            # Check if a file is included in the request
            if 'File' not in request.files:
                return jsonify({"message": "File is missing"}), 400

            # Get the uploaded file
            file = request.files['File']
            if file.filename == '':
                return jsonify({"message": "No file selected"}), 400

            # Get and sanitize the 'subProduct' form data
            subProd = request.form.get('subProduct')
            if not subProd:
                return jsonify({"message": "subProduct is missing"}), 400

            subProd = sanitize_subProd(subProd)
            if not subProd:
                return jsonify({"message": "Invalid subProduct"}), 400
            
            # Get the price from form data
            price = request.form.get('price')
            if not price:
                if subProd == "Posters":
                    price = 590
                if subProd == "Polaroids": 
                    price = 280

            # Get category and article name
            category = item.category.name
            articleName = item.name

            # Check if the category is valid
            if category not in ['Movies', 'Shows', 'Music-Albums']:
                return jsonify({'error': 'Invalid category'}), 400

            # Create the folder to save the image if it doesn't exist
            save_folder = os.path.join(UPLOAD_FOLDER, category, subProd, articleName)
            os.makedirs(save_folder, exist_ok=True)

            # Extract file extension and generate a new filename
            filename, extension = os.path.splitext(file.filename)
            filename = generate_filename(item.abbreviation, item.totalProducts)
            file.save(os.path.join(save_folder, f'{filename}.png'))

            # Create and add the new product entry to the database
            product = Products(subCategory_id=id, name=filename, subProduct=subProd, price=price)
            db.session.add(product)

            # Increment the total products count and commit the transaction
            item.totalProducts += 1
            db.session.commit()
            return jsonify({'message': 'Image uploaded successfully', 'category': category, 'filename': filename, 'price': price})

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500

    # To replace a product file
    @login_required
    def put(self):
        # Check if 'sid' and 'pid' parameters are provided in the request
        sid = request.args.get('sid')
        pid = request.args.get('pid')
        if not sid:
            return jsonify({"message": "S-ID parameter is missing"}), 400
        if not pid:
            return jsonify({"message": "P-ID parameter is missing"}), 400

        try:
            # Check if the product with the given 'pid' exists
            product = Products.query.get(pid)
            if not product:
                return jsonify({"message": "Product does not exist"}), 404

            # Check if the subcategory with the given 'sid' exists
            subcategory = SubCategory.query.get(sid)
            if not subcategory:
                return jsonify({"message": "Category does not exist"}), 404

            # Check if a file is included in the request
            if 'File' not in request.files:
                return jsonify({"message": "File is missing"}), 400

            # Get the uploaded file
            file = request.files['File']
            if file.filename == '':
                return jsonify({"message": "No file selected"}), 400

            # Get the subProduct, category, price, filename, and article name
            subProd = product.subProduct
            oldprice = product.price
            category = subcategory.category.name
            articleName = subcategory.name
            filename = product.name

            # Check if the category is valid
            if category not in ['Movies', 'Shows', 'Music-Albums']:
                return jsonify({'error': 'Invalid category'}), 400
            
            # Get the price from form data
            price = request.form.get('price')
            if not price:
                if price == 0:
                    if subProd == "Posters":
                        price = 590
                    if subProd == "Polaroids": 
                        price = 280
                    # Update the price for product in the database
                    if product.price != price:
                        product.price = price
                        db.session.commit()

            if oldprice != price:
                # Update the price for product in the database
                product.price = price
                db.session.commit()

            # Fetch the folder where the image needs to be replaced
            save_folder = os.path.join(UPLOAD_FOLDER, category, subProd, articleName)
            os.makedirs(save_folder, exist_ok=True)

            # Save the replaced file with the existing filename
            file.save(os.path.join(save_folder, f'{filename}.png'))

            return jsonify({'message': 'Image replaced successfully', 'category': category, 'filename': filename})
        
        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500
        
    @admin_access
    def delete(self):
        # Check if 'sid' and 'pid' parameters are provided in the request
        sid = request.args.get('sid')
        pid = request.args.get('pid')
        if not sid:
            return jsonify({"message": "S-ID parameter is missing"}), 400
        if not pid:
            return jsonify({"message": "P-ID parameter is missing"}), 400
        
        try:
            subcategory = SubCategory.query.get(sid)
            if not subcategory:
                return jsonify({"message": "subcategory does not exist"}), 404
            
            product = Products.query.get(pid)
            if not product:
                return jsonify({"message": "Product does not exist"}), 404

            # Delete the product from the database
            db.session.delete(product)
            subcategory.totalProducts -= 1
            db.session.commit()

            # Delete the corresponding image file from the filesystem
            category = subcategory.category.name
            subProd = product.subProduct

            file_path = os.path.join(UPLOAD_FOLDER, category, subProd, subcategory.name, f'{product.name}.png')
            if os.path.exists(file_path):
                os.remove(file_path)
                return jsonify({'message': 'Product deleted successfully'}), 200
            else:
                return jsonify({'error': 'Image file not found'}), 404

        except SQLAlchemyError as e:
            # Rollback the transaction in case of a database error
            db.session.rollback()
            # Log the error message
            # log.error(f"Database error: {str(e)}")s
            # Return a 500 error with the error message
            return jsonify({"message": "Database error", "message": str(e)}), 500

        except Exception as e:
            # Log the error message
            # log.error(f"Unexpected error: {str(e)}")
            return jsonify({"message": "Unexpected error", "message": str(e)}), 500