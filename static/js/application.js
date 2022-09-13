
$(document).ready(function(){
 $("#start").click(function(){

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
		//insert table with 6 cells
		row = table.insertRow(1);

		
		for(var j = 0; j < data_received[i].length-1; j++)
		{
			console.log(data_received[i][5]);
			if(String(data_received[i][5]) == "low")
			{
				cell = row.insertCell(j);
				cell.innerHTML = String(data_received[i][j]).fontcolor("blue");
			}
			else if(String(data_received[i][5]) == "medium")
			{
				cell = row.insertCell(j);
				cell.innerHTML = String(data_received[i][j]).fontcolor("orange");
			}
			else if(String(data_received[i][5]) == "high")
			{
				cell = row.insertCell(j);
				cell.innerHTML = String(data_received[i][j]).fontcolor("red");
			}
			else
			{
				cell = row.insertCell(j);
				cell.innerHTML = String(data_received[i][j]);
			}
		
		}
		
		
		data_received.pop(msg.data);
	}
	
    });
    });
});
