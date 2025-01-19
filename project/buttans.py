from pygame import *


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.is_hovered = False

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        draw.rect(surface, current_color, self.rect)
        self.draw_text(surface)

    def draw_text(self, surface):
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
