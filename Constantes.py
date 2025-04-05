import pygame
import pymunk

# Dimensions
WIDTH, HEIGHT = 1280, 720

# Espace physique
physique = pymunk.Space()
physique.gravity = (0, 900)
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 200, 0), (0, 0, 0)

# Noms des oiseaux, equipe selectionnée
bird_name = ['Jacky', 'Thomas', 'Adrien', 'Nicolas', 'Amadeo']

# Images
DECORS = pygame.transform.scale(pygame.image.load("Ressources/image/decor.png"), (WIDTH, HEIGHT))
fond = pygame.image.load(f"Ressources/image/intro_bck2.png")

# Paramètres du jeu
BIRD_SIZE_DEFAULT = 50
MAX_SPEED = 1000
MIN_DISTANCE = 50