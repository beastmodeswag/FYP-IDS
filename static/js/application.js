$(document).ready(function(){

var data_received = [];

	$("#start").click(function(){
		var buttonId = this.id;
		document.getElementById("start").disabled = true;

		//connect to the socket server.
		var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

		//receive details from server
		socket.on('newnumber', function(msg) {
			
			var table = document.getElementById("dataTable");
			var row = '';
			
			console.log("Received Data" + msg.data);
		
			console.log(msg.data)
			data_received.push(msg.data);
			var data_string = '';

			for (var i = 0; i < data_received.length; i++)
			{
				//insert table with 6 cells
				row = table.insertRow(1);

				
				for(var j = 0; j < data_received[i].length-1; j++)
				{
					console.log(data_received[i][6]);
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
				
			}	
		    });
	}); 
	
	//export button clicked
	$("#export").click(function(){
		console.log("Export button pressed");
		
		var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
		
		socket.send("export");
		
	});
});
