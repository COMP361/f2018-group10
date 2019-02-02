from typing import Optional

import pygame

from src.core.event_queue import EventQueue


class Scene(pygame.sprite.Group):
    """
    Scene object

    To add new components (Sprite) into the scene, use: Scene.sprite_grp.add( Sprite )
    Scene.sprite_grp returns a Sprite Group so you can just use its functions
    """
    def __init__(self, screen: Optional[pygame.Surface]=None):
        pygame.sprite.Group.__init__(self)
        if screen is not None:
            self.screen = pygame.display.get_surface()
        else:
            self.screen = screen
        self.sprite_grp = pygame.sprite.Group()
        self.info = pygame.display.Info()
        self.enabled = False

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        self.enabled = True

    def update(self, event_queue: EventQueue):
        if self.enabled:
            self.sprite_grp.update(event_queue)

    @property
    def resolution(self):
        return self.info.current_w, self.info.current_h
