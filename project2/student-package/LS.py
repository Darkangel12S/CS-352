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

# step3: accept client connection in loop.
# step3: Receive queries from client in loop, open socket connections to ts1 and ts2, send decoded query to ts1 and ts2
    while True:
        website = sock.recv(200).decode('utf-8').strip('\n')
        ts1 = build_ts_cnn(ts1_port, ts1_addr) # build connection with TS servers
        ts2 = build_ts_cnn(ts2_port, ts2_addr)

        ts1.send(website.encode('utf-8'))
        ts2.send(website.encode('utf-8'))

        # send website to ts1 and 2

        # Step4: Let select() monitor ts1 and ts2 for response
        # On getting response send it back to client.
        # if no response then select() times out, send client error message.
        inputs = [ts1, ts2]
        outputs = []
        message_queues = {}

        # Inputs list:The first is a list of the objects to be checked for incoming data to be read (ts1, ts2 sockets in
        # project)(receive)
        # Outputs list: the second contains objects that will receive outgoing data when there is room in their buffer(send)
        # Error list: the third those that may have an error (usually a combination of the input and output channel objects).
        
        while inputs: 
            readable, writable, errors = select.select(inputs, outputs, [], 5)

        # accept the messages from the client from client
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(500)
                if data != '':
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]
    for s in writable:
        try:
            message_queue = message_queues.get(s)
            send_data = ''
            if message_queue is not None:
                send_data = message_queue.get_nowait()
        except queue.Queue.Empty:
            outputs.remove(s)
        else:
            if message_queue is not None:
                s.send(send_data)
    for s in errors:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        del message_queues[s]

# function to build a connection with the TS
def build_ts_cnn(port, address):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    # connect to TS
    sock.connect(address, port)

    return sock

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