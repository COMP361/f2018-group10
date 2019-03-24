from typing import Tuple

import pygame

import src.constants.color as Color
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.action_events.vehicle_placed_event import VehiclePlacedEvent
from src.sprites.tile_sprite import TileSprite
from src.models.game_board.tile_model import TileModel
from src.constants.state_enums import GameKindEnum, GameStateEnum, SpaceKindEnum, VehicleOrientationEnum
from src.models.game_state_model import GameStateModel
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.sprites.game_board import GameBoard
from src.models.game_units.player_model import PlayerModel


class VehicleController(object):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        if VehicleController._instance:
            raise Exception("ChooseVehiclePositionController is a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("ChooseVehiclePositionController should not exist in Family Mode!")
        self.current_player = current_player
        self.game_board_sprite = GameBoard.instance()
        self.choose_engine_prompt = RectLabel(500, 0, 350, 75, Color.GREY, 0,
                                              Text(pygame.font.SysFont('Agency FB', 30), "Choose Engine Position",
                                                   Color.ORANGE))
        self.choose_ambulance_prompt = RectLabel(500, 0, 350, 75, Color.GREY, 0,
                                              Text(pygame.font.SysFont('Agency FB', 30), "Choose Ambulance Position",
                                                   Color.ORANGE))
        self.wait_prompt = RectLabel(500, 400, 350, 75, Color.GREY, 0,
                                              Text(pygame.font.SysFont('Agency FB', 30), "Host Is Placing Vehicles...",
                                                   Color.ORANGE))

        VehicleController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def _run_placement_checks(self, tile_model: TileModel):
        game_state: GameStateModel = GameStateModel.instance()
        engine_placed = game_state.game_board.engine.orientation != VehicleOrientationEnum.UNSET
        ambulance_placed = game_state.game_board.ambulance.orientation != VehicleOrientationEnum.UNSET

        if game_state.state != GameStateEnum.PLACING_VEHICLES:
            return False

        if self.current_player != game_state.players_turn:
            return False

        if tile_model.space_kind == SpaceKindEnum.INDOOR:
            return False

        # Ambulance not placed and space is not ambulance parking => nothing has been placed yet
        if not ambulance_placed and tile_model.space_kind != SpaceKindEnum.AMBULANCE_PARKING:
            return False

        # If we reach here then the ambulance has already been placed.
        if not engine_placed and ambulance_placed and tile_model.space_kind != SpaceKindEnum.ENGINE_PARKING:
            return False

        return True

    def _apply_highlight(self):
        game_state = GameStateModel.instance()

        for i in range(len(self.game_board_sprite.grid.grid)):
            for j in range(len(self.game_board_sprite.grid.grid[i])):
                tile_model = game_state.game_board.get_tile_at(j, i)
                tile_sprite = self.game_board_sprite.grid.grid[i][j]

                success = self._run_placement_checks(tile_model)

                if success and not tile_sprite.highlight_color:
                    tile_sprite.highlight_color = Color.GREEN
                elif not success:
                    tile_sprite.highlight_color = None

    def _determine_second_tile(self, parking_type: SpaceKindEnum, first_tile: TileModel) -> TileModel:
        game_state: GameStateModel = GameStateModel.instance()
        orientation = None
        if parking_type == SpaceKindEnum.AMBULANCE_PARKING:
            orientation = game_state.game_board.ambulance.orientation
        elif parking_type == SpaceKindEnum.ENGINE_PARKING:
            orientation = game_state.game_board.engine.orientation

        if orientation == VehicleOrientationEnum.HORIZONTAL:
            return game_state.game_board.get_tile_at(first_tile.row, first_tile.column+1)
        elif orientation == VehicleOrientationEnum.VERTICAL:
            return game_state.game_board.get_tile_at(first_tile.row+1, first_tile.column)

    def _player_is_in_parking_space(self, parking_spot: Tuple[TileModel, TileModel]):
        player = self.current_player
        row_match = player.row == parking_spot[0].row or player.row == parking_spot[1].row
        column_match = player.column == parking_spot[0].column or player.row == parking_spot[1].column
        return row_match and column_match

    def enable_prompts(self):
        self.game_board_sprite.add(self.choose_ambulance_prompt)
        self.game_board_sprite.add(self.wait_prompt)

    def process_input_placement(self, tile_sprite: TileSprite):
        game_state: GameStateModel = GameStateModel.instance()
        engine_placed = game_state.game_board.engine.orientation != VehicleOrientationEnum.UNSET
        ambulance_placed = game_state.game_board.ambulance.orientation != VehicleOrientationEnum.UNSET

        tile_model = game_state.game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if not self._run_placement_checks(tile_model):
            return

        event = None
        parking_spot = None
        if not ambulance_placed:
            parking_spot = [spot for spot in game_state.game_board.ambulance_spots if tile_model in spot][0]
            event = VehiclePlacedEvent(game_state.game_board.ambulance, parking_spot)
            self.game_board_sprite.add(self.choose_engine_prompt)
        elif not engine_placed:
            parking_spot = [spot for spot in game_state.game_board.engine_spots if tile_model in spot][0]
            event = VehiclePlacedEvent(game_state.game_board.engine, parking_spot)
            
        if not parking_spot:
            return

        if not event:
            return

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().send_to_server(event)

    def process_input_main_game(self, tile_sprite: TileSprite):
        game_state: GameStateModel = GameStateModel.instance()
        first_tile = game_state.game_board.get_tile_at(tile_sprite.row, tile_sprite.column)
        parking_type = first_tile.space_kind
        second_tile = self._determine_second_tile(parking_type, first_tile)

        if parking_type == SpaceKindEnum.AMBULANCE_PARKING:
            if self._player_is_in_parking_space((first_tile, second_tile)):
                # Display some kind of prompt for riding the ambulance
                pass
            else:
                # Display some kind of prompt for moving the ambulance to here
                pass

        elif parking_type == SpaceKindEnum.ENGINE_PARKING:
            # Display some kind of prompt for driving/riding the engine
            pass

    def update(self, event_queue: EventQueue):
        game_state: GameStateModel = GameStateModel.instance()
        engine_placed = game_state.game_board.engine.orientation != VehicleOrientationEnum.UNSET
        ambulance_placed = game_state.game_board.ambulance.orientation != VehicleOrientationEnum.UNSET
        if engine_placed:
            self.choose_engine_prompt.kill()

        if ambulance_placed:
            self.choose_ambulance_prompt.kill()

        if self.current_player == GameStateModel.instance().players_turn:
            self.wait_prompt.kill()

        if game_state.state == GameStateEnum.PLACING_VEHICLES:
            self._apply_highlight()
