import pygame
import pymunk

bird_images = {
    'jacky': pygame.image.load('Ressources/image/Jacky.png'),
    'thomas': pygame.image.load('Ressources/image/Thomas.png'),
    'adrien': pygame.image.load('Ressources/image/Adrien.png'),
    'nicolas': pygame.image.load('Ressources/image/Nicolas.png'),
    'amadeo': pygame.image.load('Ressources/image/Amadeo.png')
}

class Tete:
    def __init__(self, name, img, position, space):
