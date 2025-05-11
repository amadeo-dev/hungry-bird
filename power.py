import pygame
import time
from globals import *

# Fonction appelée pour activer le pouvoir spécial d’un oiseau
def activate_power(bird):
    # Vérifie que l'oiseau a le droit d'utiliser son pouvoir
    if not hasattr(bird, 'can_use_power') or not bird.can_use_power:
        return

    # Joue le son du pouvoir uniquement s’il s’active vraiment
    if not bird.power_active and bird.power != 'base':
        POWER_SOUND.play()

    # Pouvoir "boost" : vitesse augmentée + petit saut
    if bird.power == 'boost':
        bird.body.velocity = (
            bird.body.velocity[0] * 1.5,
            bird.body.velocity[1] * 1.5 - 300
        )
        bird.shape.elasticity = 2
        bird.shape.friction = 0.5
        bird.power_end_time = time.time() + 1  # durée courte

    # Pouvoir "bouclier" : active une protection temporaire
    elif bird.power == 'bouclier':
        bird.shield_active = True
        bird.power_end_time = time.time() + 2

    # Pouvoir "Gourmand" : change l’apparence de l’oiseau
    elif bird.power == 'Gourmand':
        bird.image_n = bird.special_image
        bird.image_o = bird.special_image
        bird.power_end_time = time.time() + 2

    # Pouvoir "saut" : applique une impulsion vers le haut
    elif bird.power == 'saut':
        bird.body.apply_impulse_at_local_point((0, -1000))
        bird.power_end_time = time.time() + 2

    bird.power_active = True
    bird.can_use_power = False  # ne peut l'utiliser qu'une fois

# Réinitialise l’état après la fin du pouvoir
def deactivate_power(bird):
    if bird.power == 'boost':
        bird.shape.elasticity = 0.8
        bird.shape.friction = 0.5
    elif bird.power == 'bouclier':
        bird.shield_active = False
    elif bird.power == 'Gourmand':
        bird.image_n = bird.original_image_n
        bird.image_o = bird.original_image_o

    bird.power_active = False

# Vérifie pour chaque oiseau si son pouvoir est terminé (durée écoulée)
def check_power_duration(birds):
    current_time = time.time()
    for bird in birds:
        if bird.power_active and current_time > bird.power_end_time:
            deactivate_power(bird)

# Gère l’appui sur ESPACE pour activer un pouvoir
def handle_power_input(birds):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # On prend le dernier oiseau lancé qui peut encore activer son pouvoir
        for bird in reversed(birds):
            if bird.launched and not bird.power_active and bird.can_use_power:
                speed = (bird.body.velocity[0]**2 + bird.body.velocity[1]**2)**0.5
                if speed > POWER_ACTIVATION_SPEED:
                    activate_power(bird)
                break

# Utilisé pour forcer l’image d’Amadeo à revenir à la normale en fin de pouvoir
def past_power(selec):
    for bird in selec:
        if bird.power == 'Gourmand':
            bird.original_image_n = pygame.image.load("Ressources/image/Personnages/Amadeo_n.png").convert_alpha()
            bird.original_image_o = bird.original_image_n
            bird.image_n = bird.original_image_n
            bird.image_o = bird.original_image_o