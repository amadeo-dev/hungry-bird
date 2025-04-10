import pygame
from Constantes import *
from globals import*
from perso import *

pygame.display.set_caption("Bouton avec image")

fond = pygame.transform.scale(fond, (1280, 720))

def create_button(nom, x, y, tx=150, ty=50):
    bouton = pygame.image.load(f"Ressources/image/{nom}.png")
    return pygame.transform.scale(bouton, (tx, ty)), bouton.get_rect(center=(x, y))

# Boutons
bouton_Tutoriel, button_rect1 = create_button('hotdog', WIDTH // 2, HEIGHT // 2 - 150)
bouton_niveau1, button_rect2 = create_button('select_team_ic', WIDTH // 2, HEIGHT // 2 -200)
bouton_niveau2, button_rect3 = create_button('select_team_ic', WIDTH // 2, HEIGHT // 2)
bouton_niveau3, button_rect4 = create_button('select_team_ic', WIDTH // 2, HEIGHT // 2 +200)
bouton_quitter, button_rect5 = create_button('exit', WIDTH - 100, HEIGHT -50)
bouton_Reglage, button_rect6 = create_button('reglage_ic', WIDTH - 100, 50, tx=96, ty=96)

def menu():
    while True:
        screen.blit(fond, (0, 0))
        screen.blit(bouton_Tutoriel, button_rect1)
        screen.blit(bouton_niveau1, button_rect2)
        screen.blit(bouton_niveau2, button_rect3)
        screen.blit(bouton_niveau3, button_rect4)
        screen.blit(bouton_quitter, button_rect5)
        screen.blit(bouton_Reglage, button_rect6)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect2.collidepoint(event.pos):
                    return "niveau1"
                elif button_rect3.collidepoint(event.pos):
                    return "niveau2"
                elif button_rect4.collidepoint(event.pos):
                    return "niveau3"
                elif button_rect5.collidepoint(event.pos):
                    return "quitter"
                elif button_rect6.collidepoint(event.pos):
                    return "reglage"

        pygame.display.flip()