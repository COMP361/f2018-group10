from typing import Union

import ipaddress
import socket
import threading
import logging
import time

from src.action_events.chat_event import ChatEvent
from src.core.custom_event import CustomEvent
from src.core.serializer import JSONSerializer
from src.core.event_queue import EventQueue
from src.constants.change_scene_enum import ChangeSceneEnum
from src.models.game_state_model import GameStateModel
from src.action_events.action_event import ActionEvent
from src.action_events.turn_events.turn_event import TurnEvent
from src.action_events.join_event import JoinEvent
from src.action_events.dummy_event import DummyEvent
from src.action_events.disconnect_event import DisconnectEvent
from src.external.Mastermind import *

logger = logging.getLogger("networking")
logger.setLevel(logging.INFO)


class Networking:
    """
    Class that stores networking info like host and client. This class follows a Singleton design pattern.
    """
    __instance = None

    @staticmethod
    def wait_for_reply(timeout=5):
        """
        Wait for a reply from the host before continuing with a timeout (in seconds).
        Returns false for failed attempt, true for success.
        """
        i = 0
        reply = Networking.get_instance().client.get_server_reply()
        while not reply:
            reply = Networking.get_instance().client.get_server_reply()
            time.sleep(1)
            i += 1
            if i > timeout:
                raise ConnectionError
        return reply

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
        TIMEOUT_CONNECT = 5
        TIMEOUT_RECEIVE = 5

        stop_broadcast = threading.Event()
        stop_listen = threading.Event()

        def __init__(self):
            self.host = None
            self.client = None
            self.game = None
            self.stop_broadcast.set()
            self.server_reply = None

        def create_host(self, port=20298):
            """
            Attempts to create a game host on localhost and a game client that connects to it.
            A host machine is both a server (host) and a client so that the send message workflow can be simplified.
            i.e. The send message can be hooked to a command without checking if the current machine is a host or not.
            :param port: Port to be opened on the local machine. Defaults to 20298.
            :return:
            """
            # We use UDP to broadcast the host
            self.host = Networking.Host(1, 2, 5)

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
                self.client.connect(ip, port)
                self.client.send(JoinEvent(player))
                return True
            except MastermindErrorClient as e:
                self.client.disconnect()
                logger.error(f"Error connecting to server at: {ip}:{port}")
                raise MastermindErrorClient(e)
            except OSError as e:
                self.client.disconnect()
                raise OSError(e)

        @staticmethod
        def broadcast_game(args, stop_event):
            # TODO DON'T USE THIS YET
            b_caster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            b_caster.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            b_caster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            msg = f"{socket.gethostname()} {mastermind_get_local_ip()}"
            bip = Networking.get_instance().get_broadcast_ip()
            print(f"Broadcasting at {bip}:54545\n")

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
                self.send_to_all_client(DisconnectEvent())
                self.host.disconnect_clients()
                self.host.disconnect()
                self.host.__del__()
                self.host = None
            EventQueue.post(CustomEvent(ChangeSceneEnum.STARTSCENE))

        def send_to_server(self, data, compress=True):
            """
            Send data to server
            :param data: data to be sent
            :param compress: compression, enabled by default
            :return:
            """
            if self.client is not None:
                try:
                    self.client.toggle_block_signal(True)
                    self.client.send(data, compress)
                    self.client.toggle_block_signal(False)
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
                    try:
                        self.host.callback_client_send(client, data, compress)
                    except MastermindErrorSocket as e:
                        raise MastermindErrorSocket(e)
            else:
                raise MastermindErrorServer("Server is not available")

    # Overridden classes
    class Host(MastermindServerUDP):
        def __init__(self, time_server_refresh=1.0, time_connection_refresh=2.0, time_connection_timeout=5.0):
            MastermindServerUDP.__init__(self, time_server_refresh, time_connection_refresh, time_connection_timeout)
            self.client_list = {}

        def lookup_client(self, ip_addr: str):
            """
            Look up the client list (array) and return the connection object
            :param ip_addr: client's ip address
            :return:
            """
            try:
                conn_obj = self.client_list[ip_addr]
                if conn_obj is not None:
                    return conn_obj
                else:
                    raise Networking.Host.ClientNotFoundException
            except KeyError:
                raise Networking.Host.ClientNotFoundException

        def client_exists(self, ip_addr: str):
            try:
                if self.lookup_client(ip_addr):
                    return True
                return False
            except Networking.Host.ClientNotFoundException:
                return False

        def kick_client(self, ip_addr: str):
            self.client_list.pop(ip_addr)

        def callback_connect_client(self, connection_object):
            """
            Called when a new client connects. This method can be overridden to provide useful information. It's good
            practice to call "return super(MastermindServerTCP,self).callback_connect_client(connection_object)" at the
            end of your override.
            :param connection_object: Represents the appropriate connection
            :return:
            """
            # Assign a new connection object to the address (as a key value pair)
            if not self.client_exists(connection_object.address[0]):
                if len(self.client_list) <= 6:
                    self.client_list[connection_object.address[0]] = connection_object
                    print(f"Client at {connection_object.address} is connected")
                else:
                    self.accepting_disallow()
                    print("Limit reached, stop accepting connections")
            return super(MastermindServerUDP, self).callback_connect_client(connection_object)

        def callback_disconnect_client(self, connection_object):
            """
            Called when a client disconnects. This method can be overridden to provide useful information. It's good
            practice to call "return super(MastermindServerTCP,self).callback_disconnect_client(connection_object)" at
            the end of your override.
            :param connection_object: Represents the appropriate connection
            :return:
            """
            # Pops the client's connection object
            game = GameStateModel.instance()
            if game:
                players = [x for x in game.players if x.ip == connection_object.address[0]]
                if players:
                    # game.remove_player(players[0])
                    self.kick_client(connection_object.address[0])
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
            # print("Received")
            if connection_object.address[0] == "127.0.0.1":
                return

            data = JSONSerializer.deserialize(data)
            # If it's a dummy event, don't do anything
            if isinstance(data, DummyEvent):
                # print("Received dummy event")
                return super(MastermindServerUDP, self).callback_client_handle(connection_object, data)

            print(f"Client at {connection_object.address} sent a message: {data.__class__}")
            if isinstance(data, TurnEvent) or isinstance(data, ActionEvent):
                if isinstance(data, ChatEvent):
                    Networking.get_instance().send_to_all_client(data)
                    return super(MastermindServerUDP, self).callback_client_handle(connection_object, data)

                data.execute()

                if isinstance(data, DisconnectEvent):
                    # Kick the player that send the DC event and notify all other players.
                    # Need to have similar polling mechanics like in lobby
                    self.kick_client(connection_object.address[0])

                if isinstance(data, JoinEvent):
                    Networking.get_instance().send_to_all_client(GameStateModel.instance())

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
            print(f"Sending message to client at {connection_object.address} : {data['class']}")
            return super(MastermindServerUDP, self).callback_client_send(connection_object, data, compression)

        class ClientNotFoundException(Exception):
            pass

    class Client(MastermindClientUDP):
        def __init__(self, timeout_connect=None, timeout_receive=None):
            super(MastermindClientUDP, self).__init__(MM_UDP, timeout_connect, timeout_receive)
            self._pause_receive = threading.Event()
            self._stop_receive = threading.Event()
            self._pause_blk_signal = threading.Event()
            self._reply_queue = []

        def connect(self, ip, port):
            super(MastermindClientUDP, self).connect(ip, port)
            signaler = threading.Thread(target=self.send_blocking_signal)
            receiver = threading.Thread(target=self.receive_data_from_server)
            signaler.start()
            receiver.start()

        def send(self, data: Union[ActionEvent, TurnEvent], compression=None):
            """
            Send data to the server
            :param data: data to be sent, MUST be an instance of ActionEvent
            :param compression: compression
            :return:
            """
            self._pause_receive.set()
            try:
                super(MastermindClientUDP, self).send(JSONSerializer.serialize(data), compression)
            except MastermindErrorClient:
                self.callback_disconnect()
            except MastermindErrorSocket:
                self.callback_disconnect()
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
                            self.callback_client_receive(_server_reply)
                    except MastermindErrorClient:
                        self.callback_disconnect()
                    except OSError:
                        self.callback_disconnect()

        def disconnect(self):
            self._pause_blk_signal.set()
            self._pause_receive.set()
            self._stop_receive.set()
            time.sleep(0.5)
            return super(MastermindClientUDP, self).disconnect()

        @staticmethod
        def callback_client_receive(data):
            """Handle receiving data from host."""
            data: GameStateModel = JSONSerializer.deserialize(data)
            print(f"Received {data.__class__} object from host.")
            if isinstance(data, GameStateModel):
                GameStateModel.set_game(data)
            if isinstance(data, TurnEvent) or isinstance(data, ActionEvent):
                data.execute()
                if isinstance(data, DisconnectEvent):
                    Networking.get_instance().disconnect()

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
            while not self._stop_receive.is_set():
                if not self._pause_blk_signal.is_set():
                    self.send(DummyEvent())
                    time.sleep(2)

        def toggle_block_signal(self, toggle: bool):
            if toggle:
                self._pause_blk_signal.set()
            else:
                self._pause_blk_signal.clear()

        @staticmethod
        def callback_disconnect():
            """
            Define callback here when client's connection to host is interrupted.
            :return:
            """
            print("It seems that client is not connected...")
            Networking.get_instance().disconnect()

