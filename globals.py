import pygame
import pymunk

pygame.init()
pygame.font.init()

# Noms des oiseaux disponibles
bird_name = ['Jacky', 'Thomas', 'Adrien', 'Nicolas', 'Amadeo']

# Initialisation écran
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
# Définit la fenêtre redimensionnable avec la taille initiale de l'écran
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Hungry Bird")


def ajustx(x):
    return (x * screen_width) / 1920


def ajusty(y):
    return (y * screen_height) / 1080


# Espace physique
space = pymunk.Space()
space.gravity = (0, 900)

# Couleurs
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 200, 0), (0, 0, 0)

# Autres constantes
BIRD_SIZE_DEFAULT = 50
MAX_SPEED = 1000
GRAVITY = (0, 900)
MIN_DISTANCE = 50

# SON
miam_sound = pygame.mixer.Sound("Ressources/Sons/Amadéo - slurp 2.wav")
lance_sound = pygame.mixer.Sound("Ressources/Sons/Amadéo - Yahoo.wav")
menu_sound = pygame.mixer.Sound("Ressources/Sons/Thomas - mhmhmh 2.wav")

Musique_jeu = pygame.mixer.Sound("Ressources/Sons/birds of a feather.mp3")
# Images mises à l’échelle dynamiquement
HOTDOG_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/hotdog.png"), (50, 30))
BURGER_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/burger.png"), (50, 50))
BROCOLI_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/brocolis.png"), (40, 40))
DINDE_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Dinde_Royale.png"), (60, 60))
RESTART_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Restart.png"), (50, 50))

# Décor mis à l’échelle à la taille de l’écran
DECORS_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/bck_lvl1.jpg"), (screen_width, screen_height))

# Position catapulte (utilise screen_height au lieu de HEIGHT)
CATAPULT_POS = (150, screen_height - 100)

# Variables globales du jeu
birds = []
hotdog_positions = []
burger_positions = []
brocoli_positions = []
dinde_positions = []
selected_team = []
running = True
score = 0
current_level = 1
current_bird_index = 0
start_pos = None
game_over = False
end_game_time = None


class BoutonInteractif:
    def __init__(self, nom, x, y, tx, ty):
        self.image_orig = pygame.image.load(f"Ressources/image/Menu/{nom}.png").convert_alpha()
        self.nom = nom
        self.x, self.y = x, y
        self.base_size = pygame.Vector2(tx, ty)
        self.current_size = self.base_size.copy()
        self.rect = self.image_orig.get_rect(center=(x, y))
        self.animation_timer = 0

    def update(self, mouse_pos, mouse_pressed):
        # Détection survol et clic
        hover = self.rect.collidepoint(mouse_pos)
        clicked = hover and mouse_pressed

        # Déclencher l'animation au clic
        if clicked:
            self.animation_timer = 10  # 10 frames d'animation

        # Gestion de l'animation
        if self.animation_timer > 0:
            self.animation_timer -= 0.5
            if self.animation_timer > 5:  # Première moitié: réduction
                scale = 0.95
            else:  # Deuxième moitié: retour
                scale = 1.0
        else:
            # État normal ou survol
            scale = 1.02 if hover else 1.0

        # Application de la taille
        target_size = self.base_size * scale
        self.current_size += (target_size - self.current_size) * 0.3

        # Mise à jour de l'image
        image = pygame.transform.smoothscale(self.image_orig, self.current_size)
        self.rect = image.get_rect(center=(self.x, self.y))
        return image, self.rect

