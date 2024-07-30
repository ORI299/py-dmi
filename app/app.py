# # Import routes after initializing app to avoid circular imports
# 
# from flask import Flask, render_template, redirect, url_for, request, flash
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# 
# 
# # Initialize Flask application
# flask_app = Flask(__name__)
# flask_app.config['SECRET_KEY'] = 'your_secret_key'
# 
# 
# # Initialize Flask-Login
# login_manager = LoginManager(flask_app)
# login_manager.login_view = 'login'
# 
# 
# # load routes
# from app.routes import *
# 
# 
# 
# 
# if __name__ == '__main__':
#     app.run(debug=True)# 

