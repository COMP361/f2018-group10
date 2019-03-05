import pygame

from src.UIComponents.file_importer import FileImporter
from src.constants.state_enums import PlayerStatusEnum
from src.models.game_state_model import GameStateModel
from src.observers.player_observer import PlayerObserver
import src.constants.color as Color
from src.sprites.tile_sprite import TileSprite


class PlayerSprite(pygame.sprite.Sprite, PlayerObserver):
    """Visual representation of a Player and/or his fireman."""

    def __init__(self, tile_sprite: TileSprite):
        super().__init__()
        self.associated_png = self._associate_image()
        self.image = FileImporter.import_image(self.associated_png)
        self.tile = tile_sprite
        self.rect = self.tile.rect

    @staticmethod
    def _associate_image():
        game_state = GameStateModel.instance()
        curr_player = game_state.players_turn()
        color = curr_player.color

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

    def player_ap_changed(self, updated_ap: int):
        pass

    def player_special_ap_changed(self, updated_ap: int):
        pass

    def player_position_changed(self, x_pos: int, y_pos: int):
        tile_reference = GameStateModel.instance().game_board().tile_at(x_pos, y_pos)
        self.tile = tile_reference
        self.rect = self.tile.rect

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_status_changed(self, status: PlayerStatusEnum):
        pass

    def choose_starting_location(self):
        pass


