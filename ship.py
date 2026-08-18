from pathlib import Path

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """The player's ship and its movement state."""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        image_path = Path(__file__).resolve().parent / "assets" / "ship1.bmp"
        source_image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(source_image, (86, 86))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.x = max(0, min(self.x, self.screen_rect.width - self.rect.width))
        self.rect.x = round(self.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def resize_for_screen(self, screen, old_width):
        horizontal_position = self.rect.centerx / old_width
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.rect.centerx = round(horizontal_position * self.screen_rect.width)
        self.rect.bottom = self.screen_rect.bottom
        self.rect.clamp_ip(self.screen_rect)
        self.x = float(self.rect.x)
