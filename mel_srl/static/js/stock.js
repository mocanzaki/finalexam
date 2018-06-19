function filter_manufacturers(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/search_manufacturer", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            var inner = "";

            if(result.length == 0){
                inner = "<tr><td></td><td>No manufacturer found matching your search!</td></tr>";
            }else{
                for(var i = 0; i < result.length; i++){
                    inner += "<tr id = 'row_" + result[i][0] + "'><td id = '" +
                     result[i][0] + "'>" + result[i][1] + "</td><td><button class = 'btn btn-danger' onclick = 'delete_manufacturer(" + 
                     result[i][0] + ")'>Delete</button></td></tr>";
                }
                inner += '<tr id = "new_manufacturer"><td><input type = "text" class = "form-control" id = "manufacturer" placeholder = "New manufacturer"></td>' +
                    '<td><button class = "btn btn-success" onclick = "add_manufacturer()">Add</button></td></tr>';
            }

            document.getElementById("mainbody").innerHTML = inner;
        }
    };
    var params = "input=" + document.getElementById("search").value;
    xhttp.send(params);
}

function filter_services(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/search_service", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            var inner = "";

            if(result.length == 0){
                inner = "<tr><td></td><td>No service found matching your search!</td><td></td></tr>";
            }else{
                for(var i = 0; i < result.length; i++){
                    inner += "<tr id = 'row_" + result[i][0] + "'><td id = '" +
                     result[i][0] + "'>" + result[i][1] + "</td><td><button class = 'btn btn-danger' onclick = 'delete_service(" + 
                     result[i][0] + ")'>Delete</button></td></tr>";
                }
                inner += '<tr id = "new_service"><td><input type = "text" class = "form-control" id = "service" placeholder = "New service"></td>' +
                    '<td><button class = "btn btn-success" onclick = "add_service()">Add</button></td></tr>';
            }

            document.getElementById("mainbody").innerHTML = inner;
        }
    };
    var params = "input=" + document.getElementById("search").value;
    xhttp.send(params);
}

function filter_products(){
    if(document.getElementById("search").value == ""){
        location.reload();
    }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/search_product", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            var permission = parseInt(JSON.parse(this.responseText).permission);
            var inner = "";

            if(result.length == 0){
                inner = "<tr><td></td><td>No product found matching your search!</td><td></td><td></td><td></td><td></td></tr>";
            }else{
                if(permission == -1){
                    for(var i = 0; i < result.length; i++){
                        inner += "<tr><td>" + result[i][1] + "</td><td>" + result[i][2] + "</td><td>" + result[i][3] + "/ " + result[i][4] + "/ R" + result[i][5] + "</td><td>" + result[i][6] + "</td><td>" + result[i][7] + "</td><td>" + result[i][8] + "</td></tr>";
                    }
                }
                else if(permission == 0){
                    for(var i = 0; i < result.length; i++){
                        inner += "<tr id = 'row_" + result[i][0] + "'><td>" + result[i][1] + "</td><td>" + result[i][2] + "</td><td>" + result[i][3] + "/ " + result[i][4] + "/ R" + result[i][5] + "</td><td>" + result[i][6] + "</td><td>" + result[i][7] + "</td><td>" + result[i][8] + "</td><td><div class = 'form-inline'><input type='text' class='form-control' style = 'width: 15%; margin-right: 2%'  id = 'pieces_" + result[i][0] + "' min = '0' value='1'><button class = 'btn btn-success' onclick = 'add_to_cart(" + result[i][0] + ")'>Add to cart</button></div></td></tr>";
                    }
                }else if(permission == 1){
                    for(var i = 0; i < result.length; i++){
                        inner += "<tr><td>" + result[i][1] + "</td><td>" + result[i][2] + "</td><td>" + result[i][3] + "/ " + result[i][4] + "/ R" + result[i][5] + "</td><td><input type = 'text' class = 'form-control' value = '" + result[i][6] + "' id = 'piece_" + result[i][0] + "' onchange = 'update_product(" + result[i][6] + ")'></td><td>" + result[i][7] + "</td><td>" + result[i][8] + "</td><td><button class = 'btn btn-success' onclick = 'delete_product(" + result[i][0] + ")'>Delete</button></div></td></tr>";
                    }   
                }
            }

            document.getElementById("mainbody").innerHTML = inner;
        }
    };
    var params = "input=" + document.getElementById("search").value + "&type=" + document.querySelector('input[name="search_type"]:checked').value;
    xhttp.send(params);
}

