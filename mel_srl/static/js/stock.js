function delete_manufacturer(obj){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/delete_manufacturer", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if (result == 'True'){
                document.getElementById("row_" + obj.innerHTML).remove();
                alert("Succesfully deleted manufacturer");
            }
            else{
                alert("Something went wrong when deleting manufacturer");
            }
        }
    };
    var params = "manufacturer=" + obj.innerHTML;
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
                if (result == 'True'){
                    var inner = "<tr id = 'row_" + document.getElementById("manufacturer").value + "'><td id = '" + document.getElementById("manufacturer").value + "'>" + document.getElementById("manufacturer").value +
                     "</td><td><button class = 'btn btn-danger' onclick = 'delete_manufacturer(" + document.getElementById("manufacturer").value + ")'>Delete</button></td></tr>";
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

function filter_manufacturers(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/search_manufacturer", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            var inner = "";

            if(result.length == 0){
                inner = "<tr><td></td><td>No manufacturer found matching your search!</td><td></td><td></td><td></td><td></td></tr>";
            }else{
                for(var i = 0; i < result.length; i++){
                    inner += "<tr id = 'row_" + result[i][0] + "'><td id = '" +
                     result[i][0] + "'>" + result[i][0] + "</td><td><button class = 'btn btn-danger' onclick = 'delete_manufacturer(" + 
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