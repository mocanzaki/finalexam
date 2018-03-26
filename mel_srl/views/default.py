from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound
import re, logging
from ..scripts.db_conn import Connection 
from ..scripts import user_management

# File used for describing the template rendering and the actions on every route
# SYNTAX
# route_name must correspond to a route_name from ../routes.py
# renderer must be an existing template in ../templates
# function can have any name with a request parameter which stores data from the request
# can RETURN almost anything, but mostly the data to be rendered on the renderer in a dictionary
# dictionary key is used on the template to show the value of the key

@view_config(route_name='home', renderer='../templates/home.jinja2')
def home(request):
    session = request.session
    for key in session:
        print(str(key) + " : " + str(request.session[key]))
    return {'one': "one", 'project': 'mel_srl'}

@view_config(route_name='login', renderer='../templates/login.jinja2', request_method = 'GET')
def login_GET(request):
    return {'one': "alma", 'project': 'mel_srl'}

@view_config(route_name='login', renderer='../templates/login.jinja2', request_method = 'POST')
def login_POST(request):
    # Extract user data to be checked for login
    username = request.POST['username']
    password = request.POST['password']

    # Retrieve session from request
    session = request.session

    # Validate extracted data
    if not re.match("[a-zA-Z0-9-_.]{6,25}", username):
        logging.getLogger('user_management').debug('Injection attack detected on login from:' + request.remote_addr)
        return Response("Suspicious input on username!")
    if not re.match("[a-zA-Z0-9-_.,?!@#$&*<>:;]{6,20}", password):
        logging.getLogger('user_management').debug('Injection attack detected on login from:' + request.remote_addr)
        return Response("Suspicious input on password!")

    # Try to log in with the credentials
    permission = user_management.login(username, password)

    # Check for success
    if permission is not None:
        # Store unsensitive data in session
        session['username'] = username
        session['permission'] = permission

        return HTTPFound(location = request.route_url('home'))
    else:
        return Response("Couldn't log in")

@view_config(route_name='register', renderer='../templates/register.jinja2', request_method = 'GET')
def register_GET(request):
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

    # Validate extracted data
    if not re.match("[a-zA-Z0-9-_.]{6,25}", username):
        logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
        return Response("Suspicious input on username!")
    if not re.match("[a-zA-Z0-9-_. ]{6,30}", name):
        logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
        return Response("Suspicious input on name!")
    if not re.match("(\+[0-9]{11,})|([0-9]{10,})", phone):
        logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
        return Response("Suspicious input on phone!")
    if not re.match("(^[a-zA-Z]{1,2})( ?)([0-9]{2,3})( ?)([a-zA-Z]{3})|((^[a-zA-Z]{1,2})( ?)([0-9]){6})", num_plate):
        logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
        return Response("Suspicious input on number plate!")
    if not re.match("[a-zA-Z0-9-_.,?!@#$&*<>:;]{6,20}", password):
        logging.getLogger('user_management').debug('Injection attack detected on register from:' + request.remote_addr)
        return Response("Suspicious input on password!")

    # Try to submit data to the database
    if user_management.register(username, name, email, phone, num_plate, password):
        return {}
    else:
        return Response("Something went wrong.")

@view_config(route_name='logout')
def logout(request):
    session = request.session
    del session['username']
    del session['permission']
    return HTTPFound(location = request.route_url('home'))