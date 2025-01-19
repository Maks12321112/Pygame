from pygame import *
import pygame
import json
import os
import sys
from labirint import GameSprite, Player, Enemy, Bullet, draw_lives, load_level_from_json, Bonus

from buttans import Button
import pygame
font = pygame.font

init()
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
    font_instance = font.Font(None, 74)  
    small_font = font.Font(None, 36)
    start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40, 'Начать', BLACK, GREEN, small_font)
    editor_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 40, 'Редактор', BLACK, GREEN, small_font)
    exit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 40, 'Выйти', BLACK, RED, small_font)

    while True:
        draw_text('Главное меню', font_instance, BLACK, window, WIDTH // 2, HEIGHT // 4)

        mouse_x, mouse_y = mouse.get_pos()

        start_button.update((mouse_x, mouse_y))
        editor_button.update((mouse_x, mouse_y))
        exit_button.update((mouse_x, mouse_y))

        start_button.draw(window)
        editor_button.draw(window)
        exit_button.draw(window)

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
                    open_editor(True) 
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
    global map_objects
    run = True
    lives = 1

    finish = False

    player = Player(70, 65, 30,100, 0, 0) 



    bullets = sprite.Group()
    
    clock = time.Clock()
    barriers, monsters, bonus = load_level_from_json('map.json')
    lives = 3
    m = 1200
    window = display.set_mode((m, 900))
    b = (135, 206, 235)
    finish = False
    win = transform.scale(image.load('thumb.jpg'), (700, 500))
    WIDTH, HEIGHT = 800, 600
    window = display.set_mode((WIDTH, HEIGHT))
    enemies = sprite.Group()
    running = True
    bullets = sprite.Group()
    clock = time.Clock()

    b = Bonus(300, 300, 'bonus')
    x_offset = 0
    TIMER_EVENT_TYPE = USEREVENT + 1  
    time.set_timer(TIMER_EVENT_TYPE, 3000)
    while running:
        
        for e in event.get():
            if e.type == QUIT:
                return 'menu'
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.centery)
                    bullets.add(bullet)
                #движение спрайта
                if e.key == K_UP or e.key == K_w:
                    if not player.is_jumping:
                        player.y_speed = -10 
                        player.is_jumping = True 
                if e.key == K_DOWN or e.key == K_s:
                    player.y_speed = 8
                if e.key == K_LEFT or e.key == K_a:
                    player.x_speed = -15
                if e.key == K_RIGHT or e.key == K_d:
                    player.x_speed = 15
            
            elif e.type == KEYUP:
                if e.key == K_LEFT or e.key == K_a:
                    player.x_speed = 0
                if e.key == K_RIGHT or e.key == K_d:
                    player.x_speed = 0
            
            #выстрелфы врагов
            elif e.type == TIMER_EVENT_TYPE:
                for enemy in monsters:
                    enemy.update()  
                    bullet = Bullet(enemy.rect.centerx + 30, enemy.rect.centery)
                    bullets.add(bullet)
                    bullets.update()
            if lives == 0:
                finish = True

            win = transform.smoothscale(image.load('thumb.jpg'), (1200, 1080))

        if not finish:
            if player.rect.x > 400 and player.x_speed > 0:
                x_offset += player.rect.x - 400
                player.rect.x = 400
                for obj in map_objects:
                    obj['x'] -= 10
                    obj['image'] = transform.scale(image.load(obj['image']), (75, 50))  
                    obj['image_rect'] = obj['image'].get_rect()
                    obj['image_rect'].x = obj['x']
                    obj['image_rect'].y = obj['y']
                for barrier in barriers:
                    barrier.rect.x -= 10
                for monster in monsters:
                    monster.rect.x -= 10
                
            elif player.rect.x < 100 and player.x_speed < 0:
                x_offset += player.rect.x - 100
                player.rect.x = 100
                for obj in map_objects:
                    obj['x'] += 10
                    obj['image'] = transform.scale(image.load(obj['image']), (75, 50)) 
                    obj['image_rect'] = obj['image'].get_rect()
                    obj['image_rect'].x = obj['x']
                    obj['image_rect'].y = obj['y']
                for barrier in barriers:
                    barrier.rect.x += 10
                for monster in monsters:
                    monster.rect.x += 10
                for obj in map_objects:
                    window.blit(obj['image'], (obj['image_rect'].x, obj['image_rect'].y))
            draw_lives(50, 80, lives)
            #орбработка урона
            if sprite.spritecollide(player, monsters, True):
                lives -= 1
                draw_lives(50, 80, lives)
            for enemy in monsters:
                if sprite.spritecollide(enemy, bullets, True):
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.kill()
            if sprite.spritecollide(player, bonus, True): 
                for b in bonus:  
                    b.apply(player)  
        
            sprite.groupcollide(bullets, barriers, True, False)
            sprite.groupcollide(bullets, monsters, True, True)

            
            background_image = transform.scale(image.load('level.png'), (WIDTH, HEIGHT))
            window.blit(background_image, (0, 0))
            bullets.update()
            bullets.draw(window)
            bonus.update()
            monsters.update()
            monsters.draw(window)
            bonus.draw(window)
            player.reset()
            player.update()
            b.update()
            draw_lives(10, 10,lives)
            barriers.draw(window)
            
        else:
            return 'exit'
        time.delay(30)
        display.update()
        clock.tick(100)

def open_editor(running):
    map_objects = []


    dragging = False  
    dragged_object = None 
    offset_x = 0 
    offset_y = 0
    while running:

        window.blit(background_image, (0, 0))  

        
        window.blit(block_image, (10, 10)) 
        window.blit(bonus_image, (80, 70))  
        window.blit(enemy_image, (10, 70))  


        print(map_objects)
        for obj in map_objects:
            image = images[obj['image']]  
        
            window.blit(image, (obj['x'], obj['y']))  

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window.fill((0, 0, 0))
                running = False 

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos  
                

                if 10 <= mouse_x <= 60 and 10 <= mouse_y <= 60:
                    dragged_object = {'image': 'block', 'x': mouse_x, 'y': mouse_y}  
                    dragging = True 
                elif 10 <= mouse_x <= 60 and 70 <= mouse_y <= 120:
                    dragged_object = {'image': 'enemy', 'x': mouse_x, 'y': mouse_y} 
                    dragging = True 
                elif 80 <= mouse_x <= 120 and 70 <= mouse_y <= 120:
                    dragged_object = {'image': 'bonus', 'x': mouse_x, 'y': mouse_y} 
                    dragging = True 
                else:
                    
                    for obj in map_objects:
                        if obj['x'] <= mouse_x <= obj['x'] + 50 and obj['y'] <= mouse_y <= obj['y'] + 50:
                            dragging = True  
                            offset_x = obj['x'] - mouse_x 
                            offset_y = obj['y'] - mouse_y 
                            dragged_object = obj  
                            break 

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging:  
                    dragging = False 
                    if dragged_object not in map_objects:  
                        map_objects.append(dragged_object)
                    dragged_object = None  

            if event.type == pygame.MOUSEMOTION:
                if dragging and dragged_object:  
                    mouse_x, mouse_y = event.pos  
                    dragged_object['x'] = mouse_x + offset_x  
                    dragged_object['y'] = mouse_y + offset_y  

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: 
                    with open('map.json', 'w') as f:
                        json.dump(map_objects, f)  

        pygame.display.flip()  

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