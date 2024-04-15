from bson import ObjectId
import bcrypt
from flask import render_template, request, redirect, session,Blueprint,flash,url_for
from flask_login import login_user, current_user
from .models import User
from . import mongo


auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the MongoDB collection to find the user
        user = mongo.db.users.find_one({'username': username})

        if user:
            print(user)
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                flash('Logged in successfully!', category='success')
                user = User.load_by_id(str(user['_id']))
                print(user)
                login_user(user, remember=True)
                return 'Login successful'
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password1')
        confirm_password = request.form.get('password2')

        # Check if passwords match
        if password != confirm_password:
            return 'Passwords do not match'

        # Check if the email is already registered
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            return 'Email is already registered'

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the database
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        mongo.db.users.insert_one(user_data)

        return 'Registration successful'

    return render_template('register.html')
