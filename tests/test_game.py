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
