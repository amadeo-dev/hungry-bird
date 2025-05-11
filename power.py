from main import *
from globals import *


def past_power(selec):
    for bird in selec:
        if bird.power == 'Gourmand':
            bird.image_o = pygame.image.load("Ressources/image/Personnages/amadeo_s.png").convert_alpha()
            bird.image_o = pygame.transform.smoothscale(bird.image_o, (800, 800))



        elif bird.power == 'bouclier':
            pass
        elif bird.power == 'bond':
            pass
        elif bird.power == 'boom3':
            pass
        elif bird.power == 'boom4':
            pass