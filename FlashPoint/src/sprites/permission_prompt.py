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
from src.constants.media_constants import WOOD, FRAME


class PermissionPrompt(object):
    """Prompt for the player deciding whether to allow to be commanded or not."""

    def __init__(self):
        self.accept_button = RectButton(500-75, 310, 75, 50, Color.ORANGE, 0,
                                        Text(pygame.font.SysFont('Agency FB', 20), "Accept", Color.GREEN2))
        self.accept_button.change_bg_image(WOOD)
        self.accept_button.add_frame(FRAME)
        self.deny_button = RectButton(500+300, 310, 75, 50, Color.ORANGE, 0,
                                      Text(pygame.font.SysFont('Agency FB', 20), "Deny", Color.GREEN2))
        self.deny_button.change_bg_image(WOOD)
        self.deny_button.add_frame(FRAME)
        self.accept_button.on_click(self._accept_on_click)
        self.deny_button.on_click(self._deny_on_click)

        self._source = None
        self._target = None
        self.background = RectLabel(500, 300, 300, 75, Color.GREY, 0,
                                    Text(pygame.font.SysFont('Agency FB', 20), "Permission?", Color.GREEN2))
        self.background.change_bg_image(WOOD)
        self.background.add_frame(FRAME)

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
        self.background.change_text(Text(pygame.font.SysFont('Agency FB', 20),
                                         f"{self._source.nickname} wants to command you", Color.GREEN2))
        self.background.change_bg_image(WOOD)
        self.background.add_frame(FRAME)
