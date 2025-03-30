from flask import Blueprint, request, jsonify
from app.emailservice import send_email

email_bp = Blueprint('email', __name__)

@email_bp.route('/send-email', methods=['POST'])
def send_email_route():
    data = request.get_json()
    try:
        send_email(data['email'], data['subject'], data['message'])
        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500