from pygame import *
import pygame
import json
import os
import sys
from load_map import load_map1
from buttans import Button
import pygame
font = pygame.font
import pygame
import sys
from pygame.locals import *
import os
from labirint import *
from test import *
from game2 import *
barriers = pygame.sprite.Group()


barriers, monsters, bonus = load_level_from_json('map.json')


class Player(GameSprite):
    def __init__(self, w, h, x, y, x_speed, y_speed):
        super().__init__('run1.png', 50, 50, x, y) 
        self.image = pygame.transform.scale(pygame.image.load('run1.png'), (50, 50))  
        self.frames_right = self.load_frames_from_folder('run') 

        self.x_speed = x_speed
        self.y_speed = y_speed
        self.gravity = 0.4
        self.is_jumping = False


        self.frame_width = w  
        self.frame_height = h  
        self.current_frame = 0  

        self.animation_speed = 0.2  
        self.last_update = pygame.time.get_ticks()  
        self.is_walking = False  

    def load_frames_from_folder(self, folder_path):

        frames = []
        for filename in os.listdir('run'):
            if filename.endswith('.png'):  
                frame_path = os.path.join(folder_path, filename)
                frame = pygame.transform.scale(pygame.image.load(frame_path), (50, 50))  
                frames.append(frame)
        return frames


    def update(self):

        self.rect.x += self.x_speed

 
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:  
            for p in platforms_touched:
                
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
                self.y_speed = 0  
                self.is_jumping = False
        elif self.y_speed < 0: 
            for p in platforms_touched:
                
                self.rect.top = max(self.rect.top, p.rect.bottom)
                self.y_speed = 0  

  
        if self.x_speed != 0: 
            self.is_walking = True
        else:
            self.is_walking = False

        self.update_animation()

    def update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000: 
            self.last_update = now
            if self.is_walking: 
                self.current_frame = (self.current_frame + 1) % len(self.frames_right) 
                self.image = self.frames_right[self.current_frame]
init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

player = Player(50, 50, 100, 100, 0, 0)

camera = Camera()
def a():
    pass
m = 1200
window = display.set_mode((m, 900))
b = (135, 206, 235)
display.set_caption('Моя игра')
finish = False
run = True
running = False
y_speed = 0
win = transform.scale(image.load('thumb.jpg'), (700, 500))
WIDTH, HEIGHT = 800, 600
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Конструктор карты")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
background_image = transform.scale(image.load('glav_menu.jpg'), (WIDTH, HEIGHT))
window.blit(background_image, (0, 0))
try:
    block_image = transform.scale(image.load('platform_h.png'), (75, 50))
    enemy_image = transform.scale(image.load('enemy.png'), (50, 50))
    bonus_image = transform.scale(image.load('Gold_21.png'), (50, 50))
except error as e:
    print(f"Ошибка загрузки изображения: {e}")
    quit()
    exit()

images = {
    'block': block_image,
    'enemy': enemy_image,
    'bonus': bonus_image
}

map_objects = []

dragging = False
dragged_object = None
offset_x = 0
offset_y = 0





