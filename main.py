# Import socket module
import socket               
import json
# Create a socket object
s = socket.socket()         

# Define the port on which you want to connect
port = 12345                

# connect to the server on local computer
s.connect(('127.0.0.1', port))



sizeA = json.loads(s.recv(12))
print(sizeA)
# receive data from the server
dictA = json.loads(s.recv(int(sizeA)))
print(dictA)

sizeB = json.loads(s.recv(12))
# receive data from the server
dictB = json.loads(s.recv(int(sizeB)))
print(dictB)


s.sendall(json.dumps("kurwa!").encode())
s.close()  