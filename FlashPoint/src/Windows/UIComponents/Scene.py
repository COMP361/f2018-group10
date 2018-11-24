from typing import Optional

import pygame


class Scene(pygame.sprite.Sprite):
    """
    Scene object

    To add new components (Sprite) into the scene, use: Scene.sprite_grp.add( Sprite )
    Scene.sprite_grp returns a Sprite Group so you can just use its functions
    """
    def __init__(self, screen: Optional[pygame.Surface]=None):
        pygame.sprite.Sprite.__init__(self)
        if screen is not None:
            self.screen = pygame.display.get_surface()
        else:
            self.screen = screen
        self.sprite_grp = pygame.sprite.Group()
        self.info = pygame.display.Info()
        self.enabled = False

    def draw(self):
        self.sprite_grp.draw(self.screen)
        self.enabled = True

    def update(self):
        if self.enabled:
            self.sprite_grp.update()

    def add(self, *sprites):
        self.sprite_grp.add(*sprites)

    def remove(self, *sprites):
        self.sprite_grp.remove(*sprites)

    @property
    def resolution(self):
        return self.info.current_w, self.info.current_h
