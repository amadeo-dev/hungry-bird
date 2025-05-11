import pygame
import pymunk
import random
import time
import pygame

# Imports des différents modules du projet
from perso import *
from globals import *
from menu import *
from jeu import *
from Reglage import *

def main():
    # Boucle principale du jeu
    while True:
        action = menu()  # Affiche le menu principal et récupère l'action choisie

        if action == "niveau1":
            result = jeu(1)  # Lance le niveau 1
            if result == "menu":
                continue  # Si le joueur revient au menu, on relance la boucle

        elif action == "niveau2":
            result = jeu(2)  # Niveau 2
            if result == "menu":
                continue

        elif action == "niveau3":
            result = jeu(3)  # Niveau 3
            if result == "menu":
                continue

        elif action == "reglage":
            reglages()  # Ouvre le menu de réglages

        elif action == "quitter":
            break  # Sortie du jeu

    # Une fois sorti de la boucle, on coupe la musique et on quitte pygame proprement
    pygame.mixer.music.stop()
    pygame.quit()

# Point d’entrée du programme
if __name__ == "__main__":
    main()
    pygame.quit()

