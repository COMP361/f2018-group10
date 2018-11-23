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
        self._scene_grp = pygame.sprite.Group()
        self._active_scene = default_scene

        if self._active_scene is not None:
            self.switch(self._active_scene)

    def switch(self, scene: Scene):
        if isinstance(self._active_scene, Scene):
            self._active_scene.enabled = False
        self._scene_grp.empty()
        self._scene_grp.add(scene)
        self._scene_grp.draw(self.screen)

    def update(self):
        self._scene_grp.update()
