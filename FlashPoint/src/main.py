import sys

# If PyCharm is issuing warnings on pygame methods, suppress it. it's a bug with PyCharm
import pygame

from src.Login import Login
from src.constants.Color import Color
from src.scenes.GameBoardScene import GameBoardScene


from src.Windows.UIComponents.RectButton import RectButton
from src.Windows.UIComponents.Text import Text


class Main(object):
    """Class for running the main game loop and maintaining game state."""
    SCREEN_RESOLUTION = (1280, 700)
    WINDOW_TITLE = "Flash Point"

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(Main.WINDOW_TITLE)
        self.screen = pygame.display.set_mode(Main.SCREEN_RESOLUTION)
        self.clock = pygame.time.Clock()
        #self.current_scene = GameBoardScene(self.screen)
        self.current_scene = Login(self.screen)
   
        
 


    def main(self):
        # Initialize pygame modules, get the screen and clock

        
       

        # btn_grp = pygame.sprite.Group()
        # btn1 = RectButton(10, 10, 60, 40, (255, 255, 255), 0, Text(pygame.font.SysFont('Arial', 12), "Hover msssse", (0, 255, 0)))
        # btn_grp.add(btn1)

        # Run main loop
        while True:
            # Lock frame rate at 60 FPS. Should only be called once per loop.
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Clear the screen to black and flip the double buffer
            self.screen.fill(Color.BLACK.value)
            # btn_grp.draw(self.screen)
            # btn_grp.update()
            self.current_scene.draw()
            self.current_scene.update()


            pygame.display.flip()


if __name__ == '__main__':
    Main().main()
