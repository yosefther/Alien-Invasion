import sys 
import pygame

class AlienInvasion:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("python game aliens")
        self.screen = pygame.display.set_mode((1200,800)) # object we assigned to self.screen is called a surface in pygame
        self.clock = pygame.time.Clock()
        self.bg_color = (230, 230, 230)
    
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                  sys.exit()
            pygame.display.flip()
            self.screen.fill(self.bg_color)
            self.clock.tick(60)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
