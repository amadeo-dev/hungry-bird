
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


def main():
    while True:
        action = menu()

        if action == "niveau1":
            result = jeu(1)
            if result == "menu":
                continue  # Revenir au menu principal
        elif action == "niveau2":
            result = jeu(2)
            if result == "menu":
                continue
        elif action == "niveau3":
            result = jeu(3)
            if result == "menu":
                continue
        elif action == "reglage":
            reglages()
        elif action == "quitter":
            break

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
    pygame.quit()