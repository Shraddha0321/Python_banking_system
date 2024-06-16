from flask import Blueprint
from app.views.transaction_view import deposit, withdraw, balance_check, transaction_history, all_users, all_transactions

transaction_bp = Blueprint('transaction', __name__)

transaction_bp.route('/deposit', methods=['POST'])(deposit)
transaction_bp.route('/withdraw', methods=['POST'])(withdraw)
transaction_bp.route('/balance', methods=['GET'])(balance_check)
transaction_bp.route('/history', methods=['GET'])(transaction_history)
transaction_bp.route('/all_accounts', methods=['GET'])(all_users)
transaction_bp.route('/all_transactions', methods=['GET'])(all_transactions)
