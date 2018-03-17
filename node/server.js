var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var kafka = require('kafka-node');
var HighLevelConsumer = kafka.HighLevelConsumer;
var Offset = kafka.Offset;
var Client = kafka.Client;
var topic = 'twitter-trends';
var client = new Client('localhost:2181', 'worker-' + Math.floor(Math.random() * 10000));
var payloads = [{ topic: topic }];
var consumer = new HighLevelConsumer(client, payloads);
var offset = new Offset(client);
var port = 3001;

app.get('/', function(req, res) {
  res.sendFile(__dirname + '/index.html');
});

io = io.on('connection', function(socket) {
  console.log('user connected');
  socket.on('disconnect', function() {
    console.log('user disconnected');
  });
});

consumer = consumer.on('message', function({ value }) {
  io.emit('message', JSON.parse(value));
});

http.listen(port, function() {
  console.log('Running on port ' + port);
});
