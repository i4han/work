var http = require('http');
http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end('<!DOCTYPE html>'
+ '<html>'
+ '<head>'
+ '<meta charset="utf-8">'
+ '<title>Hello</title>'
+ '<script src="./sag.js"></script>'
+ '</head><body>hello</body>\n');}).listen(1337, '127.0.0.1');