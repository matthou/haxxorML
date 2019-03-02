import socket
import sys
import time
import errno
from multiprocessing import Process

compname = socket.gethostname()
server_addresses = []
pots = []
class address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_address(server_addr):
    server_addresses.append(address(server_addr[0], server_addr[1]))

def logging(address):
    connection, client_address = address.socket.accept()
    #print('client connected: ', client_address, file = sys.stderr)
    print ('Received on ip; ' + address.ip + 'Received on port: ' + address.port)
    f = open("person.txt", "a")
    f.write(str("\n"))
    f.write(str(connection))
    f.write(str(client_address))
    f.write(str(compname))
    f.close()

def one_honeypot(address):
    print('Starting on local addresses!')
    
    try:
        address.socket.bind((address.ip, address.port))
    except socket.error:
        print("Socket error, sudo run or change ports.")
    else:
        while True:
            
            print('starting up on', (address.ip, address.port), file = sys.stderr)
            address.socket.getsockname()
            address.socket.listen(1)
            print('waiting for a connection from sneaky mofackles.', file = sys.stderr)
            connection, client_address = address.socket.accept()
            try:
               while True:
                   try:
                       connection.send(bytes('Jokes on you.', 'UTF-8'))
                       data = connection.recv(16)
                       print('recieved ', data, file = sys.stderr)
                       print(' Received on ip: ' + str(address.ip) + ' Received on port: ' + str(address.port))
                       connection.sendall(data)
                   except socket.error as e:
                       if e.args[0] in (errno.EPIPE, errno.ECONNRESET):
                           pass

                   else:
                       logging(address)
                       break
            finally:
                print('restarting')
                
if __name__ == '__main__':
    add_address(('', 22))
    add_address(('', 23))
    add_address(('', 80))
    for elt in server_addresses:
        honey = Process(target = one_honeypot, args = (elt,))
        honey.start()
        pots.append(honey)
    for h in pots:
        h.join()
