from .db_conn import Connection
import logging

# Create a pool for MySQL Connections
connection_pool = Connection()
# Get data from services
# INPUT - None
# OUTPUT - LIST([id,description])
def get_services():
    query = "SELECT id,description FROM services"
    services = connection_pool.select_query(query)
    return services