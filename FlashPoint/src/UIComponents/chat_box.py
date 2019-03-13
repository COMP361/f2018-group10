import pygame as pg
import math

from src.UIComponents.input_box import InputBox
from src.UIComponents.text import Text
from src.action_events.chat_event import ChatEvent
from src.constants.main_constants import SCREEN_RESOLUTION
from src.UIComponents.rect_label import RectLabel
import src.constants.color as Color
from src.core.event_queue import EventQueue
from src.constants.fonts import TEXT_BOX_FONT_SIZE
from src.core.networking import Networking
from src.models.game_state_model import GameStateModel
from src.models.game_units.player_model import PlayerModel


class ChatBox:
    def __init__(self, current_player: PlayerModel):
        self.chat_history = GameStateModel.instance().chat_history
        self.group = pg.sprite.Group()
        self._init_chatbox()
        self.to_be_renamed = []
        self.current_player = current_player

    def _init_chatbox(self):
        """
        Chat box dimensions
        """
        self.offset = 5
        chat_box_x = 0
        chat_box_y = int(0.6 * SCREEN_RESOLUTION[1])
        chat_box_w = 250
        chat_box_h = SCREEN_RESOLUTION[1] - chat_box_y

        """
        Chat history dimensions
        """
        chat_hist_x = chat_box_x + self.offset
        chat_hist_y = chat_box_y + self.offset
        chat_hist_w = chat_box_w - 2 * self.offset
        chat_hist_h = 0.85 * chat_box_h

        """
        Chat textbox dimensions
        """
        chat_textbox_x = chat_box_x + self.offset
        chat_textbox_y = chat_hist_y + chat_hist_h + self.offset
        chat_textbox_w = chat_hist_w
        chat_textbox_h = chat_box_h - chat_hist_h - 15

        self.chat_box = RectLabel(chat_box_x, chat_box_y, chat_box_w, chat_box_h, background=Color.BLACK)
        self.chat_history_bg = RectLabel(chat_hist_x, chat_hist_y, chat_hist_w, chat_hist_h, background=Color.WHITE)
        self.chat_history_bg.set_transparent_background(True)
        self.chat_textbox = InputBox(x=chat_textbox_x, y=chat_textbox_y, w=chat_textbox_w, h=chat_textbox_h, fsize=20)
        self.group.add([self.chat_box, self.chat_history_bg, self.chat_textbox])

    def update(self, event_queue: EventQueue):

        self.chat_textbox.update(event_queue)
        message = self.chat_textbox.message
        if message:
            chat_event = ChatEvent(self.chat_textbox.message, self.current_player.nickname)

            if self.current_player.ip == GameStateModel.instance().host.ip:
                Networking.get_instance().send_to_all_client(chat_event)
            else:
                Networking.get_instance().client.send(chat_event)

            self.chat_textbox.message = ''

        if GameStateModel.instance():
            self.chat_history = GameStateModel.instance().chat_history
            self._init_message_box()
            self.chat_textbox.rect.w = self.chat_history_bg.rect.w

    def draw(self, screen):
        for message in self.to_be_renamed:
            self.chat_history_bg.image.blit(message.image, message.rect)

        screen.blit(self.chat_history_bg.image, self.chat_history_bg.rect)
        self.chat_textbox.draw(screen)

    def _init_message_box(self):
        message_box_x = self.offset
        message_box_w = self.chat_history_bg.rect.w - 2 * self.offset
        message_box_h = TEXT_BOX_FONT_SIZE + 2
        chat_hist_bottom = self.chat_history_bg.rect.h

        max_messages = math.floor(self.chat_history_bg.rect.h/message_box_h)
        count = 0
        self.to_be_renamed = []

        for old_message in reversed(self.chat_history):
            if count < max_messages:
                message_box_y = chat_hist_bottom - (message_box_h * (count + 1))
                old_message_box = RectLabel(message_box_x, message_box_y, message_box_w, message_box_h,
                                            background=Color.WHITE, txt_pos=Text.Position.LEFT,
                                            txt_obj=Text(font=pg.font.SysFont("Agency FB", TEXT_BOX_FONT_SIZE - 2),
                                                         text=f"{old_message[1]}: {old_message[0]}"))

                self.to_be_renamed.append(old_message_box)
                count += 1
            else:
                break

    @property
    def box(self):
        return self.chat_textbox.rect
