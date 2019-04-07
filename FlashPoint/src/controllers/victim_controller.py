from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.drop_victim_event import DropVictimEvent
from src.action_events.turn_events.pick_up_victim_event import PickupVictimEvent
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.tile_sprite import TileSprite


class VictimController(Controller):

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        if VictimController._instance:
            raise Exception("Victim Controller is a singleton")

        VictimController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def check_pickup(self, tile: TileModel) -> bool:
        game: GameStateModel = GameStateModel.instance()

        victim_tile = game.game_board.get_tile_at(tile.row, tile.column)
        player = game.players_turn

        if game.game_board.get_tile_at(player.row, player.column) != victim_tile:
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

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        victims = [model for model in tile_model.associated_models if isinstance(model, VictimModel)]
        if victims:
            victim = victims[0]

        is_carrying = isinstance(self._current_player.carrying_victim, VictimModel)

        check_func = self.check_drop if is_carrying else self.check_pickup

        if not check_func(tile_model):
            menu_to_close.disable()
            return

        event = DropVictimEvent(victim.row, victim.column) if is_carrying else PickupVictimEvent(victim.row, victim.column)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

        menu_to_close.disable()

    def run_checks(self, tile_model: TileModel) -> bool:
        """Not used since this class has two separate checks."""
        pass

    def process_input(self, tile_sprite: TileSprite):
        tile_model: TileModel = GameStateModel.instance().game_board.get_tile_at(tile_sprite.row, tile_sprite.column)

        button = None
        if self.check_drop(tile_model):
            button = tile_sprite.drop_victim_button
        elif self.check_pickup(tile_model):
            button = tile_sprite.pickup_victim_button

        if button:
            button.enable()
            button.on_click(self.send_event_and_close_menu, tile_model, button)
        else:
            tile_sprite.pickup_victim_button.disable()
            tile_sprite.drop_victim_button.disable()
