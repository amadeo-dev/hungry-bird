import pygame
import time
from globals import *


def activate_power(bird):
    if not bird.launched or bird.power_active:
        return

    POWER_SOUND.play()  # Jouer le son quand un pouvoir est activé

    if bird.power == 'boost':  # Thomas - Vitesse boostée + rebonds
        bird.shape.elasticity = 2.0  # Rebonds accentués
        bird.body.velocity = (bird.body.velocity[0] * 3, bird.body.velocity[1] * 3)
        bird.power_active = True
        bird.power_end_time = time.time() + 2

    elif bird.power == 'bouclier':  # Nicolas - Bouclier
        bird.shield_active = True
        bird.power_active = True
        bird.power_end_time = time.time() + 2


    elif bird.power == 'Gourmand':  # Amadeo - Grande bouche
        bird.image_n = bird.special_image
        bird.image_o = bird.special_image
        bird.power_active = True
        bird.power_end_time = time.time() + 2

    elif bird.power == 'saut':  # Jacky - Saut
        bird.body.apply_impulse_at_local_point((0, -800))  # Force augmentée
        bird.power_active = True


def deactivate_power(bird):
    if bird.power == 'boost':
        bird.shape.elasticity = 0.8  # Retour à l'élasticité normale
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
        # Activer seulement le dernier oiseau lancé
        for bird in reversed(birds):
            if bird.launched and not bird.power_active:
                activate_power(bird)
                break  # On active seulement le dernier oiseau


def past_power(selec):
    for bird in selec:
        if bird.power == 'Gourmand':
            bird.original_image_n = pygame.image.load("Ressources/image/Personnages/Amadeo_n.png").convert_alpha()
            bird.original_image_o = bird.original_image_n
            bird.image_n = bird.original_image_n
            bird.image_o = bird.original_image_o