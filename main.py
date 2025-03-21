import pygame
import pymunk
import random
import time
from perso import tete

pygame.init()

WIDTH, HEIGHT = 1280, 720

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

# Initialisation de Pymunk
space = pymunk.Space()
space.gravity = (0, 900)

# Variables globales
personnages = []
hotdog_positions = []
burger_positions = []
brocoli_positions = []
dinde_positions = []
running = True
score = 0
current_level = 1
current_bird_index = 0
start_pos = None
game_over = False
end_game_time = None

def create_birds():
    """Crée les 3 oiseaux au début du jeu."""
    personnages.clear()
    for i in range(5):
        personnage = personnage((150 + i * 60, HEIGHT - 60))  # Oiseaux à gauche
        personnages.append(personnage)


def load_music():
    """Load the music"""
    song1 = '../resources/sounds/angry-birds.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)