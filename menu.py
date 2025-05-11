import pygame
from globals import *
from perso import *
from tutoriel import lancer_tutoriel
from Reglage import *

# Configuration de la fenêtre
pygame.display.set_caption("Menu")

# Chargement et mise à l’échelle du fond du menu
fond = pygame.image.load("Ressources/image/Menu/Decors.png")
fond = pygame.transform.scale(fond, (screen_width, screen_height))


def menu():
    clock = pygame.time.Clock()
    mouse_was_down = False  # Pour détecter un clic relâché (et pas juste un clic tenu)

    while True:
        # Affichage du fond
        screen.blit(fond, (0, 0))

        # Position de la souris + état du clic
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # clique gauche

        # Mise à jour des boutons en fonction de la souris
        for nom, bouton in boutons.items():
            img, rect = bouton.update(mouse_pos, mouse_pressed)
            screen.blit(img, rect)

        # Gestion des événements (fermeture de la fenêtre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

        # Si on vient de relâcher le clic
        if mouse_was_down and not mouse_pressed:
            for nom, bouton in boutons.items():
                if bouton.rect.collidepoint(mouse_pos):
                    # Animation rapide du bouton cliqué
                    for _ in range(5):
                        screen.blit(fond, (0, 0))
                        for n, b in boutons.items():
                            img, rect = b.update(mouse_pos, False)
                            screen.blit(img, rect)
                        pygame.display.flip()
                        clock.tick(60)
                    pygame.time.delay(100)  # petite pause après clic

                    # Lancer l’action associée au bouton
                    if nom == "tutoriel":
                        lancer_tutoriel(screen)
                    elif nom == "quitter":
                        return "quitter"
                    elif nom == "niveau1":
                        return "niveau1"
                    elif nom == "niveau2":
                        return "niveau2"
                    elif nom == "niveau3":
                        return "niveau3"
                    elif nom == "reglage":
                        return reglages()

        # Mise à jour de l’état précédent du clic pour détecter le relâchement
        mouse_was_down = mouse_pressed

        pygame.display.flip()
        clock.tick(60)  # limite la boucle à 60 FPS

