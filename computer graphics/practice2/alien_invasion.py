import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Инопланетное вторжение")

        # Загрузка фонового изображения
        self.bg_image = pygame.image.load('background.png')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Добавляем атрибут для счёта
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)  # Шрифт для отображения счёта и "Game Over"

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            # Добавляем 10 очков за каждого уничтоженного инопланетянина
            self.score += 10 * len(collisions)
        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()  # Увеличиваем скорость
            self._create_fleet()

    def _update_aliens(self):
        self.aliens.update()
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._game_over()  # Конец игры при столкновении
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._game_over()  # Конец игры, если инопланетянин дошёл до низа экрана

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Отображаем фоновое изображение
        self.screen.blit(self.bg_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Отображаем счёт
        self._display_score()
        
        pygame.display.flip()

    def _display_score(self):
        """Отображает текущий счёт в углу экрана."""
        score_str = f"Score: {self.score}"
        score_image = self.font.render(score_str, True, (255, 255, 255))
        self.screen.blit(score_image, (20, 20))

    def _game_over(self):
        """Отображение сообщения 'Game Over' с финальным счётом и завершение игры."""
        self.screen.blit(self.bg_image, (0, 0))  # Перерисовываем фон
        game_over_str = f"Game Over! Final Score: {self.score}"
        game_over_image = self.font.render(game_over_str, True, (255, 0, 0))
        self.screen.blit(game_over_image, (self.settings.screen_width // 2 - 150, self.settings.screen_height // 2))
        
        pygame.display.flip()
        pygame.time.wait(2000)  # Пауза на 2 секунды, чтобы игрок увидел счёт
        sys.exit()  # Завершаем игру

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()