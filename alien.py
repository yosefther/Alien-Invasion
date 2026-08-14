import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """One alien in the descending fleet."""

    SIZE = (58, 42)

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = self._build_image()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height + 70
        self.x = float(self.rect.x)

    @classmethod
    def _build_image(cls):
        image = pygame.Surface(cls.SIZE, pygame.SRCALPHA)
        cyan = (64, 224, 208)
        shadow = (19, 121, 132)
        eye = (245, 251, 255)

        pygame.draw.ellipse(image, shadow, (7, 8, 44, 28))
        pygame.draw.ellipse(image, cyan, (9, 5, 40, 27))
        pygame.draw.polygon(image, cyan, [(12, 23), (4, 37), (18, 31)])
        pygame.draw.polygon(image, cyan, [(46, 23), (54, 37), (40, 31)])
        pygame.draw.rect(image, cyan, (14, 28, 7, 10), border_radius=2)
        pygame.draw.rect(image, cyan, (37, 28, 7, 10), border_radius=2)
        pygame.draw.circle(image, eye, (22, 17), 4)
        pygame.draw.circle(image, eye, (36, 17), 4)
        pygame.draw.circle(image, (7, 12, 24), (22, 18), 2)
        pygame.draw.circle(image, (7, 12, 24), (36, 18), 2)
        return image

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = round(self.x)
