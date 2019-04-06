import logging
from src.UIComponents.interactable import Interactable
from src.action_events.turn_events.fire_deck_gun_event import FireDeckGunEvent
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import VehicleOrientationEnum, QuadrantEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.tile_sprite import TileSprite
logger = logging.getLogger("FlashPoint")

class FireDeckGunController(Controller):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)

        if FireDeckGunController._instance:
            raise Exception("Victim Controller is a singleton")

        self._game = GameStateModel.instance()
        self.player = current_player
        self.board: GameBoardModel = self._game.game_board
        self.engine = self.board.engine
        FireDeckGunController._instance = self

    @classmethod
    def instance(cls):
        return cls._instance

    def process_input(self, tile_sprite: TileSprite):

        assoc_model = self.board.get_tile_at(tile_sprite.row, tile_sprite.column)
        button = None
        if self.run_checks(assoc_model):
            button = tile_sprite.fire_deck_gun_button

        if button:
            tile_sprite.fire_deck_gun_button.enable()
            button.on_click(self.send_event_and_close_menu, assoc_model, button)

        else:
            tile_sprite.fire_deck_gun_button.disable()

    def run_checks(self, tile_model: TileModel) -> bool:
        """
                Determines whether or not it is
                possible to perform this event.

                :return: True if it possible to perform
                        this event. False otherwise.
                """
        if not TurnEvent.has_required_AP(self.player.ap, 4):

            return False

        # If the player is not located in the
        # same space as the engine, they cannot
        # fire the deck gun.
        engine_orient = self.engine.orientation
        if engine_orient == VehicleOrientationEnum.HORIZONTAL:
            on_first_spot = self.player.row == self.engine.row and self.player.column == self.engine.column
            on_second_spot = self.player.row == self.engine.row and self.player.column == self.engine.column + 1
            if not on_first_spot and not on_second_spot:

                return False

        elif engine_orient == VehicleOrientationEnum.VERTICAL:
            on_first_spot = self.player.row == self.engine.row and self.player.column == self.engine.column
            on_second_spot = self.player.row == self.engine.row + 1 and self.player.column == self.engine.column
            if not on_first_spot and not on_second_spot:

                return False

        engine_quadrant = self._determine_quadrant(tile_model.row, tile_model.column)
        # If there are players present in the
        # quadrant, the deck gun cannot be fired.
        if self._are_players_in_quadrant(engine_quadrant):

            return False

        return True

    @staticmethod
    def _determine_quadrant(row, column) -> QuadrantEnum:
        """
        Determines the quadrant to which
        the row and column belong to.

        :param row:
        :param column:
        :return: Quadrant in which the row and
                column are located.
        """
        if row < 4 and column < 5:
            return QuadrantEnum.TOP_LEFT
        elif row < 4 and column >= 5:
            return QuadrantEnum.TOP_RIGHT
        elif row >= 4 and column < 5:
            return QuadrantEnum.BOTTOM_LEFT
        else:
            return QuadrantEnum.BOTTOM_RIGHT

    def _are_players_in_quadrant(self, quadrant: QuadrantEnum) -> bool:
        """
        Determines whether there are any players
        in the given quadrant.

        :param quadrant: Quadrant that we are interested in.
        :return: True if there are players in the quadrant,
                False otherwise.
        """

        for player in self._game.players:
            logger.info(f"Player assoc_quadrant: {self._determine_quadrant(player.row, player.column)}")
            logger.info(f"Player row: {player.row}, Player column: {player.column}")
            logger.info(f"Quadrant to compare: {quadrant}")
            if quadrant == self._determine_quadrant(player.row, player.column):
                return True

        return False

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):

        event = FireDeckGunEvent()
        if not self.run_checks(tile_model):
            menu_to_close.disable()
            return

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

        menu_to_close.disable()
