import socket
import sys

def TS1(ts1_port):
# Step1: Open socket connection on ts1 side
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    # Step2: Bind to the (ip,port) pair and listen for client connections.
    server_binding = ('', ts1_port)
    sock.bind(server_binding)
    sock.listen(5)

# Step3: In a loop, accept connection from rs.
    lssock, addr = sock.accept()

    # read the DNSTS1.txt and put it into a map
    DNS1 = {}

# open the "PROJ2-DNSTS1.txt" file (can read this file and load into a dictionary).
    with open('PROJ2-DNSTS1.txt', 'r') as file:
        websites = file.readlines()
        for line in websites:
            URL, IP, resource = line.split(' ')
            URL = str(URL).lower()
            IP = str(IP)
            resource = str(resource)
            if (DNS1.get(URL) is None):
                DNS1[URL] = IP

    print(DNS1)

    while True:
        data, tuple = lssock.recvfrom(500)
# Receive query from rs and decode it.
        website = data.decode('utf-8').strip('\n')

        print(website + ' ' + str(website.lower() in DNS1.keys()))

# check if query is present, if present send response.
# else do nothing.close socket connection with rs.
        if website.lower() in DNS1.keys():
            print('website found')
            newData = website + ' ' + DNS1[website.lower()] + ' A IN'
            lssock.send(newData)
            
        if not data:
            break

# Step4: close the socket connection and exit.
    sock.close() 

if __name__ == "__main__":
    ts1_port = sys.argv[1]

    TS1(int(ts1_port))