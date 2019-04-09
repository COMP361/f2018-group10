import logging

import pygame
import src.constants.color as Color
from src.UIComponents.interactable import Interactable
from src.UIComponents.rect_button import RectButton
from src.UIComponents.text import Text
from src.action_events.turn_events.crew_change_event import CrewChangeEvent
from src.action_events.turn_events.turn_event import TurnEvent
from src.constants.state_enums import GameKindEnum, PlayerRoleEnum
from src.controllers.controller import Controller
from src.core.networking import Networking
from src.models.game_board.game_board_model import GameBoardModel
from src.models.game_board.tile_model import TileModel
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel
from src.sprites.game_board import GameBoard
from src.sprites.tile_sprite import TileSprite

logger = logging.getLogger("FlashPoint")


class CrewChangeController(Controller):
    _instance = None

    def __init__(self, current_player: PlayerModel):
        super().__init__(current_player)
        self.game: GameStateModel = GameStateModel.instance()
        self.board: GameBoardModel = self.game.game_board
        self._current_player = current_player
        if CrewChangeController.instance():
            raise Exception("CrewChangeController is not a singleton!")
        if GameStateModel.instance().rules != GameKindEnum.EXPERIENCED:
            raise Exception("CrewChangeController should not exist in Family Mode!")
        CrewChangeController._instance = self
        self.generalist = None
        self.cafs = None
        self.doge = None
        self.driver = None
        self.hazmat = None
        self.imaging = None
        self.paramedic = None
        self.rescue = None
        self.veteran = None
        self.captain = None
        self.button_back = None
        self.role_to_change: PlayerRoleEnum = None

    @classmethod
    def instance(cls):
        return cls._instance

    def process_input(self, tile_sprite: TileSprite):

        assoc_model = self.board.get_tile_at(tile_sprite.row, tile_sprite.column)

        if self.run_checks(assoc_model):
            tile_sprite.change_crew_button.enable()
            tile_sprite.change_crew_button.on_click(self.display_menu, assoc_model)

    def run_checks(self, tile_model: TileModel) -> bool:

        valid_to_do_event = TurnEvent.has_required_AP(self._current_player.ap, 2)

        if not valid_to_do_event:
            logger.info("Player does not have enough AP to change crews.")
            return False

        engine_spots = self.board.engine_spots
        player_coord = self._current_player.row, self._current_player.column
        valid_to_do_event = False

        for spots in engine_spots:
            if ((player_coord[0] == spots[0].row and player_coord[1] == spots[0].column) or
                (player_coord[0] == spots[1].row and player_coord[1] == spots[1].column)) and \
                    ((tile_model.row == spots[0].row and tile_model.column == spots[0].column) or
                     (tile_model.row == spots[1].row and tile_model.column == spots[1].column)):
                valid_to_do_event = True

        if not valid_to_do_event:
            logger.info("Player is not place on an engine spot! Cannot change crews.")
            return False

        if self._current_player.has_moved:
            logger.info("Player has already made an action, cannot change crews.")
            return False

        logger.info("Crew Changes Checks Have Passed")
        return True

    def send_event_and_close_menu(self, tile_model: TileModel, menu_to_close: Interactable):

        self.kill_all()
        if not self.run_checks(tile_model):
            return

        event = CrewChangeEvent(self.role_to_change, self.game.players_turn_index)
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(event)
        else:
            Networking.get_instance().send_to_server(event)

    def display_menu(self, tile: TileModel):
        board_sprite: GameBoard = GameBoard.instance()
        players = self.game.players
        offset = 200
        self.button_back = RectButton(250, 100, 100, 50, Color.BLACK, 0,
                                      Text(pygame.font.SysFont('Agency FB', 25), "Back", Color.WHITE))
        board_sprite.add(self.button_back)
        self.button_back.on_click(self.kill_all)

        if not any([player.role == PlayerRoleEnum.DRIVER for player in players]):
            self.driver = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), "Driver/Operator", Color.WHITE))
            self.driver.on_click(self.decide_role, tile, self.driver, PlayerRoleEnum.DRIVER)
            board_sprite.add(self.driver)
            offset += 50

        if not any([player.role == PlayerRoleEnum.VETERAN for player in players]):
            self.veteran = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                      Text(pygame.font.SysFont('Agency FB', 25), "Veteran", Color.WHITE))
            self.veteran.on_click(self.decide_role, tile, self.veteran, PlayerRoleEnum.VETERAN)
            board_sprite.add(self.veteran)
            offset += 50

        if not any([player.role == PlayerRoleEnum.DOGE for player in players]):
            logger.info("Doge is instantiated")
            self.doge = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                   Text(pygame.font.SysFont('Agency FB', 25), "Doge", Color.WHITE))
            self.doge.on_click(self.decide_role, tile, self.doge, PlayerRoleEnum.DOGE)
            board_sprite.add(self.doge)
            offset += 50

        if not any([player.role == PlayerRoleEnum.RESCUE for player in players]):
            self.rescue = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                     Text(pygame.font.SysFont('Agency FB', 25), "Rescue", Color.WHITE))
            self.rescue.on_click(self.decide_role, tile, self.rescue, PlayerRoleEnum.RESCUE)
            board_sprite.add(self.rescue)
            offset += 50

        if not any([player.role == PlayerRoleEnum.PARAMEDIC for player in players]):
            self.paramedic = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                        Text(pygame.font.SysFont('Agency FB', 25), "Paramedic", Color.WHITE))
            self.paramedic.on_click(self.decide_role, tile, self.paramedic, PlayerRoleEnum.PARAMEDIC)
            board_sprite.add(self.paramedic)
            offset += 50

        if not any([player.role == PlayerRoleEnum.IMAGING for player in players]):
            self.imaging = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                      Text(pygame.font.SysFont('Agency FB', 25), "Imaging Technician", Color.WHITE))
            self.imaging.on_click(self.decide_role, tile, self.driver, PlayerRoleEnum.IMAGING)
            board_sprite.add(self.imaging)
            offset += 50

        if not any([player.role == PlayerRoleEnum.CAFS for player in players]):
            self.cafs = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                   Text(pygame.font.SysFont('Agency FB', 25), "CAFS Firefighter", Color.WHITE))
            self.cafs.on_click(self.decide_role, tile, self.driver, PlayerRoleEnum.CAFS)
            board_sprite.add(self.cafs)
            offset += 50

        if not any([player.role == PlayerRoleEnum.GENERALIST for player in players]):
            self.generalist = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                         Text(pygame.font.SysFont('Agency FB', 25), "Generalist", Color.WHITE))
            self.generalist.on_click(self.decide_role, tile, self.driver, PlayerRoleEnum.GENERALIST)
            board_sprite.add(self.generalist)
            offset += 50

        if not any([player.role == PlayerRoleEnum.CAPTAIN for player in players]):
            self.captain = RectButton(300, 0 + offset, 200, 50, Color.BLACK, 0,
                                      Text(pygame.font.SysFont('Agency FB', 25), "Captain", Color.WHITE))
            self.captain.on_click(self.decide_role, tile, self.driver, PlayerRoleEnum.CAPTAIN)
            board_sprite.add(self.captain)
            offset += 50

    def decide_role(self, tile: TileModel, button, role: PlayerRoleEnum):
        tile_sprite: TileSprite = GameBoard.instance().grid.grid[tile.column][tile.row]
        tile_sprite.disable_all()
        self.role_to_change = role

        self.send_event_and_close_menu(tile, button)

    def kill_all(self):
        if self.button_back:
            self.button_back.kill()
        if self.generalist:
            self.generalist.kill()
        if self.cafs:
            self.cafs.kill()
        if self.doge:
            self.doge.kill()
        if self.driver:
            self.driver.kill()
        if self.hazmat:
            self.hazmat.kill()
        if self.imaging:
            self.imaging.kill()
        if self.paramedic:
            self.paramedic.kill()
        if self.rescue:
            self.rescue.kill()
        if self.veteran:
            self.veteran.kill()
        if self.captain:
            self.captain.kill()
