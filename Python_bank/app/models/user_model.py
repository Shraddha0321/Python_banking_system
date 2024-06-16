from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo


class User:
    @staticmethod
    def create_user(username, password,name,mobile):
        try:
            hashed_password = generate_password_hash(password)
            user_id = mongo.db.users.insert_one({
                'username': username,
                'password': hashed_password,
                'name': name,
                'mobile': mobile,
                'balance': 0
            }).inserted_id
            return str(user_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_user_by_username(username):
        try:
            user = mongo.db.users.find_one({'username': username})
            return user
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @staticmethod
    def get_user_by_userId(userId):
        try:
            user = mongo.db.users.find_one({'_id': userId})
            return user
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def update_by_userId(userId,amount):
        try:
            data = mongo.db.users.update_one({'_id': userId}, {'$set': {'balance': amount}})
            return data
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @staticmethod
    def verify_password(stored_password, provided_password):
        try:
            return check_password_hash(stored_password, provided_password)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @staticmethod
    def get_all_users():
        try:
            users = mongo.db.users.find()
            return list(users)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @staticmethod
    def get_all_transactions1():
        try:
            users = mongo.db.transactions.find()
            return list(users)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @classmethod
    def find_one(cls, param):
        pass
