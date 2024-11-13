import pygame
import math

pygame.init()
screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Спираль в виде улитки Паскаля")

background_color = (255, 255, 255)
spiral_color = (0, 0, 0)

a = 50  
b = 30  
theta_max = 12 * math.pi  

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)

    for theta in range(0, int(theta_max * 100)):
        theta_rad = theta / 100  
        r = b + 2 * a * math.cos(theta_rad)
        x = int(r * math.cos(theta_rad)) + screen_size[0] // 2  
        y = int(r * math.sin(theta_rad)) + screen_size[1] // 2  

        # Ограничиваем координаты в пределах экрана
        if 0 <= x < screen_size[0] and 0 <= y < screen_size[1]:
            screen.set_at((x, y), spiral_color)  

    pygame.display.flip()

pygame.quit()
