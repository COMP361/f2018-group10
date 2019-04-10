import pygame

import src.constants.color as Color
from src.UIComponents.interactable import Interactable
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.action_events.vehicle_placed_event import VehiclePlacedEvent
from src.constants.state_enums import GameStateEnum, SpaceKindEnum, VehicleOrientationEnum
from src.controllers.controller import Controller
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.vehicle_model import VehicleModel
from src.sprites.game_board import GameBoard
from src.sprites.tile_sprite import TileSprite


class VehiclePlacementController(Controller):
    """Class for controlling inputs during the placing vehicles phase. Displays prompts."""

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)

        if VehiclePlacementController._instance:
            self._current_player = current_player
            # raise Exception(f"{VehiclePlacementController.__name__} is a singleton!")

        self.choose_engine_prompt = RectLabel(500, 30, 350, 75, Color.GREY, 0,
                                              Text(pygame.font.SysFont('Agency FB', 30), "Choose Engine Position",
                                                   Color.GREEN2))
        self.choose_engine_prompt.change_bg_image('media/GameHud/wood2.png')
        self.choose_engine_prompt.add_frame('media/GameHud/frame.png')
        self.choose_ambulance_prompt = RectLabel(500, 30, 350, 75, Color.GREY, 0,
                                                 Text(pygame.font.SysFont('Agency FB', 30), "Choose Ambulance Position",
                                                      Color.GREEN2))
        self.choose_ambulance_prompt.change_bg_image('media/GameHud/wood2.png')
        self.choose_ambulance_prompt.add_frame('media/GameHud/frame.png')
        self.wait_prompt = RectLabel(500, 580, 350, 75, Color.GREY, 0,
                                     Text(pygame.font.SysFont('Agency FB', 30), "Host Is Placing Vehicles...",
                                          Color.GREEN2))
        self.wait_prompt.change_bg_image('media/GameHud/wood2.png')
        self.wait_prompt.add_frame('media/GameHud/frame.png')
        self.game_board_sprite = GameBoard.instance()
        self.ambulance_placed = False
        self.engine_placed = False

        VehiclePlacementController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def run_checks(self, tile_model: TileModel) -> bool:
        game: GameStateModel = GameStateModel.instance()

        if game.state != GameStateEnum.PLACING_VEHICLES:
            return False

        if not Networking.get_instance().is_host:
            return False

        if tile_model.space_kind == SpaceKindEnum.INDOOR:
            return False

        return True

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        game_board: GameBoardModel = GameStateModel.instance().game_board

        spot_list = game_board.engine_spots if self.ambulance_placed else game_board.ambulance_spots
        parking_spot = [spot for spot in spot_list if tile_model in spot]
        if not parking_spot:
            return
        parking_spot = parking_spot[0]
        vehicle = game_board.engine if self.ambulance_placed else game_board.ambulance
        event = VehiclePlacedEvent(vehicle, parking_spot)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

        if not self.ambulance_placed:
            self.ambulance_placed = True

        elif not self.engine_placed:
            self.engine_placed = True

    def _check_highlight(self, tile_model: TileModel, vehicle_type: str):
        if vehicle_type == "AMBULANCE":
            return tile_model.space_kind == SpaceKindEnum.AMBULANCE_PARKING
        elif vehicle_type == "ENGINE":
            return tile_model.space_kind == SpaceKindEnum.ENGINE_PARKING

    def _apply_highlight(self, vehicle_type: str):
        game_state = GameStateModel.instance()

        for i in range(len(self.game_board_sprite.grid.grid)):
            for j in range(len(self.game_board_sprite.grid.grid[i])):
                tile_model = game_state.game_board.get_tile_at(j, i)
                tile_sprite = self.game_board_sprite.grid.grid[i][j]

                success = self._check_highlight(tile_model, vehicle_type)

                if success and not tile_sprite.highlight_color:
                    tile_sprite.highlight_color = Color.GREEN
                elif not success:
                    tile_sprite.highlight_color = None

    def process_input(self, tile_sprite: TileSprite):
        game_state: GameStateModel = GameStateModel.instance()

        tile_model = game_state.game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if not self.run_checks(tile_model):
            return

        self.send_event_and_close_menu(tile_model, None)

    def enable_prompts(self):
        if Networking.get_instance().is_host:
            self.game_board_sprite.add(self.choose_engine_prompt)
            self.game_board_sprite.add(self.choose_ambulance_prompt)
        else:
            self.game_board_sprite.add(self.wait_prompt)

    def update(self, event_queue: EventQueue):
        game: GameStateModel = GameStateModel.instance()
        if not game.state == GameStateEnum.PLACING_VEHICLES:
            return

        if self.engine_placed:
            self.choose_engine_prompt.kill()

        if self.ambulance_placed:
            self.choose_ambulance_prompt.kill()

        ambulance: VehicleModel = GameStateModel.instance().game_board.ambulance
        engine: VehicleModel = GameStateModel.instance().game_board.engine
        if ambulance.orientation != VehicleOrientationEnum.UNSET and engine.orientation != VehicleOrientationEnum.UNSET:
            self.wait_prompt.kill()
            self.choose_ambulance_prompt.kill()
            self.choose_engine_prompt.kill()

        vehicle_type = "ENGINE" if self.ambulance_placed else "AMBULANCE"
        self._apply_highlight(vehicle_type)
