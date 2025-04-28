# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from twilio.rest import Client
import openai
from flask_cors import CORS
from zoneinfo import ZoneInfo

# Import Blueprints at top level
from app.routes.chat import chat_bp

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Twilio config
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# OpenAI config
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # Core configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key_here')

    # CORS configuration with specific allowed origins
    CORS(app, resources={r"/api/*": {
        "origins": [
            "http://localhost:5174",  # Updated to match your actual Vite dev server port
            "https://your-frontend-url.com"  # Placeholder for production (replace later)
        ],
        "supports_credentials": True,
        "allow_headers": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }})

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Scheduler setup for morning messages
    scheduler = BackgroundScheduler()
    scheduler.start()

    @app.route('/')
    def home():
        return 'Welcome to Alex Taylor!'

    # Import and register blueprints
    from app.routes.clients import clients_bp
    from app.routes.projects import projects_bp
    from app.routes.metrics import metrics_bp
    from app.routes.reports import reports_bp
    from app.routes.drivers import drivers_bp
    from app.routes.whatsapp import whatsapp_bp
    from app.routes.auth import auth_bp
    from app.routes.contracts import contracts_bp
    from app.routes.user_profile import user_profile_bp

    app.register_blueprint(clients_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(whatsapp_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contracts_bp)
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(chat_bp)  # Register the chat blueprint

    # Morning message task
    def send_morning_message():
        print(f"Sending morning message at {datetime.now()}")
        openai.api_key = OPENAI_API_KEY
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt="Generate a motivational message for a productive day.",
                max_tokens=60
            )
            message = response.choices[0].text.strip()
            sent = twilio_client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to="+254768651228"
            )
            print(f"Message sent: {sent.sid}")
        except Exception as e:
            print(f"Failed to send message: {str(e)}")

    scheduler.add_job(func=send_morning_message, trigger="cron", hour=8, minute=0)

    return app