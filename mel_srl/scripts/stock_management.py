from .db_conn import Connection

# Create a pool for MySQL Connections
connection_pool = Connection()

# INPUT - None
# OUTPUT - List of manufacturer names
def get_all_manufacturers():
    query = "SELECT id,name FROM manufacturers"
    return connection_pool.select_query(query)

def add_manufacturer(manufacturer):
    query = ("SELECT COUNT(*) FROM manufacturers WHERE name LIKE '{}'").format(manufacturer)
    if connection_pool.select_query(query)[0][0] == 0:
        query = ("INSERT INTO manufacturers(`name`) VALUES ('{}')").format(manufacturer)
        if connection_pool.insert_query(query):
            query = ("SELECT id FROM manufacturers WHERE name LIKE '{}'").format(manufacturer)
            return True, connection_pool.select_query(query)[0][0]
        else:
            return False, 0

    else:
        return None, 0

def delete_manufacturer(manufacturer):
    query = ("DELETE FROM tyres WHERE manufacturer = (SELECT id FROM manufacturers WHERE id = {})").format(manufacturer)
    if connection_pool.delete_query(query) == False:
        return False
    else:
        query = ("DELETE FROM manufacturers WHERE id = {}").format(manufacturer)
        return connection_pool.delete_query(query)


def search_manufacturer(input_data):
    query = ("SELECT id, name FROM manufacturers WHERE name LIKE '%{}%'").format(input_data)
    return connection_pool.select_query(query)

def get_all_products():
    query = ("SELECT manufacturers.name, model, width, height, diameter, pieces, price, sales_price FROM manufacturers, tyres"
            " WHERE manufacturers.id = manufacturer")
    return connection_pool.select_query(query)