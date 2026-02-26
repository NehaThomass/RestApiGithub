from app.api.employees import employees_bp
app.register_blueprint(employees_bp, url_prefix="/employees")