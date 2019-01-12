from src.external.Mastermind import *


class Networking(object):
    host = None
    client = None
    TIMEOUT_CONNECT = 200
    TIMEOUT_RECEIVE = 200

    def create_host(self):
        # We use UDP to broadcast the host
        self.host = MastermindServerUDP()
        # Start accepting connection
        try:
            self.host.connect("192.168.255.255", 20298)
            self.host.accepting_allow_wait_forever()
        except MastermindError:
                print("Server error!")

    def join_host(self, ip, port):
        self.client = MastermindClientUDP()
        try:
            self.client.connect(ip, port)
        except MastermindError:
            print("Error connecting to server at: "+ip+":"+port)
