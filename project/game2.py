import pygame
import random
from pygame import *

pygame.init()
from database import *


window = pygame.display.set_mode((1800, 1200))

print(load_database(), 12212)

data1 = load_database()
data = load(load_database())


print(data1, 1)
pickaxe_durability = data[4]

radiation_level = 0
health = data[0] * 100

uranium_ore = 0

pickaxe_damage = 2
coins = data[6]

def level_bl(a):
    global pickaxe_durability, coins
    strenght = player.strenght_list[block.level]
    strenght -= pickaxe_damage
    player.strenght_list[block.level] -= pickaxe_damage
    print(strenght)
    pickaxe_durability -= pickaxe_damage
    if strenght <= 0 and pickaxe_durability > 0:
        strenght = a
        if block.type == 'iron':
            coins += 10
        if block.type == 'stone':
            coins += 1
        if block == 'dimond':
            coins += 20
        if block == 'gold':
            coins += 50
        if block == 'uranium_ore':
            uranium_ore += 1
        player.strenght_list[block.level] = a
        block.kill()


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, type=None, image1=None, level=None):
        super().__init__()
        self.image = transform.scale(image.load(image1), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type
        self.level = level
        self.strenght_list = [10, 25, 50, 100, 500]
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(Block):
    def __init__(self, x, y, type=None, image1=None):
        super().__init__(x, y, type, image1)
        self.image = transform.scale(image.load(image1), (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    

    def move(self, dx, dy, blocks):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
 
        for block in blocks:
            if self.rect.colliderect(block.rect):

                self.rect.x -= dx * self.speed
                self.rect.y -= dy * self.speed

    def break_block(self, blocks, map):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                for i, row in enumerate(map):
                    for j, cell in enumerate(row):
                        if cell == block:
                            map[i][j] = None
                            blocks.remove(block)
                            break

def create_map(width, height):
    map = []
    block_list = []
    for i in range(height):
        row = []
        row2 = []
        for j in range(width):
            if i > 4:  
                if random.randint(0, 1000) < 60: 
                    
                    row.append(Block(j * 100, i * 100, 'iron', 'images12.jpeg', i * 100 // 1200))
                elif random.randint(0, 1000) < 1 and i > 10:  
                    row.append(Block(j * 100, i * 100, 'uran', 'uran.png', i * 100 // 1200))
                else:  
                    row.append(Block(j * 100, i * 100, 'stone', 'bulg.png', i * 100 // 1200))

            else:  
                row.append(None)  
        map.append(row)
    return map


def draw_map(map):
    for row in map:
        for block in row:
            if block is not None:
                if player.rect.y != 0: 
                    pass
                else:
                    window.blit(block.image, (block.rect.x, block.rect.y))


map = create_map(18, 40)


player = Player(100, 100, image1 = 'run1.png')

def sprite_group():
    blocks = pygame.sprite.Group()
    for i, row in enumerate(map):
        for j, cell in enumerate(row):
            if cell is not None:
                blocks.add(cell)
    return blocks


blocks = sprite_group()
print(blocks)

player_group = pygame.sprite.Group()
player_group.add(player)

running = True
i = 10
j = 0  
font = pygame.font.Font(None, 36)

y_offset = 0
strenght_prom = 10
print(data, 121221)
def game3():
    global block, coins
    blocks = sprite_group()
    print(blocks)

    player_group = pygame.sprite.Group()
    player_group.add(player)

    running = True
    i = 10
    j = 0  
    font = pygame.font.Font(None, 36)

    y_offset = 0
    strenght_prom = 10
    print(data, 121221)
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(data, 12)
                
                
                data1[6] = coins
                data1[5] = pickaxe_durability
                print(data1, 1111)
                write_to_database(data1)
                running = False
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(1)
                    for block in blocks:
                        print(player.rect.x // 100 + 10, (player.rect.y + 110) // 100)
                        if block.rect.x // 100 == player.rect.x // 100 and block.rect.y // 100 == (player.rect.y + 60) // 100:
                            
                            if block.type == 'iron':
                                coins += 1
                            map[(block.rect.y) // 100][block.rect.x // 100] = None
                            
                            if block.level == 0:
                                level_bl(block.strenght_list[block.level])
                            elif block.level == 1:
                                level_bl(block.strenght_list[block.level])
                            elif block.level == 2:
                                level_bl(block.strenght_list[block.level])
                            elif block.level == 3:
                                level_bl(block.strenght_list[block.level])
                            
                            
                            
                            j +=1
                            
                            window.fill((0, 0, 0))
                if event.key == pygame.K_e:
                    
                    for block in blocks:
                        
                        if block.rect.x // 100 == (player.rect.x + 60) // 100  and block.rect.y // 100 == (player.rect.y) // 100:
                            map[(block.rect.y -40 ) // 100][block.rect.x // 100] = None

                            if block.type == 'iron':
                                coins += 1
                            if block.level == 0:
                                level_bl(block.strenght_list[block.level])
                            elif block.level == 1:
                                level_bl(block.strenght_list[block.level])
                            elif block.level == 2:
                                level_bl(block.strenght_list[block.level])
                            elif block.level == 3:
                                level_bl(block.strenght_list[block.level])
                            
                            

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0, blocks)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0, blocks)
        if keys[pygame.K_UP]:
            player.move(0, -1, blocks)
        if keys[pygame.K_DOWN]:
            player.move(0, 1, blocks)


        
        if player.rect.y > 250:
            y_offset += player.rect.y - 250
            player.rect.y = 250
            for block in blocks:
                block.rect.y -= 10
        if player.rect.y < 250 and player.rect.y > 100:    
            y_offset += player.rect.y + 250
            player.rect.y = 250
            for block in blocks:
                block.rect.y += 10
        window.fill((0, 0, 0))
        coins_text = font.render(f"Монеты: {coins}", True, (255, 255, 255))
        pickaxe_text = font.render(f"Кирка: {pickaxe_durability}", True, (255, 255, 255))
        radiation_text = font.render(f"Радиация: {radiation_level}", True, (255, 255, 255))
        health_text = font.render(f"Жизнь: {health}", True, (255, 255, 255))
        window.blit(pickaxe_text, (10, 10))
        window.blit(coins_text, (window.get_width() - 150, 10))
        window.blit(radiation_text, (window.get_width() - 150, 50))
        window.blit(health_text, (10, 50))


    
        draw_map(map)
        blocks.draw(window)
        
        player.reset()
        

        pygame.display.flip()


        pygame.time.delay(50)


    pygame.quit()
