import msgpack_numpy
import msgpack
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        raw_data = self.rfile.read(int(self.headers['content-length'])) # Read http content
        # data = msgpack.unpackb(raw_data, object_hook = msgpack_numpy.decode) # Decode the http content
        data = raw_data # TODO: decode the data, it is a mountain of shit. 
        print("[%s] Received http request from %s, content: %s"%(
            datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"), self.client_address, data.decode()
        ))
 
        self.send_response(200)
        self.send_header("Content-type","text/html") # Set response header
        self.send_header("response", "Received your POST request. ")
        self.end_headers()
        print("[%s] Responded to %s"%(
            datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"), self.client_address
        ))
        pass

our_server_ip = "0.0.0.0" # This is right. 
our_server_port = 12345

if __name__ == '__main__':
    with HTTPServer((our_server_ip, our_server_port), MyHandler) as server:
        print("TCP server started at %s:%d"%(our_server_ip, our_server_port))
        server.serve_forever()