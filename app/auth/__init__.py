from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/user')

from app.auth.apis import *

auth_bp.add_url_rule('/register', view_func=RegistrationView.as_view("Register"), methods=['GET', 'POST', 'DELETE'])
auth_bp.add_url_rule('/login', view_func=LoginView.as_view("Login"), methods=['POST', 'GET'])
auth_bp.add_url_rule('/changeAdminAccess', view_func=ChangeAdminAccess.as_view("ChangeAdminAccess"), methods=['POST'])
auth_bp.add_url_rule('/addresslist', view_func=AddressView.as_view("AddressView"), methods=['GET','POST', 'PUT', 'DELETE'])