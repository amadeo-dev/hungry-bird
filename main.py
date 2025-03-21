import pygame
import pymunk
import random
import time
from perso import Tete

pygame.init()

# Dimensions de l'écran
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

# Initialisation de Pymunk
space = pymunk.Space()
space.gravity = (0, 900)

# Chargement des images
bird_images = {
    'jacky': pygame.image.load('Ressources/image/asch.png'),
    'thomas': pygame.image.load('Ressources/image/thomas.png'),
    'adrien': pygame.image.load('Ressources/image/adrien.png'),
    'nicolas': pygame.image.load('Ressources/image/nicolas.png'),
    'amadeo': pygame.image.load('Ressources/image/amadeo.png')
}

# Variables globales
personnages = []
running = True
score = 0
current_level = 1
current_bird_index = 0
start_pos = None
game_over = False
end_game_time = None

def create_birds():
    """Crée 5 oiseaux au début du jeu."""
    personnages.clear()
    noms_tete = ['jacky', 'thomas', 'adrien', 'nicolas', 'amadeo']
    for i in range(5):
        img = bird_images[noms_tete[i]]
        personnage = Tete(noms_tete[i], img, (150 + i * 60, HEIGHT - 60))
        personnages.append(personnage)

def load_music():
    """Charge la musique du jeu."""
    song1 = 'Ressources/sounds/angry-birds.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)  # Correction du bug ici

# Lancement de la musique et création des oiseaux
load_music()
create_birds()

# Boucle principale du jeu
clock = pygame.time.Clock()
while running:
    screen.fill((135, 206, 235))  # Fond bleu ciel

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessiner les oiseaux
    for bird in personnages:
        bird.draw(screen)

    # Mettre à jour la physique
    space.step(1 / 60.0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()