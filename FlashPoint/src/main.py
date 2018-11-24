import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.Text import Text
from src.Windows.UIComponents.FileImporter import FileImporter


def click(btn: RectButton):
    print("Holy Francis")
    btn.change_color((76, 255, 255))


def hover(btn: RectButton):
    print("Holy Francis")
    btn.change_color((255, 255, 76))


def off(btn: RectButton):
    btn.change_color((255, 76, 255))


def hover2(btn: RectButton):
    FileImporter.import_audio("media\\recording.mp3")
    pygame.mixer.music.play(-1, 0.5)
    btn.change_bg_image("media\\2lvzph.jpg")


def off2(btn: RectButton):
    btn.change_bg_image("media\\francis.jpg")


def main():
    # Initialize pygame modules, get the screen and clock
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    btn_grp = pygame.sprite.Group()
    btn1 = RectButton(10, 10, 300, 100,
                      (255, 76, 255), 0,
                      Text(pygame.font.SysFont('Arial', 12), "Hover me", (255, 255, 255)))
    btn1.on_click(click, btn1)
    btn1.on_hover(hover, btn1)
    btn1.off_hover(off, btn1)
    btn_grp.add(btn1)
    btn2 = RectButton(500, 50, 200, 280, "D:\\Users\\User\\Pictures\\francis.jpg")
    btn2.on_hover(hover2, btn2)
    btn2.off_hover(off2, btn2)
    btn_grp.add(btn2)

    # Run main loop
    while True:
        # Lock frame rate at 60 FPS. Should only be called once per loop.
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Clear the screen to black and flip the double buffer
        screen.fill((0, 0, 0))
        btn_grp.draw(screen)
        btn_grp.update()
        pygame.display.flip()


if __name__ == '__main__':
    main()
