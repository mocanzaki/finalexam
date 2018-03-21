import hashlib, uuid
from db_conn import Connection
from escape_strings import escape_sql_input

# Try to log in with the given credentials
# INPUT - Username as string, Password as string
# OUTPUT - None if authentication failed, otherwise the permission of the user
def login(username, password):
    # Escape the single quotes from the sql query input
    username = escape_sql_input(username)
    password = escape_sql_input(password)

    # Get a connection from the pool and get the credentials of the user
    [salt, pw, permission] = Connection().get_user_credentials(username)
    # Check if encrypted password is equal to the encrypted combination of the given password and the salt from the database
    if (pw == hashlib.sha512(password.encode() + salt.encode()).hexdigest()):
        # If so, return the permission of the user
        return permission
    else:
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

    # Build salt and password
    salt = uuid.uuid4().hex
    password = hashlib.sha512(password.encode() + salt.encode()).hexdigest()

    # Return insertion result
    return Connection().insert_new_user([username, name, email, phone, num_plate, salt, password, 0])