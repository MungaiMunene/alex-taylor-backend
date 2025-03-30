from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # For database migrations
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Load environment variables from the .env file
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize database migrations

    # Define root route
    @app.route('/')
    def home():
        return 'Welcome to Alex Taylor!'  # Placeholder response, can be replaced with a template

    # Import blueprints for different modules
    from app.routes.clients import clients_bp
    from app.routes.projects import projects_bp
    from app.routes.metrics import metrics_bp
    from app.routes.reports import reports_bp
    from app.routes.drivers import drivers_bp
    from app.routes.whatsapp import whatsapp_bp

    # Register blueprints to handle different routes
    app.register_blueprint(clients_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(whatsapp_bp)

    return app