from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.extinguish_event import ExtinguishEvent
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import SpaceStatusEnum, WallStatusEnum, DoorStatusEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.door_model import DoorModel
from src.models.game_board.tile_model import TileModel
from src.models.game_board.wall_model import WallModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
from src.sprites.tile_sprite import TileSprite


class ExtinguishController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)

        if ExtinguishController._instance:
            self._current_player = current_player
            # raise Exception("ExtinguishController is a singleton")
        self.game_board_sprite = GameBoard.instance()
        self.current_player = current_player
        game: GameStateModel = GameStateModel.instance()
        game.game_board.reset_tiles_visit_count()

        ExtinguishController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def run_checks(self, tile_model: TileModel) -> bool:
        if self.current_player != GameStateModel.instance().players_turn:
            return False

        # Doge cannot extinguish fire/smoke
        if self.current_player.role == PlayerRoleEnum.DOGE:
            return False

        player_tile: TileModel = GameStateModel.instance().game_board.get_tile_at(self.current_player.row,
                                                                                  self.current_player.column)

        if tile_model not in player_tile.adjacent_tiles.values() and tile_model != player_tile:
            return False

        # It costs the Rescue Specialist and Paramedic
        # twice as much AP to extinguish fire/smoke.
        if self.current_player.role in [PlayerRoleEnum.RESCUE, PlayerRoleEnum.PARAMEDIC]:
            valid_to_extinguish = TurnEvent.has_required_AP(self.current_player.ap, 2)

        # CAFS firefighter's special AP are
        # used for extinguishing fire/smoke.
        elif self.current_player.role == PlayerRoleEnum.CAFS:
            valid_to_extinguish = TurnEvent.has_required_AP(self.current_player.ap + self.current_player.special_ap, 1)

        else:
            valid_to_extinguish = TurnEvent.has_required_AP(self.current_player.ap, 1)

        if not valid_to_extinguish:
            return False

        if tile_model.space_status == SpaceStatusEnum.SAFE:
            return False

        if player_tile.get_tile_in_direction("South") == tile_model:
            obs = player_tile.get_obstacle_in_direction('South')
            if isinstance(obs, WallModel):
                if not obs.wall_status == WallStatusEnum.DESTROYED:
                    return False

            elif isinstance(obs, DoorModel):
                if obs.door_status == DoorStatusEnum.CLOSED:
                    return False

        elif player_tile.get_tile_in_direction("North") == tile_model:
            obs = player_tile.get_obstacle_in_direction('North')
            if isinstance(obs, WallModel):
                if not obs.wall_status == WallStatusEnum.DESTROYED:
                    return False

            elif isinstance(obs, DoorModel):
                if obs.door_status == DoorStatusEnum.CLOSED:
                    return False

        elif player_tile.get_tile_in_direction("East") == tile_model:
            obs = player_tile.get_obstacle_in_direction('East')
            if isinstance(obs, WallModel):
                if not obs.wall_status == WallStatusEnum.DESTROYED:
                    return False

            elif isinstance(obs, DoorModel):
                if obs.door_status == DoorStatusEnum.CLOSED:
                    return False

        elif player_tile.get_tile_in_direction("West") == tile_model:
            obs = player_tile.get_obstacle_in_direction('West')
            if isinstance(obs, WallModel):
                if not obs.wall_status == WallStatusEnum.DESTROYED:
                    return False

            elif isinstance(obs, DoorModel):
                if obs.door_status == DoorStatusEnum.CLOSED:
                    return False

        return True

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        if not self.run_checks(tile_model):
            menu_to_close.disable()
            return

        event = ExtinguishEvent(tile_model)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().send_to_server(event)

        menu_to_close.disable()

    def process_input(self, tile_sprite: TileSprite):
        tile_model = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if not self.run_checks(tile_model):
            tile_sprite.extinguish_button.disable()
            return

        tile_sprite.extinguish_button.enable()
        tile_sprite.extinguish_button.on_click(self.send_event_and_close_menu, tile_model, tile_sprite.extinguish_button)
