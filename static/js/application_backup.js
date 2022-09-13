
$(document).ready(function(){
 $("button").click(function(){

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var data_received = [];
    var table = document.getElementById("dataTable");
    var row = '';	

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received Data" + msg.data);
        
        
        data_received.push(msg.data);
        var data_string = '';
        for (var i = 0; i < data_received.length; i++)
        {
        	
		row = table.insertRow(1);
		cell1 = row.insertCell(0);
		cell2 = row.insertCell(1);
		cell3 = row.insertCell(2);
		cell4 = row.insertCell(3);
		cell5 = row.insertCell(4);
		
		/* DEBUG
		console.log("Data Received " + i + " : " + data_received[i][0]);
		console.log("Data Received " + i + " : " + data_received[i][1]);
		console.log("Data Received " + i + " : " + data_received[i][2]);
		console.log("Data Received " + i + " : " + data_received[i][3]);
		console.log("Data Received " + i + " : " + data_received[i][4]);
		*/
		
		
		cell1.innerHTML = data_received[i][0];
		cell2.innerHTML = data_received[i][1];
		cell3.innerHTML = data_received[i][2];
		cell4.innerHTML = data_received[i][3];
		cell5.innerHTML = data_received[i][4];
		
		
		//cell.innerHTML = data_received[i][j].toString()
		//data_string = data_string + '<p>' + data_received[i].toString() + '</p>';
        }
        data_received.pop(msg.data);
        //$('#log').html(data_string);
    });
 });
});
