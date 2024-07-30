from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from database.database_modles import *
from app import get_db

bp = Blueprint('main', __name__)


app = bp


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    database = get_db()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        # get data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = User.hash_password(password)

        # create user as a class
        user = User(name=username, email=email, password=password)



        # check for existing users with the same attributes
        action = Action(ActionType.GET, user)
        action_result = database.execute_action(action)
        if action_result == None:
            action = Action(ActionType.ADD, user)
            action_result = database.execute_action(action)
            flash('Your account has been created!', 'success')
            return redirect(url_for('main.login'))
        else:
            if action_result.email != None:
                flash('That email already exists!', 'danger')
                return redirect(url_for('main.register'))
            if action_result.name != None:
                flash('That username already exists!', 'danger')
                return redirect(url_for('main.register'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    database = get_db()

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(email=email)

        action = Action(ActionType.GET, user)
        action_result = database.execute_action(action)

        #if check_password_hash(action_result.password, password):

        if action_result.password == password:
            session["user_id"] = str(action_result.user_id)
            login_user(user, remember=True)
            # TODO: make this work (get back to same page after login)
            
            # next_page = "main."
            # next_page += request.args.get('next')
            # return redirect(next_page) if next_page else redirect(url_for('main.home'))
            
            # a fix for now
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
