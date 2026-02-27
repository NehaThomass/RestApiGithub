"""
Application entry point.
"""
import os
from app import create_app

config_name = os.environ.get("FLASK_ENV", "development")
app = create_app(config_name)

if _name_ == "_main_":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)