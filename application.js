$(document).ready(function(){

var data_received = [];
var id = 0;

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
				
				
				for(var j = 0; j < data_received[i].length; j++) //changed this, no more -1 at the end
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
						
						/*var Packet = {
							source_ip : String(data_received[i][0]),
							source_port : String(data_received[i][1]),
							dest_ip : String(data_received[i][2]),
							dest_port : String(data_received[i][3]),
							prot : String(data_received[i][4]),
							severity : String(data_received[i][5]),
							msg : String(data_received[i][6])
						};*/
					}
							
				}
				
				//new code for button
				button = row.insertCell(7); //Last row after message

				button.innerHTML = '<button onclick="myFunction()" class="btn btn-info btn-lg" id="view' + id + '">View</button>';
				
				//id increment for unique button id
				id++;
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
