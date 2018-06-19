from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound

import re, logging, datetime
from calendar import monthrange

from ..scripts import user_management
from ..scripts import schedule_management
from ..scripts import service_management
from ..scripts import stock_management

# File used for describing the template rendering and the actions on every route
# SYNTAX
# route_name must correspond to a route_name from ../routes.py
# renderer must be an existing template in ../templates
# function can have any name with a request parameter which stores data from the request
# can RETURN almost anything, but mostly the data to be rendered on the renderer in a dictionary
# dictionary key is used on the template to show the value of the key

@view_config(route_name='home', renderer='../templates/home.jinja2')
def home(request):
  if 'permission' in request.session and request.session['permission'] == 0:
    return {'data' : schedule_management.get_my_schedules(request.session['username'])}
  return {}

@view_config(route_name='login', renderer='../templates/login.jinja2', request_method = 'GET')
def login_GET(request):
    # Check if user is already logged in
    session = request.session
    if 'username' in session:
        return HTTPFound(location = request.route_url('home'))
    else:
        return {}



@view_config(route_name='login', renderer='../templates/login.jinja2', request_method = 'POST')
def login_POST(request):
    # Extract user data to be checked for login
    username = request.POST['username']
    password = request.POST['password']

    # Retrieve session from request
    session = request.session

    # Check if user is already logged in
    if 'username' in session:
        return HTTPFound(location = request.route_url('home'))
    else:
        # Validate extracted data
        if not re.match("[a-zA-Z0-9-_.]{6,25}", username):
            logging.getLogger('user_management').debug('Injection attack detected on login from:' + request.remote_addr)
            return render_to_response('../templates/login.jinja2',
                                  {'credential_error' : True},
                                  request=request)
        if not re.match("[a-zA-Z0-9-_.,?!@#$&*<>:;]{6,20}", password):
            logging.getLogger('user_management').debug('Injection attack detected on login from:' + request.remote_addr)
            return render_to_response('../templates/login.jinja2',
                                  {'credential_error' : True},
                                  request=request)

        # Try to log in with the credentials
        permission = user_management.login(username, password)

        # Check if user is blocked
        if permission == -1:
           return render_to_response('../templates/login.jinja2',
                                  {'user_blocked' : True},
                                  request=request) 
        # Check for success
        elif permission is not None:
            # Store data in session
            session['username'] = username
            session['permission'] = permission

            return HTTPFound(location = request.route_url('home'))
        else:
            return render_to_response('../templates/login.jinja2',
                                  {'credential_error' : True},
                                  request=request)

@view_config(route_name='register', renderer='../templates/register.jinja2', request_method = 'GET')
def register_GET(request):
    # Check if user is already logged in
    session = request.session
    if 'username' in session:
        return HTTPFound(location = request.route_url('home'))
    else:
        return {}


@view_config(route_name='register', renderer='../templates/register.jinja2', request_method = 'POST')
def register_POST(request):
    # Extract user data to be submitted in the database
    username = request.POST['username']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    num_plate = request.POST['num_plate']
    password = request.POST['password']
    address = request.POST['addr']

    # Check if user is already logged in
    session = request.session
    if 'username' in session:
        return HTTPFound(location = request.route_url('home'))
    else:
        # Validate extracted data
        if not re.match("[a-zA-Z0-9-_.]{6,25}", username):
            logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
            return render_to_response('../templates/register.jinja2',
                                  {'credential_error' : True},
                                  request=request)
        if not re.match("[a-zA-Z0-9-_. ]{6,30}", name):
            logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
            return render_to_response('../templates/register.jinja2',
                                  {'credential_error' : True},
                                  request=request)
        if not re.match("(\+[0-9]{11,})|([0-9]{10,})", phone):
            logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
            return render_to_response('../templates/register.jinja2',
                                  {'credential_error' : True},
                                  request=request)
        if not re.match("(^[a-zA-Z]{1,2})( ?)([0-9]{2,3})( ?)([a-zA-Z]{3})|((^[a-zA-Z]{1,2})( ?)([0-9]){6})", num_plate):
            logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
            return render_to_response('../templates/register.jinja2',
                                  {'credential_error' : True},
                                  request=request)
        if not re.match("[a-zA-Z0-9-_.,?!@#$&*<>:;]{6,20}", password):
            logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
            return render_to_response('../templates/register.jinja2',
                                  {'credential_error' : True},
                                  request=request)

        # Check if username is useable
        if not user_management.check_if_username_is_useable(username):
            return render_to_response('../templates/register.jinja2',
                                  {'username_error' : True},
                                  request=request)

        # Try to submit data to the database
        if user_management.register(username, name, email, phone, num_plate, password, address):
            return render_to_response('../templates/register.jinja2',
                                  {'successfully_registered' : True},
                                  request=request)
        else:
            return render_to_response('../templates/register.jinja2',
                                  {'credential_error' : True},
                                  request=request)

