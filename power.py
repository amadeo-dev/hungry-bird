import pygame
import time
from globals import *

def activate_power(bird):
    if not hasattr(bird, 'can_use_power') or not bird.can_use_power:
        return

    # Jouer le son seulement si le pouvoir s'active réellement
    if not bird.power_active and bird.power != 'base':
        POWER_SOUND.play()

    if bird.power == 'boost':
        # Vitesse extrême + rebonds
        bird.body.velocity = (
            bird.body.velocity[0] * 2.0,
            bird.body.velocity[1] * 2.0 - 300
        )
        bird.shape.elasticity = 2
        bird.shape.friction = 0.5
        # Durée de 1 seconde seulement pour Thomas
        bird.power_end_time = time.time() + 1

    elif bird.power == 'bouclier':
        bird.shield_active = True
        bird.power_end_time = time.time() + 2

    elif bird.power == 'Gourmand':
        bird.image_n = bird.special_image
        bird.image_o = bird.special_image
        bird.power_end_time = time.time() + 2

    elif bird.power == 'saut':
        bird.body.apply_impulse_at_local_point((0, -1000))
        bird.power_end_time = time.time() + 2

    bird.power_active = True
    bird.can_use_power = False

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

def check_power_duration(birds):
    current_time = time.time()
    for bird in birds:
        if bird.power_active and current_time > bird.power_end_time:
            deactivate_power(bird)

def handle_power_input(birds):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # Trouver le dernier oiseau lancé qui peut activer son pouvoir
        for bird in reversed(birds):
            if bird.launched and not bird.power_active and bird.can_use_power:
                speed = (bird.body.velocity[0]**2 + bird.body.velocity[1]**2)**0.5
                if speed > POWER_ACTIVATION_SPEED:
                    activate_power(bird)
                break

def past_power(selec):
    for bird in selec:
        if bird.power == 'Gourmand':
            bird.original_image_n = pygame.image.load("Ressources/image/Personnages/Amadeo_n.png").convert_alpha()
            bird.original_image_o = bird.original_image_n
            bird.image_n = bird.original_image_n
            bird.image_o = bird.original_image_o