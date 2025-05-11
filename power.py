import pygame
import time
from globals import *


def activate_power(bird):
    if bird.power == 'boost':  # Thomas - Vitesse boostée
        bird.body.velocity = (bird.body.velocity[0] * 10, bird.body.velocity[1] * 10)
        bird.power_active = True
        bird.power_end_time = time.time() + 2  # Durée: 2 secondes

    elif bird.power == 'bouclier':  # Nicolas - Bouclier
        bird.shield_active = True
        bird.power_active = True
        bird.power_end_time = time.time() + 2

    elif bird.power == 'Gourmand':  # Amadeo - Grande bouche
        bird.image_n = pygame.image.load("Ressources/image/Personnages/Amadeo_s.png").convert_alpha()
        bird.image_o = bird.image_n
        bird.power_active = True
        bird.power_end_time = time.time() + 2

    elif bird.power == 'saut':  # Jacky - Saut
        bird.body.apply_impulse_at_local_point((0, -500))
        bird.power_active = True


def deactivate_power(bird):
    if bird.power == 'boost':  # Thomas
        bird.body.velocity = (bird.body.velocity[0] / 4, bird.body.velocity[1] / 4)

    elif bird.power == 'bouclier':  # Nicolas
        bird.shield_active = False

    elif bird.power == 'Gourmand':  # Amadeo
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
        for bird in birds:
            if bird.launched and not bird.power_active:
                activate_power(bird)


def past_power(selec):
    for bird in selec:
        if bird.power == 'Gourmand':
            bird.original_image_n = pygame.image.load("Ressources/image/Personnages/Amadeo_n.png").convert_alpha()
            bird.original_image_o = bird.original_image_n
            bird.image_n = bird.original_image_n
            bird.image_o = bird.original_image_o