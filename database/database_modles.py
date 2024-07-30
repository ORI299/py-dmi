import sqlite3
import hashlib
import os
from config import config
from flask_login import UserMixin

# Database file path
database_path = config.SQLITE_DATABASE_FILEPATH

class User(UserMixin):
    def __init__(self, user_id=None, name=None, email=None, password=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password  # Hash the password if provided
        self.id = "None"

    @staticmethod
    def hash_password(password):
        if type(password) == bytes:
            return password
        salt = os.urandom(32)  # Generate a new salt for each user
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + password_hash  # Store the salt and hash together

    @staticmethod
    def verify_password(stored_password, provided_password):
        salt = stored_password[:32]  # Extract the salt from the stored password
        stored_hash = stored_password[32:]  # Extract the hash from the stored password
        provided_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
        return provided_hash == stored_hash  # Compare provided password hash to stored hash

    def to_tuple(self):
        return (self.user_id, self.name, self.email, self.password)

    def get_id(self,):
        print("user: ")
        return str(self.user_id)

class ActionType:
    ADD = "add"
    REMOVE = "remove"
    EDIT = "edit"
    GET = "get"

class Action:
    def __init__(self, action_type, user=None):
        self.action_type = action_type
        self.user = user

class Database:
    def __init__(self, path, project_config):
        # Define vars
        self.path = path
        self.project_config = project_config
        # Connect to the SQLite database
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        # Create users table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                password BLOB
            )
        ''')
        self.connection.commit()

    def execute_action(self, action: Action):
        if action.action_type == ActionType.ADD:
            self.add_user(action.user)
        elif action.action_type == ActionType.REMOVE:
            self.remove_user(action.user.user_id)
        elif action.action_type == ActionType.EDIT:
            self.edit_user(action.user)
        elif action.action_type == ActionType.GET:
            return self.get_user(action.user)
        else:
            raise ValueError("Unknown action type")

    def add_user(self, user: User):
        try:
            # Insert the user data into the database
            self.cursor.execute('''
                INSERT INTO users (user_id, name, email, password) VALUES (?, ?, ?, ?)
            ''', user.to_tuple())
            self.connection.commit()
            print(f"User {user.name} added.")
        except sqlite3.IntegrityError:
            print(f"User with ID {user.user_id} already exists.")

    def remove_user(self, user_id):
        self.cursor.execute('''
            DELETE FROM users WHERE user_id = ?
        ''', (user_id,))
        self.connection.commit()
        print(f"User with ID {user_id} removed.")

    def edit_user(self, user: User):
        try:
            # Update user details in the database
            if user.name:
                self.cursor.execute('''
                    UPDATE users SET name = ? WHERE user_id = ?
                ''', (user.name, user.user_id))

            if user.email:
                self.cursor.execute('''
                    UPDATE users SET email = ? WHERE user_id = ?
                ''', (user.email, user.user_id))

            if user.password:
                hashed_password = User.hash_password(user.password)
                self.cursor.execute('''
                    UPDATE users SET password = ? WHERE user_id = ?
                ''', (hashed_password, user.user_id))

            self.connection.commit()
            print(f"User with ID {user.user_id} updated.")
        except Exception as e:
            print(f"Error updating user: {e}")

    def get_user(self, user: User):
        if user.email:
            string_query = "email"
            query = user.email
        elif user.user_id:
            string_query = "user_id"
            query = user.user_id
        elif user.name:
            string_query = "name"
            query = user.name
        else:
            raise ValueError("User must have an email, user_id, or name.")

        print(query)
        print(string_query)

        self.cursor.execute(f'SELECT * FROM users WHERE {string_query} = ?', (query,))
        row = self.cursor.fetchone()
        if row:
            return User(*row)  # Return User object with password as is
        else:
            print(f"User not found.")
            return None

    def fetch_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        rows = self.cursor.fetchall()
        return [User(*row) for row in rows]

    
    def close(self):
        self.connection.close()


    
# Example usage
def test():
    # This is an example usage DO NOT USE IN THIS FILE
    # unless you know what you are doing
    
    # Initialize the database
    project_config = {}
    database = Database(database_path, project_config)

    # Add a user
    user1 = User(user_id="1", name="Alice", email="alice@example.com", password="password123")
    action1 = Action(ActionType.ADD, user1)
    database.execute_action(action1)

    # Add another user
    user2 = User(user_id="2", name="Bob", email="bob@example.com", password="securepass")
    action2 = Action(ActionType.ADD, user2)
    database.execute_action(action2)

    # Edit a user
    user1_edit = User(user_id="1", name="Alice Smith", email="alice.smith@example.com", password="newpassword")
    action3 = Action(ActionType.EDIT, user1_edit)
    database.execute_action(action3)

    # Get a user
    action_get = Action(ActionType.GET, User(user_id="1"))
    user_data = database.execute_action(action_get)
    if user_data:
        print(f"Retrieved User - ID: {user_data.user_id}, Name: {user_data.name}, Email: {user_data.email}")

    # Remove a user
    action4 = Action(ActionType.REMOVE, User(user_id="2"))
    database.execute_action(action4)

    # Fetch all users to verify changes
    users = database.fetch_all_users()
    for user in users:
        print(f"User ID: {user.user_id}, Name: {user.name}, Email: {user.email}")

    # Close the database connection
    database.close()
