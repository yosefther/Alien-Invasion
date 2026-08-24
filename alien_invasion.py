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

    def _check_keydown_events(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = True
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active and not self.stats.paused:
            self._fire_bullet()
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and not self.stats.game_active:
            self._start_game()
        elif event.key == pygame.K_p and self.stats.game_active:
            self.stats.paused = not self.stats.paused
        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
            self._quit_game()

    def _check_keyup_events(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = False
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = False

    def _start_game(self):
        self.settings.reset_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.paused = False
        self.respawn_until = 0
        self.scoreboard.prep_images()
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def _quit_game(self):
        pygame.quit()
        raise SystemExit

    def _update_game(self):
        if pygame.time.get_ticks() < self.respawn_until:
            return

        self.ship.update()
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        self._update_aliens()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            aliens_destroyed = sum(len(hit_aliens) for hit_aliens in collisions.values())
            self.stats.score += self.settings.alien_points * aliens_destroyed
            self.scoreboard.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_images()
            self._create_fleet()

    def _update_aliens(self):
        if any(alien.check_edges() for alien in self.aliens.sprites()):
            for alien in self.aliens.sprites():
                alien.rect.y += self.settings.fleet_drop_speed
            self.settings.fleet_direction *= -1

        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            return

        screen_rect = self.screen.get_rect()
        if any(alien.rect.bottom >= screen_rect.bottom for alien in self.aliens.sprites()):
            self._ship_hit()

    def _ship_hit(self):
        self.stats.ships_left -= 1
        self.scoreboard.prep_images()
        self.bullets.empty()
        self.aliens.empty()

        if self.stats.ships_left <= 0:
            self.stats.game_active = False
            self.play_button.set_message("PLAY AGAIN")
            pygame.mouse.set_visible(True)
            return

        self._create_fleet()
        self.ship.center_ship()
        self.respawn_until = pygame.time.get_ticks() + 850

    def _create_fleet(self):
        alien = Alien(self)
        horizontal_space = alien.rect.width * 1.65
        vertical_space = alien.rect.height * 1.65
        usable_width = self.settings.screen_width - (2 * alien.rect.width)
        aliens_per_row = max(1, int(usable_width // horizontal_space))
        usable_height = self.settings.screen_height - 320
        rows = max(1, min(5, int(usable_height // vertical_space)))

        fleet_width = (aliens_per_row - 1) * horizontal_space + alien.rect.width
        start_x = (self.settings.screen_width - fleet_width) / 2
        for row_number in range(rows):
            for alien_number in range(aliens_per_row):
                self._create_alien(
                    start_x + alien_number * horizontal_space,
                    108 + row_number * vertical_space,
                )

    def _create_alien(self, x_position, y_position):
        alien = Alien(self)
        alien.x = float(x_position)
        alien.rect.x = round(x_position)
        alien.rect.y = round(y_position)
        self.aliens.add(alien)

    def _draw_background(self):
        self.screen.fill(self.settings.bg_color)
        for x, y, radius, color in self.stars:
            pygame.draw.circle(self.screen, color, (x, y), radius)
        pygame.draw.line(
            self.screen,
            (26, 46, 72),
            (0, 78),
            (self.settings.screen_width, 78),
        )

    def _draw_overlay(self, title, subtitle=""):
        veil = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        veil.fill((4, 8, 18, 208))
        self.screen.blit(veil, (0, 0))

        screen_rect = self.screen.get_rect()
        title_image = self.title_font.render(title, True, (237, 245, 255))
        title_rect = title_image.get_rect(
            center=(screen_rect.centerx, screen_rect.centery - 85)
        )
        self.screen.blit(title_image, title_rect)
        if subtitle:
            subtitle_image = self.subtitle_font.render(subtitle, True, (126, 219, 213))
            subtitle_rect = subtitle_image.get_rect(
                center=(screen_rect.centerx, screen_rect.centery - 30)
            )
            self.screen.blit(subtitle_image, subtitle_rect)
