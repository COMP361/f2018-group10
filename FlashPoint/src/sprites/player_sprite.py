import pygame
from src.models.game_board.tile_model import TileModel
from src.sprites.grid_sprite import GridSprite

from src.UIComponents.file_importer import FileImporter
from src.constants.state_enums import PlayerStatusEnum
from src.models.game_state_model import GameStateModel
from src.observers.player_observer import PlayerObserver
import src.constants.color as Color


class PlayerSprite(pygame.sprite.Sprite, PlayerObserver):
    """Visual representation of a Player and/or his fireman."""

    def __init__(self, tile_model: TileModel, grid: GridSprite):
        super().__init__()
        self.grid = grid
        self.tile_model = tile_model
        self.tile_sprite = grid.grid[tile_model.column][tile_model.row]
        self.rect = self.tile_sprite.rect
        self.associated_player = GameStateModel.instance().players_turn
        self.associated_player.add_observer(self)
        self.associated_png = self._associate_image()
        self.image = FileImporter.import_image(self.associated_png)

    def _associate_image(self):

        color = self.associated_player.color

        if color is Color.BLUE:
            return "media/all_markers/blueFighter.png"
        elif color is Color.GREEN:
            return "media/all_markers/greenFighter.png"
        elif color is Color.ORANGE:
            return "media/all_markers/orangeFighter.png"
        elif color is Color.WHITE:
            return "media/all_markers/whiteFighter.png"
        elif color is Color.YELLOW:
            return "media/all_markers/yellowFighter.png"
        elif color is Color.RED:
            return "media/all_markers/redFighter.png"

    def player_ap_changed(self, updated_ap: int):
        pass

    def player_special_ap_changed(self, updated_ap: int):
        pass

    def player_position_changed(self, row: int, column: int):
        self.tile_sprite = self.grid.grid[column][row]
        self.rect = self.tile_sprite.rect

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def choose_starting_location(self):
        pass

