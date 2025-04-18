from main import *
from Constantes import *
from globals import *

for bird in birds:
    if bird.power == 'grossebouche':
        bird.image_o = birds.image_s

    elif bird.power == 'boom':
        pass