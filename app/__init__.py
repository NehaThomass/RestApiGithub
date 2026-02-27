import os
from flask import Flask
from flask_jwt_extended import JWTManager
from app.api.employees import employees_bp

jwt = JWTManager()

def create_app(config_name=None):
    app = Flask(__name__)

    # Basic Configuration
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    app.config["DATA_DIR"] = os.path.join(os.getcwd(), "data")

    # Initialize JWT
    jwt.init_app(app)

    # Register Blueprint
    app.register_blueprint(employees_bp, url_prefix="/employees")

    # Home route
    @app.route("/")
    def home():
        return {"message": "Employee API is running"}

    return app