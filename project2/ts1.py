import socket
import sys

def ts1(ts1_port):
    try:
        tss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', ts1_port)
    tss.bind(server_binding)
    tss.listen(5)
    csockid, addr = tss.accept()

    infile = open('PROJ2-DNSTS1.txt', 'r')
    lines = infile.readlines()
    dns1 = {}
    infile.close()

# open the "PROJ2-DNSTS1.txt" file (can read this file and load into a dictionary).
    for line in lines:
        domain, address, flag = line.split(' ')
        domain = str(domain).lower()
        address = str(address)
        flag = str(flag)
        if (dns1.get(domain) is None):
            dns1[domain] = address

    # print(dns1)

    while True:
        data, tuple = csockid.recvfrom(500)
        query = data.decode('utf-8').strip('\n')

        # print(website + ' ' + str(website.lower() in DNS1.keys()))

        if query.lower() in dns1.keys():
            # print('website found')
            newData = query + ' ' + dns1[query.lower()] + ' A IN'
            csockid.send(newData)
            
        if not data:
            break

    tss.close() 

if __name__ == "__main__":
    ts1_port = sys.argv[1]

    ts1(int(ts1_port))