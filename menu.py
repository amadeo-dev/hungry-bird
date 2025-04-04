import pygame
from Constantes import *
from map import *
from perso import select_team
#pygame.init()

#pygame.display.set_caption("Bouton avec image")
menu_running = False

fond = pygame.image.load(f"Ressources/image/intro_bck2.png")
fond = pygame.transform.scale(fond, (1280, 720))

def create_button(nom, x, y):
    bouton = pygame.image.load(f"Ressources/image/{nom}.png")
    return pygame.transform.scale(bouton, (150, 50)), bouton.get_rect(center=(x, y))

bouton_Tutoriel, button_rect1 = create_button('hotdog', WIDTH // 2, HEIGHT // 2 - 100)
bouton_Nv1, button_rect2 = create_button('Nicolas', WIDTH // 2, HEIGHT // 2)
bouton_Nv2, button_rect3 = create_button('burger', WIDTH // 2, HEIGHT // 2 + 100)
bouton_Nv3, button_rect4 = create_button('Ash', WIDTH // 2, HEIGHT // 2 + 200)
bouton_Reglage, button_rect5 = create_button('Amadeo', WIDTH // 1 - 150, HEIGHT // 8 - 10)
bouton_quitter, button_rect6 = create_button('Dinde_Royale', WIDTH // 2, HEIGHT // 2 + 300)

def menu():
    running = True
    while running:
        screen.blit(fond, (0, 0))

        screen.blit(bouton_Tutoriel, button_rect1)
        screen.blit(bouton_Nv1, button_rect2)
        screen.blit(bouton_Nv2, button_rect3)
        screen.blit(bouton_Nv3, button_rect4)
        screen.blit(bouton_Reglage, button_rect5)
        screen.blit(bouton_quitter, button_rect6)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect6.collidepoint(event.pos):
                    running = False
                # if button_rect5.collidepoint(event.pos):
                #     select_team()
                #     running = False

        pygame.display.flip()

    pygame.quit()