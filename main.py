import pygame
import pymunk
import random
import time
from perso import bird

pygame.init()


WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

if __name__ == "__main__":
    main()
    pygame.quit()

