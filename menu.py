import pygame
from globals import *
from perso import *
from tutoriel import lancer_tutoriel
from Reglage import *

pygame.display.set_caption("Menu")

fond = pygame.image.load("Ressources/image/Menu/Decors.png")
fond = pygame.transform.scale(fond, (screen_width, screen_height))





def menu():
    clock = pygame.time.Clock()
    mouse_was_down = False

    while True:
        screen.blit(fond, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for nom, bouton in boutons.items():
            img, rect = bouton.update(mouse_pos, mouse_pressed)
            screen.blit(img, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

        # Détection du relâchement du clic
        if mouse_was_down and not mouse_pressed:
            for nom, bouton in boutons.items():
                if bouton.rect.collidepoint(mouse_pos):
                    # Animation du bouton
                    for _ in range(5):
                        screen.blit(fond, (0, 0))
                        for n, b in boutons.items():
                            img, rect = b.update(mouse_pos, False)
                            screen.blit(img, rect)
                        pygame.display.flip()
                        clock.tick(60)
                    pygame.time.delay(100)

                    # Action selon le bouton
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

        mouse_was_down = mouse_pressed

        pygame.display.flip()
        clock.tick(60)
