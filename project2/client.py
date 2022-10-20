import socket
import sys
import time 

def client(host, port):
# Step1: Open socket connection on client side
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
# Step2: Connect to server on given port and IP address of server
    # connect to the server on local machine
    server_binding = (host, port)
    sock.connect(server_binding)

# Step3: Open the file pointers to read from and write into
    inFile = open("PROJ2-HNS.txt", 'r')
    inLines = inFile.readlines()
    outFile = open("RESOLVED.txt", 'w')
    # clear the file contents
    outFile.truncate(0)

# Step4: Send each query to server and get the response, write the response into file
    for line in inLines:
        print(line.strip('\n'))
        website = line
        sock.send(website.encode('utf-8'))
        # recieve message and write to the output file
        message = sock.recv(500)
        if (not message):
            break
        outFile.write(message + '\n')

# Step5: close the files descriptors and socket connections and exit
    sock.close()
    inFile.close()
    outFile.close()
    exit()

if __name__ == "__main__":
    # pass arguments of name and port
    lsHostname = sys.argv[1]
    lsListenPort = sys.argv[2]

    # pass arguments to thread
    client(lsHostname, int(lsListenPort))