from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

import msgpack
import msgpack_numpy

from database import DataBase

our_server_ip = "0.0.0.0" # This is right. 
our_server_port = 12345

class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, name, *args):
        print ('sever running...')
        self.db = DataBase(name) 
        BaseHTTPRequestHandler.__init__(self, *args)
        
    def do_POST(self):
        # Read the http POST content. 
        raw_data = self.rfile.read(int(self.headers['content-length'])) # Read http content
        
        data = msgpack.unpackb(raw_data, object_hook = msgpack_numpy.decode) # Data from black box, in json form. 
        devices = data["devices"] # This is the frame which is defined in the documentation of black box. 
        
        print("[%s] Received http request from %s, content: %s"%(
            datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"), self.client_address, data
        ))
        
        # TODO: Decode the devices data frame (binary). 
        mac1 = data['mac']
        for device in devices:
            mac = (device[1:7]).hex().upper()
            # Send data to mysql. 
            # TODO: Send data to mysql.
            rssi = int.from_bytes(device[7:8], byteorder='little') - 256
            self.db.insert_signal(mac, rssi)
            print ('mac', mac, 'mac1', mac1, 'rssi', rssi)        
        
        # Respond to the client. (Optional)
        self.send_response(200)
        self.send_header("Content-type","text/html") # Set response header
        self.send_header("response", "Received your POST request. ")
        self.end_headers()
        print("[%s] Responded to %s"%(
            datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"), self.client_address
        ))
        pass
        
def serve(name):
    def handler(*args):
        MyHandler(name, *args)
    with HTTPServer((our_server_ip, our_server_port), handler) as server:
        print("TCP server started at %s:%d"%(our_server_ip, our_server_port))
        server.serve_forever()

if __name__ == '__main__':
    from database import DataBase 
    serve(DataBase('test'))