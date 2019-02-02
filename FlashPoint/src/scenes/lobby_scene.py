import pygame

import src.constants.color as Color

from src.UIComponents.rect_button import RectButton
from src.UIComponents.rect_label import RectLabel
from src.UIComponents.text import Text
from src.UIComponents.chat_box import ChatBox
from src.core.networking import Networking


class LobbyScene(object):
    def __init__(self, screen, game_type: bool):
        self.resolution = (1280, 700)
        self.sprite_grp = pygame.sprite.Group()
        self._init_background()
        self._init_text_box(100, 314, 100, 32, "Player1", Color.BLUE)
        self._init_text_box(400, 239, 100, 32, "Player2", Color.BLUE)
        self._init_text_box(780, 239, 100, 32, "Player3", Color.BLUE)
        self._init_text_box(1080, 314, 100, 32, "Player4", Color.BLUE)
        self._init_text_box(565, 575, 150, 32, "You", Color.BLUE)
        self._init_text_box(100, 164, 100, 150, "", Color.GREY)
        self._init_text_box(400, 89, 100, 150, "", Color.GREY)
        self._init_text_box(780, 89, 100, 150, "", Color.GREY)
        self._init_text_box(1080, 164, 100, 150, "", Color.GREY)
        self._init_text_box(565, 375, 150, 200, "", Color.GREY)
        self._init_ip_addr()
        self.chat_box = ChatBox()
        self.is_experienced = game_type

        if game_type:
            self._init_selec_char(1050, 475, "Select Character", Color.STANDARDBTN, Color.BLACK)

        self._init_btn_back(20, 20, "Exit", Color.STANDARDBTN, Color.BLACK)
        self._init_ready(1050, 575, "Ready", Color.STANDARDBTN, Color.BLACK)

    def _init_background(self):
        box_size = (self.resolution[0], self.resolution[1])
        background_box = RectLabel(0, 0, box_size[0], box_size[1], "media/flashpoint_background.png")
        self.sprite_grp.add(background_box)

    def create_butn_img(self, x, y, width, height, path):
        box_size = (width, height)
        self.this_img = RectButton(x, y, box_size[0], box_size[1], path)

        self.sprite_grp.add(self.this_img)

    def _init_text_box(self, x_pos, y_pos, w, h, text, color):
        box_size = (w, h)

        user_box = RectLabel(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                             Text(pygame.font.SysFont('Arial', 20), text, (0, 255, 0, 0)))
        self.sprite_grp.add(user_box)

    def _init_selec_char(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonSelChar = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonSelChar)

    def _init_ready(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonReady = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonReady)

    def _init_btn_back(self, x_pos: int, y_pos: int, text: str, color: Color, color_text: Color):
        box_size = (130, 48)
        self.buttonBack = RectButton(x_pos, y_pos, box_size[0], box_size[1], color, 0,
                                     Text(pygame.font.SysFont('Arial', 20), text, color_text))
        self.sprite_grp.add(self.buttonBack)

    def _init_ip_addr(self):
        if Networking.get_instance().is_host:
            ip_addr = f"Your IP address: {Networking.get_instance().get_ip()}"
            label_width = 400
            label_left = (pygame.display.get_surface().get_size()[0]/2) - (label_width/2)
            ip_addr_label = RectLabel(label_left, 20, label_width, 50, (255, 255, 255),
                                      txt_obj=(Text(pygame.font.SysFont('Arial', 24), ip_addr)))
            ip_addr_label.set_transparent_background(True)
            self.sprite_grp.add(ip_addr_label)

    def draw(self, screen):
        self.sprite_grp.draw(screen)
        self.chat_box.draw(screen)

    def update(self, event_queue):
        self.sprite_grp.update(event_queue)
        self.chat_box.update(event_queue)
