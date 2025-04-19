import pygame
import pymunk
import random
import time
import pygame

from perso import *
from globals import*
from menu import *
from jeu import *
from Reglage import *

space = pymunk.Space()


def main():

    while True:
        action = menu()

        if action == "niveau1":
            jeu(1)
        elif action == "niveau2":
            jeu(2)
        elif action == "niveau3":
            jeu(3)
        elif action == "reglage":
            reglages()

        elif action == "quitter":
            break

    pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()