@view_config(route_name='logout')
def logout(request):
    # End Session, log out user
    session = request.session
    try:
        del session['username']
        del session['permission']
    except:
        pass
    return HTTPFound(location = request.route_url('home'))

@view_config(route_name='schedule', renderer='../templates/schedule.jinja2', request_method='GET')
def schedule_GET(request):
  # Display deafult calendar, with current month

  if 'permission' not in request.session:
    return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)

  if 'username' in request.session:
    now = datetime.datetime.now()
    days = schedule_management.get_fillness_of_month(now.year, now.month)
    return {'data' : schedule_management.get_my_schedules(request.session['username']), 'year': now.year, 'month': (now.month, now.strftime("%B")), 'days': monthrange(now.year, now.month), 'empty_days': days[0], 'average_days' : days[1], 'filled_days' : days[2]}
  else:
    return HTTPFound(location = request.route_url('home'))

@view_config(route_name='account', renderer='../templates/account.jinja2', request_method='GET')
def account_GET(request):

  if 'permission' not in request.session:
    return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)

  if request.session['permission'] == 1:
    return render_to_response('../templates/account_manager.jinja2', {'data' : user_management.get_all_user_data()}, request=request)
  elif 'username' in request.session:
    res = user_management.get_user_data(request.session['username'])
    return {'data': res}
  else:
    return HTTPFound(location = request.route_url('home'))

@view_config(route_name='account', renderer='../templates/account.jinja2', request_method='POST')
def account_POST(request):

  if 'permission' not in request.session:
    return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)
  if 'username' in request.session:
    name = request.POST["name"]
    email = request.POST["email"]
    phone = request.POST["phone"]
    address = request.POST["addr"]
    
    if user_management.update_user_data(request.session["username"], name, email, phone, address):
        return {'data' : user_management.get_user_data(request.session['username'])}
    else:
        return {'data' : user_management.get_user_data(request.session['username']), 'fail' : True}
  else:
    return HTTPFound(location = request.route_url('home'))

@view_config(route_name='manufacturer', renderer='../templates/manufacturer_manager.jinja2', request_method='GET')
def manufacturer_GET(request):

  if 'permission' in request.session:
    if request.session['permission'] != 1:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)
  else:
    return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)

  return {'data' : stock_management.get_all_manufacturers()}

@view_config(route_name='products', renderer='../templates/product_manager.jinja2', request_method='GET')
def products_GET(request):

  return {'data' : stock_management.get_all_products(), 'manufacturers' : stock_management.get_all_manufacturers()}

@view_config(route_name='service', renderer='../templates/service_manager.jinja2', request_method='GET')
def services_GET(request):

  if 'permission' in request.session:
    if request.session['permission'] != 1:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)
  else:
    return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)

  return {'data' : service_management.get_all_services()}

@view_config(route_name='cart', renderer='../templates/cart.jinja2', request_method='GET')
def cart_GET(request):

  if 'permission' in request.session:
    if request.session['permission'] != 0:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)
  else:
    return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)

  return {'data' : stock_management.get_cart_data(request.session['username'])}

@view_config(route_name='orders', renderer='../templates/orders.jinja2', request_method='GET')
def orders_GET(request):

  if 'permission' in request.session:
    if request.session['permission'] != 1:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)
  else:
    return render_to_response('../templates/403.jinja2', {'error' : True},
                                request=request)

  return {'data' : stock_management.get_orders()}
    
######################## JSON OBJECT ROUTES ######################
## The methods below are used for async calls from the frontend ##
##################################################################


# Returns the month name, month number, number of days in the month, how many days should be skipped, emptyness of the days
# OUTPUT: {month: [month number, month name], days: [days to be skipped, days in the month]}
@view_config(route_name='get_dates', renderer='json', request_method='POST')
def get_dates(request):

    if 'permission' not in request.session:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    

    year = int(request.POST['year'])
    month = int(request.POST['month'])
    days = schedule_management.get_fillness_of_month(year, month)
    return {'month': (month, datetime.datetime(year, month, 1, 1, 1, 1).strftime("%B")), 'days': monthrange(year, month), 'empty_days': days[0], 'average_days' : days[1], 'filled_days' : days[2], 'permission' : request.session['permission']}

