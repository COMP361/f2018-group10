from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.drop_victim_event import DropVictimEvent
from src.action_events.turn_events.lead_victim_event import LeadVictimEvent
from src.action_events.turn_events.pick_up_victim_event import PickupVictimEvent
from src.action_events.turn_events.stop_leading_victim_event import StopLeadingVictimEvent
from src.constants.state_enums import VictimStateEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.hazmat_model import HazmatModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.tile_sprite import TileSprite


class VictimController(Controller):

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):
        pass

    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        if VictimController._instance:
            raise Exception("Victim Controller is a singleton")

        VictimController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def check_lead(self, tile_model: TileModel) -> bool:
        """If there is a treated victim on this tile and the player is not leading a victim"""
        if self._current_player.role == PlayerRoleEnum.DOGE:
            return False

        for model in tile_model.associated_models:
            if isinstance(model, VictimModel) and model.state == VictimStateEnum.TREATED:
                return not isinstance(self._current_player.leading_victim, VictimModel)
        return False

    def check_stop_lead(self, tile_model: TileModel) -> bool:
        return isinstance(self._current_player.leading_victim, VictimModel) and \
               tile_model.row == self._current_player.row and tile_model.column == self._current_player.column

    def check_pickup(self, tile: TileModel) -> bool:
        game: GameStateModel = GameStateModel.instance()

        if isinstance(self._current_player.carrying_hazmat, HazmatModel):
            # Cant carry victim and hazmat at the same time
            return False

        victim_tile = game.game_board.get_tile_at(tile.row, tile.column)
        player = game.players_turn

        if game.game_board.get_tile_at(player.row, player.column) != victim_tile:
            return False

        for assoc_model in victim_tile.associated_models:
            if isinstance(assoc_model, VictimModel) and not assoc_model.state == VictimStateEnum.TREATED:
                return True

        return False

    def check_drop(self, tile: TileModel):
        game: GameStateModel = GameStateModel.instance()
        player = game.players_turn

        if GameStateModel.instance().game_board.get_tile_at(player.row, player.column) == tile \
                and isinstance(player.carrying_victim, VictimModel):
            return True

        return False

    def send_pickup_event(self, tile_model: TileModel, menu_to_close: Interactable):
        victims = [model for model in tile_model.associated_models if isinstance(model, VictimModel)]
        victim = None
        if victims:
            victim = victims[0]

        if not victim:
            return

        if not self.check_pickup(tile_model):
            return

        event = PickupVictimEvent(victim.row, victim.column)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

        menu_to_close.disable()

    def send_drop_event(self, tile_model: TileModel, menu_to_close: Interactable):
        if not self.check_drop(tile_model):
            return

        event = DropVictimEvent(self._current_player.row, self._current_player.column)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

        menu_to_close.disable()

    def send_lead_event(self, tile_model: TileModel, menu_to_close: Interactable):
        if not self.check_lead(tile_model):
            return

        event = LeadVictimEvent(self._current_player.row, self._current_player.column)

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

        menu_to_close.disable()

    def send_stop_lead_event(self, tile_model: TileModel, menu_to_close: Interactable):
        if not self.check_stop_lead(tile_model):
            return

        event = StopLeadingVictimEvent(self._current_player.row, self._current_player.column)

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

        if self.check_drop(tile_model):
            tile_sprite.drop_victim_button.enable()
            tile_sprite.drop_victim_button.on_click(self.send_drop_event, tile_model, tile_sprite.drop_victim_button)

        elif self.check_pickup(tile_model):
            tile_sprite.pickup_victim_button.enable()
            tile_sprite.pickup_victim_button.on_click(self.send_pickup_event, tile_model, tile_sprite.pickup_victim_button)

        if self.check_stop_lead(tile_model):
            tile_sprite.stop_lead_button.enable()
            tile_sprite.stop_lead_button.on_click(self.send_stop_lead_event, tile_model, tile_sprite.stop_lead_button)

        elif self.check_lead(tile_model):
            tile_sprite.lead_button.enable()
            tile_sprite.lead_button.on_click(self.send_lead_event, tile_model, tile_sprite.lead_button)


