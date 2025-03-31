from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # For database migrations
from dotenv import load_dotenv  # To load environment variables from the .env file
import os
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler  # Import the scheduler
from datetime import datetime
from twilio.rest import Client
import openai

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Initialize Twilio client
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def create_app():
    # Load environment variables from the .env file
    load_dotenv()

    app = Flask(__name__)

    # Flask configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')  # Database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key_here')  # Secret key for JWT

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize database migrations
    jwt.init_app(app)  # Initialize JWT for authentication

    # Set up APScheduler for background tasks
    scheduler = BackgroundScheduler()
    scheduler.start()  # Start the scheduler

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
    from app.routes.auth import auth_bp  # Import the authentication blueprint

    # Register blueprints to handle different routes
    app.register_blueprint(clients_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(whatsapp_bp)
    app.register_blueprint(auth_bp)  # Register the auth blueprint

    # Define a background task to send morning messages
    def send_morning_message():
        print(f"Sending morning message at {datetime.now()}")  # Replace with actual message-sending logic
        
        # Generate the message using OpenAI API
        openai.api_key = OPENAI_API_KEY
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Generate a motivational message for a productive day.",
            max_tokens=60
        )
        message = response.choices[0].text.strip()

        # Send the message using Twilio
        try:
            message = twilio_client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to="your_phone_number"  # Replace with the recipient's phone number
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Failed to send message: {str(e)}")

    # Add the background task to the scheduler to run daily at 8:00 AM
    scheduler.add_job(func=send_morning_message, trigger="cron", hour=8, minute=0)

    return app