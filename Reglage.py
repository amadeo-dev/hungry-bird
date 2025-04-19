import json
import pygame
from globals import *
from menu import BoutonInteractif  # Import spécifique pour une meilleure lisibilité

# Initialisation de Pygame
pygame.init()
# Charger une image de fond ou définir une couleur par défaut
try:
    fond = pygame.image.load("Ressources/image/hotdog.png")
    fond = pygame.transform.scale(fond, (screen_width, screen_height))
except pygame.error:
    fond = None


# Fonction pour ajuster les coordonnées (au cas où elles ne sont pas définies ailleurs)
def ajustx(value):
    return int(value * screen_width / 1920)


def ajusty(value):
    return int(value * screen_height / 1080)


# Classe du slider pour régler les volumes
class VolumeSlider:
    def __init__(self, x, y, width, height, initial_volume=0.5):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.volume = initial_volume
        self.dragging = False
        self.knob_radius = height * 1.5
        self.bar_rect = pygame.Rect(x, y, width, height)

    def update(self, mouse_pos, mouse_pressed):
        knob_x = self.x + self.volume * self.width
        knob_rect = pygame.Rect(knob_x - self.knob_radius,
                                self.y - (self.knob_radius - self.height) // 2,
                                self.knob_radius * 2,
                                self.knob_radius * 2)

        if mouse_pressed:
            if knob_rect.collidepoint(mouse_pos) or (not self.dragging and self.bar_rect.collidepoint(mouse_pos)):
                self.dragging = True
        else:
            self.dragging = False

        if self.dragging:
            relative_x = mouse_pos[0] - self.x
            self.volume = max(0, min(1, relative_x / self.width))

        return self.volume

    def draw(self, surface):
        # Dessiner la barre
        pygame.draw.rect(surface, (100, 100, 100), self.bar_rect, border_radius=self.height // 2)
        pygame.draw.rect(surface, (200, 200, 200), self.bar_rect, 2, border_radius=self.height // 2)

        # Dessiner la barre remplie
        filled_rect = pygame.Rect(self.x, self.y, int(self.width * self.volume), self.height)
        pygame.draw.rect(surface, (50, 150, 50), filled_rect, border_radius=self.height // 2)

        # Dessiner le bouton (curseur)
        knob_x = self.x + int(self.volume * self.width)
        pygame.draw.circle(surface, (200, 200, 200), (knob_x, self.y + self.height // 2), self.knob_radius)
        pygame.draw.circle(surface, (100, 100, 100), (knob_x, self.y + self.height // 2), self.knob_radius, 2)


# Fonction principale des réglages
def reglages():
    clock = pygame.time.Clock()

    # Créer les sliders pour régler les volumes
    music_slider = VolumeSlider(ajustx(600), ajusty(400), ajustx(600), ajusty(20))
    fx_slider = VolumeSlider(ajustx(600), ajusty(500), ajustx(600), ajusty(20))

    # Bouton retour
    bouton_retour = BoutonInteractif('Retour', ajustx(960), ajusty(800), ajustx(300), ajusty(150))

    # Police pour le texte
    font = pygame.font.Font(None, int(ajusty(50)))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if fond:
            screen.blit(fond, (0, 0))  # Afficher l'image de fond
        else:
            screen.fill((0, 0, 0))  # Fond noir par défaut

        # Mettre à jour et dessiner les sliders
        music_volume = music_slider.update(mouse_pos, mouse_pressed)
        fx_volume = fx_slider.update(mouse_pos, mouse_pressed)

        music_slider.draw(screen)
        fx_slider.draw(screen)

        # Afficher les textes
        music_text = font.render("Musique:", True, (255, 255, 255))
        fx_text = font.render("FX:", True, (255, 255, 255))

        screen.blit(music_text, (ajustx(300), ajusty(380)))
        screen.blit(fx_text, (ajustx(300), ajusty(480)))

        # Mettre à jour et dessiner le bouton retour
        img, rect = bouton_retour.update(mouse_pos, mouse_pressed)
        screen.blit(img, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

            if event.type == pygame.MOUSEBUTTONUP:
                if bouton_retour.rect.collidepoint(mouse_pos):
                    running = False

                    # Sauvegarder les volumes dans un fichier de config
                    save_config({
                        "music_volume": music_volume,
                        "fx_volume": fx_volume
                    })

        pygame.display.flip()
        clock.tick(60)

    return "menu"


# Fonction pour sauvegarder la configuration
def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f)


# Fonction pour charger la configuration
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"music_volume": 0.5, "fx_volume": 0.5}