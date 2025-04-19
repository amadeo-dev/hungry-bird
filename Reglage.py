import json
import pygame
from globals import *


class VolumeSlider:
    def __init__(self, x, y, width, height, initial_volume=0.5, color=(50, 150, 50)):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.volume = float(initial_volume)
        self.dragging = False
        self.bar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color

    def update(self, mouse_pos, mouse_pressed):
        if mouse_pressed and self.bar_rect.collidepoint(mouse_pos):
            self.dragging = True

        if not mouse_pressed:
            self.dragging = False

        if self.dragging:
            relative_x = mouse_pos[0] - self.x
            self.volume = max(0.0, min(1.0, float(relative_x / self.width)))

        return self.volume

    def draw(self, surface):
        # Barre de fond
        pygame.draw.rect(surface, (100, 100, 100), self.bar_rect, border_radius=self.height // 2)
        pygame.draw.rect(surface, (200, 200, 200), self.bar_rect, 2, border_radius=self.height // 2)

        # Partie remplie
        fill_width = int(self.width * self.volume)
        filled_rect = pygame.Rect(self.x, self.y, fill_width, self.height)
        pygame.draw.rect(surface, self.color, filled_rect, border_radius=self.height // 2)


def ajustx(value):
    return int(value * screen_width / 1920)


def ajusty(value):
    return int(value * screen_height / 1080)


def load_config():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            return {
                "music_volume": float(config.get("music_volume", 0.5)),
                "fx_volume": float(config.get("fx_volume", 0.5))
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"music_volume": 0.5, "fx_volume": 0.5}


def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f)


def update_audio_volumes(music_vol, fx_vol):
    """Met à jour les volumes audio globaux"""
    # Musique
    Musique_jeu.set_volume(music_vol)

    # Sons FX
    miam_sound.set_volume(fx_vol)
    lance_sound.set_volume(fx_vol)
    menu_sound.set_volume(fx_vol)


def reglages():
    # Charger l'image de fond
    fond = pygame.image.load("Ressources/image/hotdog.png")
    fond = pygame.transform.scale(fond, (screen_width, screen_height))

    clock = pygame.time.Clock()
    config = load_config()

    # Boutons images
    musique_btn = BoutonInteractif("Musique", ajustx(350), ajusty(400), ajustx(300), ajusty(80))
    sons_btn = BoutonInteractif("Sons", ajustx(350), ajusty(500), ajustx(300), ajusty(80))

    # Sliders
    music_slider = VolumeSlider(ajustx(650), ajusty(418), ajustx(600), ajusty(20),
                                config["music_volume"], (210, 180, 0))  # Jaune moutarde
    fx_slider = VolumeSlider(ajustx(650), ajusty(514), ajustx(600), ajusty(20),
                             config["fx_volume"], (180, 0, 0))  # Rouge ketchup

    bouton_retour = BoutonInteractif('Retour', ajustx(960), ajusty(800), ajustx(300), ajusty(150))

    # Variables pour le clic continu
    holding = {"musique": False, "sons": False}
    hold_timer = 0
    HOLD_DELAY = 15  # Frames avant accélération

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Affichage du fond
        screen.blit(fond, (0, 0))

        # Mise à jour boutons
        musique_img, musique_rect = musique_btn.update(mouse_pos, holding["musique"])
        sons_img, sons_rect = sons_btn.update(mouse_pos, holding["sons"])

        # Gestion événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if musique_rect.collidepoint(event.pos):
                    holding["musique"] = True
                    music_slider.volume = min(1.0, music_slider.volume + 0.05)
                elif sons_rect.collidepoint(event.pos):
                    holding["sons"] = True
                    fx_slider.volume = min(1.0, fx_slider.volume + 0.05)
                elif bouton_retour.rect.collidepoint(event.pos):
                    save_config({
                        "music_volume": music_slider.volume,
                        "fx_volume": fx_slider.volume
                    })
                    return "menu"

            if event.type == pygame.MOUSEBUTTONUP:
                holding["musique"] = False
                holding["sons"] = False
                hold_timer = 0

        # Clic continu
        if mouse_pressed:
            hold_timer += 1
            increment = 0.02 if hold_timer < HOLD_DELAY else 0.05

            if holding["musique"]:
                music_slider.volume = min(1.0, music_slider.volume + increment)
            elif holding["sons"]:
                fx_slider.volume = min(1.0, fx_slider.volume + increment)

        # Mise à jour sliders et volumes
        music_vol = music_slider.update(mouse_pos, mouse_pressed)
        fx_vol = fx_slider.update(mouse_pos, mouse_pressed)
        update_audio_volumes(music_vol, fx_vol)

        # Affichage
        music_slider.draw(screen)
        fx_slider.draw(screen)
        screen.blit(musique_img, musique_rect)
        screen.blit(sons_img, sons_rect)

        retour_img, retour_rect = bouton_retour.update(mouse_pos, mouse_pressed)
        screen.blit(retour_img, retour_rect)

        pygame.display.flip()
        clock.tick(60)

    return "menu"