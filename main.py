import pygame
import pymunk
import random
import time
from perso import *
from Constantes import *
from menu import *

pygame.init()
pygame.font.init()

space = pymunk.Space()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")



def main():
    while True:
        action = menu()  # On récupère l'action choisie dans le menu
        if action == "select_team":
            create_birds()
            selec_trois.clear()  # Réinitialise la sélection précédente
            selection_running = True  # Active la boucle de sélection
            # Lance la sélection
            select_team()
            print(f"Équipe sélectionnée ({len(selec_trois)}/3) : {[b.name for b in selec_trois]}")


        elif action == "reglage":
            print("Afficher les réglages (fonction à coder)")

        elif action == "quitter" or action is None:
            break  # Quitte le jeu

    pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()