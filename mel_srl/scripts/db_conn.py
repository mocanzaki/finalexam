import mysql.connector
import mysql.connector.pooling

# Class implementing connection pooling and including every necessary query for the business logic of the webapp
# Every SQL query should use single quotes, escaping is implemented for avoiding injection based on single quotes
class Connection:
    # Configures the class for the connection pooling
    # INPUT - None
    # OUTPUT - None
    def __init__(self):
        # Config for the MySQL database
        self.dbconfig = {
            "user"     : "root",
            "password" : "1234",
            "database" : "final_exam",
            #"database" : "test",
        }
        

        # Creates the MySQL connection pool, using the above config, and a pool with 32 connections
        self.pool =  mysql.connector.pooling.MySQLConnectionPool(
            pool_name = "connection_pool",
            pool_size = 32,
            **self.dbconfig)

    # Returns a connection from the pool
    # INPUT - None
    # OUTPUT - If there is available connection in the pool, then the connection, otherwise None
    def get_connection(self):
        try:
            return self.pool.get_connection()
        except:
            return None

    # Executes a select like query
    # INPUT - query strin
    # OUTPUT - list of lists, with every result
    def select_query(self, query):
        con = self.get_connection()
        cursor = con.cursor()

        cursor.execute(query)

        result = cursor.fetchall()
        con.commit()

        cursor.close()
        con.close()

        return result

    # Executes a user insertion in the table
    # INPUT - list of user data  IN ORDER AND ESCAPED!
    # OUTPUT - boolean, depending on the result of the insertion
    def insert_new_user(self, user_data):
        con = self.get_connection()
        query = ("INSERT INTO  users (`username`, `name`, `email`, `phone`, `num_plate`, `salt`, `password`, `permission`) "
                     "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {})").format(*user_data)
        try:
            cursor = con.cursor()

            cursor.execute(query)

            cursor.close()
            con.commit()
            con.close()

            return True

        except :
            print("Something bad happened, during inserting a new user!")

            try:
                con.rollback()
                print("The transaction of the new user insertion was successfully rollbacked!")

            except:
                print("Error rolling back the transaction of the user insertion!")
                pass

            con.close()
            return False

    # Returns the user login credentials for a certain user
    # INPUT - username ESCAPED!
    # OUTPUT - a list of the user credentials
    def get_user_credentials(self, username):
        query = "SELECT `salt`, `password`, `permission` FROM users WHERE `username` LIKE '{}'".format(username)
        return self.select_query(query)[0]