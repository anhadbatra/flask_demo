from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from .models import User

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask'
    app.config['SECRET_KEY'] = 'your_secret_key'
    mongo.init_app(app)

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Load user from the database based on user_id
        return User.query.get(user_id)

    return app

def create_db(app):
    with app.app_context():
        # Your database creation logic goes here
        print("Created Database")


