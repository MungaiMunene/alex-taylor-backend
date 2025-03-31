from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token

# Initialize the blueprint
auth_bp = Blueprint('auth', __name__)

# Route to login and return JWT token
@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username != 'admin' or password != 'admin':  # Example check
        return jsonify({'msg': 'Bad username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Route to register a new user (you can expand this)
@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Add logic to store the user credentials (hashed password etc.)
    return jsonify({'msg': f'User {username} registered successfully.'}), 201