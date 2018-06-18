from .db_conn import Connection
from .escape_strings import escape_sql_input
import datetime

# Create a pool for MySQL Connections
connection_pool = Connection()

# INPUT - None
# OUTPUT - List of manufacturer names
def get_all_manufacturers():
    query = "SELECT id,name FROM manufacturers"
    return connection_pool.select_query(query)

def add_manufacturer(manufacturer):
    manufacturer = escape_sql_input(manufacturer)
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
    manufacturer = escape_sql_input(manufacturer)
    query = ("DELETE FROM tyres WHERE manufacturer = (SELECT id FROM manufacturers WHERE id = {})").format(manufacturer)
    if connection_pool.delete_query(query) == False:
        return False
    else:
        query = ("DELETE FROM manufacturers WHERE id = {}").format(manufacturer)
        return connection_pool.delete_query(query)


def search_manufacturer(manufacturer):
    manufacturer = escape_sql_input(manufacturer)
    query = ("SELECT id, name FROM manufacturers WHERE name LIKE '%{}%'").format(manufacturer)
    return connection_pool.select_query(query)

def get_all_products():
    query = ("SELECT tyres.id, manufacturers.name, model, width, height, diameter, pieces, price, sales_price FROM manufacturers, tyres"
            " WHERE manufacturers.id = manufacturer")
    return connection_pool.select_query(query)

def search_product_by_name(input_data):
    input_data = escape_sql_input(input_data)
    input_data = input_data.split(" ")
    
    if len(input_data) == 1:
        input_data.append(" ")

    query = ("SELECT tyres.id, manufacturers.name, model, width, height, diameter, pieces, price, sales_price FROM manufacturers, tyres"
            " WHERE manufacturers.id = manufacturer AND (manufacturers.name LIKE '%{0}%' OR model LIKE '%{0}%' OR (manufacturers.name LIKE '%{0}%' AND model LIKE '%{1}%'))").format(input_data[0], input_data[1])
    return connection_pool.select_query(query)

def search_product_by_size(input_data):
    input_data = escape_sql_input(input_data)
    try:
        width, height, diameter = input_data.split('/')
        width = int(width)
        height = int(height)
        diameter = int(diameter)
    except:
        return list()

    query = ("SELECT tyres.id, manufacturers.name, model, width, height, diameter, pieces, price, sales_price FROM manufacturers, tyres"
            " WHERE manufacturers.id = manufacturer AND width = {} AND height = {} AND diameter = {}").format(width, height, diameter)
    return connection_pool.select_query(query)

def search_product_by_price(input_data):
    input_data = escape_sql_input(input_data)
    try:
        min_price, max_price = input_data.split('-')
        min_price = int(min_price)
        max_price = int(max_price)
    except:
        return list()

    query = ("SELECT tyres.id, manufacturers.name, model, width, height, diameter, pieces, price, sales_price FROM manufacturers, tyres"
            " WHERE manufacturers.id = manufacturer AND sales_price BETWEEN {} AND {}").format(min_price, max_price)
    return connection_pool.select_query(query)

def add_product(manufacturer, model, size, piece, price, sales_price):
    try:
        width, height, diameter = size.split('/')
        diameter.strip("R")
        width = int(width)
        height = int(height)
        diameter = int(diameter)
        piece = int(piece)
        price = int(price)
        sales_price = int(sales_price)
        manufacturer = int(manufacturer)
        model = escape_sql_input(model)
    except:
        return False
    query = ("INSERT INTO tyres(manufacturer, model, width, height, diameter, pieces, price, sales_price) "
             "VALUES ({}, '{}', {}, {}, {}, {}, {}, {})").format(manufacturer, model, width, height, diameter, piece, price, sales_price)
    return connection_pool.insert_query(query)

def delete_product(p_id):
    try:
        p_id = int(p_id)
    except:
        return False
    query = ("DELETE FROM tyres WHERE id = {}").format(p_id)
    return connection_pool.delete_query(query)

def update_product(p_id, value):
    try:
        p_id = int(p_id)
    except:
        return False

    if value.startswith('*'):
        value = int(value.strip('*'))
        query = ("UPDATE tyres SET pieces = pieces + {} WHERE id = {}").format(value, p_id)
    elif value.startswith('-'):
        value = int(value.strip('-'))
        query = ("UPDATE tyres SET pieces = IF(pieces - {} < 0, 0, pieces - {}) WHERE id = {}").format(value, value, p_id)
    else:
        value = int(value)
        query = ("UPDATE tyres SET pieces = {} WHERE id = {}").format(value, p_id)

    return connection_pool.update_query(query)

