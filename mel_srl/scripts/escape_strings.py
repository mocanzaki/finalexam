# Returns a string with every single quote escaped
# INPUT - String
# OUTPUT - String with single quotes escaped
def escape_sql_input(string):
    return string.replace("\'","\\'")