import os
from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config_name=None):
    app = Flask(__name__)

    # Configuration
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["DATA_DIR"] = os.path.join(os.getcwd(), "data")

    jwt.init_app(app)

    # Import blueprints INSIDE function
    from app.api.auth import auth_bp
    from app.api.students import students_bp
    from app.api.health import health_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(students_bp, url_prefix="/api/students")
    app.register_blueprint(health_bp)

    return app