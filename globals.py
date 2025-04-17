import pygame
import pymunk

pygame.init()
pygame.font.init()

# Initialisation écran
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Hungry Bird")

# Espace physique
space = pymunk.Space()
space.gravity = (0, 900)

# Couleurs
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 200, 0), (0, 0, 0)

# Autres constantes
BIRD_SIZE_DEFAULT = 50
MAX_SPEED = 1000
GRAVITY = (0, 900)
MIN_DISTANCE = 50

#SON
miam_sound = pygame.mixer.Sound("Ressources/Sons/Amadéo - slurp 2.wav")
lance_sound = pygame.mixer.Sound("Ressources/Sons/Amadéo - Yahoo.wav")
menu_sound = pygame.mixer.Sound("Ressources/Sons/Thomas - mhmhmh 2.wav")

# Images mises à l’échelle dynamiquement
HOTDOG_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/hotdog.png"), (50, 30))
BURGER_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/burger.png"), (50, 50))
BROCOLI_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/brocolis.png"), (40, 40))
DINDE_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Dinde_Royale.png"), (60, 60))
RESTART_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Restart.png"), (50, 50))

# Décor mis à l’échelle à la taille de l’écran
DECORS_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/bck_lvl1.jpg"), (screen_width, screen_height))

# Position catapulte (utilise screen_height au lieu de HEIGHT)
CATAPULT_POS = (150, screen_height - 100)

# Variables globales du jeu
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