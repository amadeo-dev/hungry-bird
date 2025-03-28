import pygame

from Constantes import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def create_bordures():
    """Crée les bordures gauche, droite et bas du jeu et les ajoute directement à space."""
    left_border = pymunk.Segment(physique.static_body, (0, 0), (0, HEIGHT), 5)
    right_border = pymunk.Segment(physique.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5)
    bottom_border = pymunk.Segment(physique.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 5)

    # Définir directement l'élasticité
    left_border.elasticity = right_border.elasticity =  0.8
    bottom_border.elasticity = 0.3 # Ajouter les bordures au moteur physique
    physique.add(left_border, right_border, bottom_border)