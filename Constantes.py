import pygame
import pymunk

bird_images = {}
bird_name = ['Jacky', 'Thomas', 'Adrien', 'Nicolas', 'Amadeo' ]
WIDTH, HEIGHT = 1280, 720
physique = pymunk.Space()
physique.gravity = (0,900)
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 200, 0), (0, 0, 0)

HOTDOG = pygame.transform.scale(pygame.image.load("Ressources/image/hotdog.png"), (50, 30))
BURGER = pygame.transform.scale(pygame.image.load("Ressources/image/burger.png"), (50, 50))
BROCOLI = pygame.transform.scale(pygame.image.load("Ressources/image/brocolis.png"), (40, 40))
DINDE = pygame.transform.scale(pygame.image.load("Ressources/image/Dinde Royale.png"), (60, 60))
RESTART = pygame.transform.scale(pygame.image.load("Ressources/image/Restart.png"), (50, 50))
DECORS = pygame.transform.scale(pygame.image.load("Ressources/image/decor.png"), (WIDTH, HEIGHT))