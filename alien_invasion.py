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

    def _resize_screen(self, size):
        old_width = self.settings.screen_width
        old_height = self.settings.screen_height
        new_width = max(self.settings.min_screen_width, int(size[0]))
        new_height = max(self.settings.min_screen_height, int(size[1]))

        self.screen = pygame.display.set_mode(
            (new_width, new_height),
            pygame.RESIZABLE,
        )
        self.settings.screen_width = new_width
        self.settings.screen_height = new_height

        self.ship.resize_for_screen(self.screen, old_width)
        self.scoreboard.resize_for_screen(self.screen)
        self.play_button.resize_for_screen(self.screen)
        self._resize_sprites(old_width, old_height)
        self.stars = self._create_starfield()

    def _resize_sprites(self, old_width, old_height):
        width_ratio = self.settings.screen_width / old_width
        height_ratio = self.settings.screen_height / old_height
        screen_rect = self.screen.get_rect()

        for bullet in self.bullets.sprites():
            bullet.screen = self.screen
            bullet.rect.centerx = round(bullet.rect.centerx * width_ratio)
            bullet.y *= height_ratio
            bullet.rect.y = round(bullet.y)

        play_top = 88
        old_play_bottom = max(play_top + 1, old_height - self.ship.rect.height - 24)
        new_play_bottom = max(
            play_top + 1,
            self.settings.screen_height - self.ship.rect.height - 24,
        )
        play_height_ratio = (new_play_bottom - play_top) / (old_play_bottom - play_top)
        for alien in self.aliens.sprites():
            alien.screen = self.screen
            alien.rect.centerx = round(alien.rect.centerx * width_ratio)
            alien.rect.y = round(
                play_top + (alien.rect.y - play_top) * play_height_ratio
            )
            alien.rect.clamp_ip(screen_rect)
            alien.x = float(alien.rect.x)
