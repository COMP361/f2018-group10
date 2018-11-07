
        self.clock = pygame.time.Clock()
        #self.current_scene = GameBoardScene(self.screen)
        self.current_scene = Login()




    def main(self):
        # Run main game loop
        while True:
            # Lock frame rate at 60 FPS. Should only be called once per loop.
            self.clock.tick(60)
            
            # Check events for if the user closed the window.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            # Clear the screen to black
            self.screen.fill(Color.BLACK.value)

            self.current_scene.update()
            self.current_scene.draw()
            # Flip double buffer
            pygame.display.flip()

           # self.current_scene.draw()


# Should only be used for debugging purposes
if __name__ == '__main__':
    Main().main()

from src.Login import Login
from src.UIComponents.RectButton import RectButton
from src.UIComponents.Text import Text

def main():
    # Initialize pygame modules, get the screen and clock
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
from src.constants.Color import Color
from src.scenes.GameBoardScene import GameBoardScene
    btn_grp = pygame.sprite.Group()
    btn1 = RectButton(10, 10, 60, 40, (255, 255, 255), 0, Text(pygame.font.SysFont('Arial', 12), "Hover me", (0, 255, 0)))
    btn_grp.add(btn1)

    # Run main loop
    while True:
        # Lock frame rate at 60 FPS. Should only be called once per loop.
        clock.tick(60)
class Main(object):
    """Class for running the main game loop and maintaining game state."""
    SCREEN_RESOLUTION = (1280, 700)
    WINDOW_TITLE = "Flash Point"
        # Clear the screen to black and flip the double buffer
        screen.fill((0, 0, 0))
        btn_grp.draw(screen)
        btn_grp.update()
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        #self.current_scene = GameBoardScene(self.screen)
        self.current_scene = Login()




    def main(self):
        # Run main game loop
        while True:
            # Lock frame rate at 60 FPS. Should only be called once per loop.
            self.clock.tick(60)
            
            # Check events for if the user closed the window.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            # Clear the screen to black
            self.screen.fill(Color.BLACK.value)

            self.current_scene.update()
            self.current_scene.draw()
            # Flip double buffer
            pygame.display.flip()

           # self.current_scene.draw()


# Should only be used for debugging purposes
if __name__ == '__main__':
    Main().main()
