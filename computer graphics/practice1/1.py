import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Task 1")

point = np.array([10, 20])  
T = np.array([[1, 3], [4, 1]])  

transformed_point = T @ point

print(f"Начальные координаты: {point}")
print(f"Преобразованные координаты: {transformed_point}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (255, 0, 0), point, 5)  # Исходная точка (красная)
    pygame.draw.circle(screen, (0, 255, 0), transformed_point, 5)  # Преобразованная точка (зеленая)

    pygame.display.flip()

pygame.quit()
