from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

import msgpack
import msgpack_numpy


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the http POST content. 
        raw_data = self.rfile.read(int(self.headers['content-length'])) # Read http content
        
        data = msgpack.unpackb(raw_data, object_hook = msgpack_numpy.decode) # Data from black box, in json form. 
        devices = data["devices"] # This is the frame which is defined in the documentation of black box. 
        # TODO: Decode the devices data frame (binary). 
        
        print("[%s] Received http request from %s, content: %s"%(
            datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"), self.client_address, data
        ))
        
        # Send data to mysql. 
        # TODO: Send data to mysql. 
        
        # Respond to the client. (Optional)
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