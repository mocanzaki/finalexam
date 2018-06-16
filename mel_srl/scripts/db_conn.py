import mysql.connector
import mysql.connector.pooling
import logging

# Class implementing connection pooling and including every necessary query for the business logic of the webapp
# Every SQL query should use single quotes, escaping is implemented for avoiding injection based on single quotes
class Connection:
    # Configures the class for the connection pooling
    # INPUT - None
    # OUTPUT - None
    def __init__(self):
        # Create logger object 
        self.logger = logging.getLogger('db_conn')

        # Config for the MySQL database
        self.dbconfig = {
            "user"     : "root",
            "password" : "1234",
            "database" : "final_exam",
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
            self.logger.debug('Returning connection from the pool')
            return self.pool.get_connection()
        except:
            self.logger.error('Couldn\'t return connection from the pool')
            return None

    # Executes a select like query
    # INPUT - query string
    # OUTPUT - list of lists, with every result
    def select_query(self, query):
        con = self.get_connection()
        cursor = con.cursor()
        try:
            cursor.execute(query)

            result = cursor.fetchall()
            con.commit()

            cursor.close()
            con.close()
        except:
            return list()

        self.logger.debug(query)
        self.logger.debug(result)

        return result

    # Executes a delete like query
    # INPUT - query string
    # OUTPUT - True / False depenging on result
    def delete_query(self, query):
        con = self.get_connection()
        self.logger.debug(query)

        try:
            cursor = con.cursor()

            cursor.execute(query)

            cursor.close()
            con.commit()
            con.close()

            self.logger.info('Successfully executed delete query!')

            return True

        except :
            self.logger.error("Something bad happened, during executing delete query!")

            try:
                con.rollback()
                self.logger.debug("The transaction of the delete query was successfully rollbacked!")

            except:
                self.logger.error("Error rolling back the transaction of the delete query!")
                pass

            con.close()
            return False

    # Executes an insert like query
    # INPUT - query string
    # OUTPUT - True / False depenging on result
    def insert_query(self, query):
        con = self.get_connection()
        self.logger.debug(query)

        try:
            cursor = con.cursor()

            cursor.execute(query)

            cursor.close()
            con.commit()
            con.close()

            self.logger.info('Successfully executed insert query!')

            return True

        except :
            self.logger.error("Something bad happened, during executing insert query!")

            try:
                con.rollback()
                self.logger.debug("The transaction of the insert query was successfully rollbacked!")

            except:
                self.logger.error("Error rolling back the transaction of the insert query!")
                pass

            con.close()
            return False

    # Executes an update like query
    # INPUT - query string
    # OUTPUT - True / False depenging on result
    def update_query(self, query):
        con = self.get_connection()
        self.logger.debug(query)

        try:
            cursor = con.cursor()

            cursor.execute(query)

            cursor.close()
            con.commit()
            con.close()

            self.logger.info('Successfully executed update query!')

            return True

        except :
            self.logger.error("Something bad happened, during executing update query!")

            try:
                con.rollback()
                self.logger.debug("The transaction of the update query was successfully rollbacked!")

            except:
                self.logger.error("Error rolling back the transaction of the update query!")
                pass

            con.close()
            return False

    # Executes multiple insert like queries
    # INPUT - one string containing queries separated with semicolon
    # OUTPUT - True / False depenging on result
    def multiple_insert_query(self, query):
        con = self.get_connection()
        self.logger.debug(query)

        try:
            cursor = con.cursor(buffered=True)

            cursor.execute(query, multi=True)

            for cur in cursor.execute(query, multi=True):
                if cur.with_rows:
                    cur.fetchall()

            cursor.close()
            con.commit()
            con.close()

            self.logger.info('Successfully executed multiple insert queries!')

            return True

        except :
            self.logger.error("Something bad happened, during executing multiple insert queries!")

            try:
                con.rollback()
                self.logger.debug("The transaction of the multiple insert queries was successfully rollbacked!")

            except:
                self.logger.error("Error rolling back the transaction of the multiple insert queries!")
                pass

            con.close()
            return False