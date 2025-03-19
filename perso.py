import pygame
import pymunk


class personnage():
    def __init__(self,name, img):
        self.name = name
        self.img = img
        self.body = pymunk.Body()