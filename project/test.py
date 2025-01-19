import pygame
import sys
from database import *

pygame.init()

window = pygame.display.set_mode((800, 600))

font = pygame.font.Font(None, 36)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.is_hovered = False

    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        self.draw_text(surface)

    def draw_text(self, surface):
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
create_database()

loaded_data = load_database()
print(load(loaded_data))

print(loaded_data)
upgrades = [
    {"name": "Здоровье", "level": loaded_data[0], "price": 100},
    {"name": "Скорость", "level": loaded_data[1], "price": 150},
    {"name": "Прыжок", "level": loaded_data[2], "price": 200},
    {"name": "Защита от радиации", "level": loaded_data[3], "price": 250},
    {"name": "Кирка", "level": loaded_data[4], "price": 300},
    {"name": "Прочность", "level": loaded_data[5], "price": 350},
]


buttons = []
for i, upgrade in enumerate(upgrades):
    if i < 3:
        button = Button(10, 10 + i * 120, 100, 30, f"{upgrade['price']}", (0, 255, 0), (0, 200, 0), font)
    else:
        button = Button(250, 10 + (i - 3) * 120, 100, 30, f"{upgrade['price']}", (0, 255, 0), (0, 200, 0), font)
    buttons.append(button)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print([upgrades[i]['level'] for i in range(6)] + [loaded_data[-1]])
            reset_database()
            write_to_database([upgrades[i]['level'] for i in range(6)] + [loaded_data[-1]])

            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(buttons):
                if button.is_clicked(event.pos):
                    if upgrades[i]["level"] < 5:
                        upgrades[i]["level"] += 1
                        upgrades[i]["price"] += 100


    window.fill((255, 255, 255))


    for i, upgrade in enumerate(upgrades):
        if i < 3:
            text_surface = font.render(upgrade["name"], True, (0, 0, 0))
            window.blit(text_surface, (10, 200 + i * 120 - 30))
            text_surface = font.render(f"Уровень: {upgrade['level']}", True, (0, 0, 0))
            window.blit(text_surface, (10, 200 + i * 120))
        else:
            text_surface = font.render(upgrade["name"], True, (0, 0, 0))
            window.blit(text_surface, (250, 200 + (i - 3) * 120 - 30))
            text_surface = font.render(f"Уровень: {upgrade['level']}", True, (0, 0, 0))
            window.blit(text_surface, (250, 200 + (i - 3) * 120))

    for i, button in enumerate(buttons):
        if i < 3:
            button.rect.y = 200 + i * 120 + 30
        else:
            button.rect.y = 200 + (i - 3) * 120 + 30
        button.update(pygame.mouse.get_pos())
        button.draw(window)


    pygame.display.flip()


    pygame.time.delay(30)