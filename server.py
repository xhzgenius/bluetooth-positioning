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
            
            #####################################

our_server_ip = "114.51.4.19" # Change it. TODO: @szm
our_server_port = 12345

if __name__ == '__main__':
    serv = ThreadingTCPServer((our_server_ip, our_server_port), MyHandler)
    serv.serve_forever()