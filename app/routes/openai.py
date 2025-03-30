import openai
from flask import Blueprint, request, jsonify
from app import app

openai_bp = Blueprint('openai', __name__)

@openai_bp.route('/summarize-email', methods=['POST'])
def summarize_email():
    data = request.get_json()
    prompt = f"Summarize the following email: {data['email_content']}"
    openai.api_key = app.config['OPENAI_API_KEY']
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return jsonify({"summary": response.choices[0].text.strip()}), 200