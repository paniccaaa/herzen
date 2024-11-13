import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Task 3")

line_start = np.array([100, 150])
line_end = np.array([200, 250])

T = np.array([[1, 3], [4, 1]])

transformed_start = T @ line_start
transformed_end = T @ line_end

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.line(screen, (255, 0, 0), line_start, line_end, 3)  # Исходный отрезок
    pygame.draw.line(screen, (0, 255, 0), transformed_start, transformed_end, 3)  # Преобразованный отрезок
    pygame.display.flip()

pygame.quit()
