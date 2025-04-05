import pygame
import pymunk
import random
import time
from perso import *
from Constantes import *
from menu import *
import pygame

pygame.init()
pygame.font.init()

space = pymunk.Space()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Hungry Bird")


def main():

    while True:
        action = menu()  # récupère l'action choisie dans le menu

        if action == "select_team":
            create_birds()
            select_team()
            break
            #print(f"Équipe sélectionnée ({len(selec_trois)}/3) : {[b.name for b in selec_trois]}")

        elif action == "reglage":
            print("Afficher les réglages (fonction à coder)")

        elif action == "quitter":
            break


    pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()