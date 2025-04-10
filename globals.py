# globals.py

import pygame
import pymunk
from Constantes import WIDTH, HEIGHT

pygame.init()
pygame.font.init()

# Fenêtre et affichage
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

# Espace physique
space = pymunk.Space()
space.gravity = (0, 900)

# Font principale
font = pygame.font.Font(None, 58)


# Fonds d'écran
fond = pygame.image.load("Ressources/image/intro_bck2.png")
fond = pygame.transform.scale(fond, (WIDTH, HEIGHT))

DECORS = pygame.transform.scale(pygame.image.load("Ressources/image/decor.png"), (WIDTH, HEIGHT))