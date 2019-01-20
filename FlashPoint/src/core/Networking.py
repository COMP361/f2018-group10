import ipaddress
import socket
import threading
import logging

from src.external.Mastermind import *

logger = logging.getLogger("networking")
logger.setLevel(logging.INFO)


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
            logger.exception("Attempted to instantiate another singleton")
            raise Exception("Networking is a Singleton")

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    class NetworkingInner:
        host = None
        client = None
        TIMEOUT_CONNECT = 200
        TIMEOUT_RECEIVE = 200

        stop_broadcast = threading.Event()
        stop_listen = threading.Event()

        def __init__(self):
            self.stop_broadcast.set()

        def create_host(self, port=20298):
            # We use UDP to broadcast the host
            self.host = Networking.Host()

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
                logger.info(f"Listening to all IPs: {server_ip}:{port}")
                self.host.connect(server_ip, port)

                logger.info("Starts accepting connection")
                self.host.accepting_allow()

                # Clear the broadcast blocker
                self.stop_broadcast.clear()
                broadcaster = threading.Thread(target=self.broadcast_game, args=(None, self.stop_broadcast))
                broadcaster.start()

                # The host also acts as a client
                self.join_host(client_ip)
            except MastermindErrorSocket:
                logger.error("Failed to create a host")

        def join_host(self, ip, port=20298):
            self.client = Networking.Client(self.TIMEOUT_CONNECT, self.TIMEOUT_RECEIVE)
            try:
                print(f"Attempting to connect to host at {ip}:{port}")
                logger.info(f"Attempting to connect to host at {ip}:{port}")
                self.client.connect(ip, port)
                self.client.send("I've connected")
            except MastermindErrorClient:
                logger.error(f"Error connecting to server at: {ip}:{port}")
                raise ConnectionError
            except OSError:
                raise OSError

        @staticmethod
        def broadcast_game(args, stop_event):
            b_caster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            b_caster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            b_caster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            msg = f"{socket.gethostname()} {mastermind_get_local_ip()}"
            bip = Networking.get_instance().get_broadcast_ip()
            print(f"Broadcasting at {bip}:54545")

            while not stop_event.is_set():
                b_caster.sendto(str.encode(msg), (str(bip), 54545))

        @staticmethod
        def search_game(stop_event):
            listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            listener.bind('')
            while not stop_event.is_set():
                msg = listener.recvfrom(2048)
                return msg

        @property
        def is_host(self):
            return self.host is not None

        @staticmethod
        def get_ip():
            return mastermind_get_local_ip()

        @staticmethod
        def get_broadcast_ip():
            return ipaddress.IPv4Network(mastermind_get_local_ip()).broadcast_address

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
                logger.info("Disconnecting client")
                self.client.disconnect()
                self.client.__del__()
                self.client = None
            if self.host is not None:
                logger.info("Disconnecting host")
                # Kill the broadcast
                self.stop_broadcast.set()

                self.host.accepting_disallow()
                self.host.disconnect_clients()
                self.host.disconnect()
                self.host.__del__()
                self.host = None

        # If game is started, stops new client from connecting
        def start_game(self):
            # Kill the broadcast
            self.stop_broadcast.set()

            if self.host is not None:
                self.host.accepting_disallow()

        def send(self, data, compress=0):
            self.client.send(data, compress)

    """Overridden classes"""
    class Host(MastermindServerUDP):
        def callback_connect_client(self, connection_object):
            print(f"Client at {connection_object.address} is connected")
            return super(MastermindServerUDP, self).callback_connect_client(connection_object)

        def callback_client_handle(self, connection_object, data):
            print(f"Client at {connection_object.address} sent a message: {data}")
            return super(MastermindServerUDP, self).callback_client_handle(connection_object, data)

    class Client(MastermindClientUDP):
        """Override callbacks here"""
