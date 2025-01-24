from pygame import *
import random
m = 1200
window = display.set_mode((m, 900))
b = (135, 206, 235)
display.set_caption('Моя игра')
finish = False
run = True
y_speed = 0
win = transform.scale(image.load('thumb.jpg'), (700, 500))


import json
WIDTH, HEIGHT = 800, 600


def load_level_from_json(filename):
    with open(filename, 'r') as file:
        level_data = json.load(file)
    
    block_list = sprite.Group()
    enemy_list = sprite.Group()
    bonus_list = sprite.Group()
    for item in level_data:
        if item["image"] == "block":
            block = GameSprite(item["image"] + '.png', 150, 50, item["x"], item["y"])  
            block_list.add(block)
        elif item["image"] == "enemy":
            enemy = Enemy(item["image"] + '.png', 70, 65, item["x"], item["y"], 0, 0, 0)  
            enemy_list.add(enemy)
        elif item["image"] == "bonus":
            bonus = Bonus(item["x"], item['y'], 'bonus')
            bonus_list.add(bonus)
    return block_list, enemy_list, bonus_list

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

import pygame
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
                print(p.rect.x, p.rect.y)
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
                self.y_speed = 0  
                self.is_jumping = False
        elif self.y_speed < 0: 
            for p in platforms_touched:
                print(p.rect.x, p.rect.y)
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

    
class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - 300)
        self.dy = -(target.rect.y + target.rect.h // 2 - 300)


class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed, p, win_didth):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.direction = 'right'
        self.p = p
        self.win_didth = win_didth
        self.health = 3 
        self.last_shot_time = 0  
        self.shoot_interval = 3000 

    def update(self):
        current_time = time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_interval:
            self.shoot()
            self.last_shot_time = current_time

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)  
        bullet.speed = 5  
        bullets.add(bullet) 


class Bullet(sprite.Sprite):
    def __init__(self, x, y, type = 'enemy'):
        super().__init__()
        self.type = type
        self.image = Surface((10, 5))  
        self.image.fill((255, 0, 0))  
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  
        self.speed = 10 

    def update(self):
        self.rect.x += self.speed  
        if self.rect.x > WIDTH: 
            self.kill()

def draw_lives(x, y, lives):
    for i in range(lives):
        image1 = transform.scale(image.load('heat.png'), (40, 40))
        x = x + 40
        y = y
        window.blit(image1, (x, y))



import os


class Bonus(GameSprite):
    def __init__(self, x, y, frames_folder):
        super().__init__('Gold_21.png', 50, 50, x, y) 
        self.types = ['health', 'speed', 'bullets', 'damage']
        self.type = random.choice(self.types)
        self.speed_y = 2
        self.direction = 1

        self.frames = self.load_frames_from_folder(frames_folder)
        self.current_frame = 0  
        self.animation_speed = 0.2  
        self.last_update = time.get_ticks()  

    def load_frames_from_folder(self, folder_path):

        frames = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):  
                frame_path = os.path.join(folder_path, filename)
                frame = transform.scale(image.load(frame_path), (50, 50))  
                frames.append(frame)
        return frames

    def update(self):
        # Анимация
        now = time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000: 
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)  
            self.image = self.frames[self.current_frame]  

        self.rect.y += self.speed_y * self.direction
        if self.rect.y > 500:
            self.direction = -1
        elif self.rect.y < 100:
            self.direction = 1

    def apply(self, player):
        if self.type == 'health':
            player.health += 10
            print(1)
        elif self.type == 'speed':
            player.speed += 2
            print(2)
        elif self.type == 'bullets':
            print(3)
            player.bullets += 10
        elif self.type == 'damage':
            print(4)
            player.damage += 2

lives = 1
player = Player(70, 65, 30,100, 0, 0)
def load_map(filename):
    global map_objects  

    with open(filename, 'r') as f:
        map_objects = json.load(f)  
    
bullets = sprite.Group()
barriers, monsters, bonus = load_level_from_json('map.json')

