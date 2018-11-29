import pygame as pg

from src.Windows.UIComponents.InputBox import InputBox
from src.Windows.UIComponents.Text import Text
from src.constants.MainConstants import SCREEN_RESOLUTION
from src.Windows.UIComponents.RectLabel import RectLabel
import src.constants.Color as Color
from src.core.EventQueue import EventQueue
from src.constants.Fonts import TEXT_BOX_FONT_SIZE


class ChatBox:

    def __init__(self):
        self.messages = []
        self.group = pg.sprite.Group()
        self._init_chatbox()

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
        self.chat_history_bg = RectLabel(chat_hist_x, chat_hist_y, chat_hist_w, chat_hist_h, background=Color.GREY)
        self.chat_textbox = InputBox(x=chat_textbox_x, y=chat_textbox_y, w=chat_textbox_w, h=chat_textbox_h)
        self.chat_history = []
        self.group.add([self.chat_box, self.chat_history_bg, self.chat_textbox])

    def update(self, event_queue: EventQueue):
        self.chat_textbox.update(event_queue)
        message = self.chat_textbox.message
        if message:
            self.messages.append(self.chat_textbox.message)
            self.chat_textbox.message = ''

            self._init_message_box(message)

    def draw(self, screen):
        #self.group.draw(screen)
        for message in self.chat_history:
            self.chat_history_bg.image.blit(message.image, message.rect)

        screen.blit(self.chat_history_bg.image, self.chat_history_bg.rect)
        self.chat_textbox.draw(screen)

    def _init_message_box(self, message: str):
        message_box_x = self.offset
        message_box_y = self.chat_history_bg.rect.h - TEXT_BOX_FONT_SIZE - 2
        message_box_w = self.chat_history_bg.rect.w - 2 * self.offset
        message_box_h = TEXT_BOX_FONT_SIZE + 2
        message_box = RectLabel(message_box_x, message_box_y, message_box_w, message_box_h, background=Color.GREY,
                                txt_obj=Text(font=pg.font.SysFont("Arial", TEXT_BOX_FONT_SIZE - 2), text=message),
                                txt_pos=Text.Position.RIGHT)
        self.chat_history.append(message_box)


# def main():
#     clock = pg.time.Clock()
#     input_box1 = InputBox(100, 100, 140, 32)
#     input_box2 = InputBox(100, 300, 140, 32)
#     input_boxes = [input_box1, input_box2]
#     done = False
#
#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             for box in input_boxes:
#                 box.handle_event(event)
#
#         for box in input_boxes:
#             box.update()
#
#         screen.fill((30, 30, 30))
#         for box in input_boxes:
#             box.draw(screen)
#
#         pg.display.flip()
#         clock.tick(30)


# if __name__ == '__main__':
#     main()
#     pg.quit()