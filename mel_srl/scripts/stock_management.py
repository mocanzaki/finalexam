from .db_conn import Connection

# Create a pool for MySQL Connections
connection_pool = Connection()

# INPUT - None
# OUTPUT - List of manufacturer names
def get_all_manufacturers():
    query = "SELECT name FROM manufacturers"
    return connection_pool.select_query(query)

def add_manufacturer(manufacturer):
    query = ("SELECT COUNT(*) FROM manufacturers WHERE name LIKE '{}'").format(manufacturer)
    if connection_pool.select_query(query)[0][0] == 0:
        query = ("INSERT INTO manufacturers(`name`) VALUES ('{}')").format(manufacturer)
        return connection_pool.insert_query(query)
    else:
        return None

def add_manufacturer(manufacturer):
    query = ("SELECT COUNT(*) FROM manufacturers WHERE name LIKE '{}'").format(manufacturer)
    if connection_pool.select_query(query)[0][0] == 0:
        query = ("INSERT INTO manufacturers(`name`) VALUES ('{}')").format(manufacturer)
        return connection_pool.insert_query(query)
    else:
        return None

def delete_manufacturer(manufacturer):
    query = ("DELETE FROM manufacturers WHERE name LIKE '{}'").format(manufacturer)
    return connection_pool.delete_query(query)

def search_manufacturer(input_data):
    query = ("SELECT name FROM manufacturers WHERE name LIKE '%{}%'").format(input_data)
    return connection_pool.select_query(query)