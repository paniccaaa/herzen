import pygame
import numpy as np
import math

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Task 11")

square = np.array([[2, -2], [-2, -2], [-2, 2], [2, 2]]) * 50
scale_factor = 0.9
angle = math.pi / 32

center = np.array([300, 300])

running = True
for _ in range(20):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    scale_matrix = np.array([[scale_factor, 0], [0, scale_factor]])
    rotation_matrix = np.array([[math.cos(angle), -math.sin(angle)],
                                [math.sin(angle), math.cos(angle)]])

    square = (rotation_matrix @ scale_matrix @ square.T).T

    pygame.draw.polygon(screen, (0, 0, 255), square + center, 3)
    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
