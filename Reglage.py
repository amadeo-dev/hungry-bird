import json
import pygame
import math
import random
from globals import *

# Classe pour gérer la barre de volume avec un design un peu stylé (vagues)
class VolumeSlider:
    def __init__(self, x, y, width, height, initial_volume=0.5, color=(218, 165, 32)):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.volume = float(initial_volume)
        self.dragging = False
        self.bar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.min_display_volume = 0.09  # pour éviter que la barre disparaisse quand le volume est trop bas

    # Gère l’interaction avec la souris
    def update(self, mouse_pos, mouse_pressed):
        if mouse_pressed and self.bar_rect.collidepoint(mouse_pos):
            self.dragging = True
        if not mouse_pressed:
            self.dragging = False
        if self.dragging:
            relative_x = mouse_pos[0] - self.x
            self.volume = max(0.0, min(1.0, float(relative_x / self.width)))  # clamp entre 0 et 1
        return self.volume

    # Dessine la barre avec des petites ondulations stylées (comme une sauce)
    def draw(self, surface):
        visual_volume = self.min_display_volume + self.volume * (1 - self.min_display_volume)
        fill_width = int(self.width * visual_volume)

        if fill_width > 0:
            max_wave = self.height // 3
            wave_length = 13

            # points pour la vague du haut
            top_points = []
            for x in range(self.x, self.x + fill_width + 1, 3):
                wave = (math.sin(x / wave_length) * 0.7 + math.cos(x / (wave_length*1.3)) * 0.3) * max_wave
                top_points.append((x, self.y + self.height // 2 + wave))

            # points pour la vague du bas
            bottom_points = []
            for x in range(self.x, self.x + fill_width + 1, 3):
                wave = (math.sin(x / wave_length + math.pi / 2) * 0.6 + math.cos(x / (wave_length * 0.9)) * 0.4) * (max_wave * 0.7)
                bottom_points.append((x, self.y + self.height + wave))

            # dessine le remplissage + bordure
            if len(top_points) > 1:
                pygame.draw.polygon(surface, self.color, top_points + bottom_points[::-1])
                border_color = (
                    max(0, self.color[0] - 30),
                    max(0, self.color[1] - 20),
                    max(0, self.color[2] - 10)
                )
                pygame.draw.lines(surface, border_color, False, top_points, 1)
                pygame.draw.lines(surface, border_color, False, bottom_points, 1)

# fonctions pour adapter les coordonnées à la résolution de l’écran
def ajustx(value):
    return int(value * screen_width / 1920)

def ajusty(value):
    return int(value * screen_height / 1080)

# charge les volumes depuis un fichier config
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

# sauvegarde les volumes dans le fichier config
def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f)

# applique les volumes au son du jeu
def update_audio_volumes(music_vol, fx_vol):
    try:
        pygame.mixer.music.set_volume(max(0.0, min(1.0, music_vol)))

        if 'miam_sound' in globals() and isinstance(miam_sound, pygame.mixer.Sound):
            miam_sound.set_volume(max(0.0, min(1.0, fx_vol)))
        if 'lance_sound' in globals() and isinstance(lance_sound, pygame.mixer.Sound):
            lance_sound.set_volume(max(0.0, min(1.0, fx_vol)))
        if 'menu_sound' in globals() and isinstance(menu_sound, pygame.mixer.Sound):
            menu_sound.set_volume(max(0.0, min(1.0, fx_vol)))
    except Exception as e:
        print(f"Erreur volume audio: {e}")

# fonction qui gère tout le menu des réglages (musique et sons)
def reglages():
    saved_screen = screen.copy()

    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((100, 100, 100, 130))  # fond semi-transparent
    saved_screen.blit(overlay, (0, 0))

    fond_original = pygame.image.load("Ressources/image/Menu/hotdog_r.png").convert_alpha()
    fond_rotated = pygame.transform.rotate(fond_original, 4)
    new_width = int(screen_width * 0.6)
    new_height = int(screen_height * 0.6)
    fond = pygame.transform.scale(fond_rotated, (new_width, new_height))
    fond_pos = ((screen_width - new_width) // 2, (screen_height - new_height + 230) // 3)

    clock = pygame.time.Clock()
    config = load_config()

    # pour gérer quand on laisse le clic appuyé sur un bouton
    holding = {"musique": False, "sons": False}
    hold_timer = 0
    HOLD_DELAY_INITIAL = 15
    HOLD_DELAY_CONTINUE = 3
    CLICK_INCREMENT = 0.15
    HOLD_INCREMENT = 0.02

    # couleurs qui rappellent la bouffe
    music_color = (228, 175, 42)  # moutarde
    fx_color = (210, 60, 40)      # ketchup

    music_slider = VolumeSlider(ajustx(650), ajusty(418), ajustx(600), ajusty(25), config.get("music_volume", 0.5), music_color)
    fx_slider = VolumeSlider(ajustx(650), ajusty(514), ajustx(600), ajusty(25), config.get("fx_volume", 0.5), fx_color)

    musique_btn = BoutonInteractif("Musique", ajustx(450), ajusty(430), ajustx(300), ajusty(70))
    sons_btn = BoutonInteractif("Sons", ajustx(450), ajusty(530), ajustx(300), ajusty(70))

    running = True
    while running:
        screen.blit(saved_screen, (0, 0))
        screen.blit(fond, fond_pos)
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        screen.blit(overlay, (0, 0))
        screen.blit(fond, fond_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if musique_btn.rect.collidepoint(event.pos):
                    holding["musique"] = True
                    hold_timer = 0
                    music_slider.volume = min(1.0, music_slider.volume + CLICK_INCREMENT)
                elif sons_btn.rect.collidepoint(event.pos):
                    holding["sons"] = True
                    hold_timer = 0
                    fx_slider.volume = min(1.0, fx_slider.volume + CLICK_INCREMENT)
                else:
                    fond_rect = pygame.Rect(fond_pos[0], fond_pos[1], fond.get_width(), fond.get_height())
                    if not fond_rect.collidepoint(event.pos):
                        save_config({
                            "music_volume": music_slider.volume,
                            "fx_volume": fx_slider.volume
                        })
                        return "menu"

            elif event.type == pygame.MOUSEBUTTONUP:
                holding["musique"] = False
                holding["sons"] = False
                hold_timer = 0

        # gestion du clic long pour augmenter le volume progressivement
        if mouse_pressed:
            hold_timer += 1
            if holding["musique"]:
                if hold_timer == HOLD_DELAY_INITIAL or (hold_timer > HOLD_DELAY_INITIAL and (hold_timer - HOLD_DELAY_INITIAL) % HOLD_DELAY_CONTINUE == 0):
                    music_slider.volume = min(1.0, music_slider.volume + HOLD_INCREMENT)
            elif holding["sons"]:
                if hold_timer == HOLD_DELAY_INITIAL or (hold_timer > HOLD_DELAY_INITIAL and (hold_timer - HOLD_DELAY_INITIAL) % HOLD_DELAY_CONTINUE == 0):
                    fx_slider.volume = min(1.0, fx_slider.volume + HOLD_INCREMENT)

        # mise à jour volumes et affichage sliders
        music_vol = music_slider.update(mouse_pos, mouse_pressed)
        fx_vol = fx_slider.update(mouse_pos, mouse_pressed)
        update_audio_volumes(music_vol, fx_vol)

        music_slider.draw(screen)
        fx_slider.draw(screen)

        musique_img, _ = musique_btn.update(mouse_pos, holding["musique"])
        sons_img, _ = sons_btn.update(mouse_pos, holding["sons"])

        screen.blit(musique_img, musique_btn.rect)
        screen.blit(sons_img, sons_btn.rect)

        pygame.display.flip()
        clock.tick(60)

    return "menu"

