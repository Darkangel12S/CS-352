# Step1: Open socket connection on ts1 side
# Step2: Bind to the (ip,port) pair and listen for rs connections.
# Step3: In a loop, accept connection from rs.
# Receive query from rs and decode it.
# open the "PROJ2-DNSTS2.txt" file (can read this file and load into a dictionary).
# check if query is present, if present send response.
# else do nothing.close socket connection with rs.
# Step4: close the socket connection and exit.

# Step3: In a loop, accept connection from rs.
# Receive query from rs and decode it.
# open the "PROJ2-DNSTS1.txt" file (can read this file and load into a dictionary).
# check if query is present, if present send response.
# else do nothing.close socket connection with rs.
# Step4: close the socket connection and exit.

import select
import socket
import sys
import threading

def TS2(ts2_port):
# Step1: Open socket connection on ts1 side
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS2 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    # Step2: Bind to the (ip,port) pair and listen for client connections.
    host = socket.gethostname()
    port = ts2_port
    server_binding = (host, port)
    sock.bind(server_binding)
    sock.listen(5)

    # read the DNSTS1.txt and put it into a map
    DNS2 = {}

    with open('PROJ2-DNSTS2.txt', 'r') as file:
        websites = file.readLines()
        for line in websites:
            URL, IP, resource = line.split(' ')
            URL = str(URL)
            IP = str(IP)
            resource = str(resource)
            if (DNS2.get(URL) is None):
                DNS2[URL] = IP
    
    while True:
        data = sock.recv(500)
        website = data.decode('utf-8')

        if DNS2.has_key(website):
            newData = website + ' ' + DNS2[website] + ' A IN'
            sock.send(newData)
            break

    sock.close() 

if __name__ == "__main__":
    # pass arguments of name and port
    ts2_port = sys.args[1]

    # pass arguments to thread
    ts2 = threading.Thread(name='TS2', target=TS2, args=(ts2_port, ))
    ts2.start()

    # time.sleep(5)
    print("Done.")



