from flask import jsonify
from .. import mongo
from datetime import datetime

class Transaction:
    @staticmethod
    def create_transaction(user_id, tran_type, amount, total):
        try:
            transaction_id = mongo.db.transactions.insert_one({
                "User_id": user_id,
                "Type": tran_type,
                "Amount": amount,
                "Timestamp": datetime.utcnow(),
                "Total Balance": total
            }).inserted_id
            return str(transaction_id)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_transactions_by_userId(user_id):
        data = mongo.db.transactions.find({'User_id': user_id})
        transactions_list = list(data)
        for transaction in transactions_list:
            transaction['_id'] = str(transaction['_id'])
            transaction['User_id'] = str(transaction['User_id'])
        return transactions_list

    @staticmethod
    def update_balance(user_id, amount, operation):
        user = mongo.db.users.find_one({'_id': user_id})
        if operation == 'deposit':
            new_balance = user['balance'] + amount
        elif operation == 'withdraw' and user['balance'] >= amount:
            new_balance = user['balance'] - amount
        else:
            return None
        mongo.db.users.update_one({'_id': user_id}, {'$set': {'balance': new_balance}})
        return new_balance

    @staticmethod
    def get_all_transactions(user_id):
        try:
            data = mongo.db.transactions.find()
            transactions_list = list(data)
            for transaction in transactions_list:
                transaction['_id'] = str(transaction['_id'])
                transaction['User_id'] = str(transaction['User_id'])
            return transactions_list
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def get_balance(user_id):
        try:
            user = mongo.db.users.find_one({'_id': user_id})
            return user['balance'] if user else None
        except Exception as e:
            return jsonify({"error": str(e)}), 500