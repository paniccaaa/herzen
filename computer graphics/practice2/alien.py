# alien.py

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Загрузка и масштабирование изображения инопланетянина
        self.image = pygame.image.load('alien.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (50, 50))  
        
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
