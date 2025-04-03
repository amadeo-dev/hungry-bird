import pygame
import pymunk

# Dimensions
WIDTH, HEIGHT = 1280, 720

# Espace physique
physique = pymunk.Space()
physique.gravity = (0, 900)
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 200, 0), (0, 0, 0)

# Noms des oiseaux
bird_name = ['Jacky', 'Thomas', 'Adrien', 'Nicolas', 'Amadeo']

# Images
HOTDOG = pygame.transform.scale(pygame.image.load("Ressources/image/hotdog.png"), (50, 30))
BURGER = pygame.transform.scale(pygame.image.load("Ressources/image/burger.png"), (50, 50))
BROCOLI = pygame.transform.scale(pygame.image.load("Ressources/image/brocolis.png"), (40, 40))
DINDE = pygame.transform.scale(pygame.image.load("Ressources/image/Dinde Royale.png"), (60, 60))
RESTART = pygame.transform.scale(pygame.image.load("Ressources/image/Restart.png"), (50, 50))
DECORS = pygame.transform.scale(pygame.image.load("Ressources/image/decor.png"), (WIDTH, HEIGHT))

# Paramètres du jeu
BIRD_SIZE_DEFAULT = 50
MAX_SPEED = 1000
MIN_DISTANCE = 50