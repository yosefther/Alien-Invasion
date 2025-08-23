import sys 
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("python game aliens")
        self.settings = Settings()
        Set = self.settings
        self.screen = pygame.display.set_mode((Set.screen_width,Set.screen_height)) # object we assigned to self.screen is called a surface in pygame
        self.clock = pygame.time.Clock()
        self.bg_color = (Set.bg_color)
        self.ship = Ship(self)
 
    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  sys.exit()

    def _update_screen(self):
            self.screen.fill(self.bg_color)
            self.ship.blitme()
            pygame.display.flip()

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()