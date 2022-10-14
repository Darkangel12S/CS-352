# Step3: In a loop, accept connection from rs.
# Receive query from rs and decode it.
# open the "PROJ2-DNSTS1.txt" file (can read this file and load into a dictionary).
# check if query is present, if present send response.
# else do nothing.close socket connection with rs.
# Step4: close the socket connection and exit.

import socket

def TS1():
# Step1: Open socket connection on ts1 side
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    # Step2: Bind to the (ip,port) pair and listen for client connections.
    host = 0# host name
    port = 0# port number
    server_binding = (host, port)
    sock.bind(server_binding)
    sock.listen(5)