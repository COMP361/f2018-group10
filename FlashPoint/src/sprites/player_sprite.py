import pygame

from src.models.game_board.tile_model import TileModel
from src.models.game_units.player_model import PlayerModel
from src.models.game_units.victim_model import VictimModel
from src.sprites.grid_sprite import GridSprite

from src.UIComponents.file_importer import FileImporter
from src.constants.state_enums import PlayerStatusEnum, PlayerRoleEnum
from src.observers.player_observer import PlayerObserver
import src.constants.color as Color


class PlayerSprite(pygame.sprite.Sprite, PlayerObserver):
    """Visual representation of a Player and/or his fireman."""

    def player_role_changed(self, role: PlayerRoleEnum):
        pass

    def player_carry_changed(self, carry):
        pass

    def player_leading_victim_changed(self, leading_victim):
        pass

    def __init__(self, current_player: PlayerModel, tile_model: TileModel, grid: GridSprite):
        super().__init__()
        self.grid = grid
        self.tile_model = tile_model
        self.tile_sprite = grid.grid[tile_model.column][tile_model.row]
        self.rect = self.tile_sprite.rect
        self.associated_player = current_player
        self.associated_player.add_observer(self)
        if self.associated_player.role == PlayerRoleEnum.DOGE:
            self.associated_png = 'src/media/all_markers/DogePlayer.png'
        else:
            self.associated_png = self._associate_image(self.associated_player.color)

        self.image = FileImporter.import_image(self.associated_png)

    def _associate_image(self, color: Color):
        return {
            Color.WHITE: "src/media/all_markers/whiteFighter.png",
            Color.BLUE: "src/media/all_markers/blueFighter.png",
            Color.RED: "src/media/all_markers/redFighter.png",
            Color.ORANGE: "src/media/all_markers/orangeFighter.png",
            Color.YELLOW: "src/media/all_markers/yellowFighter.png",
            Color.GREEN: "src/media/all_markers/greenFighter.png",
        }[color]

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

    def player_role_changed(self, role: PlayerRoleEnum):

        if self.associated_player.role == PlayerRoleEnum.DOGE:
            self.associated_png = 'src/media/all_markers/DogePlayer.png'
        else:
            self.associated_png = self._associate_image(self.associated_player.color)

        self.image = FileImporter.import_image(self.associated_png)