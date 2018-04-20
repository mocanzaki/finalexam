from .db_conn import Connection
import logging

# Create a pool for MySQL Connections
connection_pool = Connection()

def get_fillness_of_month(year, month):
    filled_days = list()
    average_days = list()
    empty_days = list()

    result = connection_pool.get_fillness_of_month(year, month)

    for i in result:
        if(i[1] == 18):
            filled_days.append(i[0])
        elif(i[1] > 13):
            average_days.append(i[0])
        else:
            empty_days.append(i[0])

    return empty_days, average_days, filled_days

def get_remaining_hours(year, month, day):
    free_hours = list()
    for i in range(8,17):
        free_hours.append(str(i)+"0")
        free_hours.append(str(i)+"30")

    occupied_hour = connection_pool.get_occupied_hours(year, month, day)
    occupied_hours = list()

    for i in occupied_hour:
        occupied_hours.append(str(int(i[0]))+str(i[1]))

    return [hour for hour in free_hours if hour not in occupied_hours]




