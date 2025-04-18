import pygame
from Constantes import *
from globals import *
from perso import *

pygame.display.set_caption("Menu")

fond = pygame.image.load("Ressources/image/Menu/Decors.png")
fond = pygame.transform.scale(fond, (screen_width, screen_height))



def create_button(nom, x, y, tx, ty):
    bouton = pygame.image.load(f"Ressources/image/Menu/{nom}.png")
    return pygame.transform.scale(bouton, (tx, ty)), bouton.get_rect(center=(x, y))

# Boutons
bouton_Tutoriel, button_rect1 = create_button('Tutoriel', ajustx(1450), ajusty(980), tx=ajustx(285), ty=ajusty(203))
bouton_niveau1, button_rect2 = create_button('Nv1', ajustx(1050), ajusty(470), tx=ajustx(520), ty=ajusty(188))
bouton_niveau2, button_rect3 = create_button('Nv2', ajustx(1080), ajusty(640), tx=ajustx(520), ty=ajusty(188))
bouton_niveau3, button_rect4 = create_button('Nv3', ajustx(1050), ajusty(810), tx=ajustx(520), ty=ajusty(188))
bouton_quitter, button_rect5 = create_button('Quitter',  ajustx(200), ajusty(760), tx=ajustx(247), ty=ajusty(247))
bouton_Reglage, button_rect6 = create_button('Reglages', ajustx(570), ajusty(980), tx=ajustx(325), ty=ajusty(235))


def menu():
    while True:
        screen.blit(fond, (ajustx(0), ajusty(0)))
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
                #elif button_rect1.collidepoint(event.pos):
                #    return ("tutoriel")

        pygame.display.flip()