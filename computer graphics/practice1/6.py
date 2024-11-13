import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Task 6")

lines = np.array([[-0.5, 1.5], [3, -2], [-1, -1], [3, 5/3]]) * 100

T = np.array([[1, 2], [1, -3]])

transformed_lines = (T @ lines.T).T + np.array([300, 300])  # смещаем в видимую область

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.line(screen, (255, 0, 0), lines[0], lines[1], 3)
    pygame.draw.line(screen, (255, 0, 0), lines[2], lines[3], 3)

    pygame.draw.line(screen, (0, 255, 0), transformed_lines[0], transformed_lines[1], 3)
    pygame.draw.line(screen, (0, 255, 0), transformed_lines[2], transformed_lines[3], 3)

    pygame.display.flip()

pygame.quit()
