import pygame
import src.constants.color as Color
from src.models.game_units.player_model import PlayerModel
from src.constants.state_enums import GameStateEnum
from src.core.event_queue import EventQueue
from src.models.game_state_model import GameStateModel
from src.observers.game_state_observer import GameStateObserver


class InGameStates(pygame.sprite.Sprite, GameStateObserver):

    def notify_game_state(self, game_state: GameStateEnum):
        pass

    def player_command(self, source: PlayerModel, target: PlayerModel):
        pass

    def __init__(self, x: int, y: int, current_damage: int, victims_dead: int, victims_saved: int):
        super().__init__()
        GameStateModel.instance().add_observer(self)
        self.image = pygame.Surface([880, 50])
        self.font = pygame.font.SysFont('Agency FB', 35)

        self.bg = pygame.image.load('media/GameHud/wood2.png')
        self.bg = pygame.transform.scale(self.bg, (880, 50))
        self.frame = pygame.image.load('media/GameHud/frame.png')
        self.frame = pygame.transform.scale(self.frame, (880, 50))

        self.damage_str = f"Damage: {current_damage}/24"
        self.victims_dead_str = f"Victims Lost: {victims_dead}/4"
        self.victims_saved_str = f"Victims Saved: {victims_saved}/7"
        self.damage = self.font.render(self.damage_str, True, Color.GREEN2)
        self.victims_dead = self.font.render(self.victims_dead_str, True, Color.GREEN2)
        self.victims_saved = self.font.render(self.victims_saved_str, True, Color.GREEN2)

        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.damage_rect = self.damage.get_rect()
        self.damage_rect.move_ip(55, 5)
        self.victims_dead_rect = self.victims_dead.get_rect()
        self.victims_dead_rect.move_ip(630, 5)
        self.victims_saved_rect = self.victims_saved.get_rect()
        self.victims_saved_rect.move_ip(330, 5)

    def update(self, event_queue: EventQueue):
        self.image.blit(self.bg, self.image.get_rect())
        self.image.blit(self.frame, self.image.get_rect())
        self.image.blit(self.damage, self.damage_rect)
        self.image.blit(self.victims_saved, self.victims_saved_rect)
        self.image.blit(self.victims_dead, self.victims_dead_rect)

    def damage_changed(self, new_damage: int):
        self.damage_str = f"Damage: {new_damage}/24"
        self.damage = self.font.render(self.damage_str, True, Color.GREEN2)

    def saved_victims(self, victims_saved: int):
        self.victims_saved_str = f"Victims Saved: {victims_saved}/7"
        self.victims_saved = self.font.render(self.victims_saved_str, True, Color.GREEN2)

    def dead_victims(self, victims_dead: int):
        self.victims_dead_str = f"Victims Lost: {victims_dead}/4"
        self.victims_dead = self.font.render(self.victims_dead_str, True, Color.GREEN2)

    def notify_player_index(self, player_index: int):
        pass

    def player_added(self, player: PlayerModel):
        pass

    def player_removed(self, player: PlayerModel):
        pass
