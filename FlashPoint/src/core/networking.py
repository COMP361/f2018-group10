import ipaddress
import socket
import threading
import logging

from src.core.serializer import JSONSerializer
from src.action_events.action_event import ActionEvent
from src.action_events.join_event import JoinEvent
from src.external.Mastermind import *

logger = logging.getLogger("networking")
logger.setLevel(logging.INFO)


class TestObject(object):

    class_thing = 69

    def __init__(self):
        self.something = "Francis is gay"
        self.something_else = "Holy"


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

    @staticmethod
    def set_game(game):
        Networking.__instance.game = game

    class NetworkingInner:
        host = None
        client = None
        TIMEOUT_CONNECT = 200
        TIMEOUT_RECEIVE = 200

        stop_broadcast = threading.Event()
        stop_listen = threading.Event()

        server_reply = None

        def __init__(self):
            self.game = None
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

            # port = self.get_open_port()
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

        def join_host(self, ip, port=20298, player = None):
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
                self.client.send(JoinEvent(player))
                return True
            except MastermindErrorClient as e:
                logger.error(f"Error connecting to server at: {ip}:{port}")
                raise MastermindErrorClient(e)
            except OSError as e:
                raise OSError(e)

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
            print("Broadcast killed")

            if self.host is not None:
                self.host.accepting_disallow()

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
                except MastermindErrorSocket as e:
                    raise MastermindErrorSocket(e)
            else:
                raise MastermindErrorClient("Client is not available")

        def send_to_client(self, ip_addr: str, data, compress=True):
            """
            Send data to client
            :param ip_addr: client id
            :param data: data to be sent
            :param compress: compression, enabled by default
            :return:
            """
            if self.host is not None:
                try:
                    client_conn_obj = self.host.lookup_client(ip_addr)
                    self.host.callback_client_send(client_conn_obj, data, compress)
                except MastermindErrorSocket as e:
                    raise MastermindErrorSocket(e)
            else:
                raise MastermindErrorServer("Server is not available")

        def send_to_all_client(self, data, compress=True):
            """
            Similar to send_to_client, but sends to every client connected to host
            :param data:
            :param compress:
            :return:
            """
            if self.host:
                for client in self.host.client_list.values():
                    print(f"Sending to client at {client.address}\n")
                    try:
                        self.host.callback_client_send(client, data, compress)
                    except MastermindErrorSocket as e:
                        raise MastermindErrorSocket(e)
            else:
                raise MastermindErrorServer("Server is not available")

    # Overridden classes
    class Host(MastermindServerUDP):
        client_list = {}

        def lookup_client(self, ip_addr: str):
            """
            Look up the client list (array) and return the connection object
            :param ip_addr: client's ip address
            :return:
            """
            conn_obj = self.client_list[ip_addr]
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
            print(f"Client at {connection_object.address} is connected")
            # Assign a new connection object to the address (as a key value pair)
            self.client_list[connection_object.address[0]] = connection_object

            # inform the event queue that a client is connected, with the respective client id
            # event = pygame.event.Event(CustomEvents.CLIENT_CONNECTED, {'client_id': client_id})
            # pygame.event.post(event)

            return super(MastermindServerUDP, self).callback_connect_client(connection_object)

        def callback_disconnect(self):
            """
            Called when the server disconnects (i.e., when .disconnect(...) is called). This method can be overridden
            to provide useful information. It's good practice to call
            "return super(MastermindServerTCP,self).callback_disconnect()" at the end of your override.
            :return:
            """
            # Pops the client's connection object
            game = Networking.get_instance().game
            players = [x for x in game.players]
            if players:
                for player in players:
                    game.remove_player(player)
            return super(MastermindServerUDP, self).callback_disconnect()

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
            if connection_object.address[0] == "127.0.0.1":
                return

            data = JSONSerializer.deserialize(data)
            print(f"Client at {connection_object.address} sent a message: {data}")
            if isinstance(data, ActionEvent):
                if isinstance(data, JoinEvent):
                    print(Networking.get_instance().game.players)
                    Networking.get_instance().game.add_player(data.player)
                    Networking.get_instance().send_to_all_client(Networking.get_instance().game)
                data.execute()
            return super(MastermindServerUDP, self).callback_client_handle(connection_object, data)

        def callback_client_send(self, connection_object, data, compression=None):
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
            data = JSONSerializer.serialize(data)
            return super(MastermindServerUDP, self).callback_client_send(connection_object, data, compression)

        class ClientNotFoundException(Exception):
            pass

    class Client(MastermindClientUDP):
        _pause_receive = threading.Event()
        _stop_receive = threading.Event()
        _reply_queue = []

        def connect(self, ip, port):
            super(MastermindClientUDP, self).connect(ip, port)
            receiver = threading.Thread(target=self.receive_data_from_server)
            receiver.start()

        def send(self, data: ActionEvent, compression=None):
            """
            Send data to the server
            :param data: data to be sent, MUST be an instance of ActionEvent
            :param compression: compression
            :return:
            """
            self._pause_receive.set()
            super(MastermindClientUDP, self).send(JSONSerializer.serialize(data), compression)
            self._pause_receive.clear()

        def receive_data_from_server(self):
            """
            Listen to the server and receives any data
            :return:
            """
            while not self._stop_receive.is_set():
                if not self._pause_receive.is_set():
                    try:
                        _server_reply = self.receive(False)
                        if _server_reply:
                            self._reply_queue.append(_server_reply)
                            print(f"Received: {_server_reply}")
                    except OSError as e:
                        print(f"Error receiving data: {e}")

        def disconnect(self):
            self._stop_receive.set()
            return super(MastermindClientUDP, self).disconnect()

        def get_server_reply(self):
            """
            Retrieves the last message sent by the server
            :return:
            """
            if len(self._reply_queue) > 0:
                return self._reply_queue.pop(0)

        def send_blocking_signal(self):
            """
            Informs the host of the client's existence, so that it doesn't get disconnected automatically
            :return:
            """
            pass
