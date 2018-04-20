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
            var days_list = "";

            for(var i = 1; i < days[0] + 1; i++){
                days_list = days_list + "<li id = 'disabled'></li>";
            }

            for(var i = 1; i < days[1] + 1; i++){
                if((i + days[0]) % 7 == 0){
                    days_list = days_list + "<li id = 'disabled'>" + i + "</li>";
                }
                else{
                    if(filled_days.includes(i))
                        days_list = days_list + "<li class = 'filled' id = 'disabled'>" + i + "</li>";
                    else if(average_days.includes(i))
                        days_list = days_list + "<li class = 'average' onclick = 'set_time(this)'>" + i + "</li>";
                    else
                        days_list = days_list + "<li class = 'empty' onclick = 'set_time(this)'>" + i + "</li>";
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
                    if(filled_days.includes(i))
                        days_list = days_list + "<li class = 'filled' id = 'disabled'>" + i + "</li>";
                    else if(average_days.includes(i))
                        days_list = days_list + "<li class = 'average' onclick = 'set_time(this)'>" + i + "</li>";
                    else
                        days_list = days_list + "<li class = 'empty' onclick = 'set_time(this)'>" + i + "</li>";
                }
            }

            document.getElementById("days").innerHTML = days_list;

        }
    };
    var params = "year=" + year + "&month=" + month;
    xhttp.send(params);

}

function set_time(obj){
    var year = parseInt(document.getElementById("year").innerHTML);
    var month = parseInt(document.getElementById("month_no").innerHTML);
    var day = parseInt(obj.innerHTML);

    var select_list = '<label for="time">Time:</label><select class="form-control" id="hour">';

    var hours = [];
    var minutes = [];

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "json/get_hours", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            hour = JSON.parse(this.responseText).hours;
            console.log(hour);
            for(var i = 0; i < hour.length; i++){

                if(hour[i].startsWith("1")){
                    if(hour[i].length == 3){
                        select_list = select_list + '<option>' + hour[i].substring(0,2) + ':' + hour[i].substring(2,3) + '</option>';
                    }
                    else{
                        select_list = select_list + '<option>' + hour[i].substring(0,2) + ':' + hour[i].substring(2,4) + '</option>';
                    }
                }

                else{
                    if(hour[i].length == 2){
                        select_list = select_list + '<option>' + hour[i].substring(0,1) + ':' + hour[i].substring(1,2) + '</option>';
                    }
                    else{
                        select_list = select_list + '<option>' + hour[i].substring(0,1) + ':' + hour[i].substring(1,3) + '</option>';
                    }
                }
            }

            document.getElementById("select_time").innerHTML = select_list + '</select><button type = "submit" class="btn btn-warning" value="submit">Submit</button>';

        }
    };
    var params = "year=" + year + "&month=" + month + "&day=" + day;
    xhttp.send(params);
}