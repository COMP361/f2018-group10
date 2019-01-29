import pygame
import ipaddress
import socket
import threading
import logging
from enum import Enum

from src.core.EventQueue import EventQueue
from src.constants.enums.EventsEnum import EventsEnum
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

        server_reply = None

        def __init__(self):
            self.stop_broadcast.set()

        def create_host(self, port=20298):
            """
            Attempts to create a game host on localhost and a game client that connects to it.
            A host machine is both a server (host) and a client so that the send message workflow can be simplified.
            i.e. The send message can be hooked to a command without checking if the current machine is a host or not.
            :param port: Port to be opened on the local machine. Defaults to 20298.
            :return:
            """
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
            """
            Attempt to join host at the specified ip address
            :param ip: IP address
            :param port: Port to connect, defaults to 20298
            :return:
            """
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
            # TODO DON'T USE THIS YET
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
            # TODO DON'T USE THIS YET
            listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            listener.bind('')
            while not stop_event.is_set():
                msg = listener.recvfrom(2048)
                return msg

        @property
        def is_host(self):
            """
            Returns True if the local machine is a host
            :return:
            """
            return self.host is not None

        @staticmethod
        def get_ip():
            return mastermind_get_local_ip()

        @staticmethod
        def get_broadcast_ip():
            return ipaddress.IPv4Network(mastermind_get_local_ip()).broadcast_address

        @staticmethod
        def get_open_port():
            """
            Returns a port number that is unused
            :return:
            """
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", 0))
            s.listen(1)
            port = s.getsockname()[1]
            s.close()
            return port

        def disconnect(self):
            """
            Disconnects the current machine. If the current machine is a host, it ends the game as well.
            :return:
            """
            if self.client is not None:
                logger.info("Disconnecting client")
                self.client.disconnect()
                self.client.__del__()
                self.client = None
            if self.host is not None:
                logger.info("Disconnecting host")
                # Kill the broadcast
                self.stop_broadcast.set()

                # Stops accepting connection
                self.host.accepting_disallow()
                # Disconnects all clients
                self.host.disconnect_clients()
                self.host.disconnect()
                self.host.__del__()
                self.host = None

        # If game is started, stops new client from connecting
        def start_game(self):
            """
            Starts the game
            :return:
            """
            # Kill the broadcast
            self.stop_broadcast.set()

            if self.host is not None:
                self.host.accepting_disallow()

        def chat(self, message: str):
            data = Networking.DataPayload.make_chat_data(message)
            self.client.send(data, True)

        def send_to_server(self, data, compress=True):
            """
            Send data to server
            :param data: data to be sent
            :param compress: compression, enabled by default
            :return:
            """
            if self.client is not None:
                try:
                    self.client.send(data, compress)
                except MastermindErrorSocket:
                    raise MastermindErrorSocket("Connectivity problem")
            else:
                raise MastermindErrorClient("Client is not available")

        def send_to_client(self, client_id: int, data, compress=True):
            """
            Send data to client
            :param client_id: client id
            :param data: data to be sent
            :param compress: compression, enabled by default
            :return:
            """
            if self.host is not None:
                try:
                    client_conn_obj = self.host.lookup_client(client_id)
                    self.host.callback_client_send(client_conn_obj, data, compress)
                except MastermindErrorSocket:
                    raise MastermindErrorSocket("Connectivity problem")
            else:
                raise MastermindErrorServer("Server is not available")

        def handle_command(self, command):
            """Handle the commands here"""
            if command.type == Networking.DataPayload.Command.CHAT:
                """Chat action"""

        def update(self, event_queue: EventQueue):
            for event in event_queue:
                # Handles the event if it's a command defined in DataPayload.Command
                if event.type in [command.value for command in Networking.DataPayload.Command]:
                    self.handle_command(event)

    # Overridden classes
    class Host(MastermindServerUDP):
        client_list = []

        def lookup_client(self, client_id):
            """
            Look up the client list (array) and return the connection object
            :param client_id: client id
            :return:
            """
            conn_obj = self.client_list[client_id]
            if conn_obj is not None:
                return conn_obj
            else:
                raise Networking.Host.ClientNotFoundException

        def callback_connect_client(self, connection_object):
            """
            Called when a new client connects. This method can be overridden to provide useful information. It's good
            practice to call "return super(MastermindServerTCP,self).callback_connect_client(connection_object)" at the
            end of your override.
            :param connection_object: Represents the appropriate connection
            :return:
            """
            # print(f"Client at {connection_object.address} is connected")
            # Assign a new connection object to the address (as a key value pair)
            self.client_list.append(connection_object)
            client_id = len(self.client_list)-1

            # inform the event queue that a client is connected, with the respective client id
            event = pygame.event.Event(EventsEnum.CLIENT_CONNECTED, {'client_id': client_id})
            pygame.event.post(event)

            return super(MastermindServerUDP, self).callback_connect_client(connection_object)

        def callback_client_handle(self, connection_object, data):
            """
            Called to handle data received from a connection. This method is often overridden to provide custom server
            logic and useful information. It's good practice (and in this case essential) to call
            "return super(MastermindServerTCP,self).callback_client_handle(connection_object,data)" at the end of your
            override.
            :param connection_object: Represents the appropriate connection
            :param data: Data received from the connection
            :return:
            """
            # print(f"Client at {connection_object.address} sent a message: {data}")
            if isinstance(data, Networking.DataPayload):
                # look up and append the client id to the event post
                client_id = self.lookup_client(connection_object.address)
                params = {'client_id': client_id, 'args': data.args, 'kwargs': data.kwargs}
                pygame.event.post(pygame.event.Event(data.command, **params))
            return super(MastermindServerUDP, self).callback_client_handle(connection_object, data)

        def callback_client_send(self, connection_object, data, compression=True):
            """
            Called to when data is about to be sent to a connection. If sending fails, the connection is silently
            terminated. This method can be overridden to provide useful information. It's good practice (and in this
            case essential) to call
            "return super(MastermindServerTCP,self).callback_client_send(connection_object,data,compression)" at the
            end of your override.
            :param connection_object: Represents the appropriate connection
            :param data: Data to be sent
            :param compression: Compression, enabled by default
            :return:
            """
            # define override here
            return super(MastermindServerUDP, self).callback_client_send(connection_object, data, compression)

        class ClientNotFoundException(Exception):
            pass

    class Client(MastermindClientUDP):
        pause_receive = threading.Event()
        _server_reply = None

        def connect(self, ip,port):
            super(MastermindClientUDP, self).connect(ip, port)
            receiver = threading.Thread(target=self.receive_data_from_server)
            receiver.start()

        def send(self, data, compression=None):
            """
            Send data to the server
            :param data: data to be sent
            :param compression: compression
            :return:
            """
            self.pause_receive.set()
            super(MastermindClientUDP, self).send(data, compression)
            self.pause_receive.clear()

        def receive_data_from_server(self):
            """
            Listen to the server and receives any data
            :return:
            """
            while self is not None:
                while not self.pause_receive.is_set():
                    self._server_reply = self.receive(False)

        def get_server_reply(self):
            """
            Retrieves the last message sent by the server
            :return:
            """
            return self._server_reply

    class DataPayload(object):
        """
            Unified data object to be sent over the network
        """
        # Constants for command type
        class Command(Enum):
            CHAT = pygame.USEREVENT+20
            MOVE = pygame.USEREVENT+21
            ACTION = pygame.USEREVENT+22

        def __init__(self, cmd: Command, *args, **kwargs):
            self.command = cmd
            self.args = args
            self.kwargs = kwargs

        # Factory methods
        @staticmethod
        def make_chat_data(*args, **kwargs):
            return Networking.DataPayload(Networking.DataPayload.Command.CHAT, args, kwargs)

        @staticmethod
        def make_move_data(*args, **kwargs):
            return Networking.DataPayload(Networking.DataPayload.Command.MOVE, args, kwargs)
