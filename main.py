import pygame
import pymunk
import random
import time
from Constantes import *
from perso import *

pygame.init()
pygame.font.init()

from perso import *

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

def main():
    while True:
        create_birds()

if __name__ == "__main__":
    main()
    pygame.quit()