import pygame
import pymunk
import random
import time
from perso import *
from Constantes import *
from menu import *

pygame.init()
pygame.font.init()



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

def main():
    while True:
        menu()
        create_birds()
        team = select_team()


if __name__ == "__main__":
    main()
    pygame.quit()