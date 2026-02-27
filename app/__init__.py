from flask import Flask
from app.extensions import jwt


def create_app(config_name="default"):
    app = Flask(__name__)   

    from app.config import config_by_name
    app.config.from_object(config_by_name[config_name])

    jwt.init_app(app)

    from app.api.auth import auth_bp
    from app.api.employees import employees_bp
    from app.api.health import health_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(employees_bp, url_prefix="/api/students")
    app.register_blueprint(health_bp, url_prefix="/api/health")

    return app