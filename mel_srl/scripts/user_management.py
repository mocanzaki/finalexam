import hashlib, uuid
from .db_conn import Connection
from .escape_strings import escape_sql_input
import logging

# Create a pool for MySQL Connections
connection_pool = Connection()

# Try to log in with the given credentials
# INPUT - Username as string, Password as string
# OUTPUT - None if authentication failed, otherwise the permission of the user
def login(username, password):
    # Escape the single quotes from the sql query input
    username = escape_sql_input(username)
    password = escape_sql_input(password)

    # Get the credentials of the user
    [salt, pw, permission] = connection_pool.get_user_credentials(username)
    # Check if encrypted password is equal to the encrypted combination of the given password and the salt from the database
    if (pw == hashlib.sha512(password.encode() + salt.encode()).hexdigest()):
        logging.getLogger('user_management').debug('Login succesfully for user: ' + username + ', with permission: ' + str(permission))
        # If so, return the permission of the user
        return permission
    else:
        logging.getLogger('user_management').debug('Login failed for user: ' + username)
        # Otherwise he has no permission
        return None

# Insert new user into the database
# INPUT - Raw user data as seen in parameters
# OUTPUT - True / False depending on the result of the insertion
def register(username, name, email, phone, num_plate, password): 
    # Escape the single quotes from the sql query input
    username = escape_sql_input(username)
    password = escape_sql_input(password)
    name = escape_sql_input(name)
    email = escape_sql_input(email)
    num_plate = escape_sql_input(num_plate)

    # Build salt and password
    salt = uuid.uuid4().hex
    password = hashlib.sha512(password.encode() + salt.encode()).hexdigest()

    # Return insertion result
    return connection_pool.insert_new_user([username, name, email, phone, salt, password, 0], num_plate)

# Check is username is available for register
# INPUT - Raw username
# OUTPUT - True / False depending if the username is occupied
def check_if_username_is_useable(username):
    username = escape_sql_input(username)
    query = ("SELECT COUNT(*) FROM `users` WHERE username LIKE '{}'").format(username)
    
    return connection_pool.select_query(query)[0][0] == 0
