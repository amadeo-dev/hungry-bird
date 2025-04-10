import pygame
import pymunk
import random
import time
import pygame

from perso import *
from Constantes import *
from globals import*
from menu import *
from jeu import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
space = pymunk.Space()


fond = pygame.image.load("Ressources/image/intro_bck2.png")
fond = pygame.transform.scale(fond, (WIDTH, HEIGHT))
DECORS = pygame.transform.scale(pygame.image.load("Ressources/image/decor.png"), (WIDTH, HEIGHT))


def main():

    while True:
        action = menu()  # récupère l'action choisie dans le menu

        if action == "niveau1":
            jeu(1)
        elif action == "niveau2":
            jeu(2)
        elif action == "niveau3":
            jeu(3)
        elif action == "reglage":
            print("Afficher les réglages (fonction à coder)")

        elif action == "quitter":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()