function delete_manufacturer(obj){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/delete_manufacturer", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("row_" + obj).remove();
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully deleted manufacturer!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while deleting manufacturer!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';

            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };
    var params = "manufacturer=" + obj;
    xhttp.send(params);
}

function delete_service(obj){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/delete_service", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully deleted the service!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while deleting the service!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';

            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };
    var params = "service=" + obj;
    xhttp.send(params);
}

function add_manufacturer(){
    if(document.getElementById("manufacturer").value != ""){
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/json/add_manufacturer", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var result = JSON.parse(this.responseText).result;
                var id = JSON.parse(this.responseText).id;
                if (result == 'True'){
                    var inner = "<tr id = 'row_" + id + "'><td id = '" + id + "'>" + document.getElementById("manufacturer").value +
                     "</td><td><button class = 'btn btn-danger' onclick = 'delete_manufacturer(" + id + ")'>Delete</button></td></tr>";
                    document.getElementById("new_manufacturer").remove();
                    document.getElementById("mainbody").innerHTML += inner + '<tr id = "new_manufacturer"><td><input type = "text" class = "form-control"' +
                     'id = "manufacturer" placeholder = "New manufacturer"></td><td><button class = "btn btn-success" onclick = "add_manufacturer()">Add</button></td></tr>';
                    document.getElementById("modal_header").innerHTML = "Request result"; 
                    document.getElementById("modal_body").innerHTML = "Succesfully added the manufacturer!"; 
                    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
                }
                else if(result == 'False'){
                    document.getElementById("modal_header").innerHTML = "Request result"; 
                    document.getElementById("modal_body").innerHTML = "Something went wrong while adding the manufacturer!"; 
                    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
                }
                else{
                    document.getElementById("modal_header").innerHTML = "Request result"; 
                    document.getElementById("modal_body").innerHTML = "Manufacturer already in database!"; 
                    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
                }
                $(document).ready(function(){
                    $("#myModal").modal();
                });
            }
        };
        var params = "manufacturer=" + document.getElementById("manufacturer").value;
        xhttp.send(params);
    }
    else{
        document.getElementById("modal_header").innerHTML = "Request result"; 
        document.getElementById("modal_body").innerHTML = "Can not add empty manufacturer!"; 
        document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
        $(document).ready(function(){
            $("#myModal").modal();
        });   
    }
}

function add_service(){
    if(document.getElementById("service").value != ""){
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/json/add_service", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var result = JSON.parse(this.responseText).result;
                var id = JSON.parse(this.responseText).id;
                if (result == 'True'){
                    var inner = "<tr id = 'row_" + id + "'><td id = '" + id + "'>" + document.getElementById("service").value +
                     "</td><td><button class = 'btn btn-danger' onclick = 'delete_service(" + id + ")'>Delete</button></td></tr>";
                    document.getElementById("new_service").remove();
                    document.getElementById("mainbody").innerHTML += inner + '<tr id = "new_service"><td><input type = "text" class = "form-control"' +
                     'id = "service" placeholder = "New service"></td><td><button class = "btn btn-success" onclick = "add_service()">Add</button></td></tr>';
                    document.getElementById("modal_header").innerHTML = "Request result"; 
                    document.getElementById("modal_body").innerHTML = "Succesfully added new service!"; 
                    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
                }
                else if(result == 'False'){
                    document.getElementById("modal_header").innerHTML = "Request result"; 
                    document.getElementById("modal_body").innerHTML = "Something went wring while adding new service!"; 
                    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
                }
                else{
                    document.getElementById("modal_header").innerHTML = "Request result"; 
                    document.getElementById("modal_body").innerHTML = "Service already in database!"; 
                    document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
                }
                $(document).ready(function(){
                    $("#myModal").modal();
                });
            }
        };
        var params = "service=" + document.getElementById("service").value;
        xhttp.send(params);
    }
    else{
        document.getElementById("modal_header").innerHTML = "Request result"; 
        document.getElementById("modal_body").innerHTML = "Can not add empty service!"; 
        document.getElementById("modal_footer").innerHTML = '<button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>';
        $(document).ready(function(){
            $("#myModal").modal();
        });
    }
}

