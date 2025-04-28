# app/routes/chat.py

from flask import Blueprint, request, jsonify
import openai
import os

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/ask', methods=['POST'])
def ask_chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    openai.api_key = os.getenv('OPENAI_API_KEY')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Use "gpt-4o" if you have access, or fallback to "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are Alex Taylor, a warm but professional productivity assistant helping Mungai Munene succeed."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500