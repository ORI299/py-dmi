from flask import Flask, current_app, g, session
from flask_login import LoginManager
from database.database_modles import Database, User, Action, ActionType
from config import config

def get_db():
    if 'db' not in g:
        g.db = Database(config.SQLITE_DATABASE_FILEPATH, {})
    return g.db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

# Initialize the database
database = Database(config.SQLITE_DATABASE_FILEPATH, {})
app.config['DATABASE'] = database

@login_manager.user_loader
def load_user(user_id):
    # db = current_app.config['DATABASE']
    #TODO: user_id is always None for some reason
    print("load_user")
    try:
        user_id = session["user_id"]
    except:
        print("couldnt find user_id in session")
    db = get_db()

    # Attempt to load the user by user_id first (assuming user_id is a unique identifier)
    user = User(user_id=user_id)
    action = Action(ActionType.GET, user)
    user_from_db = db.execute_action(action)
    
    # If not found by user_id, try loading by email or name (if needed)
    if not user_from_db:
        user = User(email=user_id)
        action = Action(ActionType.GET, user)
        user_from_db = db.execute_action(action)
        
        if not user_from_db:
            user = User(name=user_id)
            action = Action(ActionType.GET, user)
            user_from_db = db.execute_action(action)

    return user_from_db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Import and register the blueprint
from .routes import bp as main_routes

app.register_blueprint(main_routes, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
