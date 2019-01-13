import socket
import threading
import time

from src.external.Mastermind import *


class Networking:
    """
    Class that stores networking info like host and client. This class follows a Singleton design pattern.
    """
    __instance = None

    @staticmethod
    def get_instance():
        if Networking.__instance is None:
            Networking()
        return Networking.__instance

    def __init__(self):
        if Networking.__instance is None:
            Networking.__instance = Networking.NetworkingInner()
        else:
            raise Exception("Networking is a Singleton")

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    class NetworkingInner:
        host = None
        client = None
        TIMEOUT_CONNECT = 200
        TIMEOUT_RECEIVE = 200

        def create_host(self, port=20298):
            # We use UDP to broadcast the host
            self.host = MastermindServerUDP()

            """
            # find unused ip address
            for i in range(255, 0, -1):
                for j in range(255, 0, -1):
                    try:
                        print("Checking for free address at 192.168."+str(i)+"."+str(j))
                        # try to connect to the specified ip address
                        socket.gethostbyaddr("192.168."+str(i)+"."+str(j))
                    except socket.error:
                        print("Address is unused")
                        # if we cannot connect to the address, that means the ip address is unused
                        server_ip = "192.168."+str(i)+"."+str(j)
                        break
                if server_ip is not None:
                    break
            """

            #port = self.get_open_port()
            # listen to all address
            server_ip = "0.0.0.0"
            client_ip = "localhost"

            try:
                print("Listening at "+server_ip+":"+str(port))
                self.host.connect(server_ip, port)

                print("Starts accepting connection")
                t = threading.Thread(target=self.host.accepting_allow)
                t.start()
                # The host also acts as a client
                self.join_host(client_ip)
            except MastermindErrorSocket:
                print("Failed to create a host")

        def join_host(self, ip, port=20298):
            self.client = MastermindClientUDP(self.TIMEOUT_CONNECT, self.TIMEOUT_RECEIVE)
            try:
                print("Attempting to connect to host at "+ip+":"+str(port))
                self.client.connect(ip, port)
            except MastermindError:
                print("Error connecting to server at: "+ip+":"+str(port))

        @property
        def is_host(self):
            return self.host is not None

        @staticmethod
        def get_open_port():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", 0))
            s.listen(1)
            port = s.getsockname()[1]
            s.close()
            return port

        def disconnect(self):
            if self.client is not None:
                self.client.disconnect()
            if self.host is not None:
                self.host.disconnect_clients()
                self.host.disconnect()

        def send(self, data, compress=0):
            self.client.send(data, compress)
