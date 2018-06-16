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
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/search_product", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            var inner = "";

            if(result.length == 0){
                inner = "<tr><td></td><td>No product found matching your search!</td><td></td><td></td><td></td><td></td></tr>";
            }else{
                for(var i = 0; i < result.length; i++){
                    inner += "<tr><td>" + result[i][1] + "</td><td>" + result[i][2] + "</td><td>" + result[i][3] + "/ " + result[i][4] + "/ R" + result[i][5] + "</td><td>" + result[i][6] + "</td><td>" + result[i][7] + "</td><td>" + result[i][8] + "</td></tr>";
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
            if (result == 'True'){
                document.getElementById("row_" + obj).remove();
                alert("Succesfully deleted manufacturer");
            }
            else{
                alert("Something went wrong when deleting manufacturer");
            }
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
            if (result == 'True'){
                document.getElementById("row_" + obj).remove();
                alert("Succesfully deleted service");
            }
            else{
                alert("Something went wrong when deleting service");
            }
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
                    alert("Succesfully added manufacturer");
                }
                else if(result == 'False'){
                    alert("Something went wrong when adding manufacturer");
                }
                else{
                    alert("Manufacturer already in database");
                }
            }
        };
        var params = "manufacturer=" + document.getElementById("manufacturer").value;
        xhttp.send(params);
    }
    else{
        alert("Can not add empty manufacturer!");
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
                    alert("Succesfully added service");
                }
                else if(result == 'False'){
                    alert("Something went wrong when adding service");
                }
                else{
                    alert("Service already in database");
                }
            }
        };
        var params = "service=" + document.getElementById("service").value;
        xhttp.send(params);
    }
    else{
        alert("Can not add empty service!");
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
            if (result == 'True'){
                location.reload();
                alert("Succesfully added product");
            }
            else{
                alert("Something went wrong when adding product!");
            }
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
            if (result == 'True'){
                location.reload();
                alert("Succesfully deleted product");
            }
            else{
                alert("Something went wrong when deleting product!");
            }
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
            if (result == 'True'){
                location.reload();
                alert("Succesfully updated product");
            }
            else{
                alert("Something went wrong when updating product!");
            }
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