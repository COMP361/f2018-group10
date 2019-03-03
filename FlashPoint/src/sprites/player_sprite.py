import pygame
from constants.state_enums import PlayerStatusEnum
from src.observers.player_observer import PlayerObserver


class PlayerSprite(pygame.sprite.Sprite, PlayerObserver):
    """Visual representation of a Player and/or his fireman."""

    def __init__(self):
        super().__init__()

    def player_ap_changed(self, updated_ap: int):
        pass

    def player_special_ap_changed(self, updated_ap: int):
        pass

    def player_position_changed(self, x_pos: int, y_pos: int):
        pass

    def player_wins_changed(self, wins: int):
        pass

    def player_losses_changed(self, losses: int):
        pass

    def player_status_changed(self, status: PlayerStatusEnum):
        pass
