# import socket

# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# # s = 通信类型(type) + 协议家族(protocol)

# # AF_INET = IPV4 ; AF_INET6 = IPV6

# # SOCK_STREAM = TCP ; SOCK_DGRAM UDP

# s.connect(("82.157.173.163", 12345))
# print("Connected. ")
# message = "Testing message"
# s.sendall(message.encode())
# print("Sent: %s"%message)
# response = s.recv(8192)
# print("Received:", response.decode())
# s.close()
# print("Closed. ")

import requests

response = requests.post("http://82.157.173.163:12345", data={"foo": "bar"})
print("Response:", response)
print("Finished!")