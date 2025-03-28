from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # ✅ ADD THIS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()  # ✅ ADD THIS

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)  # ✅ INITIALIZE MIGRATIONS

    # Import blueprints
    from app.routes.clients import clients_bp
    from app.routes.projects import projects_bp
    from app.routes.metrics import metrics_bp
    from app.routes.reports import reports_bp
    from app.routes.drivers import drivers_bp  # ✅ ADD THIS
    from app.routes.whatsapp import whatsapp_bp  # ✅ ADD THIS

    # Register blueprints
    app.register_blueprint(clients_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(drivers_bp)  # ✅ REGISTER NEW ROUTE
    app.register_blueprint(whatsapp_bp)  # ✅ REGISTER WHATSAPP ROUTE

    return app
