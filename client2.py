import socket
import json
import Cryptography

secondPublic = 913976530180265085042697477389115151869748071814837123379332008739392866713102250041200017676149556821235075470316986869464472195625810059634970920260874471356039519174314701524259881656553402746070368557994562881416288454072541823
myRSA = Cryptography.RSA()
myDH = Cryptography.DH()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_name = socket.gethostname()
port_number = 1300
print ("The name of local machine", host_name)

host_port_pair = (host_name, port_number)

sock.connect(host_port_pair)

package = Cryptography.packMessage(str(myDH.publicKey).encode(), myRSA.d, myRSA.N)
sock.send(package.encode())
value = json.loads(sock.recv(2048))
sign = value.get('signature')
message = str(value.get('message'))
verifactionOfConnection = Cryptography.verifySignature(sign, message, secondPublic, myRSA.N)

if (verifactionOfConnection):
    myDH.generatePrivateKey(int(message))
    myAES = Cryptography.AESCipher(str(myDH.privateKey))

    while True:
        msg_for_server = input("message for server =>")
        msg_for_server = myAES.encrypt(msg_for_server)
        package_for_server = Cryptography.packMessage(msg_for_server, myRSA.d, myRSA.N)
        if not msg_for_server:
            print ("no message for server")
            break
        sock.send(package_for_server.encode())
        package_from_server = json.loads(sock.recv(2048))
        if not package_from_server:
            print ("no reply from server")
            break
        else:
            sign = package_from_server.get('signature')
            msg_from_server = package_from_server.get('message')
            verificationOfMessage = Cryptography.verifySignature(sign, str(msg_from_server), secondPublic, myRSA.N)
            if (verificationOfMessage):
                msg_from_server = myAES.decrypt(msg_from_server.encode())
                print("message from server => ", msg_from_server)
            else:
                print("message verification failed")
                break
else:
    print("server key verification  failed")

sock.close()