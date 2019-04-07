import pygame

import src.constants.color as Color

from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.action_events.dodge_reply_event import DodgeReplyEvent
from src.core.event_queue import EventQueue
from src.core.networking import Networking


class DodgePrompt(object):
    """Prompt for the player deciding whether to dodge or not."""

    def __init__(self):
        self.accept_button = RectButton(550-75, 310, 75, 50, Color.ORANGE, 0,
                                        Text(pygame.font.SysFont('Arial', 20), "Accept", Color.WHITE))
        self.deny_button = RectButton(550+200, 310, 75, 50, Color.ORANGE, 0,
                                      Text(pygame.font.SysFont('Arial', 20), "Deny", Color.WHITE))
        self.accept_button.on_click(self._accept_on_click)
        self.deny_button.on_click(self._deny_on_click)

        self.background = RectLabel(550, 300, 200, 75, Color.GREY, 0,
                                    Text(pygame.font.SysFont('Arial', 20), "Dodge?", Color.WHITE))

        self.enabled = False

    def _send_reply_event(self, reply: bool):
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(DodgeReplyEvent(reply))
        else:
            Networking.get_instance().send_to_server(DodgeReplyEvent(reply))

    def _deny_on_click(self):
        self.enabled = False
        self._send_reply_event(False)

    def _accept_on_click(self):
        self.enabled = False
        self._send_reply_event(True)

    def update(self, event_queue: EventQueue):
        self.background.update(event_queue)
        self.accept_button.update(event_queue)
        self.deny_button.update(event_queue)

    def draw(self, screen):
        if self.enabled:
            self.background.draw(screen)
            self.accept_button.draw(screen)
            self.deny_button.draw(screen)