# Returns the month name, month number, number of days in the month, how many days should be skipped, emptyness of the days
# OUTPUT: {month: [month number, month name], days: [days to be skipped, days in the month]}
@view_config(route_name='get_data_for_scheduling', renderer='json', request_method='POST')
def get_data_for_scheduling(request):

    if 'permission' not in request.session:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    

    year = int(request.POST['year'])
    month = int(request.POST['month'])
    day = int(request.POST['day'])

    hours = schedule_management.get_remaining_hours(year, month, day)
    services = service_management.get_all_services()
    num_plates = schedule_management.get_num_plates_available_for_scheduling(request.session['username'])

    return {'hours' : hours, 'services' : services, 'num_plates' : num_plates}

# Makes the schedule on the requested date
# OUTPUT: {success : true / false}
@view_config(route_name='make_schedule', renderer='json', request_method='POST')
def make_schedule(request):

    if 'permission' in request.session:
      if request.session['permission'] != 0:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    year = int(request.POST['year'])
    month = int(request.POST['month'])
    day = int(request.POST['day'])
    hour = int(request.POST['hour'])
    minute = int(request.POST['minute'])
    service_id = int(request.POST['service_id'])
    num_plate = request.POST['num_plate']

    if schedule_management.make_schedule(year, month, day, hour, minute, num_plate, service_id):
      return {'success' : 'true'}
    else:
      return {'success' : 'false'}

@view_config(route_name='delete_schedule', renderer='json', request_method='POST')
def delete_schedule(request):

    if 'permission' in request.session:
      if request.session['permission'] != 0:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    s_id = int(request.POST['id'])

    return { 'result' : str(schedule_management.delete_schedule(s_id))}


