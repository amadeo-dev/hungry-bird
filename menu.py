import pygame
from Constantes import *
from map import *
#from perso import select_team
#pygame.init()

#pygame.display.set_caption("Bouton avec image")
menu_running = False

fond = pygame.image.load(f"Ressources/image/intro_bck2.png")
fond = pygame.transform.scale(fond, (1280, 720))

bouton_Tutoriel = pygame.image.load(f"Ressources/image/hotdog.png")
bouton_Tutoriel = pygame.transform.scale(bouton_Tutoriel, (150, 50))
button_rect = bouton_Tutoriel.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))


bouton_Nv1 = pygame.image.load(f"Ressources/image/Nicolas.png")
bouton_Nv1 = pygame.transform.scale(bouton_Nv1, (150, 50))
button_rect2 = bouton_Nv1.get_rect(center=(WIDTH // 2, HEIGHT //2))


bouton_Nv2 = pygame.image.load(f"Ressources/image/burger.png")
bouton_Nv2 = pygame.transform.scale(bouton_Nv2, (150, 50))
button_rect3 = bouton_Nv2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

bouton_Nv3 = pygame.image.load(f"Ressources/image/Ash.png")
bouton_Nv3 = pygame.transform.scale(bouton_Nv3, (150, 50))
button_rect4 = bouton_Nv3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

bouton_Reglage = pygame.image.load(f"Ressources/image/Amadeo.png")
bouton_Reglage = pygame.transform.scale(bouton_Reglage, (150, 50))
button_rect5 = bouton_Reglage.get_rect(center=(WIDTH // 1 - 150, HEIGHT // 8 - 10))

bouton_quitter = pygame.image.load(f"Ressources/image/Dinde Royale.png")
bouton_quitter = pygame.transform.scale(bouton_quitter, (150, 50))
button_rect6 = bouton_quitter.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 300))



running = True
while running:
    screen.fill((50, 50, 50))
    screen.blit(fond, (0,0))
    screen.blit(bouton_Tutoriel, button_rect)
    screen.blit(bouton_Nv1, button_rect2)
    screen.blit(bouton_Nv2, button_rect3)
    screen.blit(bouton_Reglage, button_rect5)
    screen.blit(bouton_Nv3, button_rect4)
    screen.blit(bouton_quitter, button_rect6)

# Gestion des événements

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect6.collidepoint(event.pos):
                pygame.quit()
                exit()
            #if button_rect5.collidepoint(event.pos):
             #   select_team()
              #  exit()




    #for event in pygame.event.get():
     #   if event.type == pygame.QUIT:
      #      running = False

    pygame.display.flip()

pygame.quit()
