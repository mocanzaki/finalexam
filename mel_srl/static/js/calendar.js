function prevmonth(){
    var year = parseInt(document.getElementById("year").innerHTML);
    var month = parseInt(document.getElementById("month_no").innerHTML);
    if(month > 1){
            month = month - 1;
    }
    else{
        month = 12;
        year = year - 1;
    }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/get_dates", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("month_no").innerHTML = JSON.parse(this.responseText).month[0];
            document.getElementById("month_name").innerHTML = JSON.parse(this.responseText).month[1];
            document.getElementById("year").innerHTML = year;
            var days = JSON.parse(this.responseText).days;
            days[0] = parseInt(days[0]);
            days[1] = parseInt(days[1]);
            var filled_days = JSON.parse(this.responseText).filled_days;
            var average_days = JSON.parse(this.responseText).average_days;
            var permission = parseInt(JSON.parse(this.responseText).permission);
            var days_list = "";

            for(var i = 1; i < days[0] + 1; i++){
                days_list = days_list + "<li id = 'disabled'></li>";
            }

            for(var i = 1; i < days[1] + 1; i++){
                if((i + days[0]) % 7 == 0){
                    days_list = days_list + "<li id = 'disabled'>" + i + "</li>";
                }
                else{
                    if(permission == 0){
                        if(filled_days.includes(i))
                            days_list = days_list + "<li class = 'filled' id = 'disabled'>" + i + "</li>";
                        else if(average_days.includes(i))
                            days_list = days_list + "<li class = 'average' onclick = 'set_time(this)'>" + i + "</li>";
                        else
                            days_list = days_list + "<li class = 'empty' onclick = 'set_time(this)'>" + i + "</li>";
                    }else{
                        if(filled_days.includes(i))
                            days_list = days_list + "<li class = 'filled' id = 'disabled'>" + i + "</li>";
                        else if(average_days.includes(i))
                            days_list = days_list + "<li class = 'average' onclick = 'get_schedule(this)'>" + i + "</li>";
                        else
                            days_list = days_list + "<li class = 'empty' onclick = 'get_schedule(this)'>" + i + "</li>";
                    }
                }
            }

            document.getElementById("days").innerHTML = days_list;

        }
    };
    var params = "year=" + year + "&month=" + month;
    xhttp.send(params);

}

function nextmonth(){
    var year = parseInt(document.getElementById("year").innerHTML);
    var month = parseInt(document.getElementById("month_no").innerHTML);
    if(month < 12){
            month = month + 1;
    }
    else{
        month = 1;
        year = year + 1;
    }

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/get_dates", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("month_no").innerHTML = JSON.parse(this.responseText).month[0];
            document.getElementById("month_name").innerHTML = JSON.parse(this.responseText).month[1];
            document.getElementById("year").innerHTML = year;
            var days = JSON.parse(this.responseText).days;
            days[0] = parseInt(days[0]);
            days[1] = parseInt(days[1]);
            var filled_days = JSON.parse(this.responseText).filled_days;
            var average_days = JSON.parse(this.responseText).average_days;
            var days_list = "";

            for(var i = 1; i < days[0] + 1; i++){
                days_list = days_list + "<li id = 'disabled'></li>";
            }

            for(var i = 1; i < days[1] + 1; i++){
                if((i + days[0]) % 7 == 0){
                    days_list = days_list + "<li id = 'disabled'>" + i + "</li>";
                }
                else{
                    if(permission == 0){
                        if(filled_days.includes(i))
                            days_list = days_list + "<li class = 'filled' id = 'disabled'>" + i + "</li>";
                        else if(average_days.includes(i))
                            days_list = days_list + "<li class = 'average' onclick = 'set_time(this)'>" + i + "</li>";
                        else
                            days_list = days_list + "<li class = 'empty' onclick = 'set_time(this)'>" + i + "</li>";
                    }else{
                        if(filled_days.includes(i))
                            days_list = days_list + "<li class = 'filled' id = 'disabled'>" + i + "</li>";
                        else if(average_days.includes(i))
                            days_list = days_list + "<li class = 'average' onclick = 'get_schedule(this)'>" + i + "</li>";
                        else
                            days_list = days_list + "<li class = 'empty' onclick = 'get_schedule(this)'>" + i + "</li>";
                    }
                }
            }

            document.getElementById("days").innerHTML = days_list;

        }
    };
    var params = "year=" + year + "&month=" + month;
    xhttp.send(params);

}

