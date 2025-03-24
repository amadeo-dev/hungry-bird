import pygame
import pymunk


WIDTH, HEIGHT = 1280, 720
physique = pymunk.Space()
physique.gravity = (0,900)