import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Task 2")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (255, 0, 0), (300, 300), 50)  # Красная окружность
    pygame.draw.line(screen, (0, 255, 0), (50, 50), (550, 50), 5)  # Зеленая линия
    pygame.draw.line(screen, (0, 0, 255), (50, 100), (550, 100), 5)  # Синяя линия

    font = pygame.font.SysFont(None, 48)
    text = font.render("Hello, Pygame!", True, (0, 0, 0))  # Текст
    screen.blit(text, (150, 200))

    pygame.display.flip()

pygame.quit()
