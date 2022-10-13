# read domain names from PROJ2-HNS.txt
# Write outputs it receives into RESOLVED.txt 
import socket 

def client():
# Step1: Open socket connection on client side
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
# Step2: Connect to server on given port and IP address of server
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    sock.connect(server_binding)

# Step3: Open the file pointers to read from and write into
    inFile = open("PROJ2-DNSTS1.txt", 'r')
    inLines = inFile.readlines()
    outFile = open("RESOLVED.txt", 'w')
    # clear the file contents
    outFile.truncate(0)

# Step4: Send each query to server and get the response, write the response into file
    for line in inLines:
        website = line.strip('\n')
        sock.sendall(website.encode('utf-8'))
        ok = sock.recv(100)
        if ok != 'ok':
           break  

# Step5: close the files descriptors and socket connections and exit
    sock.close()
    inFile.close()
    outFile.close()
    exit()