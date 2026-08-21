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

    def _create_starfield(self):
        rng = random.Random(42)
        stars = []
        for _ in range(115):
            stars.append(
                (
                    rng.randrange(self.settings.screen_width),
                    rng.randrange(75, self.settings.screen_height),
                    rng.choice((1, 1, 1, 2)),
                    rng.choice(((74, 95, 130), (112, 142, 174), (189, 212, 229))),
                )
            )
        return stars

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active and not self.stats.paused:
                self._update_game()
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.VIDEORESIZE:
                self._resize_screen(event.size)
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and not self.stats.game_active
                and self.play_button.rect.collidepoint(event.pos)
            ):
                self._start_game()
