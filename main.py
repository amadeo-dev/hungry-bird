import pygame
import pymunk
import pymunk.pygame_util
import math
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Birds - Version Avancée")

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0, 255)  # Ajout de la composante alpha
GREEN = (0, 255, 0, 255)  # Ajout de la composante alpha
BLACK = (0, 0, 0, 255)  # Ajout de la composante alpha
BROWN = (139, 69, 19, 255)  # Ajout de la composante alpha
GRAY = (200, 200, 200, 255)  # Ajout de la composante alpha

# Initialisation de Pymunk
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Création du sol
def create_ground():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (WIDTH // 2, HEIGHT - 20)
    shape = pymunk.Poly.create_box(body, (WIDTH, 40))
    shape.elasticity = 0.5
    shape.friction = 1.0
    space.add(body, shape)
    return shape

ground = create_ground()

# Fonction pour créer un oiseau
def create_bird(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    body.position = x, y
    shape = pymunk.Circle(body, 15)
    shape.elasticity = 0.5
    shape.friction = 0.5
    shape.color = (255, 0, 0, 255)  # Ajout de la composante alpha
    space.add(body, shape)
    return body

# Fonction pour créer une cible (cochon)
def create_pig(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = x, y
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 0.5
    shape.friction = 0.5
    shape.color = (0, 255, 0, 255)  # Ajout de la composante alpha
    space.add(body, shape)
    return body

# Fonction pour créer une structure (bloc destructible)
def create_block(x, y, width, height):
    body = pymunk.Body(5, pymunk.moment_for_box(5, (width, height)))
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (width, height))
    shape.elasticity = 0.3
    shape.friction = 0.8
    shape.color = (139, 69, 19, 255)  # Ajout de la composante alpha
    space.add(body, shape)
    return body

# Création de l'oiseau, des cochons et des blocs
bird = create_bird(150, 400)
pigs = [create_pig(600, 500), create_pig(650, 500)]
blocks = [
    create_block(600, 450, 50, 100),
    create_block(650, 450, 50, 100),
    create_block(625, 400, 100, 20)
]

# Variables de contrôle
running = True
launched = False
start_pos = None

dt = 1 / 60.0
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not launched:
            start_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and not launched:
            end_pos = pygame.mouse.get_pos()
            force_x = (start_pos[0] - end_pos[0]) * 5
            force_y = (start_pos[1] - end_pos[1]) * 5
            bird.apply_impulse_at_local_point((force_x, force_y))  # Applique l'impulsion
            launched = True

    # Dessiner les objets
    space.debug_draw(draw_options)
    space.step(dt)
    pygame.display.flip()
    pygame.time.delay(int(dt * 1000))

pygame.quit()
