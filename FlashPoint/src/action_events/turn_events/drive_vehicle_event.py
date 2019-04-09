from typing import Tuple
import logging

from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import VictimStateEnum
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel

logger = logging.getLogger("FlashPoint")


class DriveVehicleEvent(TurnEvent):
    """Move the Vehicle and all its passengers to the designated spot. Assumes passengers have already climbed on."""

    def __init__(self, vehicle_type: str, parking_spot: Tuple[TileModel, TileModel] = None):
        super().__init__()
        self._vehicle_type = vehicle_type
        self._player: PlayerModel = GameStateModel.instance().players_turn
        self._row = min(tile.row for tile in parking_spot) if parking_spot else -1
        self._column = min(tile.column for tile in parking_spot) if parking_spot else -1
        self._board_model: GameBoardModel = GameStateModel.instance().game_board

    def _check_for_rescued_victims(self, parking_spot):
        board: GameBoardModel = GameStateModel.instance().game_board
        tile = board.get_tile_at(parking_spot[0], parking_spot[1])
        second_tile = board.get_other_parking_tile(tile)

        for model in tile.associated_models + second_tile.associated_models:
            if isinstance(model, VictimModel):
                model.state = VictimStateEnum.RESCUED
                GameStateModel.instance().victims_saved = GameStateModel.instance().victims_saved + 1
                # remove the victim from the list of active POIs on the board
                # and disassociate the victim from the player
                board.remove_poi_or_victim(model)

        players_on_spot = [player for player in GameStateModel.instance().players if
                           player.row in [tile.row, second_tile.row] and
                           player.column in [tile.column, second_tile.column]]

        for player in players_on_spot:
            if isinstance(player.carrying_victim, VictimModel):
                player.carrying_victim.state = VictimStateEnum.RESCUED
                GameStateModel.instance().victims_saved = GameStateModel.instance().victims_saved + 1
                board.remove_poi_or_victim(player.carrying_victim)

    def execute(self, *args, **kwargs):
        logger.info("Executing DriveVehicle Event")
        destination_first_tile = self._board_model.get_tile_at(self._row, self._column)
        destination_second_tile = self._board_model.get_other_parking_tile(destination_first_tile)

        ap_multiplier = self._board_model.get_distance_to_parking_spot(self._vehicle_type,
                                                                    (destination_first_tile, destination_second_tile))
        self._player.ap = self._player.ap - 2*ap_multiplier

        if self._vehicle_type == "AMBULANCE":
            self._board_model.ambulance.drive((self._row, self._column))
            self._check_for_rescued_victims((self._row, self._column))
        else:
            self._board_model.engine.drive((self._row, self._column))
