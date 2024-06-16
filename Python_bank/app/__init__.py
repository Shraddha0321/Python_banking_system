from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

mongo = PyMongo()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mongo.init_app(app)
    jwt.init_app(app)

    # Debug prints
    print(f'MongoDB URI: {app.config["MONGO_URI"]}')
    print(f'MongoDB initialized: {mongo.db}')

    from app.controllers.auth_controller import auth_bp
    from app.controllers.transaction_controller import transaction_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(transaction_bp, url_prefix='/transaction')

    return app
