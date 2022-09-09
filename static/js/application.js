
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var data_received = [];

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received Data" + msg.data);
        
        
        data_received.push(msg.data);
        data_string = '';
        for (var i = 0; i < data_received.length; i++){
            data_string = data_string + '<p>' + data_received[i].toString() + '</p>';       
            
        }
        $('#log').html(data_string);
    });

});
