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
        pygame.draw.rect(surface, (70, 70, 70), self.bar_rect, border_radius=self.height // 2)
        pygame.draw.rect(surface, (150, 150, 150), self.bar_rect, 2, border_radius=self.height // 2)

        # Dessin sauce avec vagues fixes
        fill_width = int(self.width * (self.volume or 0))
        if fill_width > 0:
            wave_height = self.height // 3
            points = []
            segments = max(3, fill_width // 15)

            for i in range(segments + 1):
                x = self.x + (i / segments) * fill_width
                wave = math.sin(x / 15) * wave_height  # Pattern fixe
                y = self.y + self.height // 2 + wave
                points.append((x, y))

            points.append((self.x + fill_width, self.y + self.height))
            points.append((self.x, self.y + self.height))

            pygame.draw.polygon(surface, self.color, points)
            # Contour brillant
            highlight_color = (
                min(255, self.color[0] + 40),
                min(255, self.color[1] + 40),
                min(255, self.color[2] + 40)
            )
            pygame.draw.polygon(surface, highlight_color, points, 1)


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
    """Met à jour les volumes avec vérification des valeurs"""
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


def reglages():
    # Charger l'image de fond redimensionnée (70% de la taille originale)
    try:
        fond_original = pygame.image.load("Ressources/image/Menu/hotdog_r.png")
        new_width = int(screen_width * 0.7)
        new_height = int(screen_height * 0.7)
        fond = pygame.transform.scale(fond_original, (new_width, new_height))
        fond_pos = ((screen_width - new_width) // 2, (screen_height - new_height) // 3)  # Positionné plus haut
    except:
        fond = pygame.Surface((screen_width, screen_height))
        fond.fill((40, 40, 40))  # Fond sombre uni
        fond_pos = (0, 0)

    clock = pygame.time.Clock()
    config = load_config()

    # Sliders avec effet sauce
    music_slider = VolumeSlider(ajustx(650), ajusty(418), ajustx(600), ajusty(25),
                                config.get("music_volume", 0.5), (218, 165, 32))  # Jaune moutarde
    fx_slider = VolumeSlider(ajustx(650), ajusty(514), ajustx(600), ajusty(25),
                             config.get("fx_volume", 0.5), (200, 40, 40))  # Rouge ketchup

    # Boutons
    musique_btn = BoutonInteractif("Musique", ajustx(350), ajusty(400), ajustx(300), ajusty(70))
    sons_btn = BoutonInteractif("Sons", ajustx(350), ajusty(500), ajustx(300), ajusty(70))
    bouton_retour = BoutonInteractif('Retour', ajustx(960), ajusty(850), ajustx(300), ajusty(120))

    holding = {"musique": False, "sons": False}
    hold_timer = 0
    HOLD_DELAY = 15

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Affichage
        screen.fill((50, 50, 50))  # Fond uni
        screen.blit(fond, fond_pos)  # Image centrée et réduite

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quitter"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if musique_btn.rect.collidepoint(event.pos):
                    holding["musique"] = True
                    music_slider.volume = min(1.0, music_slider.volume + 0.05)
                elif sons_btn.rect.collidepoint(event.pos):
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

        # Mise à jour volumes
        music_vol = music_slider.update(mouse_pos, mouse_pressed)
        fx_vol = fx_slider.update(mouse_pos, mouse_pressed)
        update_audio_volumes(music_vol, fx_vol)

        # Affichage des éléments
        music_slider.draw(screen)
        fx_slider.draw(screen)

        musique_img, _ = musique_btn.update(mouse_pos, holding["musique"])
        sons_img, _ = sons_btn.update(mouse_pos, holding["sons"])
        retour_img, _ = bouton_retour.update(mouse_pos, mouse_pressed)

        screen.blit(musique_img, musique_btn.rect)
        screen.blit(sons_img, sons_btn.rect)
        screen.blit(retour_img, bouton_retour.rect)

        pygame.display.flip()
        clock.tick(60)

    return "menu"