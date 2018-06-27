def synchronizedCommunication():
    myDH, myRSA, hisRSA = initializeCryptography()

    loadPrivateData(myRSA)

    loadPublicData(hisRSA)

    sock = initializeSocket()


    package = Cryptography.packMessage(str(myDH.publicKey).encode(), myRSA.d, myRSA.N)
    # print ("sent " + json.dumps(package, indent=1))
    answer = input("Do you want to send package \n %s \n 'n' to abort protocol\n" % (package))
    if (answer == 'n'):
        closeConnection(sock)
        return
    sock.send(package.encode())
    value = json.loads(sock.recv(2048))
    print("received" + json.dumps(value, indent=1))
    sign = value.get('signature')
    message = str(value.get('message'))
    verifactionOfConnection = Cryptography.verifySignature(sign, message, hisRSA.e, hisRSA.N)

    if (verifactionOfConnection):
        myDH.generatePrivateKey(int(message))
        myAES = Cryptography.AESCipher(str(myDH.privateKey))

        while True:
            msg_for_server = input("message for server =>")
            msg_for_server = myAES.encrypt(msg_for_server)
            package_for_server = Cryptography.packMessage(msg_for_server, myRSA.d, myRSA.N)
            print("sent " + json.dumps(package_for_server, indent=1))
            if not msg_for_server:
                print ("no message for server")
                break
            sock.send(package_for_server.encode())
            package_from_server = json.loads(sock.recv(2048))
            print("received" + json.dumps(package_from_server, indent=1))
            if not package_from_server:
                print ("no reply from server")
                break
            else:
                sign = package_from_server.get('signature')
                msg_from_server = package_from_server.get('message')
                verificationOfMessage = Cryptography.verifySignature(sign, str(msg_from_server), hisRSA.e, hisRSA.N)
                if (verificationOfMessage):
                    msg_from_server = myAES.decrypt(msg_from_server.encode())
                    print("message from server => ", msg_from_server)
                else:
                    print("message verification failed")
                    break
    else:
        print("server key verification  failed")

    closeConnection(sock)

def initializeCryptography():
    myDH = Cryptography.DH()
    myRSA = Cryptography.RSA()
    hisRSA = Cryptography.RSA()
    return myDH, myRSA, hisRSA

def loadPrivateData(myRSA):
    clientPrivateData = sys.argv[1]
    temp = []
    with open(clientPrivateData, "r") as file:
        for line in file:
            temp.append(line)
    ## (p, q, N, e, d)
    myRSA.setRSA(int(temp[0]), int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4]))

def loadPublicData(hisRSA):
    serverPublicData = sys.argv[2]
    temp = []
    with open(serverPublicData, "r") as file:
        for line in file:
            temp.append(line)
    # (N, e)
    hisRSA.setPublicKey(int(temp[0]), int(temp[1]))

def initializeSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    port_number = 1300
    print ("The name of local machine", host_name)
    host_port_pair = (host_name, port_number)
    sock.connect(host_port_pair)
    return sock

def closeConnection(socket):
    socket.close()

if __name__ == "__main__":
    import socket
    import json
    import Cryptography
    import sys
    if (len(sys.argv) == 3):
        synchronizedCommunication()
    else:
        print ("Please, provide two parameters!")