from pyramid.response import Response
from pyramid.view import view_config
from scripts.db_conn import Connection 

# File used for describing the template rendering and the actions on every route
# SYNTAX
# route_name must correspond to a route_name from ../routes.py
# renderer must be an existing template in ../templates
# function can have any name with a request parameter which stores data from the request
# can RETURN almost anything, but mostly the data to be rendered on the renderer in a dictionary
# dictionary key is used on the template to show the value of the key

@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def home(request):
    return {'one': "one", 'project': 'mel_srl'}

@view_config(route_name='login', renderer='../templates/mytemplate.jinja2')
def login(request):
    return {'one': "alma", 'project': 'mel_srl'}

@view_config(route_name='register', renderer='../templates/register.jinja2', request_method = 'GET')
def register_GET(request):
    return {}

@view_config(route_name='register', renderer='../templates/register.jinja2', request_method = 'POST')
def register_POST(request):
    return Response("succesfully registered")