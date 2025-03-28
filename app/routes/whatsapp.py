# app/routes/whatsapp.py

from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from app.models import Project, Metric

whatsapp_bp = Blueprint('whatsapp', __name__, url_prefix='/whatsapp')

@whatsapp_bp.route('/', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body').lower().strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == "projects":
        projects = Project.query.all()
        projects_list = "\n".join([f"- {p.name}" for p in projects])
        msg.body(f"📁 *Your Projects:*\n{projects_list}")
    elif incoming_msg == "metrics":
        metrics = Metric.query.all()
        metrics_list = "\n".join([f"- {m.name}: {m.value}" for m in metrics])
        msg.body(f"📊 *Current Metrics:*\n{metrics_list}")
    else:
        msg.body("👋 Hello! Send 'projects' or 'metrics' to get real-time updates from Alex Taylor.")

    return str(resp)