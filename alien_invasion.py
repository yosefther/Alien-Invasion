import random

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Coordinate input, game state, collisions, and drawing."""

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height),
            pygame.RESIZABLE,
        )
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.play_button = Button(self)
        self.respawn_until = 0
        self.title_font = pygame.font.SysFont("arial", 64, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 20)
        self.stars = self._create_starfield()
        self._create_fleet()
