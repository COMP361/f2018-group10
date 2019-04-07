from typing import Tuple

import pygame

import src.constants.color as Color
from src.action_events.permission_reply_event import PermissionReplyEvent
from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.models.game_units.player_model import PlayerModel
from src.core.event_queue import EventQueue
from src.core.networking import Networking


class PermissionPrompt(object):
    """Prompt for the player deciding whether to allow to be commanded or not."""

    def __init__(self):
        self.accept_button = RectButton(550-75, 310, 75, 50, Color.ORANGE, 0,
                                        Text(pygame.font.SysFont('Arial', 20), "Accept", Color.WHITE))
        self.deny_button = RectButton(550+200, 310, 75, 50, Color.ORANGE, 0,
                                      Text(pygame.font.SysFont('Arial', 20), "Deny", Color.WHITE))
        self.accept_button.on_click(self._accept_on_click)
        self.deny_button.on_click(self._deny_on_click)

        self._source = None
        self._target = None
        self.background = RectLabel(550, 300, 200, 75, Color.GREY, 0,
                                    Text(pygame.font.SysFont('Arial', 20), "Permission?", Color.WHITE))

        self._enabled = False

    def _send_reply_event(self, reply: bool):
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(PermissionReplyEvent(reply, self._source, self._target))
        else:
            Networking.get_instance().send_to_server(PermissionReplyEvent(reply, self._source, self._target))

    def _deny_on_click(self):
        self.enabled = False
        self._send_reply_event(False)

    def _accept_on_click(self):
        self.enabled = False
        self._send_reply_event(True)

    def update(self, event_queue: EventQueue):
        if self._enabled:
            self.background.update(event_queue)
            self.accept_button.update(event_queue)
            self.deny_button.update(event_queue)

    def draw(self, screen):
        if self._enabled:
            self.background.draw(screen)
            self.accept_button.draw(screen)
            self.deny_button.draw(screen)

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, enable: bool):
        self._enabled = enable

    @property
    def command(self) -> Tuple[PlayerModel, PlayerModel]:
        return self._source, self._target

    @command.setter
    def command(self, command: Tuple[PlayerModel, PlayerModel]):
        self._source = command[0]
        self._target = command[1]
        self.background.change_text(Text(pygame.font.SysFont('Arial', 20),
                                         f"{self._source.nickname} wants to command you", Color.WHITE))
