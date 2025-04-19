import pygame
from Constantes import *
from globals import *
from perso import *

pygame.display.set_caption("Menu")

fond = pygame.image.load("Ressources/image/Menu/Decors.png")
fond = pygame.transform.scale(fond, (screen_width, screen_height))

class BoutonInteractif:
    def __init__(self, nom, x, y, tx, ty):
        self.image_orig = pygame.image.load(f"Ressources/image/Menu/{nom}.png").convert_alpha()
        self.nom = nom
        self.x, self.y = x, y
        self.base_size = pygame.Vector2(tx, ty)
        self.current_size = self.base_size.copy()
        self.target_size = self.base_size.copy()
        self.rect = self.image_orig.get_rect(center=(x, y))
        self.state = "normal"  # 'normal', 'hover', 'pressed'

    def update(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed:
                self.state = "pressed"
                self.target_size = self.base_size * 0.70
            else:
                self.state = "hover"
                self.target_size = self.base_size * 1.05
        else:
            self.state = "normal"
            self.target_size = self.base_size

        self.current_size += (self.target_size - self.current_size) * 0.1
        image = pygame.transform.smoothscale(self.image_orig, self.current_size)
        rect = image.get_rect(center=(self.x, self.y))
        self.rect = rect
        return image, rect

# Création des boutons
boutons = {
    "tutoriel":  BoutonInteractif('Tutoriel', ajustx(1450), ajusty(980), ajustx(285), ajusty(203)),
    "niveau1":   BoutonInteractif('Nv1',      ajustx(980), ajusty(470), ajustx(520), ajusty(188)),
    "niveau2":   BoutonInteractif('Nv2',      ajustx(1000), ajusty(640), ajustx(520), ajusty(188)),
    "niveau3":   BoutonInteractif('Nv3',      ajustx(980), ajusty(810), ajustx(520), ajusty(188)),
    "quitter":   BoutonInteractif('Quitter',  ajustx(200),  ajusty(710), ajustx(247), ajusty(247)),
    "reglage":   BoutonInteractif('Reglages', ajustx(570),  ajusty(980), ajustx(325), ajusty(235)),
}

def menu():
    clock = pygame.time.Clock()
    bouton_clique = None
    mouse_was_down = False

    while True:
        screen.blit(fond, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for nom, bouton in boutons.items():
            img, rect = bouton.update(mouse_pos, mouse_pressed)
            screen.blit(img, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

        # Détection du relâchement du clic
        if mouse_was_down and not mouse_pressed:
            for nom, bouton in boutons.items():
                if bouton.rect.collidepoint(mouse_pos):
                    # Relâchement détecté sur le bouton -> jouer animation retour
                    for _ in range(5):  # laisse le bouton grossir un peu
                        screen.blit(fond, (0, 0))
                        for n, b in boutons.items():
                            img, rect = b.update(mouse_pos, False)  # plus de clic
                            screen.blit(img, rect)
                        pygame.display.flip()
                        clock.tick(60)
                    pygame.time.delay(100)
                    return nom

        mouse_was_down = mouse_pressed

        pygame.display.flip()
        clock.tick(60)
