import pygame
import pymunk

bird_images = {}
bird_name = ['Jacky', 'Thomas', 'Adrien', 'Nicolas', 'Amadeo' ]
WIDTH, HEIGHT = 1280, 720
physique = pymunk.Space()
physique.gravity = (0,900)
HOTDOG_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/hotdog.png"), (50, 30))
BURGER_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/burger.png"), (50, 50))
BROCOLI_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/brocolis.png"), (40, 40))
DINDE_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Dinde Royale.png"), (60, 60))
RESTART_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Restart.png"), (50, 50))
DECORS_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/decor.png"), (WIDTH, HEIGHT))
