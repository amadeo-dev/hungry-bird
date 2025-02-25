import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu Pygame")

BLACK = (0, 0, 0)
RED = (255, 0, 0)


player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5


running = True
while running:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed



    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW, RED, (player_x, player_y, player_size, player_size))
    pygame.display.update()

pygame.quit()
