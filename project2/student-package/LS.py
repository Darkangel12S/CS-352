# Step1: Open socket connection on rs side.
# Step2: Bind to the (ip,port) pair and listen for client connections.
# step3: accept client connection in loop.
# step3: Receive queries from client in loop open socket connections to ts1 and ts2 send decoded query to ts1 and ts2
# Step4: Let select() monitor ts1 and ts2 for response
# On getting response send it back to client.
# if no response then select() times out, send client error message.
import socket

def server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
        
    host = socket.gethostname()
    port = 50007
    server_binding = (host, port)
    sock.bind(server_binding)
    sock.listen(5)