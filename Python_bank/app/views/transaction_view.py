import datetime
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transaction_model import Transaction
from app.models.user_model import User
from bson import ObjectId

def convert_object_ids(obj):
    if isinstance(obj, list):
        return [convert_object_ids(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_object_ids(value) for key, value in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

@jwt_required()
def deposit():
    try:
        data = request.get_json()
        amount = data.get('amount')

        if amount <= 0:
            return jsonify({"msg": "Deposit amount must be greater than zero"}), 400

        user_identity = get_jwt_identity()
        user_id = ObjectId(user_identity['user_id'])
        user = User.get_user_by_userId(user_id)

        new_balance = user['balance'] + amount
        User.update_by_userId(user_id, new_balance)

        Transaction.create_transaction(user_id, "Deposit", amount, new_balance)

        return jsonify({"msg": "Deposit successful", "new_balance": new_balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jwt_required()
def withdraw():
    try:
        data = request.get_json()
        amount = data.get('amount')

        if amount is None or amount <= 0:
            return jsonify({"msg": "Invalid amount"}), 400

        user_identity = get_jwt_identity()
        user_id = ObjectId(user_identity['user_id'])
        user = User.get_user_by_userId(user_id)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        if user['balance'] < amount:
            return jsonify({"msg": "Insufficient balance"}), 400

        new_balance = user['balance'] - amount
        User.update_by_userId(user_id, new_balance)
        Transaction.create_transaction(user_id, "Withdraw", amount, new_balance)

        return jsonify({"msg": "Withdraw successful", "new_balance": new_balance}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@jwt_required()
def balance_check():
    try:
        user_identity = get_jwt_identity()
        user_id = ObjectId(user_identity['user_id'])
        user = User.get_user_by_userId(user_id)
        print(user)
        if user is None:
            user_data = {
                "user_id": user_identity['user_id'],
                "username": user_identity.get('username', 'unknown'),
                "balance": 0
            }
            return jsonify({"msg": "User not found", "user": user_data}), 404

        user_data = {
            "user_id": str(user['_id']),
            "username": user.get('username'),
            "balance": user.get('balance')
        }

        return jsonify({"user": user_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jwt_required()
def transaction_history():
    try:
        user_identity = get_jwt_identity()
        user_id = ObjectId(user_identity['user_id'])
        print(user_id)
        transactions = Transaction.get_transactions_by_userId(user_id)
        return jsonify({"history": transactions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@jwt_required()
def all_users():
    try:
        users = User.get_all_users()
        users_list = list(users)

        users_list = convert_object_ids(users_list)

        return jsonify(accounts=users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@jwt_required()
def all_transactions():
    try:
        users = User.get_all_transactions1()
        users_list = list(users)

        # Convert all ObjectId fields to strings
        users_list = convert_object_ids(users_list)

        return jsonify(all_transactions=users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


