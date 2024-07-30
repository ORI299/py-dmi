// tried to do this with chatgpt, didnt work 100%
TODO: fix this file 
```DATABASE_PROJECT.md```markdown
```markdown
# Database Project Documentation

## Overview

This project provides a simple SQLite-based database implementation in Python to manage user data. It includes functionality to add, remove, edit, and retrieve users, with secure password handling using hashing and salting.

## Requirements

- Python 3.6 or higher
- SQLite (comes bundled with Python)

## File Structure

- `database/modles.py`: Contains classes for managing the database and user data.
- `config.py`: Configuration file for database path.
- `database/readme.md`: This documentation file.

## Configuration

### `config.py`

```python
SQLITE_DATABASE_FILEPATH = 'path/to/database.sqlite'
```

## Classes User

Represents a user in the database with secure password handling.Methods

```__init__(self, user_id=None, name=None, email=None, password=None)```Initializes a ```User``` instance.```password``` is hashed if provided.

```hash_password(password)```Hashes the given password with a salt using PBKDF2 and SHA-256.

```verify_password(stored_password, provided_password)```Verifies if the provided password matches the stored hashed password.

```to_tuple()```Returns user attributes as a tuple for database insertion.```ActionType```

Defines constants for different types of actions.```ADD```: Add a new user.```REMOVE```: Remove an existing user.```EDIT```: Update user details.```GET```: Retrieve user details.```Action```

Encapsulates an action to be performed on the database.Methods```__init__(self, action_type, user=None)```Initializes an ```Action``` instance with a type and optional ```User``` object.```Database```

Manages SQLite database operations and interactions.Methods

```__init__(self, path, project_config)```Initializes the database connection and creates necessary tables.

```create_table()```Creates the ```users``` table if it does not exist.

```execute_action(self, action: Action)```Executes the specified action (add, remove, edit, or get).

```add_user(self, user: User)```Adds a new user to the database.

```remove_user(self, user_id)```Removes a user by ID from the database.

```edit_user(self, user: User)```Updates user details in the database.

```get_user(self, user_id)```Retrieves a user by ID from the database.

```fetch_all_users(self)```Fetches all users from the database.

```close(self)```Closes the database connection.Example Usagepython
```python
if __name__ == "__main__":
    project_config = {}
    database = Database(database_path, project_config)

    # Add a user
    user1 = User(user_id="1", name="Alice", email="alice@example.com", password="password123")
    action1 = Action(ActionType.ADD, user1)
    database.execute_action(action1)

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
```TODO List

Validation:Implement input validation for user data (e.g., email format, password strength).

Logging:Replace ```print``` statements with logging for better debugging and monitoring.

Error Handling:Enhance error handling to provide more detailed feedback and handle edge cases.

Unit Tests:Write unit tests to cover different scenarios and ensure code reliability.

Database Migration:Implement a migration system for database schema changes.

User Management:Add additional user management features like role assignments or permissions.

Connection Pooling:Consider implementing connection pooling for efficiency in multi-threaded or high-traffic environments.

Security Enhancements:Explore additional security measures such as encryption for sensitive data beyond passwords.

Documentation:Expand the documentation to cover additional features, usage scenarios, and configuration options.

Deployment:Prepare deployment instructions and ensure the project is production-ready.
