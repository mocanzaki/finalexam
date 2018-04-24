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

        self.logger.debug(query)
        self.logger.debug(result)

        return result

    # Executes a user insertion in the table
    # INPUT - list of user data  IN ORDER AND ESCAPED!
    # OUTPUT - boolean, depending on the result of the insertion
    def insert_new_user(self, user_data, num_plate):
        con = self.get_connection()
        query = ("INSERT INTO  users (`username`, `name`, `email`, `phone`, `salt`, `password`, `permission`) "
                     "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {}); INSERT INTO num_plates (`user_id`, `name`) VALUES ( (SELECT id FROM users WHERE username LIKE '{}'), '{}')").format(*user_data, user_data[0], num_plate)
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

            return True

        except :
            self.logger.error("Something bad happened, during inserting a new user!")

            try:
                con.rollback()
                self.logger.debug("The transaction of the new user insertion was successfully rollbacked!")

            except:
                self.logger.error("Error rolling back the transaction of the user insertion!")
                pass

            con.close()
            return False

    # Returns the user login credentials for a certain user
    # INPUT - username ESCAPED!
    # OUTPUT - a list of the user credentials
    def get_user_credentials(self, username):
        query = "SELECT `salt`, `password`, `permission` FROM users WHERE `username` LIKE '{}'".format(username)
        return self.select_query(query)[0]

    def get_schedule_of_day(self, year, month, day):
        query = ("SELECT * FROM schedule WHERE DATE(date) = '{}-{}-{}'").format(year, month, day)
        return self.select_query(query)

    def get_fillness_of_month(self, year, month):
        query = ("SELECT DAY(date) as day, COUNT(*) as total FROM schedule WHERE YEAR(date) = '{}' AND MONTH(date) = '{}' GROUP BY DAY(date)").format(year, month)
        return self.select_query(query)

    def get_occupied_hours(self, year, month, day):
        query = ("SELECT HOUR(date) as hour, MINUTE(date) as minute FROM schedule WHERE YEAR(date) = '{}' AND MONTH(date) = '{}' AND DAY(date) = '{}'").format(year, month, day)
        return self.select_query(query)

    def insert_new_schedule(self, num_plate, date, service_id):
        con = self.get_connection()
        query = ("INSERT INTO schedule (`num_plate_id`, `date`, `service_id`) VALUES((SELECT id FROM num_plates WHERE name LIKE '{}'), '{}', '{}')").format(num_plate, date, service_id)
        self.logger.debug(query)

        try:
            cursor = con.cursor()

            cursor.execute(query)

            cursor.close()
            con.commit()
            con.close()

            self.logger.info('Successfully inserted new schedule!')

            return True

        except :
            self.logger.error("Something bad happened, during inserting a new schedule!")

            try:
                con.rollback()
                self.logger.debug("The transaction of the new schedule insertion was successfully rollbacked!")

            except:
                self.logger.error("Error rolling back the transaction of the schedule insertion!")
                pass

            con.close()
            return False