function add_product(){
    var manufacturer = document.getElementById("new_manufacturer").options[document.getElementById("new_manufacturer").options.selectedIndex].value;
    var model = document.getElementById("new_model").value;
    var size = document.getElementById("new_size").value;
    var piece = document.getElementById("new_pieces").value;
    var price = document.getElementById("new_price").value;
    var sales_price = document.getElementById("new_sales_price").value;

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/add_product", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully added the product!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while adding the product!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';

            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };
    var params = "manufacturer=" + manufacturer + "&model=" + model + "&size=" + size + "&piece=" + piece + "&price=" + price + "&sales_price=" + sales_price;
    xhttp.send(params);

}

function delete_product(obj){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/delete_product", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully deleted the product!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while deleting the product!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';

            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };
    var params = "id=" + obj;
    xhttp.send(params);

}

function update_product(obj){

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/update_product", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully updated the product!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while updating the product!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';

            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };

    if(document.getElementById("piece_" + obj).value.startsWith('+')){
        var params = "id=" + obj + "&value=" + document.getElementById("piece_" + obj).value.replace('+','*');
        xhttp.send(params);
    }
    else{
        var params = "id=" + obj + "&value=" + document.getElementById("piece_" + obj).value;
        xhttp.send(params);
    }

}

function add_to_cart(obj){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/add_to_cart", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully added the product tot cart!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
            }
            else if(result == 'False'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while adding the product to cart!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
              
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Not enough products on stock! Only " + JSON.parse(this.responseText).available + " pieces available."; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
               
            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };

    var params = "tyre_id=" + obj + "&pieces=" + document.getElementById("pieces_" + obj).value;
    xhttp.send(params);
}

function delete_product_from_cart(obj){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/delete_product_from_cart", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully deleted the product from cart!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
               
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while deleting the product from cart!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
               
            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };
    var params = "id=" + obj;
    xhttp.send(params);

}

function place_order(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/place_order", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully placed the order!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
                
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while placing the order!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
               
            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };
    xhttp.send();

}

function show_order_details(username, order_date){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/get_order_details", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var total = 0;
            var result = JSON.parse(this.responseText).result;
            var inner = '<table class="table table-hover"><thead class = "thead-dark"><tr><th>Manufacturer</th><th>Model</th><th>Size</th><th>Pieces</th><th>Price</th></tr></thead>';
            document.getElementById("modal_header").innerHTML = username + "'s order"; 

            for(var i = 0; i < result.length; i++){
                inner += "<tr><td>" + result[i][0] + "</td><td>" + result[i][1] + "</td><td>" + result[i][2] + "/ " + result[i][3] + "/ R" + result[i][4] + "</td><td>" + result[i][5] + "</td><td>" + result[i][6] + "</td></tr>";
                total += parseInt(result[i][6] ) * parseInt(result[i][5] );
            }

            inner += "<tr><td></td><td></td><td></td><td></td><td>Total: " + total + "RON</td></tr>";
            document.getElementById("modal_body").innerHTML = inner;
            order_date = '"' + order_date + '"';
            username = '"' + username + '"';
            document.getElementById("modal_footer").innerHTML = "<button type='button' class='btn btn-danger' data-dismiss='modal'>Close</button><button class = 'btn btn-info' onclick = 'send_order(" + username + "," + order_date + ")'>Send order</button>";

            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };
    var params = "username=" + username + "&order_date=" + order_date;
    xhttp.send(params);
}

function send_order(username, order_date){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/send_order", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if(result == 'True'){
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Succesfully sent the order!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
               
            }
            else{
                document.getElementById("modal_header").innerHTML = "Request result"; 
                document.getElementById("modal_body").innerHTML = "Something went wrong while sending the order!"; 
                document.getElementById("modal_footer").innerHTML = '<button type="button" onclick = "location.reload()" class="btn btn-danger" data-dismiss="modal">Close</button>';
                
            }
            $(document).ready(function(){
                $("#myModal").modal();
            });
        }
    };
    var params = "username=" + username + "&order_date=" + order_date;
    xhttp.send(params);
}
