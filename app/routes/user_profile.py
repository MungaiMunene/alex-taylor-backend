# src/app/routes/user_profile.py

from flask import Blueprint, jsonify
from app.models import User

user_profile_bp = Blueprint('user_profile', __name__, url_prefix='/api')

@user_profile_bp.route('/user-profile', methods=['GET'])
def get_user_profile():
    user = User.query.first()
    if user:
        return jsonify(user.serialize()), 200
    else:
        return jsonify({"error": "No user found"}), 404