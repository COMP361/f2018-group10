from typing import Tuple

import pygame

import src.constants.color as Color
from src.core.event_queue import EventQueue
from src.models.game_units.player_model import PlayerModel
from src.UIComponents.text import Text
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.rect_button import RectButton


class CommandNotification(object):
    """Displays the command status to the targeted players (source and target)"""

    def __init__(self):
        self._source = None
        self._target = None
        self._notification = RectLabel(500, 0, 350, 75, Color.GREY, 0,
                                       Text(pygame.font.SysFont('Agency FB', 30), f"Commanding: None",
                                            Color.ORANGE))
        self._wait_command = RectLabel(500, 400, 300, 50, Color.GREY, 0,
                                       Text(pygame.font.SysFont('Agency FB', 30), f"Commanded by: None",
                                            Color.ORANGE))
        self._end_command_btn = RectButton(1130, 500, 150, 50, background=Color.ORANGE,
                                           txt_obj=Text(pygame.font.SysFont('Arial', 23), "END COMMAND", Color.GREEN2))
        self._is_source = False
        self._is_target = False

    @property
    def command(self) -> Tuple[PlayerModel, PlayerModel]:
        return self._source, self._target

    @command.setter
    def command(self, command: Tuple[PlayerModel, PlayerModel]):
        (self._source, self._target) = command
        self._notification.change_text(Text(pygame.font.SysFont('Agency FB', 30),
                                            f"Commanding: {self._target.nickname}", Color.ORANGE))
        self._wait_command.change_text(Text(pygame.font.SysFont('Agency FB', 30),
                                            f"Commanded by: {self._source.nickname}", Color.ORANGE))

    @property
    def is_source(self) -> bool:
        return self._is_source

    @is_source.setter
    def is_source(self, source: bool):
        self._is_source = source

    @property
    def is_target(self) -> bool:
        return self._is_target

    @is_target.setter
    def is_target(self, target: bool):
        self._is_target = target

    def update(self, event_queue: EventQueue):
        if self.is_source:
            self._notification.update(event_queue)
            self._end_command_btn.update(event_queue)
        elif self.is_target:
            self._wait_command.update(event_queue)

    def draw(self, screen):
        if self.is_source:
            self._notification.draw(screen)
            self._end_command_btn.draw(screen)
        elif self.is_target:
            self._wait_command.draw(screen)