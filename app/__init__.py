from flask import Flask
from app.extensions import jwt
from app.config import config_by_name


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)

    # Safe configuration loading
    config = config_by_name.get(config_name)
    if config is None:
        config = config_by_name["development"]

    app.config.from_object(config)

    # Initialize extensions
    jwt.init_app(app)

    # Import blueprints
    from app.api.auth import auth_bp
    from app.api.health import health_bp
    from app.api.employees import employees_bp

    # Register blueprints
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(employees_bp, url_prefix="/api/v1/employees")

    # Error handlers
    try:
        from app.errors import register_error_handlers
        register_error_handlers(app)
    except Exception:
        pass

    @app.route("/")
    def home():
        return {
            "message": "Employee REST API is running. Use /api/v1/... endpoints."
        }

    return app