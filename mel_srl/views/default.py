from pyramid.response import Response
from pyramid.renderers import render_to_response
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

        # Check for success
        if permission is not None:
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
        if user_management.register(username, name, email, phone, num_plate, password):
            return render_to_response('../templates/register.jinja2',
                                  {'successfully_registered' : True},
                                  request=request)
        else:
            return render_to_response('../templates/register.jinja2',
                                  {'credential_error' : True},
                                  request=request)

@view_config(route_name='logout')
def logout(request):
    session = request.session
    try:
        del session['username']
        del session['permission']
    except:
        pass
    return HTTPFound(location = request.route_url('home'))