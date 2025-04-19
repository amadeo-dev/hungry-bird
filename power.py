from main import *
from Constantes import *
from globals import *


def past_power(selec):
    for bird in selec:
        if bird.power == 'gros':
            bird.image_o = f"Ressources/image/Personnages/{bird.name}_s.png"
            bird.size *= 2

        elif bird.power == 'bouclier':
            pass
        elif bird.power == 'chienem':
            pass
        elif bird.power == 'boom3':
            pass
        elif bird.power == 'boom4':
            pass