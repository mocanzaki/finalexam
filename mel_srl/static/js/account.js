function add_new_num_plate(){
    var div = document.getElementById("num_plates_div");
    try{
        var last_id = parseInt(document.getElementsByName("num_plate")[document.getElementsByName("num_plate").length - 1].getAttribute("id").substring(9));
    }
    catch(err){
        last_id = 0;
    }
    var doc = '<div class="input-group">' +
            '<input type = "text" class = "form-control" name = "num_plate" id = "num_plate' + last_id + '" minlength = "6" maxlength = "10" pattern = "(^[a-zA-Z]{1,2})( ?)([0-9]{2,3})( ?)([a-zA-Z]{3})|((^[a-zA-Z]{1,2})( ?)([0-9]){6})" placeholder = "Number plate" style = "margin-bottom: 1%;" required/>' +
            '<span class="input-group-btn">' +
              '<button class="btn btn-danger" type="button" id = "delete' + last_id + '" onclick="delete_num_plate(' + last_id + ')">Delete</button>' +
            '</span></div>';
    div.innerHTML += doc;
}

function delete_num_plate(obj){
    var num_plate = document.getElementById("num_plate" + String(obj)).value;

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
            else{
                alert("Something went wrong when deleting number plate");
            }
        }
    };
    var params = "num_plate=" + num_plate;
    xhttp.send(params);

}