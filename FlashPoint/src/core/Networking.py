import socket

from src.external.Mastermind import *


class Networking(object):
    host = None
    client = None
    TIMEOUT_CONNECT = 200
    TIMEOUT_RECEIVE = 200

    def create_host(self, port=20298):
        # We use UDP to broadcast the host
        self.host = MastermindServerUDP()

        server_ip = None
        # find unused ip address
        for i in range(255, 0, -1):
            for j in range(255, 0, -1):
                try:
                    # try to connect to the specified ip address
                    socket.gethostbyaddr("192.168."+str(i)+"."+str(j))
                except socket.error:
                    # if we cannot connect to the address, that means the ip address is unused
                    server_ip = "192.168."+str(i)+"."+str(j)
                    break
            if server_ip is not None:
                break

        try:
            self.host.connect(server_ip, port)
            # Start accepting connection
            self.host.accepting_allow_wait_forever()
            # The host also acts as a client
            self.client = MastermindClientUDP()
            self.client.connect(server_ip, port)
        except MastermindError:
            print("Server error!")

    def join_host(self, ip, port=20298):
        global TIMEOUT_CONNECT, TIMEOUT_RECEIVE
        self.client = MastermindClientUDP(TIMEOUT_CONNECT, TIMEOUT_RECEIVE)
        try:
            print("Attempting to connect to host at "+ip+":"+port)
            self.client.connect(ip, port)
        except MastermindError:
            print("Error connecting to server at: "+ip+":"+port)

    @property
    def is_host(self):
        return self.host is not None

    def send(self, data, compress=0):
        self.client.send(data, compress)
