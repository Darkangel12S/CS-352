from http import server
import queue
import select
import socket
import sys
import threading

def Lserver(port, ts1_port, ts1_addr, ts2_port, ts2_addr):
# Step1: Open socket connection on rs side.
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(0)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

# Step2: Bind to the (ip,port) pair and listen for client connections.
    host = socket.gethostname()
    server_binding = (host, port)
    sock.bind(server_binding)
    sock.listen(5)

    # save ts1,2 addresses and port
    ts1Connect = (ts1_addr, ts1_port)
    ts2Connect = (ts2_addr, ts2_port)

    # connect to TS1
    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    ts1.setblocking(0)

    # connect to TS2
    try:
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS2 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    ts2.setblocking(0)

    # lists for select 
    inputs = [ts1, ts2]
    outputs = []
    message_queues = {}

# step3: accept client connection in loop.
# step3: Receive queries from client in loop, open socket connections to ts1 and ts2, send decoded query to ts1 and ts2
    while True:
        website = sock.recv(200).decode('utf-8').strip('\n')

        # send website to ts1 and 2
        ts1.sendto(website.encode('utf-8'), ts1Connect)
        ts2.sendto(website.encode('utf-8'), ts2Connect)

        # Step4: Let select() monitor ts1 and ts2 for response
        # On getting response send it back to client.
        # if no response then select() times out, send client error message.

        if not website:
            break

        # Inputs list:The first is a list of the objects to be checked for incoming data to be read (ts1, ts2 sockets in
        # project)(receive)
        # Outputs list: the second contains objects that will receive outgoing data when there is room in their buffer(send)
        # Error list: the third those that may have an error (usually a combination of the input and output channel objects).
        
        readable, writable, exceptional = select.select(inputs, outputs, [], 5)

        # accept the messages from the client from client
        if readable: 
            for s in readable:
                website = s.recv(500)
        else:
            website = 'TIMED OUT'.encode('utf-8')
        
        # send data to client
        sock.send(website)

if __name__ == "__main__":
    # pass arguments of name and port
    lsListenPort = sys.args[1]
    ts1Hostname = sys.args[2]
    ts1ListenPort = sys.args[3]
    ts2Hostname = sys.args[4]
    ts2ListenPort = sys.args[5]

    # pass arguments to thread
    t2 = threading.Thread(name='Lserver', target=Lserver, args=(lsListenPort, ts1Hostname, 
                                                                ts1ListenPort, ts2Hostname, ts2ListenPort, ))
    t2.start()

    # time.sleep(5)
    print("Done.")