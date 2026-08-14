class Settings:
    """Store static and difficulty-dependent game settings."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.min_screen_width = 800
        self.min_screen_height = 600
        self.bg_color = (7, 12, 24)
        self.fps = 60

        self.ship_speed = 6.0
        self.ship_limit = 3

        self.bullet_speed = 9.0
        self.bullet_width = 4
        self.bullet_height = 18
        self.bullet_color = (255, 218, 92)
        self.bullets_allowed = 4

        self.fleet_drop_speed = 22
        self.speedup_scale = 1.14
        self.score_scale = 1.35
        self.reset_dynamic_settings()

    def reset_dynamic_settings(self):
        self.alien_speed = 1.25
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
