from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

from app.auth.apis import *

auth_bp.add_url_rule('/register', view_func=RegistrationView.as_view("Register"), methods=['POST', 'DELETE'])
auth_bp.add_url_rule('/login', view_func=LoginView.as_view("Login"), methods=['POST'])
auth_bp.add_url_rule('/changeAdminAccess', view_func=ChangeAdminAccess.as_view("ChangeAdminAccess"), methods=['POST'])