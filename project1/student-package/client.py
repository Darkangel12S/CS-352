import threading
import time
import random

import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # reads in the input file line by line and sends it to the server
    inFile = open("in-proj.txt", 'r')
    inLines = inFile.readlines()

    for line in inLines: 
        cs.sendall(line.encode('utf-8'))
        ok = cs.recv(100)
        print(line.strip('\n'))
        if ok != 'ok':
           break  

    # close the client socket
    cs.close()

    # close the file
    inFile.close()

    exit()

def func():
    with open("out-proj.txt", 'r+') as fp:
        lines = fp.readlines()
        # move file pointer to the beginning of a file
        fp.seek(0)
        # truncate the file
        fp.truncate()
        fp.writelines(lines[1:])

if __name__ == "__main__":
    # t1 = threading.Thread(name='server', target=server)
    # t1.start()

    # time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()
    
    # time.sleep(5)
    print("Done.")

    func()