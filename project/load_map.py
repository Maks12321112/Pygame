import pygame
import json
import os

# Инициализация Pygame
pygame.init()

# Установите размеры окна
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна с заданными размерами
pygame.display.set_caption("Конструктор карты")  # Установка заголовка окна

# Загрузка изображения фона
try:
    background_image = pygame.transform.scale(pygame.image.load('level.png'), (WIDTH, HEIGHT))  # Загрузка и масштабирование фона
    block_image = pygame.transform.scale(pygame.image.load('platform_h.png'), (150, 30))  # Загрузка и масштабирование изображения блока
    enemy_image = pygame.transform.scale(pygame.image.load('enemy.png'), (50, 50))  # Загрузка и масштабирование изображения врага
except pygame.error as e:
    print(f"Ошибка загрузки изображения: {e}")  # Вывод ошибки, если изображения не удалось загрузить
    pygame.quit()  # Завершение Pygame
    exit()  # Выход из программы

# Словарь для хранения изображений объектов
images = {
    'block': block_image,
    'enemy': enemy_image
}

# Список для хранения объектов карты
map_objects = []

# Переменные для перетаскивания объектов
dragging = False  # Флаг, указывающий, перетаскивается ли объект
dragged_object = None  # Текущий перетаскиваемый объект
offset_x = 0  # Смещение по оси X
offset_y = 0  # Смещение по оси Y

# Функция для загрузки карты из файла
def load_map(filename):
    global map_objects  # Используем глобальную переменную map_objects
    try:
        with open(filename, 'r') as f:
            map_objects = json.load(f)  # Загрузка объектов карты из JSON-файла
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Пожалуйста, сохраните карту перед загрузкой.")  # Сообщение об ошибке, если файл не найден
    except json.JSONDecodeError:
        print(f"Ошибка при загрузке файла {filename}. Возможно, файл поврежден.")  # Сообщение об ошибке, если файл поврежден

# Основной игровой цикл
running = True
while running:
    # Отображение фона
    window.blit(background_image, (0, 0))  # Отрисовка фона на экране

    # Отображение объектов (блоков и врагов)
    window.blit(block_image, (10, 10))  # Отрисовка блока в фиксированной позиции
    window.blit(enemy_image, (10, 70))  # Отрисовка врага в фиксированной позиции

    # Отрисовка объектов карты
    for obj in map_objects:
        image = images[obj['image']]  # Получение изображения объекта по его типу
       
        window.blit(image, (obj['x'], obj['y']))  # Отрисовка объекта на экране

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Выход из цикла, если окно закрыто

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos  # Получение позиции мыши
            
            # Проверка, нажата ли мышь на блоке или враге для начала перетаскивания
            if 10 <= mouse_x <= 60 and 10 <= mouse_y <= 60:
                dragged_object = {'image': 'block', 'x': mouse_x, 'y': mouse_y}  # Создание нового блока
                dragging = True  # Установка флага перетаскивания
            elif 10 <= mouse_x <= 60 and 70 <= mouse_y <= 120:
                dragged_object = {'image': 'enemy', 'x': mouse_x, 'y': mouse_y}  # Создание нового врага
                dragging = True  # Установка флага перетаскивания
            else:
                # Проверка, нажата ли мышь на существующем объекте карты
                for obj in map_objects:
                    if obj['x'] <= mouse_x <= obj['x'] + 50 and obj['y'] <= mouse_y <= obj['y'] + 50:
                        dragging = True  # Установка флага перетаскивания
                        offset_x = obj['x'] - mouse_x  # Вычисление смещения по оси X
                        offset_y = obj['y'] - mouse_y  # Вычисление смещения по оси Y
                        dragged_object = obj  # Установка текущего перетаскиваемого объекта
                        break  # Выход из цикла, если объект найден

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging:  # Если объект перетаскивается
                dragging = False  # Сброс флага перетаскивания
                if dragged_object not in map_objects:  # Если объект новый, добавляем его в список
                    map_objects.append(dragged_object)
                dragged_object = None  # Сброс текущего перетаскиваемого объекта

        if event.type == pygame.MOUSEMOTION:
            if dragging and dragged_object:  # Если объект перетаскивается
                mouse_x, mouse_y = event.pos  # Получение текущей позиции мыши
                dragged_object['x'] = mouse_x + offset_x  # Обновление позиции объекта по оси X
                dragged_object['y'] = mouse_y + offset_y  # Обновление позиции объекта по оси Y

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Если нажата клавиша S
                with open('map.json', 'w') as f:
                    json.dump(map_objects, f)  # Сохранение объектов карты в JSON-файл
            if event.key == pygame.K_l:  # Если нажата клавиша L
                load_map('map.json')  # Загрузка объектов карты из JSON-файла

    pygame.display.flip()  # Обновление экрана

pygame.quit()  # Завершение Pygame