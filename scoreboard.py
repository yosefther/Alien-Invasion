import pygame


class Scoreboard:
    """Render the score, high score, wave, and remaining ships."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        self.ship_image = pygame.transform.smoothscale(ai_game.ship.image, (32, 32))
        self.text_color = (230, 239, 255)
        self.muted_color = (139, 160, 190)
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16, bold=True)
        self.prep_images()

    def resize_for_screen(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.prep_images()

    def prep_images(self):
        score = f"{self.stats.score:,}"
        high_score = f"BEST  {self.stats.high_score:,}"
        level = f"WAVE  {self.stats.level}"
        self.score_image = self.font.render(score, True, self.text_color)
        self.high_score_image = self.small_font.render(high_score, True, self.muted_color)
        self.level_image = self.small_font.render(level, True, self.muted_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.topright = (self.screen_rect.right - 28, 20)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = (self.screen_rect.centerx, 24)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.topleft = (28, 28)

    def check_high_score(self):
        self.stats.high_score = max(self.stats.high_score, self.stats.score)
        self.prep_images()
