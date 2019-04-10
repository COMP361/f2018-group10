import logging

import pygame

import src.constants.color as Color

from src.UIComponents.interactable import Interactable
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.action_events.turn_events.fire_deck_gun_event import FireDeckGunEvent
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import VehicleOrientationEnum, QuadrantEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.flashpoint_exceptions import FlippingDiceProblemException
from src.core.networking import Networking
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
from src.sprites.tile_sprite import TileSprite

logger = logging.getLogger("FlashPoint")


class FireDeckGunController(Controller):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)

        if FireDeckGunController._instance:
            raise Exception("Victim Controller is a singleton")

        self._game: GameStateModel = GameStateModel.instance()
        self.player = current_player
        self.board: GameBoardModel = self._game.game_board
        self.engine = self.board.engine
        FireDeckGunController._instance = self
        self.label = None
        self.input1 = None
        self.input2 = None
        self.input3 = None
        self.input4 = None
        self.max_input = 0

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
            if self._current_player.role == PlayerRoleEnum.DRIVER:
                button.on_click(self.driver_menu_popup, assoc_model)
            else:
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
        # Doge cannot fire the deck gun
        if self.player.role == PlayerRoleEnum.DOGE:
            return False

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

        engine_quadrant = self._determine_quadrant(self.engine.row, self.engine.column)
        tile_input_quadrant = self._determine_quadrant(tile_model.row, tile_model.column)
        # If there are players present in the
        # quadrant, the deck gun cannot be fired.
        # tile input gotta be on quadrant adjacent to engine
        if self._are_players_in_quadrant(engine_quadrant) or tile_input_quadrant != engine_quadrant:
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

    @staticmethod
    def _determine_quadrant_player(row, column) -> QuadrantEnum:
        """
        Determines the quadrant to which
        the row and column belong to.

        :param row:
        :param column:
        :return: Quadrant in which the row and
                column are located.
        """
        if 4 > row > 0 and 5 > column > 0:
            return QuadrantEnum.TOP_LEFT
        elif 4 > row > 0 and 5 <= column < 9:
            return QuadrantEnum.TOP_RIGHT
        elif 4 <= row < 7 and 5 > column > 0:
            return QuadrantEnum.BOTTOM_LEFT
        elif 4 <= row < 7 and 5 <= column < 9:
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
            logger.info(f"Player assoc_quadrant: {self._determine_quadrant_player(player.row, player.column)}")
            logger.info(f"Player row: {player.row}, Player column: {player.column}")
            logger.info(f"Quadrant to compare: {quadrant}")
            if quadrant == self._determine_quadrant_player(player.row, player.column):
                return True

        return False

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable,
                                  row: int = -1, column: int = -1):

        event = FireDeckGunEvent(row=row, column=column)

        if not self.run_checks(tile_model):
            menu_to_close.disable()
            return

        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().client.send(event)

        if menu_to_close:
            menu_to_close.disable()

    def _set_target_tile(self, row: int = -1, column: int = -1):
        """
        Set the tile which will be the
        target for the firing of the deck gun.

        :return:
        """
        engine_quadrant = self._determine_quadrant(self.engine.row, self.engine.column)
        if row == -1:
            target_row = GameStateModel.instance().roll_red_dice()
        else:
            target_row = row

        if column == -1:
            target_column = GameStateModel.instance().roll_black_dice()
        else:
            target_column = column

        target_quadrant = self._determine_quadrant(target_row, target_column)
        # If the roll gives a tile in the engine's
        # quadrant, that will become the target tile.
        if target_quadrant == engine_quadrant:
            target_tile = GameStateModel.instance().game_board.get_tile_at(target_row, target_column)
            return target_tile

        else:
            # Flipping the red dice involves
            # subtracting the roll value from 7.
            flipped_row = 7 - target_row
            # Try out the following combinations
            # and see if any of them are in the
            # engine's quadrant:
            # 1. flipping the row, same column
            # 2. same row, flipping the column
            # 3. flipping the row, flipping the column
            new_target_quadrant = self._determine_quadrant(flipped_row, target_column)
            if new_target_quadrant == engine_quadrant:
                target_tile = GameStateModel.instance().game_board.get_tile_at(flipped_row, target_column)
                return target_tile

            flipped_column = GameStateModel.instance().determine_black_dice_opposite_face(target_column)
            new_target_quadrant = self._determine_quadrant(target_row, flipped_column)
            if new_target_quadrant == engine_quadrant:
                target_tile = GameStateModel.instance().game_board.get_tile_at(target_row, flipped_column)
                return target_tile

            new_target_quadrant = self._determine_quadrant(flipped_row, flipped_column)

            if new_target_quadrant == engine_quadrant:
                target_tile = GameStateModel.instance().game_board.get_tile_at(flipped_row, flipped_column)
                return target_tile

        # $$$$$$$$$$$$$$$$$
        # Shouldn't be able to reach this point!!
        # One of the cases above should have worked.
        # $$$$$$$$$$$$$$$$$
        logger.error("Possible issue with dice flipping! Stop!!")
        raise FlippingDiceProblemException()

    def driver_menu_popup(self, tile_model: TileModel):
        decision: int = 0
        targetTile: TileModel = self._set_target_tile()
        red_dice = targetTile.row
        black_dice = targetTile.column
        boardSprite: GameBoard = GameBoard.instance()
        self.label = RectLabel(200, 400, 600, 200, Color.BLACK, 0, Text(pygame.font.SysFont('Agency FB',25), f"Roll: {red_dice}, {black_dice}",Color.GREEN2))
        self.label.change_bg_image('media/GameHud/wood2.png')
        self.label.add_frame('media/GameHud/frame.png')

        self.input1 = RectButton(200, 350, 150, 50, Color.BLACK, 0,
                            Text(pygame.font.SysFont('Agency FB', 25), "Accept Roll", Color.GREEN2))
        self.input1.change_bg_image('media/GameHud/wood2.png')
        self.input1.add_frame('media/GameHud/frame.png')
        self.input2 = RectButton(350, 350, 150, 50, Color.BLACK, 0,
                            Text(pygame.font.SysFont('Agency FB', 25), "Re-Roll Black Dice", Color.GREEN2))
        self.input2.change_bg_image('media/GameHud/wood2.png')
        self.input2.add_frame('media/GameHud/frame.png')
        self.input3 = RectButton(500, 350, 150, 50, Color.BLACK, 0,
                            Text(pygame.font.SysFont('Agency FB', 25), "Re-Roll Red Dice", Color.GREEN2))
        self.input3.change_bg_image('media/GameHud/wood2.png')
        self.input3.add_frame('media/GameHud/frame.png')
        self.input4 = RectButton(650, 350, 150, 50, Color.BLACK, 0,
                            Text(pygame.font.SysFont('Agency FB', 25), "Re-Roll Both Die", Color.GREEN2))
        self.input4.change_bg_image('media/GameHud/wood2.png')
        self.input4.add_frame('media/GameHud/frame.png')

        self.input1.on_click(self.input1_process, tile_model, red_dice, black_dice)
        self.input2.on_click(self.input2_process, tile_model, red_dice, black_dice)
        self.input3.on_click(self.input3_process, tile_model, red_dice, black_dice)
        self.input4.on_click(self.input4_process, tile_model, red_dice, black_dice)
        boardSprite.add(self.label)
        boardSprite.add(self.input1)
        boardSprite.add(self.input2)
        boardSprite.add(self.input3)
        boardSprite.add(self.input4)

    def input1_process(self, tile: TileModel, red_dice: int, black_dice: int):
        self.kill_all()
        self.max_input = 0
        self.send_event_and_close_menu(tile, self.input1, red_dice, black_dice)

    def input2_process(self, tile: TileModel, red_dice: int, black_dice: int):
        self.max_input += 1
        board_sprite: GameBoard = GameBoard.instance()
        self.kill_all()
        new_tile: TileModel = self._set_target_tile(red_dice)
        if self.max_input == 2:
            self.max_input = 0
            self.send_event_and_close_menu(tile, self.input1, new_tile.row, new_tile.column)
        else:

            black_dice = new_tile.column
            self.label = RectLabel(200, 400, 600, 200, Color.BLACK, 0,
                                   Text(pygame.font.SysFont('Agency FB', 25), f"Roll: {red_dice}, {black_dice}",Color.GREEN2))
            self.label.change_bg_image('media/GameHud/wood2.png')
            self.label.add_frame('media/GameHud/frame.png')
            self.input1 = RectButton(200, 350, 150, 50, Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), "Accept Roll", Color.GREEN2))
            self.input1.change_bg_image('media/GameHud/wood2.png')
            self.input1.add_frame('media/GameHud/frame.png')
            self.input3 = RectButton(350, 350, 150, 50, Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), "Re-Roll Red Dice", Color.GREEN2))
            self.input3.change_bg_image('media/GameHud/wood2.png')
            self.input3.add_frame('media/GameHud/frame.png')

            self.input1.on_click(self.input1_process, tile, red_dice, new_tile.column)
            self.input3.on_click(self.input3_process, tile, red_dice, new_tile.column)
            board_sprite.add(self.label)
            board_sprite.add(self.input1)
            board_sprite.add(self.input3)

    def input3_process(self, tile: TileModel, red_dice: int, black_dice: int):
        self.max_input += 1
        board_sprite: GameBoard = GameBoard.instance()
        self.kill_all()
        new_tile: TileModel = self._set_target_tile(-1,black_dice)

        if self.max_input == 2:
            self.max_input = 0
            self.send_event_and_close_menu(tile, self.input1, new_tile.row, new_tile.column)

        else:
            red_dice = new_tile.row
            self.label = RectLabel(200, 400, 600, 200, Color.BLACK, 0,
                                   Text(pygame.font.SysFont('Agency FB', 25), f"Roll: {red_dice}, {black_dice}", Color.GREEN2))
            self.label.change_bg_image('media/GameHud/wood2.png')
            self.label.add_frame('media/GameHud/frame.png')
            self.input1 = RectButton(200, 350, 150, 50, Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), "Accept Roll", Color.GREEN2))
            self.input1.change_bg_image('media/GameHud/wood2.png')
            self.input1.add_frame('media/GameHud/frame.png')
            self.input2 = RectButton(350, 350, 150, 50, Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), "Re-Roll Black Dice", Color.GREEN2))
            self.input2.change_bg_image('media/GameHud/wood2.png')
            self.input2.add_frame('media/GameHud/frame.png')

            self.input1.on_click(self.input1_process, tile, new_tile.row, black_dice)
            self.input2.on_click(self.input2_process, tile, new_tile.row, black_dice)
            board_sprite.add(self.label)
            board_sprite.add(self.input1)
            board_sprite.add(self.input2)

    def input4_process(self, tile: TileModel, red_dice: int, black_dice: int):
        self.kill_all()
        new_tile: TileModel = self._set_target_tile()
        self.send_event_and_close_menu(tile, self.input1, new_tile.row, new_tile.column)

    def kill_all(self):
        self.input1.kill()
        self.input2.kill()
        self.input3.kill()
        self.input4.kill()
        self.label.kill()