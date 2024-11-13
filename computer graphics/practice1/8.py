import pygame
import numpy as np

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Task 8")

triangle = np.array([[8, 1], [7, 3], [6, 2]]) * 35
T = np.array([[0, 1], [1, 0]])  

reflected_triangle = (T @ triangle.T).T + np.array([300, 300])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.polygon(screen, (255, 0, 0), triangle + [300, 300], 3)  
    pygame.draw.polygon(screen, (0, 255, 0), reflected_triangle, 3)

    pygame.display.flip()

pygame.quit()
