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
    query = ("SELECT DAY(date) as day, COUNT(*) as total FROM schedule WHERE YEAR(date) = '{}' AND MONTH(date) = '{}' GROUP BY DAY(date)").format(year, month)
    result = connection_pool.select_query(query)

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
    query = ("SELECT HOUR(date) as hour, MINUTE(date) as minute FROM schedule WHERE YEAR(date) = '{}' AND MONTH(date) = '{}' AND DAY(date) = '{}'").format(year, month, day)
    occupied_hour = connection_pool.select_query(query)
    occupied_hours = list()

    # convert into same format as the available hours
    for i in occupied_hour:
        occupied_hours.append(str(int(i[0]))+str(i[1]))

    # return the remaining (available) hours
    return [hour for hour in free_hours if hour not in occupied_hours]

def make_schedule(year, month, day, hour, minute, num_plate, service_id):
     # build up datetime for mysql
    date = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":00"
    query = ("INSERT INTO schedule (`num_plate_id`, `date`, `service_id`) VALUES((SELECT id FROM num_plates WHERE name LIKE '{}'), '{}', '{}')").format(num_plate, date, service_id)

     # check if date is really available and number plate isn't scheduled yet
    if (str(hour)+str(minute)) not in get_remaining_hours(year, month, day):
        return False
    elif check_if_num_plate_is_scheduled(num_plate):
        if connection_pool.insert_query(query):
            return True
        else:
            return False
    else:
        return False

# Return all number plates for a user which aren't scheduled yet
# INPUT - Username
# OUPUT - List of number plates
def get_num_plates_available_for_scheduling(username):
    query = ("SELECT name FROM `num_plates` WHERE `user_id` = (SELECT id FROM `users` WHERE `username` LIKE '{}') "
            "AND name NOT IN (SELECT name FROM `num_plates` WHERE id IN (SELECT num_plate_id FROM schedule WHERE date > NOW()))").format(username)
    return connection_pool.select_query(query)

# Checks if a number plate is already scheduled for a future date
# INPUT - Number plate
# OUTPUT - True / False depending if it is or not scheduled
def check_if_num_plate_is_scheduled(num_plate):
    query = ("SELECT COUNT(*) FROM `schedule` WHERE num_plate_id = (SELECT id FROM num_plates WHERE name LIKE '{}') AND date > NOW()").format(num_plate)
    return connection_pool.select_query(query)[0][0] == 0



# Return all number plates for a user which aren't scheduled yet
# INPUT - Year, Month, Day
# OUPUT - 5 lists containing the hours, minutes, names, number plates, services
def get_schedule_of_day(year, month, day):
    query = ("SELECT HOUR(date), MINUTE(date), users.name, num_plates.name, services.description FROM schedule, users, num_plates, services"
            " WHERE YEAR(date) = {} AND MONTH(date) = {} AND DAY(date) = {} AND num_plates.id = schedule.num_plate_id AND"
            " services.id = schedule.service_id AND users.id = num_plates.user_id ORDER BY date ASC;").format(year,month,day)

    result = connection_pool.select_query(query)

    hour = list()
    minute = list()
    name = list()
    number_plate = list()
    service = list()

    for i in result:
        hour.append(i[0])
        minute.append(i[1])
        name.append(i[2])
        number_plate.append(i[3])
        service.append(i[4])

    return hour, minute, name, number_plate, service


