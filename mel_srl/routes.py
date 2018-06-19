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
    config.add_route('cart', '/cart')


    ##########################################################
    ################# ADMIN ROUTES ###########################
    ##########################################################

    config.add_route('manufacturer', '/manufacturers')
    config.add_route('products', '/products')
    config.add_route('service', '/services')
    config.add_route('orders', '/orders')

    ##########################################################
    ################# JSON ROUTES ############################
    ##########################################################
    
    config.add_route('get_dates', '/json/get_dates')
    config.add_route('get_data_for_scheduling', '/json/get_data_for_scheduling')
    config.add_route('make_schedule', '/json/make_schedule')
    config.add_route('get_schedules_of_day', '/json/get_schedules_of_day')
    config.add_route('delete_schedule', '/json/delete_schedule')

    config.add_route('delete_num_plate', '/json/delete_num_plate')
    config.add_route('add_num_plate', '/json/add_num_plate')

    config.add_route('modify_block', '/json/modify_block')
    config.add_route('modify_permission', '/json/modify_permission')
    config.add_route('search_users', '/json/search_users')

    config.add_route('add_manufacturer', '/json/add_manufacturer')
    config.add_route('delete_manufacturer', '/json/delete_manufacturer')
    config.add_route('search_manufacturer', '/json/search_manufacturer')

    config.add_route('search_product', '/json/search_product')
    config.add_route('add_product', '/json/add_product')
    config.add_route('delete_product', '/json/delete_product')
    config.add_route('update_product', '/json/update_product')

    config.add_route('add_service', '/json/add_service')
    config.add_route('delete_service', '/json/delete_service')
    config.add_route('search_service', '/json/search_service')

    config.add_route('add_to_cart', '/json/add_to_cart')
    config.add_route('delete_product_from_cart', '/json/delete_product_from_cart')
    config.add_route('place_order', '/json/place_order')

    config.add_route('get_order_details', '/json/get_order_details')
    config.add_route('send_order', '/json/send_order')
