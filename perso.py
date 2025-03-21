import pygame
import pymunk
from pymunk import Vec2d
from main import *

# Chargement des images
jacky_IMG = pygame.image.load("Ressources/image/Jacky.png")
thomas_IMG = pygame.image.load("Ressources/image/Jacky.png")
adrien_IMG = pygame.image.load("Ressources/image/Jacky.png")
nicolas_IMG = pygame.image.load("Ressources/image/Jacky.png")
amadeo_IMG = pygame.image.load("Ressources/image/Jacky.png")

class tete():
    def __init__(self,name, img, position):
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        space.add(self.body, self.shape)
        self.size = 70
        self.launched = False