import pygame

import src.constants.color as Color

from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.action_events.dodge_reply_event import DodgeReplyEvent
from src.core.event_queue import EventQueue
from src.core.networking import Networking
from src.constants.media_constants import WOOD, FRAME


class DodgePrompt(object):
    """Prompt for the player deciding whether to dodge or not."""

    def __init__(self):

        self.bg = pygame.image.load(WOOD)
        self.frame = pygame.image.load(FRAME)
        self.frame = pygame.transform.scale(self.frame, (400, 100))

        self.accept_button = RectButton(550-75, 310, 75, 50, Color.ORANGE, 0,
                                        Text(pygame.font.SysFont('Agency FB', 25), "Accept", Color.GREEN2))
        self.accept_button.change_bg_image(WOOD)
        self.accept_button.add_frame(FRAME)

        self.deny_button = RectButton(550+200, 310, 75, 50, Color.ORANGE, 0,
                                      Text(pygame.font.SysFont('Agency FB', 25), "Deny", Color.GREEN2))
        self.deny_button.change_bg_image(WOOD)
        self.deny_button.add_frame(FRAME)
        self.accept_button.on_click(self._accept_on_click)
        self.deny_button.on_click(self._deny_on_click)

        self.background = RectLabel(550, 300, 200, 75, Color.GREY, 0,
                                    Text(pygame.font.SysFont('Agency FB', 25), "Dodge?", Color.GREEN2))
        self.background.change_bg_image(WOOD)
        self.background.add_frame(FRAME)
        self.enabled = False
        self.disable()

    def enable(self):
        self.deny_button.enable()
        self.accept_button.enable()
        self.accept_button.on_click(self._accept_on_click)
        self.deny_button.on_click(self._deny_on_click)
        self.enabled = True

    def disable(self):
        self.deny_button.disable()
        self.accept_button.disable()
        self.accept_button.on_click(None)
        self.deny_button.on_click(None)
        self.enabled = False

    def _send_reply_event(self, reply: bool):
        if Networking.get_instance().is_host:
            Networking.get_instance().send_to_all_client(DodgeReplyEvent(reply))
        else:
            Networking.get_instance().send_to_server(DodgeReplyEvent(reply))

    def _deny_on_click(self):
        self.disable()
        self._send_reply_event(False)

    def _accept_on_click(self):
        self.disable()
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
