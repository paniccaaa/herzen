import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Загрузка и масштабирование изображения корабля
        self.image = pygame.image.load('ship.bmp')
        self.image = pygame.transform.scale(self.image, (50, 50))  # Масштабируем до 50x50
        
        # Устанавливаем белый цвет как прозрачный
        self.image.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()
        self.screen_rect = ai_game.screen.get_rect()

        # Изначально расположение корабля внизу по центру
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        # Флаги движения
        self.moving_right = False
        self.moving_left = False

        # Количество жизней корабля
        self.lives = 3  # Начинаем с 3 жизнями

    def update(self):
        """Обновляет позицию корабля в зависимости от флагов движения."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        """Отображает корабль на экране."""
        self.screen.blit(self.image, self.rect)

    def hit(self):
        """Обрабатывает столкновение с инопланетянином."""
        self.lives -= 1  # Уменьшаем количество жизней
        if self.lives <= 0:
            return True  # Возвращаем True, если жизни закончились
        else:
            # Возвращаем корабль в начальное положение после столкновения
            self.rect.midbottom = self.screen_rect.midbottom
            self.x = float(self.rect.x)
            return False