def main_menu():
    background_image = transform.scale(image.load('glav_menu.jpg'), (WIDTH, HEIGHT))
    window.blit(background_image, (0, 0))
    font_instance = pygame.font.Font(None, 74)  
    small_font = pygame.font.Font(None, 36)
    start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40, 'Начать', BLACK, GREEN, small_font)
    editor_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 40, 'Редактор', BLACK, GREEN, small_font)
    editor_button1 = Button(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 40, 'Копатель', BLACK, GREEN, small_font)
    editor_button2 = Button(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 40, 'Магазин', BLACK, GREEN, small_font)
    exit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 180, 200, 40, 'Выйти', BLACK, RED, small_font)

    while True:
        draw_text('Главное меню', font_instance, BLACK, window, WIDTH // 2, HEIGHT // 4)

        mouse_x, mouse_y = mouse.get_pos()

        start_button.update((mouse_x, mouse_y))
        editor_button.update((mouse_x, mouse_y))
        exit_button.update((mouse_x, mouse_y))
        editor_button1.update((mouse_x, mouse_y))
        editor_button2.update((mouse_x, mouse_y))


        start_button.draw(window)
        editor_button.draw(window)
        exit_button.draw(window)
        editor_button1.draw(window)
        editor_button2.draw(window)
        for e in event.get():  
            if e.type == QUIT:
                quit()
                sys.exit()

            if e.type == MOUSEBUTTONDOWN:
                if start_button.is_clicked((mouse_x, mouse_y)):
                    print("Кнопка 'Начать' нажата")  
                    return  'game'
                elif editor_button.is_clicked((mouse_x, mouse_y)): 
                    running = True
                    load_map1() 
                    window.blit(background_image, (0, 0))
                elif editor_button2.is_clicked((mouse_x , mouse_y)):
                    game2() 
                    window.blit(background_image, (0, 0))
                elif editor_button1.is_clicked((mouse_x, mouse_y)):
                    game3()
                    print(1)
                    window.blit(background_image, (0, 0))
                elif exit_button.is_clicked((mouse_x , mouse_y)):
                
                    quit()
                    sys.exit()
                
        display.flip()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def game_loop():
    b = Bonus(300, 300, 'bonus')
    running = True
    TIMER_EVENT_TYPE = USEREVENT + 1  
    time.set_timer(TIMER_EVENT_TYPE, 3000)
    finish = False
    lives = 3
    bullets2 = pygame.sprite.Group()
    while running:
        
        for e in event.get():
            if e.type == QUIT:
                return 'menu'
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.centery, 'player')
                    bullets.add(bullet)
                #движение спрайта
                if e.key == K_UP or e.key == K_w:
                    if not player.is_jumping:
                        player.y_speed = -9
                        player.is_jumping = True 
                if e.key == K_DOWN or e.key == K_s:
                    player.y_speed = 9
                if e.key == K_LEFT or e.key == K_a:
                    player.x_speed = -9
                if e.key == K_RIGHT or e.key == K_d:
                    player.x_speed = 9
            
            elif e.type == KEYUP:
                if e.key == K_LEFT or e.key == K_a:
                    player.x_speed = 0
                if e.key == K_RIGHT or e.key == K_d:
                    player.x_speed = 0
            
            #выстрелфы врагов
            elif e.type == TIMER_EVENT_TYPE:
                for enemy in monsters:
                    enemy.update()  
                    bullet = Bullet(enemy.rect.centerx + 30, enemy.rect.centery, 'enemy_bullet')
                    bullets2.add(bullet)
                    bullets2.update()
            if lives == 0:
                finish = True

            win = transform.smoothscale(image.load('thumb.jpg'), (1200, 1080))

        if not finish:
            
            draw_lives(50, 80, lives)
            #орбработка урона
            if pygame.sprite.spritecollide(player, monsters, True):
                lives -= 1
                draw_lives(50, 80, lives)
            for enemy in monsters:
                for bullet in bullets:
                    if bullet.type == 'player':
                        if pygame.sprite.collide_rect(enemy, bullet):
                            bullet.kill
                            enemy.health -= 1
                            
                            if enemy.health <= 0:
                                enemy.kill()
                            bullet.kill()
            if pygame.sprite.spritecollide(player, bonus, True): 
                for b in bonus:  
                    b.apply(player)  
        
           

            window.fill((0, 0, 0))
            background_image = transform.scale(image.load('level.png'), (WIDTH, HEIGHT))
            window.blit(background_image, (0, 0))
            bullets.update()
            bullets.draw(window)
            bullets2.update()
            bullets2.draw(window)
            bonus.update()
            monsters.update()
            monsters.draw(window)
            bonus.draw(window)
            player.reset()
            player.update()
            b.update()
            draw_lives(10, 10,lives)
            barriers.draw(window)
            camera.update(player)
            for sprite in [player]  + list(barriers.sprites()) + list(bonus.sprites()) + list(monsters.sprites()):
                
                camera.apply(sprite)
                
            
                
        else:
            return 'exit'
        
        display.update()
        clock.tick(1200)
        
        



if __name__ == "__main__":
    
        state = "menu"
        while True:
            if state == "menu":
                state = main_menu()
            elif state == "game":
                state = game_loop()
            
            elif state == "exit":
                print(1)
                break
quit() 