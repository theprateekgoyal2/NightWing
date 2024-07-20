from flask import Flask

from config import Config
from app.extensions import db, mail, bcrypt, login_manager, jwt_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt_manager.init_app(app)

    # Register blueprints here
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.popscape import popscape_bp
    app.register_blueprint(popscape_bp)

    # Initialize SQLAlchemy
    with app.app_context():
        db.create_all()
        app.run(debug=True)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
