from flask import Blueprint, request, session
from twilio.twiml.messaging_response import MessagingResponse
from app.models import Project, Metric
import random

whatsapp_bp = Blueprint('whatsapp', __name__, url_prefix='/whatsapp')

# Helper function for random greeting
def get_greeting():
    greetings = ["Hello!", "Hi there!", "Hey! How's it going?"]
    return random.choice(greetings)

@whatsapp_bp.route('/', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body').lower().strip()
    resp = MessagingResponse()
    msg = resp.message()

    user_name = session.get('user_name', 'there')  # Use session to remember the user's name

    # Greet the user and ask for action
    if "hello" in incoming_msg or "hi" in incoming_msg:
        msg.body(f"{get_greeting()} {user_name}! How can I assist you today? Send 'projects' for your projects or 'metrics' for your metrics.")
    elif "projects" in incoming_msg:
        projects = Project.query.all()
        if projects:
            projects_list = "\n".join([f"- {p.name}" for p in projects])
            msg.body(f"📁 *Your Projects:*\n{projects_list}")
        else:
            msg.body("You don't have any projects at the moment.")
    elif "metrics" in incoming_msg:
        metrics = Metric.query.all()
        if metrics:
            metrics_list = "\n".join([f"- {m.name}: {m.value}" for m in metrics])
            msg.body(f"📊 *Current Metrics:*\n{metrics_list}")
        else:
            msg.body("No metrics have been defined yet.")
    elif "consultant" in incoming_msg or "help" in incoming_msg:
        msg.body(f"Connecting you to a consultant, {user_name}...")
        # Logic for contacting a consultant could be here
    elif "my name is" in incoming_msg:
        user_name = incoming_msg.split("is")[-1].strip()
        session['user_name'] = user_name  # Store name in session
        msg.body(f"Nice to meet you, {user_name}! How can I assist you further?")
    else:
        msg.body(f"Sorry {user_name}, I didn't understand that. Please type 'projects' to see your projects or 'metrics' to get your metrics.")

    return str(resp)