# Returns the scheduled cars on a day
# OUTPUT: {month: [month number, month name], days: [days to be skipped, days in the month]}
@view_config(route_name='get_schedules_of_day', renderer='json', request_method='POST')
def get_schedules_of_day(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    year = int(request.POST['year'])
    month = int(request.POST['month'])
    day = int(request.POST['day'])

    hour, minute, name, num_plate, service = schedule_management.get_schedule_of_day(year, month, day)

    return {'hour' : hour, 'minute' : minute, 'name' : name, 'num_plate' : num_plate, 'service' : service}


# Deletes a number plate from  a user
# OUTPUT: succesfully deleted or not
@view_config(route_name='delete_num_plate', renderer='json', request_method='POST')
def delete_num_plate(request):

    if 'permission' in request.session:
      if request.session['permission'] != 0:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    num_plate = str(request.POST['num_plate'])

    res = user_management.get_num_plates_and_users()
    result = False

    for i in res:
        if(num_plate == i[1] and request.session['username'] == i[0]):
            user_management.delete_num_plate(num_plate)
            result = True

    return {'result' : str(result)}

# Add a number plate for  a user
# OUTPUT: succesfully added or not
@view_config(route_name='add_num_plate', renderer='json', request_method='POST')
def add_num_plate(request):

    if 'permission' in request.session:
      if request.session['permission'] != 0:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    num_plate = str(request.POST['num_plate'])
    username = request.session['username']

    result = user_management.add_num_plate(num_plate,username)
    if result == None:
      return {'result' : "Number plate already in database!"}
    return {'result' : str(result)}

# Modify block on user
# OUTPUT: succesfully modified or not
@view_config(route_name='modify_block', renderer='json', request_method='POST')
def modify_block(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    userid = request.POST['user_id']
    action = request.POST['action']

    if request.session['permission'] == 1:
        return {'result' : str(user_management.modify_block(userid, action))}

# Modify permission of user
# OUTPUT: succesfully modified or not
@view_config(route_name='modify_permission', renderer='json', request_method='POST')
def modify_permission(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    userid = request.POST['user_id']
    action = request.POST['action']

    if request.session['permission'] == 1:
        return {'result' : str(user_management.modify_permission(userid, action))}

# Search users
# OUTPUT: a list of matched manufacturers
@view_config(route_name='search_users', renderer='json', request_method='POST')
def search_users(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    input_data = request.POST['input']
    return {'result' : user_management.search_users(input_data)}

# Add a manufacturer
# OUTPUT: succesfully added or not and the id of the added manufacturer
@view_config(route_name='add_manufacturer', renderer='json', request_method='POST')
def add_manufacturer(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    manufacturer = str(request.POST['manufacturer'])

    result, mid = stock_management.add_manufacturer(manufacturer)
    return {'result' : str(result), 'id' : mid}

# Delete a manufacturer
# OUTPUT: succesfully deleted or not
@view_config(route_name='delete_manufacturer', renderer='json', request_method='POST')
def delete_manufacturer(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    manufacturer = str(request.POST['manufacturer'])

    result = stock_management.delete_manufacturer(manufacturer)
    return {'result' : str(result)}

# Search manufacturer
# OUTPUT: a list of matched manufacturers
@view_config(route_name='search_manufacturer', renderer='json', request_method='POST')
def search_manufacturer(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    input_data = request.POST['input']
    return {'result' : stock_management.search_manufacturer(input_data)}

# Add a service
# OUTPUT: succesfully added or not and the id of the added service
@view_config(route_name='add_service', renderer='json', request_method='POST')
def add_service(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    service = str(request.POST['service'])

    result, sid = service_management.add_service(service)
    return {'result' : str(result), 'id' : sid}

# Delete a manufacturer
# OUTPUT: succesfully deleted or not
@view_config(route_name='delete_service', renderer='json', request_method='POST')
def delete_service(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
  
    service = str(request.POST['service'])

    result = service_management.delete_service(service)
    return {'result' : str(result)}

# Search product
# OUTPUT: a list of matched products
@view_config(route_name='search_product', renderer='json', request_method='POST')
def search_product(request):
    input_data = request.POST['input']
    search_type = request.POST['type']

    if 'permission' in request.session:
        if search_type == "by_name":
            return {'result' : stock_management.search_product_by_name(input_data), 'permission' : request.session['permission']}
        elif search_type == "by_size":
            return {'result' : stock_management.search_product_by_size(input_data), 'permission' : request.session['permission']}
        else:
            return {'result' : stock_management.search_product_by_price(input_data), 'permission' : request.session['permission']}
    else:
        if search_type == "by_name":
            return {'result' : stock_management.search_product_by_name(input_data), 'permission' : '-1'}
        elif search_type == "by_size":
            return {'result' : stock_management.search_product_by_size(input_data), 'permission' : '-1'}
        else:
            return {'result' : stock_management.search_product_by_price(input_data), 'permission' : '-1'}

# Add a product
# OUTPUT: succesfully added or not
@view_config(route_name='add_product', renderer='json', request_method='POST')
def add_product(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    manufacturer = request.POST['manufacturer']
    model = request.POST['model']
    size = request.POST['size']
    piece = request.POST['piece']
    price = request.POST['price']
    sales_price = request.POST['sales_price']

    result = stock_management.add_product(manufacturer, model, size, piece, price, sales_price)
    return {'result' : str(result)}

# Delete a product
# OUTPUT: succesfully deleted or not
@view_config(route_name='delete_product', renderer='json', request_method='POST')
def delete_product(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    p_id = str(request.POST['id'])

    result = stock_management.delete_product(p_id)
    return {'result' : str(result)}

# Update a product
# OUTPUT: succesfully updated or not
@view_config(route_name='update_product', renderer='json', request_method='POST')
def update_product(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    p_id = str(request.POST['id'])
    value = str(request.POST['value'])

    result = stock_management.update_product(p_id, value)
    return {'result' : str(result)}

# Add products to cart
# OUTPUT: succesfully updated or not
@view_config(route_name='add_to_cart', renderer='json', request_method='POST')
def add_to_cart(request):

    if 'permission' in request.session:
      if request.session['permission'] != 0:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    tyre_id = str(request.POST['tyre_id'])
    pieces = str(request.POST['pieces'])

    result, available = stock_management.add_to_cart(tyre_id, pieces, request.session['username'])
    return {'result' : str(result), 'available' : str(available)}

# Delete a product from cart
# OUTPUT: succesfully deleted or not
@view_config(route_name='delete_product_from_cart', renderer='json', request_method='POST')
def delete_product_from_cart(request):

    if 'permission' in request.session:
      if request.session['permission'] != 0:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    p_id = str(request.POST['id'])

    result = stock_management.delete_product_from_cart(p_id, request.session['username'])
    return {'result' : str(result)}

# Place order
# OUTPUT: succesfully sent or not
@view_config(route_name='place_order', renderer='json', request_method='POST')
def place_order(request):

    if 'permission' in request.session:
      if request.session['permission'] != 0:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    result = stock_management.place_order(request.session['username'])
    return {'result' : str(result)}

# Get order details
@view_config(route_name='get_order_details', renderer='json', request_method='POST')
def get_order_details(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    username = request.POST['username']
    date = request.POST['order_date']
    result = stock_management.get_order_details(username, date)
    return {'result' : result}

# Send order
# OUTPUT: succesfully sent or not
@view_config(route_name='send_order', renderer='json', request_method='POST')
def send_order(request):

    if 'permission' in request.session:
      if request.session['permission'] != 1:
        return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)
    else:
      return render_to_response('../templates/403.jinja2', {'error' : True},
                                  request=request)

    username = request.POST['username']
    date = request.POST['order_date']
    result = stock_management.send_order(username, date)
    return {'result' : str(result)}
