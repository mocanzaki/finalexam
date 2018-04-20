def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Configure routing here
    # SYNTAX - config.add_route('route_name', 'route')
    # route_name must be an existing value in /views/default.py
    # route is the link which will redirect to route_name function
    
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('register', '/register')
    config.add_route('logout', '/logout')
    config.add_route('schedule', '/schedule')
    config.add_route('get_dates', '/json/get_dates')
    config.add_route('get_hours', '/json/get_hours')
    config.add_route('test', '/json/test/{year}/{month}/{day}')
