import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Платформер с порталом')

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Цвет врагов
YELLOW = (255, 255, 0)  # Цвет монет
BROWN = (139, 69, 19)  # Цвет платформ
PURPLE = (128, 0, 128)  # Цвет портала

# Настройки персонажа
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 100
player_velocity = 5
player_jump_power = 15
is_jumping = False
jump_velocity = player_jump_power

# Гравитация
gravity = 1
fall_velocity = 0

# Функция для генерации случайных платформ
def generate_random_platforms(num_platforms, width, height):
    platforms = []
    for _ in range(num_platforms):
        platform_width = random.randint(150, 300)  # Случайная ширина платформы
        platform_height = 20  # Высота платформы
        platform_x = random.randint(0, width - platform_width)
        platform_y = random.randint(100, height - 50)  # Не на самом верху или снизу
        platforms.append(pygame.Rect(platform_x, platform_y, platform_width, platform_height))
    platforms.append(pygame.Rect(0, HEIGHT - 20, WIDTH, 20))  # Земля
    return platforms

# Генерация платформ
platforms = generate_random_platforms(7, WIDTH, HEIGHT)

# Враги
enemies = [
    {"rect": pygame.Rect(600, 470, 50, 50), "health": 2},  # Враг 1 (здоровье = 2)
    {"rect": pygame.Rect(200, 350, 50, 50), "health": 2},  # Враг 2
]

# Монеты
coins = [
    pygame.Rect(150, 460, 30, 30),  # Монета 1
    pygame.Rect(500, 360, 30, 30),  # Монета 2
]

# Создаем портал
portal = pygame.Rect(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 50, 50)

# Создаем игрока
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Счетчик монет
coin_count = 0
font = pygame.font.SysFont('Arial', 30)

# Главный игровой цикл
clock = pygame.time.Clock()
while True:
    screen.fill(WHITE)
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Движение игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_velocity
    if keys[pygame.K_RIGHT]:
        player.x += player_velocity

    # Проверка на падение
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and player.bottom <= platform.top + fall_velocity:
            fall_velocity = 0
            player.y = platform.top - player.height
            on_ground = True
            break

    if not on_ground:
        fall_velocity += gravity
        player.y += fall_velocity
    else:
        is_jumping = False
        jump_velocity = player_jump_power

    # Прыжок
    if not is_jumping and keys[pygame.K_SPACE]:
        is_jumping = True
        fall_velocity = -jump_velocity

    # Рисуем платформы
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)

    # Рисуем врагов
    for enemy in enemies[:]:
        pygame.draw.rect(screen, GREEN, enemy["rect"])

    # Рисуем монеты и проверка на сбор
    for coin in coins[:]:
        pygame.draw.rect(screen, YELLOW, coin)
        if player.colliderect(coin):
            coins.remove(coin)  # Удаляем монету при сборе
            coin_count += 1  # Увеличиваем счетчик монет

    # Рисуем портал
    pygame.draw.rect(screen, PURPLE, portal)
    
    # Проверка на вход в портал
    if player.colliderect(portal):
        player.x = random.randint(0, WIDTH - player_width)  # Телепортируем на случайную позицию
        player.y = random.randint(0, HEIGHT - player_height)

        # Перемещаем портал на новое место
        portal.x = random.randint(100, WIDTH - 100)
        portal.y = random.randint(100, HEIGHT - 100)

    # Рисуем игрока
    pygame.draw.rect(screen, RED, player)

    # Отображаем счетчик монет
    score_text = font.render(f'Монеты: {coin_count}', True, BLACK)
    screen.blit(score_text, (10, 10))

    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)
