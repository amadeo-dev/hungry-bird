import pygame

# Initialisation de Pygame
#pygame.init()

# Création de la fenêtre
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Bouton avec image")

fond = pygame.image.load(f"Ressources/image/selec_bckg.jpg")
fond = pygame.transform.scale(fond, (1280, 720))

#créaion bouton
niveau_1 = pygame.image.load(f"Ressources/image/hotdog.png")
niveau_1 = pygame.transform.scale(niveau_1, (150, 50))
button_rect = niveau_1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))


niveau_2 = pygame.image.load(f"Ressources/image/Nicolas.png")
niveau_2 = pygame.transform.scale(niveau_2, (150, 50))
button_rect2 = niveau_2.get_rect(center=(WIDTH // 2, HEIGHT //2))


niveau_3 = pygame.image.load(f"Ressources/image/burger.png")
niveau_3 = pygame.transform.scale(niveau_3, (150, 50))
button_rect3 = niveau_3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

quitter = pygame.image.load(f"Ressources/image/Amadeo.png")
quitter = pygame.transform.scale(quitter, (150, 50))
button_rect4 = quitter.get_rect(center=(WIDTH // 1 - 60, HEIGHT // 8 - 50))

menu = pygame.image.load(f"Ressources/image/Ash.png")
menu = pygame.transform.scale(menu, (150, 50))
button_rect5 = menu.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))


#
running = True
while running:
    screen.fill((50, 50, 50))
    screen.blit(fond, (0,0))
    screen.blit(niveau_1, button_rect)
    screen.blit(niveau_2, button_rect2)
    screen.blit(niveau_3, button_rect3)
    screen.blit(quitter, button_rect4)
    screen.blit(menu, button_rect5)

# Gestion des événements
for event in pygame.event.get():
    if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if quitter.collidepoint(event.pos):
            pygame.quit()
            exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_rect2.collidepoint(event.pos):
            print("Bouton cliqué !")

pygame.display.flip()

pygame.quit()
