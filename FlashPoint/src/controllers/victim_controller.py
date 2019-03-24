from src.constants.state_enums import GameStateEnum
from src.core.event_queue import EventQueue
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.tile_sprite import TileSprite


class VictimController(object):
    _instance = None

    def __init__(self):
        if VictimController._instance:
            raise Exception("Victim Controller is a singleton")

        VictimController._instance = self
        self.fireman = GameStateModel.instance().players_turn

        self.action_tile: TileSprite = None
        self.can_drop = False
        self.can_pickup = False

    @classmethod
    def instance(cls):
        return cls.instance()

    def check_pickup(self, tile: TileModel) -> bool:
        game: GameStateModel = GameStateModel.instance()

        victim_tile = game.game_board.get_tile_at(tile.row, tile.column)
        player = game.players_turn

        if not game.game_board.get_tile_at(player.row, player.column) == victim_tile:
            return False

        for assoc_model in victim_tile.associated_models:
            if isinstance(assoc_model, VictimModel):
                return True

        return False

    def check_drop(self, tile: TileModel):
        game: GameStateModel = GameStateModel.instance()
        player = game.players_turn

        if GameStateModel.instance().game_board.get_tile_at(player.row, player.column) == tile \
                and isinstance(player.carrying_victim, VictimModel):
            return True

        return False

    def process_input_(self, tile: TileSprite):
        if self.action_tile:
            self.action_tile.disable_drop()
            self.action_tile.disable_pickup()
            self.action_tile = None

        tile_model: TileModel = GameStateModel.instance().game_board.get_tile_at(tile.row, tile.column)

        if self.check_drop(tile_model):
            self.can_drop = True
            self.can_pickup = False
            self.action_tile = tile
            self.action_tile.drop_victim_button.enable()
            return

        elif self.check_pickup(tile_model):
            self.can_pickup = True
            self.can_drop = False
            self.action_tile = tile
            self.action_tile.pickup_victim_button.enable()

        else:
            self.can_drop = False
            self.can_pickup = False
            tile.pickup_victim_button.disable()
            tile.drop_victim_button.disable()

    def update(self, event_queue: EventQueue):
        if GameStateModel.instance().state != GameStateEnum.MAIN_GAME:
            return