function set_time(obj){
    if(document.getElementById("active") != null)
        document.getElementById("active").removeAttribute("id");
    obj.setAttribute("id", "active");
    var year = parseInt(document.getElementById("year").innerHTML);
    var month = parseInt(document.getElementById("month_no").innerHTML);
    var day = parseInt(obj.innerHTML);

    var inner_doc = '<label for="time">Time:</label><select class="form-control" id="hour">';

    var hours = [];
    var minutes = [];

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/get_data_for_scheduling", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            hour = JSON.parse(this.responseText).hours;
            services = JSON.parse(this.responseText).services;
            num_plates = JSON.parse(this.responseText).num_plates;

            for(var i = 0; i < hour.length; i++){

                if(hour[i].startsWith("1")){
                    if(hour[i].length == 3){
                        inner_doc = inner_doc + '<option>' + hour[i].substring(0,2) + ':' + hour[i].substring(2,3) + '</option>';
                    }
                    else{
                        inner_doc = inner_doc + '<option>' + hour[i].substring(0,2) + ':' + hour[i].substring(2,4) + '</option>';
                    }
                }

                else{
                    if(hour[i].length == 2){
                        inner_doc = inner_doc + '<option>' + hour[i].substring(0,1) + ':' + hour[i].substring(1,2) + '</option>';
                    }
                    else{
                        inner_doc = inner_doc + '<option>' + hour[i].substring(0,1) + ':' + hour[i].substring(1,3) + '</option>';
                    }
                }
            }

            inner_doc = inner_doc + '</select><label for="num_plate">Number plate:</label><select class="form-control" id="num_plate">';

            for(var i = 0; i < num_plates.length; i++){

                inner_doc = inner_doc + '<option>' + num_plates[i] + '</option>';
                
            }

            inner_doc = inner_doc + '</select><label for="services">Service:</label><select class="form-control" id="services">';

            for(var i = 0; i < services.length; i++){

                inner_doc = inner_doc + '<option>' + services[i][1] + '</option>';
                
            }

            inner_doc = inner_doc + '</select><button type = "submit" class="btn btn-warning" value="schedule" onclick ="schedule()">Schedule</button>';
            document.getElementById("day_content").innerHTML = inner_doc;

        }
    };
    var params = "year=" + year + "&month=" + month + "&day=" + day;
    xhttp.send(params);
}

function schedule(){
    var year = parseInt(document.getElementById("year").innerHTML);
    var month = parseInt(document.getElementById("month_no").innerHTML);
    var day = parseInt(document.getElementById("active").innerHTML);
    var time = document.getElementById("hour").options[document.getElementById("hour").options.selectedIndex].text;
    var service_id = parseInt(document.getElementById("services").options.selectedIndex) + 1;
    var hour = parseInt(time.split(":")[0]);
    var minute = parseInt(time.split(":")[1]);
    try{
        var num_plate = document.getElementById("num_plate").options[document.getElementById("num_plate").options.selectedIndex].text;
        document.getElementById("num_plate").remove(document.getElementById("num_plate").selectedIndex);
        document.getElementById("hour").remove(document.getElementById("hour").selectedIndex);
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/json/make_schedule", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if (JSON.parse(this.responseText).success == 'true')
                    alert("OK!");
                else{
                    alert("NOT OK!");
                }
            }
        };

        var params = "year=" + year + "&month=" + month + "&day=" + day + "&hour=" + hour + "&minute=" + minute + "&service_id=" + service_id + "&num_plate=" + num_plate;
        xhttp.send(params);
    }catch(err){
        alert("Please select a number plate! In case the list is empty, you already have scheduled all your cars!");
    }
}

function get_schedule(obj){
    if(document.getElementById("active") != null)
        document.getElementById("active").removeAttribute("id");
    obj.setAttribute("id", "active");
    var year = parseInt(document.getElementById("year").innerHTML);
    var month = parseInt(document.getElementById("month_no").innerHTML);
    var day = parseInt(obj.innerHTML);

    var inner_doc = '<table class="table table-hover"><thead class = "thead-dark"><tr><th>Time</th><th>Name</th><th>Number plate</th><th>Service</th></tr></thead><tbody>';

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/json/get_schedules_of_day", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var hour = JSON.parse(this.responseText).hour;
            var minute = JSON.parse(this.responseText).minute;  
            var name = JSON.parse(this.responseText).name; 
            var num_plate = JSON.parse(this.responseText).num_plate; 
            var service = JSON.parse(this.responseText).service; 

            var k = 0;

            for(var i = 8; i < 17; i++){

                if(k < hour.length && parseInt(hour[k]) == i){
                    while(k < hour.length && parseInt(hour[k]) == i){
                        console.log(hour[k]);
                        console.log(minute[k]);
                        console.log(name[k]);
                        console.log(num_plate[k]);
                        console.log(service[k]);
                        inner_doc = inner_doc + "<tr><td>" + hour[k] + ":" + minute[k] + "</td><td>" + name[k] + "</td><td>" + num_plate[k] + "</td><td>" + service[k] + "</td></tr>";

                        k = k + 1;
                    }
                }
                else{
                    inner_doc = inner_doc + "<tr><td>" + i + ":00</td><td>-</td><td>-</td><td>-</td></tr>";
                    inner_doc = inner_doc + "<tr><td>" + i + ":30</td><td>-</td><td>-</td><td>-</td></tr>";
                }
            }         

            inner_doc = inner_doc + '</tbody></table>';
            console.log(hour.indexOf(8))
            document.getElementById("day_content").innerHTML = inner_doc;
        }
    };
    var params = "year=" + year + "&month=" + month + "&day=" + day;
    xhttp.send(params);
}