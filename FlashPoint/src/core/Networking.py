import sys
import socket

from src.external.Mastermind import *


class Networking(object):
    host = None
    client = None
    TIMEOUT_CONNECT = 200
    TIMEOUT_RECEIVE = 200

    def create_host(self):
        # We use UDP to broadcast the host
        self.host = MastermindServerUDP()

        server_ip = None
        # find unused ip address
        for i in range(255, 0, -1):
            for j in range(255, 0, -1):
                try:
                    socket.gethostbyaddr("192.168."+str(i)+"."+str(j))
                except socket.error:
                    server_ip = "192.168."+str(i)+"."+str(j)
                    break
            if server_ip is not None:
                break

        try:
            self.host.connect(server_ip, 20298)
            # Start accepting connection
            self.host.accepting_allow_wait_forever()
        except MastermindError:
                print("Server error!")

    def join_host(self, ip, port):
        self.client = MastermindClientUDP()
        try:
            self.client.connect(ip, port)
        except MastermindError:
            print("Error connecting to server at: "+ip+":"+port)
