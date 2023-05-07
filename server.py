from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from key import *
from algorithm import global_analyzer, global_visualizer
from database import global_db

import msgpack
import msgpack_numpy


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
                  (datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"), self.client_address
            ))
            return
        devices = data["devices"] # This is the frame which is defined in the documentation of black box. 
        
        print("[%s] Received http request from %s, content length: %d"%(
            datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"), self.client_address, len(data)
        ))
        
        # Decode the devices data frame (binary). 
        box_mac = data['mac']
        rssi_lst = []
        for device in devices:
            device_mac = (device[1:7]).hex().upper()
            # concentrate on target device
            if device_mac != target_mac:
                continue
            rssi = int.from_bytes(device[7:8], byteorder='little') - 256
            rssi_lst.append(rssi)
        rssi_len = len(rssi_lst)
        if rssi_len == 0:
            return
        avg_rssi = int(sum(rssi_lst)/rssi_len)

        # Send data to mysql. 
        global_db.insert_signal(box_mac, avg_rssi)
        print ('target_mac:', target_mac, 'box_mac:', box_mac, 'avg_rssi:', avg_rssi)        
        
        # Calculate position. 
        global_analyzer.single_run()

        # Visualize. 
        global_visualizer.single_run()
        # You'd better run successfully. 

        pass
        
def serve():
    with ThreadingHTTPServer((our_server_ip, our_server_port), MyHandler) as server:
        print("TCP server started at %s:%d"%(our_server_ip, our_server_port))
        try:
            server.serve_forever()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    serve("test")