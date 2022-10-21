import socket
import sys

def ts2(ts2_port):
    try:
        tss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: TS2 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', ts2_port)
    tss.bind(server_binding)
    tss.listen(5)
    csockid, addr = tss.accept()

    infile = open("PROJ2-DNSTS2.txt", "r")
    lines = infile.readlines()
    dns2 = {}
    infile.close()

    for line in lines:
        domain, address, flag = line.split(' ')
        domain = str(domain).lower()
        address = str(address)
        flag = str(flag)
        if (dns2.get(domain) is None):
            dns2[domain] = address

    # print(dns2)
    
    while True:
        data, tuple = csockid.recvfrom(500)
        query = data.decode('utf-8').strip('\n')

        # print(query + ' ' + str(query.lower() in dns2.keys()))

        if query.lower() in dns2.keys():
            # print('website found')
            resp = query + ' ' + dns2[query.lower()] + ' A IN'
            csockid.send(resp)
            
        if not data:
            break

    tss.close() 

if __name__ == "__main__":
    ts2_port = sys.argv[1]
    
    ts2(int(ts2_port))