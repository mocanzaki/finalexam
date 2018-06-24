import hashlib, uuid
from .db_conn import Connection
from .smtp_conn import SMTP
from .escape_strings import escape_sql_input
import logging

# Create a pool for MySQL Connections
connection_pool = Connection()

# Try to log in with the given credentials
# INPUT - Username as string, Password as string
# OUTPUT - None if authentication failed, -1 if user is blocked, otherwise the permission of the user
def login(username, password):
    # Escape the single quotes from the sql query input
    username = escape_sql_input(username)
    password = escape_sql_input(password)

    # Get the credentials of the user
    try:
        [salt, pw, permission, blocked] = get_user_credentials(username)[0]
    except:
        return None

    if blocked == 1:
        return -1
        
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
def register(username, name, email, phone, num_plate, password, address): 
    # Escape the single quotes from the sql query input
    username = escape_sql_input(username)
    password = escape_sql_input(password)
    name = escape_sql_input(name)
    email = escape_sql_input(email)
    num_plate = escape_sql_input(num_plate)
    address = escape_sql_input(address)

    # Build salt and password
    salt = uuid.uuid4().hex
    password = hashlib.sha512(password.encode() + salt.encode()).hexdigest()

    # Return insertion result
    return insert_new_user([username, name, email, phone, salt, password, 0], num_plate, address)

# Executes a user insertion in the table
# INPUT - list of user data  IN ORDER AND ESCAPED!
# OUTPUT - boolean, depending on the result of the insertion
def insert_new_user(user_data, num_plate, address):
    query = ("INSERT INTO  users (`username`, `name`, `email`, `phone`, `salt`, `password`, `permission`, `address`) "
                 "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}, '{}'); INSERT INTO num_plates (`user_id`, `name`) VALUES ( (SELECT id FROM users WHERE username LIKE '{}'), '{}')").format(*user_data, address, user_data[0], num_plate)
    
    return connection_pool.multiple_insert_query(query)

# Returns the user login credentials for a certain user
# INPUT - username ESCAPED!
# OUTPUT - a list of the user credentials
def get_user_credentials(username):
    query = "SELECT `salt`, `password`, `permission`, `blocked` FROM users WHERE `username` LIKE '{}'".format(username)
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
    query = ("SELECT username, users.name, email, phone, address, num_plates.name FROM `users` LEFT JOIN `num_plates` ON  user_id = users.id WHERE username LIKE '{}'").format(username)

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

# Adds number plate, checks if already exists
# INPUT - Number plate, username
# OUTPUT - None if number plate is already in database, True / False if query runs
def add_num_plate(num_plate, username):
    num_plate = escape_sql_input(num_plate)
    username = escape_sql_input(username)
    
    query = ("INSERT INTO num_plates(`user_id`, `name`) VALUES((SELECT id FROM users WHERE username LIKE '{}'), '{}')").format(username, num_plate)

    for i in get_num_plates_and_users():
        if i[1] == num_plate:
            return None

    return connection_pool.insert_query(query)

# Updates user data
# INPUT - Username, Name, Email, Phone
# OUTPUT - True / False
def update_user_data(username, name, email, phone, address):
    username = escape_sql_input(username)
    name = escape_sql_input(name)
    email = escape_sql_input(email)
    phone = escape_sql_input(phone)
    address = escape_sql_input(address) 

    user_data = get_user_data(username)[0]

    query = "UPDATE users "
    execute = False

    if name != user_data[1]:
        query += "SET name = '" + name + "' "
        execute = True

    if email != user_data[2]:
        if execute:
            query += ", SET email = '" + email + "' "
        else:
            query += "SET email = '" + email + "' "
        execute = True

    if phone != user_data[3]:
        if execute:
            query += ", SET phone = '" + phone + "' "
        else:
            query += "SET phone = '" + phone + " "
        execute = True

    if address != user_data[4]:
        if execute:
            query += ", SET address = '" + address + "' "
        else:
            query += "SET address = '" + address + "' "
        execute = True
        
    if execute:
        query += "WHERE username LIKE '" + username + "'"
        return connection_pool.update_query(query)
    return True

def get_all_user_data():
    query = "SELECT id, username, name, email, phone, blocked, permission FROM users"
    return connection_pool.select_query(query)

def modify_block(userid, action):
    if action == "block":
        query = "UPDATE users SET blocked = 1 WHERE id = " + userid
    else:
        query = "UPDATE users SET blocked = 0 WHERE id = " + userid
    return connection_pool.update_query(query)

def modify_permission(userid, action):
    if action == "admin":
        query = "UPDATE users SET permission = 1 WHERE id = " + userid
    else:
        query = "UPDATE users SET permission = 0 WHERE id = " + userid
    return connection_pool.update_query(query)

def search_users(input_data):
    input_data = escape_sql_input(input_data)
    
    query = ("SELECT id, username, name, email, phone, blocked, permission FROM users WHERE username LIKE '%{0}%'"
             "OR name LIKE '%{0}%' OR email LIKE '%{0}%' OR phone LIKE '%{0}%'").format(input_data)

    return connection_pool.select_query(query)

def reset_password(email):
    email = escape_sql_input(email)
    token = uuid.uuid4().hex

    query = ("UPDATE users SET reset_pw = '{}' WHERE email LIKE '{}'").format(token, email)
    if connection_pool.update_query(query):
        smtp = SMTP()
        smtp.start()
        result = smtp.send_mail(email, "[MEL SRL] Password reset", "Dear user, \nPlease visit this link to reset your password: http://localhost:6543/reset_pw/" + token + "\n Thank you, \n Mel SRL group.")
        smtp.close()
        return result
    else:
        return False

def change_password(pw, token):
    salt = uuid.uuid4().hex
    password = hashlib.sha512(pw.encode() + salt.encode()).hexdigest()
    query = ("UPDATE users SET salt = '{}', password = '{}', reset_pw = NULL WHERE reset_pw = '{}'").format(salt, password, token)
    return connection_pool.update_query(query)