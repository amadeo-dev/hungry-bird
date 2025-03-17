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

# Charger les images
try:
    BIRD_IMG = pygame.image.load(r"C:\Users\Nicolas\Downloads\Jacky.png")  # Remplace par le bon chemin
    HOTDOG_IMG = pygame.image.load(r"C:\Users\Nicolas\Downloads\hotdog.png")  # Remplace par le bon chemin
except pygame.error:
    print("Erreur lors du chargement des images.")

# Redimensionner l'image de l'oiseau pour qu'elle soit un peu plus grande
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (50, 50))  # Redimensionne l'image de l'oiseau à 50x50
HOTDOG_IMG = pygame.transform.scale(HOTDOG_IMG, (50, 30))  # Redimensionne l'image du hot-dog à 50x30

# Couleurs avec alpha (transparence à 255 pour opacité complète)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 255)

# Initialisation de Pymunk
space = pymunk.Space()
space.gravity = (0, 900)


# Création du sol
def create_ground():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (WIDTH // 2, HEIGHT - 20)
    shape = pymunk.Poly.create_box(body, (WIDTH, 40))
    shape.elasticity = 0.5
    shape.friction = 1.0
    space.add(body, shape)
    return shape


# Création des bordures autour de l'écran (haut, bas, gauche, droite)
def create_boundaries():
    # Haut
    top_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    top_body.position = (WIDTH // 2, 0)
    top_shape = pymunk.Poly.create_box(top_body, (WIDTH, 10))
    space.add(top_body, top_shape)

    # Bas
    bottom_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    bottom_body.position = (WIDTH // 2, HEIGHT)
    bottom_shape = pymunk.Poly.create_box(bottom_body, (WIDTH, 10))
    space.add(bottom_body, bottom_shape)

    # Gauche
    left_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    left_body.position = (0, HEIGHT // 2)
    left_shape = pymunk.Poly.create_box(left_body, (10, HEIGHT))
    space.add(left_body, left_shape)

    # Droite
    right_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    right_body.position = (WIDTH, HEIGHT // 2)
    right_shape = pymunk.Poly.create_box(right_body, (10, HEIGHT))
    space.add(right_body, right_shape)


# Fonction pour créer un oiseau
def create_bird(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    body.position = x, y
    shape = pymunk.Circle(body, 15)
    shape.elasticity = 0.5
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape


# Fonction pour créer un hot-dog
def create_hotdog(x, y):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (50, 30)))
    body.position = x, y
    shape = pymunk.Poly.create_box(body, (50, 30))
    shape.elasticity = 0.5
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape


# Création de l'oiseau, des cochons, des blocs et du hot-dog
bird_body, bird_shape = create_bird(150, 400)
hotdog_body, hotdog_shape = create_hotdog(600, 300)

# Création des limites
create_boundaries()

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
            bird_body.apply_impulse_at_local_point((force_x, force_y))  # Applique l'impulsion
            launched = True

    # Appliquer les changements de la physique
    space.step(dt)

    # Dessiner l'oiseau (en premier plan)
    bird_rect = BIRD_IMG.get_rect(center=(int(bird_body.position[0]), int(bird_body.position[1])))
    screen.blit(BIRD_IMG, bird_rect)

    # Dessiner le hot-dog (en premier plan)
    hotdog_rect = HOTDOG_IMG.get_rect(center=(int(hotdog_body.position[0]), int(hotdog_body.position[1])))
    screen.blit(HOTDOG_IMG, hotdog_rect)

    # Affichage du résultat
    pygame.display.flip()
    pygame.time.delay(int(dt * 1000))

pygame.quit()
