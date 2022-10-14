
# Step4: Let select() monitor ts1 and ts2 for response
# On getting response send it back to client.
# if no response then select() times out, send client error message.
import socket

def server():

# Step1: Open socket connection on rs side.
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

# Step2: Bind to the (ip,port) pair and listen for client connections.
    host = socket.gethostname()
    port = 50007
    server_binding = (host, port)
    sock.bind(server_binding)
    sock.listen(5)

# step3: accept client connection in loop.
    while True:
        website = sock.recv(200).decode('utf-8').strip('\n')
        sock.send('ok')
# step3: Receive queries from client in loop, open socket connections to ts1 and ts2, send decoded query to ts1 and ts2
        ts1 = build_ts_cnn(ts1_port, ts1_addr) # build connection with TS servers
        ts2 = build_ts_cnn(ts2_port, ts2_addr) # what to use for ts_port, ts_addr?

        # send website to ts1 and 2

    while True:
        ts1.recv() # will return only when receive something or time out
        ts2.recv() # ts2 will be blocked if ts1 did not feedback
        break

    while True:
        csockid_1, addr_1 = sock.accept()
        csockid_2, addr_2 = sock.accept()
        msg = "hello"*10000000 # huge string: hellohellohellohello...
        # will return only when the sending is finished
        csockid_1.send(msg.encode("utf-8"))
        # will be executed only after csockid_1 returns, might take very long time
        csockid_2.send(msg.encode("utf-8"))

def build_ts_cnn(port, address):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    ts_binding = (address, port)
    sock.bind(ts_binding)
    sock.listen(5)