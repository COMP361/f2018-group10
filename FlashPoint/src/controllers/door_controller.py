from typing import List

import pygame

from src.action_events.turn_events.close_door_event import CloseDoorEvent
from src.action_events.turn_events.extinguish_event import ExtinguishEvent
from src.action_events.turn_events.move_event import MoveEvent
from src.action_events.turn_events.open_door_event import OpenDoorEvent
from src.action_events.turn_events.turn_event import TurnEvent
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.models.game_board.door_model import DoorModel
from src.sprites.hud.door_sprite import DoorSprite
from src.sprites.game_board import GameBoard
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import GameStateEnum, DoorStatusEnum
from src.models.game_state_model import GameStateModel


class DoorController(object):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        if DoorController._instance:
            raise Exception("DoorController is a singleton")

        DoorController._instance = self
        self.board = GameStateModel.instance().game_board
        self.current_player = current_player
        self.door: DoorSprite = None
        self.can_open = False

    @classmethod
    def instance(cls):
        return cls._instance

    def check(self, door_model: DoorModel) -> bool:
        valid_to_open_close = TurnEvent.has_required_AP(self.current_player.ap, 1)
        if not valid_to_open_close:
            return False

        player_tile = self.board.get_tile_at(self.current_player.row, self.current_player.column)

        if door_model not in player_tile.adjacent_edge_objects.values():
            return False

        door_status = door_model.door_status
        if door_status == DoorStatusEnum.DESTROYED:
            return False

        return True

    def process_input(self, door_sprite: DoorSprite):
        door_model = door_sprite.door_model

        if self.door:
            self.door.button_input.disable()
            self.door = None

        if not self.check(door_model):
            door_sprite.button_input.disable()
            self.can_open = False
            print("Check failed")
            return

        self.can_open = True
        door_sprite.menu_shown = True
        self.door = door_sprite
        self.door.button_input.enable()
        # print(door_model.door_status)
        self.door.button_input.on_click(self.instantiate_event, door_model)

    def instantiate_event(self, door_model: DoorModel):
        event: TurnEvent = None
        self.door.menu_shown = False
        self.door.button_input.disable()
        if door_model.door_status == DoorStatusEnum.OPEN:
            event = CloseDoorEvent(door_model)

        elif door_model.door_status == DoorStatusEnum.CLOSED:
            event = OpenDoorEvent(door_model)

        if event:
            if Networking.get_instance().is_host:
                Networking.get_instance().send_to_all_client(event)
            else:
                Networking.get_instance().client.send(event)


    def update(self, queue: EventQueue):
        if GameStateModel.instance().state != GameStateEnum.MAIN_GAME:
            return

        doors: List[DoorSprite] = GameBoard.instance().grid.get_doors

        for door in doors:
            for event in queue:
                if event.type == pygame.MOUSEBUTTONUP:
                    if door.direction == 'West' or door.direction == 'East':
                        if door.button.rect.x <= pygame.mouse.get_pos()[
                            0] <= door.button.rect.x + 20 and door.button.rect.y + 40 <= \
                                pygame.mouse.get_pos()[1] <= door.button.rect.y + 100:
                            # means the user is pressing on the door
                            print("door detected")
                            self.process_input(door)

                    if door.direction == 'North' or door.direction == 'South':
                        if door.button.rect.x + 40 <= pygame.mouse.get_pos()[
                            0] <= door.button.rect.x + 100 and door.button.rect.y <= \
                                pygame.mouse.get_pos()[1] <= door.button.rect.y + 20:
                            # means the user is pressing on the door
                            print("door detected")
                            self.process_input(door)

