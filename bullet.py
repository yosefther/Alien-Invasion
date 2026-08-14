import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A projectile fired by the ship."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        self.rect = pygame.Rect(
            0,
            0,
            self.settings.bullet_width,
            self.settings.bullet_height,
        )
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = round(self.y)

    def draw_bullet(self):
        glow_rect = self.rect.inflate(6, 4)
        pygame.draw.rect(self.screen, (95, 214, 255), glow_rect, border_radius=4)
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=2)
