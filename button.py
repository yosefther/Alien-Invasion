import pygame


class Button:
    """A start and restart button."""

    def __init__(self, ai_game, message="PLAY"):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 220, 62
        self.button_color = (255, 196, 61)
        self.hover_color = (255, 218, 105)
        self.text_color = (7, 12, 24)
        self.font = pygame.font.SysFont("arial", 27, bold=True)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self._position_button()
        self.set_message(message)

    def _position_button(self):
        self.rect.center = (self.screen_rect.centerx, self.screen_rect.centery + 82)

    def resize_for_screen(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self._position_button()
        self.set_message(self.message)

    def set_message(self, message):
        self.message = message
        self.message_image = self.font.render(message, True, self.text_color)
        self.message_rect = self.message_image.get_rect(center=self.rect.center)

    def draw(self):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.button_color
        pygame.draw.rect(self.screen, color, self.rect, border_radius=6)
        pygame.draw.rect(self.screen, (255, 241, 187), self.rect, width=2, border_radius=6)
        self.screen.blit(self.message_image, self.message_rect)
