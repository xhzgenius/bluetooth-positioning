from socketserver import BaseRequestHandler, ThreadingTCPServer

class MyHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        
        while True:
            msg = self.request.recv(8192)
            if not msg:
                break
            #####################################
            # Do something with the message
            # TODO: unpack the message
            # TODO: Send data to mysql
            print("Received raw data:", msg)
            #####################################

# our_server_ip = "82.157.173.163" # Our server's ip. # It's not this!!! 
our_server_ip = "127.0.0.1" # This is right. 
our_server_port = 12345

if __name__ == '__main__':
    serv = ThreadingTCPServer((our_server_ip, our_server_port), MyHandler)
    print("TCP server started at %s:%d"%(our_server_ip, our_server_port))
    serv.serve_forever()