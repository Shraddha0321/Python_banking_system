from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user_model import User
import re

def validate_mobile(mobile):
    return re.match(r'^\+?\d{10,15}$', mobile)
def register_user():
    try:
        data = request.get_json()
        name = data.get('name')
        mobile = data.get('mobile')
        username = data.get('username')
        password = data.get('password')

        if not all([name, mobile, username, password]):
            return jsonify({"msg": "All fields are required: name, mobile, username, password"}), 400

        if not validate_mobile(mobile):
            return jsonify({"msg": "Invalid mobile number format"}), 400

        if len(password) < 6:
            return jsonify({"msg": "Password must be at least 6 characters long"}), 400

        if not username or not password:
            return jsonify({"msg": "Username and password are required"}), 400

        if User.get_user_by_username(username):
            return jsonify({"msg": "Username already exists"}), 400


        user_id = User.create_user(username, password,name,mobile)
        return jsonify({"msg": "User created", "user_id": user_id,"username": username}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"msg": "Username and password are required"}), 400

        user = User.get_user_by_username(username)
        if not user or not User.verify_password(user['password'], password):
            return jsonify({"msg": "Invalid credentials"}), 401

        # Check if 'name' key exists, otherwise handle it
        identity = {
            "user_id": str(user['_id']),
            "name": user['name'],
            "username": user['username']
        }
        # Default to 'Unknown' if 'name' key is missing
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500