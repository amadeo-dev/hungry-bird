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

# dico avc les images
bird_images = {
    'jacky': pygame.image.load('Ressources/image/Jacky.png'),
    'thomas': pygame.image.load('Ressources/image/Thomas.png'),
    'adrien': pygame.image.load('Ressources/image/Adrien.png'),
    'nicolas': pygame.image.load('Ressources/image/Nicolas.png'),
    'amadeo': pygame.image.load('Ressources/image/Amadeo.png')
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


def cree_bord   ():
    thickness = 10
    elasticity = 0.8

    # Sol
    ground = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), thickness)
    ground.elasticity = elasticity
    ground.friction = 0.5

    # Murs gauche et droit
    left_wall = pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), thickness)
    left_wall.elasticity = elasticity
    left_wall.friction = 0.5

    right_wall = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), thickness)
    right_wall.elasticity = elasticity
    right_wall.friction = 0.5

    # Ajouter au space
    space.add(ground, left_wall, right_wall)


def create_birds():
    """Crée 5 oiseaux au début du jeu."""
    personnages.clear()
    noms_tete = ['jacky', 'thomas', 'adrien', 'nicolas', 'amadeo']
    for i in range(5):
        img = bird_images[noms_tete[i]]
        personnage = Tete(noms_tete[i], img, (150 + i * 60, HEIGHT - 60), space)
        personnages.append(personnage)


def load_music():
    """Charge la musique du jeu."""
    song1 = 'Ressources/sound/ridin.mp3'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)



cree_bord()

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

    # Dessiner le sol et les murs (pour qu'ils soient visibles)
    pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT), (WIDTH, HEIGHT), 10)  # Sol
    pygame.draw.line(screen, (0, 0, 0), (0, 0), (0, HEIGHT), 10)  # Mur gauche
    pygame.draw.line(screen, (0, 0, 0), (WIDTH, 0), (WIDTH, HEIGHT), 10)  # Mur droit

    # Dessiner les oiseaux
    for bird in personnages:
        bird.draw(screen)

    # Mettre à jour la physique
    space.step(1 / 60.0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()