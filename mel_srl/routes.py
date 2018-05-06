def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Configure routing here
    # SYNTAX - config.add_route('route_name', 'route')
    # route_name must be an existing value in /views/default.py
    # route is the link which will redirect to route_name function
    
    ##########################################################
    ################# GUEST ROUTES ###########################
    ########################################################## 

    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('register', '/register')


    ##########################################################
    ################# USER ROUTES ############################
    ##########################################################

    config.add_route('logout', '/logout')
    config.add_route('schedule', '/schedule')
    config.add_route('account', '/account')


    ##########################################################
    ################# ADMIN ROUTES ###########################
    ##########################################################

    ##########################################################
    ################# JSON ROUTES ############################
    ##########################################################
    
    config.add_route('get_dates', '/json/get_dates')
    config.add_route('get_data_for_scheduling', '/json/get_data_for_scheduling')
    config.add_route('make_schedule', '/json/make_schedule')
    config.add_route('get_schedules_of_day', '/json/get_schedules_of_day')
    config.add_route('delete_num_plate', '/json/delete_num_plate')
