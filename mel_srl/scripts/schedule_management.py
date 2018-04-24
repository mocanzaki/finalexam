from .db_conn import Connection
import logging

# Create a pool for MySQL Connections
connection_pool = Connection()

# Returns a list of the days in the actual year/month according to empty spaces
# INPUT - YEAR int, MONTH int
# OUTPUT - 3 lists containing every day of month categorized
def get_fillness_of_month(year, month):
    filled_days = list()
    average_days = list()
    empty_days = list()

    # Contains pairs, day - number of schedules
    result = connection_pool.get_fillness_of_month(year, month)

    for i in result:
        if(i[1] == 18):
            filled_days.append(i[0])
        elif(i[1] > 13):
            average_days.append(i[0])
        else:
            empty_days.append(i[0])

    return empty_days, average_days, filled_days

# Returns the hours of a day on which scheduling can be made
# INPUT - YEAR int, MONTH int, DAY int
# OUTPUT - a list made of hour minute concatenations containing only available hours
def get_remaining_hours(year, month, day):
    free_hours = list()
    # scheduling can be made from 8 am to 17 pm every 30 min
    for i in range(8,17):
        free_hours.append(str(i)+"0")
        free_hours.append(str(i)+"30")

    # contains the hours already scheduled
    occupied_hour = connection_pool.get_occupied_hours(year, month, day)
    occupied_hours = list()

    # convert into same format as the available hours
    for i in occupied_hour:
        occupied_hours.append(str(int(i[0]))+str(i[1]))

    # return the remaining (available) hours
    return [hour for hour in free_hours if hour not in occupied_hours]

def make_schedule(year, month, day, hour, minute, num_plate, service_id):
     # build up datetime for mysql
    date = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":00"

     # check if date is really available and number plate isn't scheduled yet
    if (str(hour)+str(minute)) not in get_remaining_hours(year, month, day):
        return False
    elif check_if_num_plate_is_scheduled(num_plate):
        if connection_pool.insert_new_schedule(num_plate, date, service_id):
            return True
        else:
            return False
    else:
        return False

# Return all number plates for a user which aren't scheduled yet
# INPUT - Username
# OUPUT - List of number plates
def get_num_plates_available_for_scheduling(username):
    query = ("SELECT name FROM `num_plates` WHERE `user_id` = (SELECT id FROM `users` WHERE `username` LIKE '{}') AND name NOT IN (SELECT name FROM `num_plates` WHERE id IN (SELECT num_plate_id FROM schedule WHERE date > NOW()))").format(username)
    print(query)
    return connection_pool.select_query(query)

# Checks if a number plate is already scheduled for a future date
# INPUT - Number plate
# OUTPUT - True / False depending if it is or not scheduled
def check_if_num_plate_is_scheduled(num_plate):
    query = ("SELECT COUNT(*) FROM `schedule` WHERE num_plate_id = (SELECT id FROM num_plates WHERE name LIKE '{}') AND date > NOW()").format(num_plate)
    return connection_pool.select_query(query)[0][0] == 0


