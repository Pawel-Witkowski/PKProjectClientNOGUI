import socket
import json
import DH


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_name = socket.gethostname()  # To get the name of host
port_number = 1234
print ("The name of local machine", host_name)  # The name of local machine admins-MacBook-Pro-3.local

host_port_pair = (host_name, port_number)  # A tuple

sock.connect(host_port_pair)  # To actively intiate the TCP Server connection

myDH = DH.DH()
sock.send(json.dumps(str(myDH.publicKey)).encode())
value = int(json.loads(sock.recv(2048)))
myDH.generatePrivateKey(value)



print ("dh private key", myDH.privateKey)

while True:
    msg_for_server = input("message for server =>")
    # print ("TYPE A MESSAGE FOR SERVER ==> ", msg_for_server = input())
    if not msg_for_server:
        break
    sock.send(json.dumps(msg_for_server).encode())

    msg_from_server = json.loads(sock.recv(2048))
    if not msg_from_server:
        print ("<...No Reply from Server...>")
    else:
        print ("From Server ==> ", msg_from_server)

sock.close()