# globals.py

import pygame
import pymunk
from Constantes import WIDTH, HEIGHT

pygame.init()
pygame.font.init()

# Fenêtre et affichage
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

# Espace physique
space = pymunk.Space()
space.gravity = (0, 900)


#SON
miam_sound = pygame.mixer.Sound("Ressources/Sons/Amadéo - slurp 2.wav")
lance_sound = pygame.mixer.Sound("Ressources/Sons/Amadéo - Yahoo.wav")
menu_sound = pygame.mixer.Sound("Ressources/Sons/Thomas - mhmhmh 2.wav")

WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 200, 0), (0, 0, 0)
BIRD_SIZE_DEFAULT = 50
MAX_SPEED = 1000
GRAVITY = (0, 900)
MIN_DISTANCE = 50

#temporaire vs me degagez ça

HOTDOG_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/hotdog.png"), (50, 30))
BURGER_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/burger.png"), (50, 50))
BROCOLI_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/brocolis.png"), (40, 40))
DINDE_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Dinde_Royale.png"), (60, 60))
RESTART_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Restart.png"), (50, 50))

DECORS_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/bck_lvl1.jpg"), (WIDTH, HEIGHT))

screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h



birds = []
hotdog_positions = []
burger_positions = []
brocoli_positions = []
dinde_positions = []
selected_team = []
running = True
score = 0
current_level = 1
current_bird_index = 0
start_pos = None
game_over = False
end_game_time = None