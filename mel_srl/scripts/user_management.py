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
    try:
        [salt, pw, permission] = get_user_credentials(username)[0]
    except:
        return None
        
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
    return insert_new_user([username, name, email, phone, salt, password, 0], num_plate)

# Executes a user insertion in the table
# INPUT - list of user data  IN ORDER AND ESCAPED!
# OUTPUT - boolean, depending on the result of the insertion
def insert_new_user(user_data, num_plate):
    query = ("INSERT INTO  users (`username`, `name`, `email`, `phone`, `salt`, `password`, `permission`) "
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}); INSERT INTO num_plates (`user_id`, `name`) VALUES ( (SELECT id FROM users WHERE username LIKE '{}'), '{}')").format(*user_data, user_data[0], num_plate)
    
    return connection_pool.multiple_insert_query(query)

# Returns the user login credentials for a certain user
# INPUT - username ESCAPED!
# OUTPUT - a list of the user credentials
def get_user_credentials(username):
    query = "SELECT `salt`, `password`, `permission` FROM users WHERE `username` LIKE '{}'".format(username)
    return connection_pool.select_query(query)

# Check is username is available for register
# INPUT - Raw username
# OUTPUT - True / False depending if the username is occupied
def check_if_username_is_useable(username):
    username = escape_sql_input(username)
    query = ("SELECT COUNT(*) FROM `users` WHERE username LIKE '{}'").format(username)
    
    return connection_pool.select_query(query)[0][0] == 0
    
# Get all user data
# INPUT - Raw username
# OUTPUT - All user data in a list
def get_user_data(username):
    username = escape_sql_input(username)
    query = ("SELECT username, users.name, email, phone, num_plates.name FROM `users` LEFT JOIN `num_plates` ON  user_id = users.id WHERE username LIKE '{}'").format(username)

    return connection_pool.select_query(query)


# Get number plates and users
# INPUT - None
# OUTPUT - (username , number plate) in a list
def get_num_plates_and_users():
    query = ("SELECT username, num_plates.name FROM users, num_plates WHERE user_id = users.id")
    return connection_pool.select_query(query)

# Deletes number plate
# INPUT - Number plate
# OUTPUT - True / False
def delete_num_plate(num_plate):
    num_plate = escape_sql_input(num_plate)
    query = ("DELETE FROM num_plates WHERE name LIKE '{}'").format(num_plate)
    return connection_pool.delete_query(query)