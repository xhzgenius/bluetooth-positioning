from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from key import *

import msgpack
import msgpack_numpy

from database import global_db


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)
        
    def do_POST(self):
        # Read the http POST content. 
        raw_data = self.rfile.read(int(self.headers['content-length'])) # Read http content
        
        try:
            data = msgpack.unpackb(raw_data, object_hook = msgpack_numpy.decode) # Data from black box, in json form. 
        except:
            print("[%s] Received invalid data from %s. "%
                  (datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"), self.client_address
            ))
            return
        devices = data["devices"] # This is the frame which is defined in the documentation of black box. 
        
        print("[%s] Received http request from %s, content length: %d"%(
            datetime.strftime(datetime.now(), "%Y-%m-%d %H-%M-%S"), self.client_address, len(data)
        ))
        
        # Decode the devices data frame (binary). 
        box_mac = data['mac']
        for device in devices:
            device_mac = (device[1:7]).hex().upper()
            # concentrate on target device
            if device_mac != target_mac:
                continue
            # Send data to mysql. 
            rssi = int.from_bytes(device[7:8], byteorder='little') - 256
            global_db.insert_signal(box_mac, rssi)
            # print ('mac:', mac, 'mac1:', mac1, 'rssi:', rssi)        
        
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
    with HTTPServer((our_server_ip, our_server_port), MyHandler) as server:
        print("TCP server started at %s:%d"%(our_server_ip, our_server_port))
        try:
            server.serve_forever()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    serve("test")