from typing import Optional

import pygame

from src.Windows.UIComponents.Scene import Scene


class SceneManager(object):
    def __init__(self, screen: Optional[pygame.Surface]=None):
        if screen is not None:
            self.screen = pygame.display.get_surface()
        else:
            self.screen = screen
        self._scene_grp = pygame.sprite.Group()

    def switch(self, scene: Scene):
        self._scene_grp.empty()
        self._scene_grp.add(scene)
        self._scene_grp.draw(self.screen)

    def update(self):
        self._scene_grp.update()
