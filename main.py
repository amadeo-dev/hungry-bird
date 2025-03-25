import pygame
import pymunk
import random
import time


pygame.init()
pygame.font.init()

from perso import *
from Constantes import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

def main():
    while True:
        create_birds()

if __name__ == "__main__":
    main()
    pygame.quit()