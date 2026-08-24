import os
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

from alien_invasion import AlienInvasion
from bullet import Bullet


class AlienInvasionTests(unittest.TestCase):
    def setUp(self):
        self.game = AlienInvasion()
        self.game._start_game()

    def tearDown(self):
        pygame.quit()

    def test_ship_stays_inside_screen(self):
        self.game.ship.moving_left = True
        for _ in range(300):
            self.game.ship.update()
        self.assertEqual(self.game.ship.rect.left, 0)

        self.game.ship.moving_left = False
        self.game.ship.moving_right = True
        for _ in range(300):
            self.game.ship.update()
        self.assertEqual(self.game.ship.rect.right, self.game.screen.get_rect().right)

    def test_bullet_limit_is_enforced(self):
        for _ in range(self.game.settings.bullets_allowed + 3):
            self.game._fire_bullet()
        self.assertEqual(len(self.game.bullets), self.game.settings.bullets_allowed)

    def test_collision_removes_alien_and_awards_points(self):
        alien = next(iter(self.game.aliens))
        initial_alien_count = len(self.game.aliens)
        bullet = Bullet(self.game)
        bullet.rect.center = alien.rect.center
        self.game.bullets.add(bullet)

        self.game._check_bullet_alien_collisions()

        self.assertEqual(len(self.game.aliens), initial_alien_count - 1)
        self.assertEqual(self.game.stats.score, self.game.settings.alien_points)
        self.assertEqual(self.game.stats.high_score, self.game.stats.score)

    def test_clearing_fleet_advances_wave_and_difficulty(self):
        initial_speed = self.game.settings.alien_speed
        self.game.aliens.empty()

        self.game._check_bullet_alien_collisions()

        self.assertEqual(self.game.stats.level, 2)
        self.assertGreater(self.game.settings.alien_speed, initial_speed)
        self.assertGreater(len(self.game.aliens), 0)

    def test_last_ship_ends_the_game(self):
        self.game.stats.ships_left = 1
        self.game._ship_hit()

        self.assertFalse(self.game.stats.game_active)
        self.assertEqual(self.game.stats.ships_left, 0)
        self.assertEqual(self.game.play_button.message, "PLAY AGAIN")

    def test_screen_renders_in_headless_mode(self):
        self.game._update_screen()
        self.assertEqual(self.game.screen.get_size(), (1200, 800))
