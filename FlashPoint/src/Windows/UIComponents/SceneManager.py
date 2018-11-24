from typing import Optional

import pygame

from src.Windows.UIComponents.Scene import Scene


class SceneManager(object):
    def __init__(self, screen: Optional[pygame.Surface]=None, default_scene: Optional[Scene]=None):
        """
        Scene Manager. Initialize this before the game loop

        :param screen:
        :param default_scene:
        """
        if screen is not None:
            self.screen = pygame.display.get_surface()
        else:
            self.screen = screen
        self._active_scene = default_scene

        if self._active_scene is not None:
            self.switch(self._active_scene)

    def switch(self, scene: Scene):
        if isinstance(self._active_scene, Scene):
            self._active_scene.enabled = False
        self._active_scene = scene

    def draw(self, screen: Optional[pygame.Surface]=None):
        if screen is not None:
            self._active_scene.draw(screen)
        else:
            self._active_scene.draw(self.screen)

    def update(self):
        self._active_scene.update()
