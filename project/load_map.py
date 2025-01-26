import pygame
from pygame import *
map_objects = []


dragging = False  
dragged_object = None 
offset_x = 0 
offset_y = 0
block_image = transform.scale(image.load('platform_h.png'), (150, 50))
enemy_image = transform.scale(image.load('enemy.png'), (50, 50))
bonus_image = transform.scale(image.load('Gold_21.png'), (50, 50))
window = display.set_mode((800, 800))
WIDTH, HEIGHT = 800, 600
background_image = transform.scale(image.load('glav_menu.jpg'), (WIDTH, HEIGHT))

window.blit(background_image, (0, 0))
images = {
    'block': block_image,
    'enemy': enemy_image,
    'bonus': bonus_image
}

import json

def draw_objects(camera_x, camera_y):
    window.blit(background_image, (0, 0))

    window.blit(block_image, (10, 10))
    window.blit(bonus_image, (80 , 70))
    window.blit(enemy_image, (10, 70))

    for obj in map_objects:
        image = images[obj['image']]
        window.blit(image, (obj['x'] - camera_x, obj['y'] - camera_y))

def handle_events(camera_x, camera_y):
    global dragging, dragged_object, offset_x, offset_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.fill((0, 0, 0))
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            mouse_x += camera_x
            mouse_y += camera_y

            if 10 + camera_x <= mouse_x <= 60 + camera_x and 10 + camera_y <= mouse_y <= 60 + camera_y:
                dragged_object = {'image': 'block', 'x': mouse_x, 'y': mouse_y}
                dragging = True
            elif 10 + camera_x <= mouse_x <= 60 + camera_x and 70 + camera_y <= mouse_y <= 120 + camera_y:
                dragged_object = {'image': 'enemy', 'x': mouse_x, 'y': mouse_y}
                dragging = True
            elif 80 + camera_x <= mouse_x <= 120 + camera_x and 70 + camera_y <= mouse_y <= 120 + camera_y:
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
                mouse_x += camera_x
                mouse_y += camera_y
                dragged_object['x'] = mouse_x + offset_x
                dragged_object['y'] = mouse_y + offset_y

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                with open('map.json', 'w') as f:
                    json.dump(map_objects, f)

            if event.key == pygame.K_LEFT:
                camera_x += 10

            if event.key == pygame.K_RIGHT:
                camera_x -= 10
            if event.key == pygame.K_UP:
                camera_y += 10
            if event.key == pygame.K_DOWN:
                camera_y -= 10

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera_x += 10
        if keys[pygame.K_RIGHT]:
            camera_x -= 10
        if keys[pygame.K_UP]:
            camera_y += 10
        if keys[pygame.K_DOWN]:
            camera_y -= 10

    return camera_x, camera_y

def load_map1():
    global camera_x, camera_y
    camera_x = 0
    camera_y = 0

    running = True
    while running:
        result = handle_events(camera_x, camera_y)
        if result is False:
            running = False
        else:
            camera_x, camera_y = result
        draw_objects(camera_x, camera_y)
        pygame.display.flip()