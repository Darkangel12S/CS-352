import threading
import time
import random

import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    port = 50007
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    # Creates the output file
    outFile = open("out-proj.txt","a")
    outFile.truncate(0)

    inFile = open("in-proj.txt", 'r')
    inLines = inFile.readlines()
    numLines = len(inLines)

    # Continuously receives data from the client
    iteration = 0
    while True:
        data = csockid.recv(200).decode('utf-8').strip('\n')
        csockid.send('ok')
        reversed = data[::-1]
        print(reversed)
        iteration += 1
        if (iteration == numLines):
            outFile.writelines('\n')
        outFile.writelines(reversed)
        if not data:
            break

    # Close the file
    outFile.close()

    # Close the server socket
    ss.close()

    exit() 

if __name__ == "__main__":
    t1 = threading.Thread(name='server', target=server)
    t1.start()

    # time.sleep(5)
    print("Done.")


    