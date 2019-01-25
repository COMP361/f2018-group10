import pygame

from src.models.game_units import GameUnit


class GameUnitSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_of_interest: pygame.sprite.Sprite, game_unit: GameUnit):
        super.__init__()
        self.sprite = sprite_of_interest
        self.game_unit_model = game_unit

    def get_sprite(self):
        return self.sprite
