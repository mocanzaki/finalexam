from .db_conn import Connection

# Create a pool for MySQL Connections
connection_pool = Connection()

# Get data from services
# INPUT - None
# OUTPUT - LIST([id,description])
def get_all_services():
    query = "SELECT id,description FROM services"
    return connection_pool.select_query(query)

def add_service(service):
    query = ("SELECT COUNT(*) FROM services WHERE description LIKE '{}'").format(service)
    if connection_pool.select_query(query)[0][0] == 0:
        query = ("INSERT INTO services(`description`) VALUES ('{}')").format(service)
        if connection_pool.insert_query(query):
            query = ("SELECT id FROM services WHERE description LIKE '{}'").format(service)
            return True, connection_pool.select_query(query)[0][0]
        else:
            return False, 0
    else:
        return None, 0

def delete_service(service):
    query = ("DELETE FROM services WHERE id = {}").format(service)
    return connection_pool.delete_query(query)  

# Get data from services
# INPUT - None
# OUTPUT - LIST([id,description])
def search_service(service):
    query = ("SELECT id,description FROM services WHERE description LIKE '%{}%'").format(service)
    return connection_pool.select_query(query)