def add_to_cart(tyre_id, pieces, user):
    try:
        tyre_id = int(tyre_id)
        pieces = int(pieces)
    except:
        return False, 0

    query = ("SELECT pieces FROM tyres WHERE id = {}").format(tyre_id)
    available_pieces = connection_pool.select_query(query)[0][0]

    query = ("SELECT COUNT(*) FROM cart WHERE tyre_id = {} AND userid = (SELECT id FROM users WHERE username LIKE '{}') AND order_date IS NULL").format(tyre_id, user)
    product_already_in_cart = connection_pool.select_query(query)[0][0]

    if(available_pieces < pieces):
        return None, available_pieces
    else:
        if product_already_in_cart == 0:
            query = ("INSERT INTO cart(tyre_id, userid, pieces) VALUES ({}, (SELECT id FROM users WHERE username LIKE '{}'), {})").format(tyre_id, user, pieces)
            if connection_pool.insert_query(query):
                query = ("UPDATE tyres SET pieces = pieces - {} WHERE id = {}").format(pieces, tyre_id)
                return connection_pool.update_query(query), 0
            else:
                return False, 0
        else:
            query = ("UPDATE cart SET pieces = pieces + {} WHERE tyre_id = {} AND userid = (SELECT id FROM users WHERE username LIKE '{}') AND order_date IS NULL").format(pieces, tyre_id, user)
            if connection_pool.update_query(query):
                query = ("UPDATE tyres SET pieces = pieces - {} WHERE id = {}").format(pieces, tyre_id)
                return connection_pool.update_query(query), 0
            else:
                return False, 0

def get_cart_data(user):
    query = ("SELECT tyres.id, manufacturers.name, tyres.model, tyres.width, tyres.height, tyres.diameter, cart.pieces, tyres.price, tyres.sales_price FROM cart, tyres, manufacturers "
             " WHERE userid = (SELECT id FROM users WHERE username LIKE '{}') AND manufacturers.id = tyres.manufacturer AND cart.tyre_id = tyres.id AND order_date IS NULL").format(user)
    return connection_pool.select_query(query)

def delete_product_from_cart(p_id, user):
    try:
        p_id = int(p_id)
    except:
        return False
    query = ("SELECT pieces FROM cart WHERE tyre_id = {} AND userid = (SELECT id FROM users WHERE username LIKE '{}') AND order_date IS NULL").format(p_id, user)
    pieces = connection_pool.select_query(query)[0][0]
    query = ("DELETE FROM cart WHERE tyre_id = {} AND userid = (SELECT id FROM users WHERE username LIKE '{}') AND order_date IS NULL").format(p_id, user)
    if connection_pool.delete_query(query):
        query = ("UPDATE tyres SET pieces = pieces + {} WHERE id = {}").format(pieces, p_id)
        return connection_pool.update_query(query)
    else:
        return False

def place_order(user):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    query = ("UPDATE cart SET order_date = '{}' WHERE userid = (SELECT id FROM users WHERE username LIKE '{}') AND order_date IS NULL").format(date, user)
    return connection_pool.update_query(query)

def get_orders():
    query = ("SELECT username, order_date, SUM(cart.pieces * sales_price) FROM users, cart, tyres WHERE users.id = userid AND tyre_id = tyres.id AND order_date IS NOT NULL AND finalized = 0 GROUP BY username, order_date ORDER BY order_date ASC")
    return connection_pool.select_query(query)

def get_order_details(username, date):
    username = escape_sql_input(username)
    date  = escape_sql_input(date)
    query = ("SELECT manufacturers.name, tyres.model, tyres.width, tyres.height, tyres.diameter, cart.pieces, tyres.sales_price FROM cart, manufacturers, tyres"
             " WHERE userid = (SELECT id FROM users WHERE username LIKE '{}') AND manufacturers.id = tyres.manufacturer AND cart.tyre_id = tyres.id AND order_date = '{}'").format(username, date)
    return connection_pool.select_query(query)

def send_order(username, order_date):
    query = ("UPDATE cart SET finalized = 1 WHERE userid = (SELECT id FROM users WHERE username LIKE '{}') AND order_date = '{}'").format(username, order_date)
    return connection_pool.update_query(query)