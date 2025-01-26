import pygame
import sys
import os

pygame.init()

screen = pygame.display.set_mode((1200, 900))

city_image = pygame.image.load('city.png')
city_image = pygame.transform.scale(city_image, (1200, 900))

car_image = pygame.image.load('car.png')
car_image = pygame.transform.scale(car_image, (50, 50))

explosion_frames = []
explosion_folder = "explosion_frames" 
for frame_name in sorted(os.listdir(explosion_folder)):
    frame_path = os.path.join(explosion_folder, frame_name)
    frame_image = pygame.image.load(frame_path).convert_alpha() 
    frame_image = pygame.transform.scale(frame_image, (400, 400))   
    explosion_frames.append(frame_image)

# Создание спрайтов
city_sprite = pygame.sprite.Sprite()
city_sprite.image = city_image
city_sprite.rect = city_image.get_rect()

car_sprites = []
for i in range(5):
    car_sprite = pygame.sprite.Sprite()
    car_sprite.image = car_image
    car_sprite.rect = car_image.get_rect()
    car_sprite.rect.x = i * 200
    car_sprite.rect.y = 670
    car_sprites.append(car_sprite)


all_sprites = pygame.sprite.Group()
all_sprites.add(city_sprite)
for car_sprite in car_sprites:
    all_sprites.add(car_sprite)

clock = pygame.time.Clock()
running = True
start_time = pygame.time.get_ticks()
fade_out_start_time = 0
explosion_start_time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for car_sprite in car_sprites:
        car_sprite.rect.x += 2
        if car_sprite.rect.x > 1200:
            car_sprite.rect.x = 0

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    current_time = pygame.time.get_ticks()
    if current_time - start_time > 6000 and fade_out_start_time == 0:
        fade_out_start_time = current_time
    if fade_out_start_time != 0:
        fade_out_alpha = int(255 * (current_time - fade_out_start_time) / 4000)  
        s = pygame.Surface((1200, 900))
        s.set_alpha(fade_out_alpha)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

    if current_time - start_time > 7000 and explosion_start_time == 0:
        explosion_sprite = pygame.sprite.Sprite()

        explosion_sprite.visible = False

        explosion_sprite.image = pygame.Surface((400, 400))  
        explosion_sprite.rect = explosion_sprite.image.get_rect()
        explosion_sprite.rect.x = 600 - 200  
        explosion_sprite.rect.y = 450 - 200
        all_sprites.add(explosion_sprite)  
        explosion_start_time = current_time
        explosion_sprite.image = explosion_frames[0] 
        explosion_sprite.visible = True
        print(1)
    if explosion_start_time != 0:

        frame_index = (current_time - explosion_start_time) // 250 
        if frame_index < len(explosion_frames):
            explosion_sprite.image = explosion_frames[frame_index]
        else:
            explosion_sprite.visible = False  
            
    if current_time - start_time > 10000: 
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()