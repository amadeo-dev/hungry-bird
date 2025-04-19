import json
import pygame
import math
from globals import *


class VolumeSlider:
    def __init__(self, x, y, width, height, initial_volume=0.5, color=(50, 150, 50)):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.volume = float(initial_volume) if initial_volume is not None else 0.5
        self.dragging = False
        self.color = color

    def update(self, mouse_pos, mouse_pressed):
        if mouse_pressed:
            if self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height:
                self.dragging = True

        if not mouse_pressed:
            self.dragging = False

        if self.dragging:
            relative_x = mouse_pos[0] - self.x
            self.volume = max(0.0, min(1.0, float(relative_x / self.width)))

        return self.volume

    def draw(self, surface):
        # Dessin sauce avec vagues fixes
        fill_width = int(self.width * (self.volume or 0))
        if fill_width > 0:
            wave_height = self.height // 3
            points = []
            segments = max(3, fill_width // 15)

            for i in range(segments + 1):
                x = self.x + (i / segments) * fill_width
                wave = math.sin(x / 15) * wave_height
                y = self.y + self.height // 2 + wave
                points.append((x, y))

            points.append((self.x + fill_width, self.y + self.height))
            points.append((self.x, self.y + self.height))

            pygame.draw.polygon(surface, self.color, points)


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
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return {"music_volume": 0.5, "fx_volume": 0.5}


def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f)


def update_audio_volumes(music_vol, fx_vol):
    try:
        music_vol = float(music_vol or 0.5)
        fx_vol = float(fx_vol or 0.5)

        pygame.mixer.music.set_volume(max(0.0, min(1.0, music_vol)))

        if 'miam_sound' in globals() and isinstance(miam_sound, pygame.mixer.Sound):
            miam_sound.set_volume(max(0.0, min(1.0, fx_vol)))
        if 'lance_sound' in globals() and isinstance(lance_sound, pygame.mixer.Sound):
            lance_sound.set_volume(max(0.0, min(1.0, fx_vol)))
        if 'menu_sound' in globals() and isinstance(menu_sound, pygame.mixer.Sound):
            menu_sound.set_volume(max(0.0, min(1.0, fx_vol)))
    except Exception as e:
        print(f"Erreur volume audio: {e}")


def reglages(previous_screen):
    # Créer un overlay semi-transparent
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((100, 100, 100, 128))  # Gris semi-transparent

    # Charger l'image de fond redimensionnée (1/4 de la taille)
    try:
        fond_original = pygame.image.load("Ressources/image/Menu/hotdog_r.png")
        new_width = int(screen_width * 0.25)
        new_height = int(screen_height * 0.25)
        fond = pygame.transform.scale(fond_original, (new_width, new_height))
        fond_rect = fond.get_rect(center=(screen_width // 2, screen_height // 2))
    except:
        fond = pygame.Surface((new_width, new_height))
        fond.fill((150, 75, 0))
        fond_rect = fond.get_rect(center=(screen_width // 2, screen_height // 2))

    clock = pygame.time.Clock()
    config = load_config()

    # Sliders sauce
    music_slider = VolumeSlider(ajustx(650), ajusty(418), ajustx(600), ajusty(20),
                                config.get("music_volume", 0.5), (218, 165, 32))
    fx_slider = VolumeSlider(ajustx(650), ajusty(514), ajustx(600), ajusty(20),
                             config.get("fx_volume", 0.5), (200, 40, 40))

    # Boutons
    musique_btn = BoutonInteractif("Musique", ajustx(350), ajusty(400), ajustx(300), ajusty(80))
    sons_btn = BoutonInteractif("Sons", ajustx(350), ajusty(500), ajustx(300), ajusty(80))
    bouton_retour = BoutonInteractif('Retour', ajustx(1000), ajusty(1000), ajustx(300), ajusty(150))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Afficher l'écran précédent avec overlay
        screen.blit(previous_screen, (0, 0))
        screen.blit(overlay, (0, 0))

        # Afficher le hotdog au centre
        screen.blit(fond, fond_rect)

        # Mise à jour boutons
        musique_img, musique_rect = musique_btn.update(mouse_pos, False)
        sons_img, sons_rect = sons_btn.update(mouse_pos, False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_retour.rect.collidepoint(event.pos):
                    save_config({
                        "music_volume": music_slider.volume,
                        "fx_volume": fx_slider.volume
                    })
                    return "menu"

        # Mise à jour sliders
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