var express = require('express');
var app = express();

var server_port = process.env.YOUR_PORT || process.env.PORT || 80;
var server_host = process.env.YOUR_HOST || '0.0.0.0';

app.use('/', express.static(__dirname));
server.listen(server_port, server_host, function() {
    console.log('Listening on port %d', server_port);
});