import pygame
from Constantes import *
from map import *
#pygame.init()

#pygame.display.set_caption("Bouton avec image")

fond = pygame.image.load(f"Ressources/image/selec_bck.jpg")
fond = pygame.transform.scale(fond, (1280, 720))

bouton_1 = pygame.image.load(f"Ressources/image/hotdog.png")
bouton_1 = pygame.transform.scale(bouton_1, (150, 50))
button_rect = bouton_1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))


bouton_2 = pygame.image.load(f"Ressources/image/Nicolas.png")
bouton_2 = pygame.transform.scale(bouton_2, (150, 50))
button_rect2 = bouton_2.get_rect(center=(WIDTH // 2, HEIGHT //2))


bouton_3 = pygame.image.load(f"Ressources/image/burger.png")
bouton_3 = pygame.transform.scale(bouton_3, (150, 50))
button_rect3 = bouton_3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

bouton_4 = pygame.image.load(f"Ressources/image/Amadeo.png")
bouton_4 = pygame.transform.scale(bouton_4, (150, 50))
button_rect4 = bouton_4.get_rect(center=(WIDTH // 1 - 60, HEIGHT // 8 - 50))

bouton_5 = pygame.image.load(f"Ressources/image/Ash.png")
bouton_5 = pygame.transform.scale(bouton_5, (150, 50))
button_rect5 = bouton_5.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))



running = True
while running:
    screen.fill((50, 50, 50))
    screen.blit(fond, (0,0))
    screen.blit(bouton_1, button_rect)
    screen.blit(bouton_2, button_rect2)
    screen.blit(bouton_3, button_rect3)
    screen.blit(bouton_4, button_rect4)
    screen.blit(bouton_5, button_rect5)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect2.collidepoint(event.pos):
                print("Bouton cliqué !")

    pygame.display.flip()

pygame.quit()
