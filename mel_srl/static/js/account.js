function add_new_num_plate(){
    var div = document.getElementById("num_plates_div");
    try{
        var last_id = document.getElementsByName("num_plate").length + 1;
    }
    catch(err){
        var last_id = 0;
    }
    var doc = '<div class="input-group">' +
            '<input type = "text" class = "form-control" name = "num_plate" id = "num_plate' + last_id + '" minlength = "6" maxlength = "10" pattern = "(^[a-zA-Z]{1,2})( ?)([0-9]{2,3})( ?)([a-zA-Z]{3})|((^[a-zA-Z]{1,2})( ?)([0-9]){6})" placeholder = "Number plate" style = "margin-bottom: 1%;" required/>' +
            '<span class="input-group-btn">' +
              '<button class="btn btn-danger" type="button" id = "delete' + last_id + '" onclick="delete_num_plate(' + last_id + ')">Delete</button>' +
            '</span><span class="input-group-btn">' +
              '<button class="btn btn-success" type="button" id = "add' + last_id + '" onclick="add_num_plate(' + last_id + ')">Add</button>' +
            '</span></div>';
    div.innerHTML += doc;
}

function delete_num_plate(obj){
    var num_plate = document.getElementById("num_plate" + String(obj)).value;
    if(num_plate == ""){
        document.getElementById("num_plate" + obj).parentElement.remove();
    }
    else{
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/json/delete_num_plate", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var result = JSON.parse(this.responseText).result;
                if (result == 'True'){
                    document.getElementById("num_plate" + obj).parentElement.remove();
                    alert("Succesfully deleted number plate");
                }
                else if(result == 'False'){
                    alert("Something went wrong when deleting number plate");
                }
                else{
                    alert("Number plate already in database! Please use only your own!");
                }
            }
        };
        var params = "num_plate=" + num_plate;
        xhttp.send(params);
    }

}

function add_num_plate(obj){
    var num_plate = document.getElementById("num_plate" + String(obj)).value;
    if(num_plate != ""){
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/json/add_num_plate", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var result = JSON.parse(this.responseText).result;
                if (result == 'True'){
                    document.getElementById("num_plate" + obj).disabled = true;
                    document.getElementById("add" + obj).parentElement.removeChild(document.getElementById("add" + obj));
                    alert("Succesfully added number plate");
                }
                else{
                    alert("Something went wrong when adding number plate");
                }
            }
        };
        var params = "num_plate=" + num_plate;
        xhttp.send(params);
    }
    else{
        alert("Can not add empty number plate!");
    }
}

function block(obj){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/modify_block", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if (result == 'True'){
                alert("Succesfully blocked user!");
                document.getElementById("btn"+obj).innerHTML = "Unblock";
                document.getElementById("btn"+obj).setAttribute( "onClick", "unblock("+obj+");" );
            }
            else{
                alert("Something went wrong when blocking user!");
            }
        }
    };
    var params = "action=block&user_id=" + obj;
    xhttp.send(params);
    
}

function unblock(obj){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/modify_block", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            if (result == 'True'){
                document.getElementById("btn"+obj).innerHTML = "Block";
                document.getElementById("btn"+obj).setAttribute( "onClick", "block("+obj+");" );
                alert("Succesfully unblocked user!");
            }
            else{
                alert("Something went wrong when unblocking user!");
            }
        }
    };
    var params = "action=unblock&user_id=" + obj;
    xhttp.send(params);
    
}

function filter(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/search_users", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText).result;
            var inner = "";
            for(var i = 0; i < result.length; i++){
                inner += "<tr><td>" + result[i][0] + "</td><td>" + result[i][1] + "</td><td>" + result[i][2] + "</td><td>" + result[i][3] + "</td><td>" + result[i][4] + "</td><td>";
                if(result[i][5] == 0){
                    inner += "<button id = 'btn" + result[i][0] + "' class = 'btn btn-info' onclick = 'block(" + result[i][0] + ")'>Block</button>";
                }
                else{
                    inner += "<button id = 'btn" + result[i][0] + "' class = 'btn btn-info' onclick = 'unblock(" + result[i][0] + ")'>Unblock</button>";
                }
                inner += "</td></tr>";
            }

            document.getElementById("mainbody").innerHTML = inner;
        }
    };
    var params = "input=" + document.getElementById("search").value;
    xhttp.send(params);
}