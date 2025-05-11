import pygame
import pymunk
import random

pygame.init()
pygame.font.init()

# Noms des oiseaux disponibles
bird_name = ['Adrien','Nicolas', 'Thomas','Amadeo', 'Jacky']

def load_high_quality_image(path, target_size=None):
    """Charge une image avec un redimensionnement de haute qualité"""
    image = pygame.image.load(path).convert_alpha()
    if target_size:
            # Utilisation de smoothscale pour une meilleure qualité
        return pygame.transform.smoothscale(image, target_size)
    return image

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

musique_list = [
        "Ressources/Sons/blue skies and sunshine - kortani (Official Audio).mp3",
        "Ressources/Sons/soleil.mp3",
        "Ressources/Sons/~FREE~ Elmaa & Khali Type Beat ｜ God Bless.mp3",
        "Ressources/Sons/GIMS - CIEL (Official Lyrics Video).mp3"
    ]
Musique_jeu = random.choice(musique_list)
pygame.mixer.music.load(Musique_jeu)
pygame.mixer.music.play(-1)


# Images mises à l’échelle dynamiquement

best_scores = {1: 0, 2: 0, 3: 0}  # Dictionnaire pour stocker les meilleurs scores par niveau



# Images pour le niveau 1
DECORS_NV1 = pygame.transform.scale(pygame.image.load("Ressources/image/Niveau 1/decors nv1.png"), (screen_width, screen_height))
# Dans globals.py, modifiez les tailles des images :
SCALE_FACTOR = 0.8

def load_scaled_image(path):
    """Charge une image et la redimensionne selon SCALE_FACTOR"""
    image = pygame.image.load(path).convert_alpha()
    new_size = (int(image.get_width() * SCALE_FACTOR),
                int(image.get_height() * SCALE_FACTOR))
    return pygame.transform.smoothscale(image, new_size)

# Images pour le niveau 1

# Chargement simplifié de toutes les images avec redimensionnement automatique
GOBELET_BLEU = load_scaled_image("Ressources/image/Niveau 1/Gobelet bleu.png")
GOBELET_ROUGE = load_scaled_image("Ressources/image/Niveau 1/Gobelet Rouge.png")
GOBELET_VERT = load_scaled_image("Ressources/image/Niveau 1/Gobelet Vert.png")

JUS_OBSTACLE = load_scaled_image("Ressources/image/Niveau 1/Jus.png")
JOUET_OBSTACLE = load_scaled_image("Ressources/image/Niveau 1/jouet.png")
BANANE_MALUS = load_scaled_image("Ressources/image/Niveau 1/Banane Pourri-.png")
BANANE_BONUS = load_scaled_image("Ressources/image/Niveau 1/Banane.png")
HOTDOG_BONUS = load_scaled_image("Ressources/image/Niveau 1/Hot Dog.png")
BURGER_BONUS = load_scaled_image("Ressources/image/Niveau 1/Burger.png")

POUBELLE_MALUS = load_scaled_image("Ressources/image/Niveau 1/Poubelle.png")

# Remplacer dans globals.py:
HOTDOG_IMG = load_high_quality_image("Ressources/image/hotdog.png", (50, 30))
BURGER_IMG = load_high_quality_image("Ressources/image/burger.png", (50, 50))
BROCOLI_IMG = load_high_quality_image("Ressources/image/brocolis.png", (40, 40))
DINDE_IMG = load_high_quality_image("Ressources/image/Dinde_Royale.png", (60, 60))
RESTART_IMG = load_high_quality_image("Ressources/image/Restart.png", (50, 50))

# Charger le décor à la bonne taille
DECORS_IMG = pygame.transform.scale(pygame.image.load("Ressources/image/Papier.png"),(screen_width, screen_height))

# Images pour le niveau 2
DECORS_NV2 = pygame.transform.scale(pygame.image.load("Ressources/image/Niveau 2/Decors2.png"), (screen_width, screen_height))

# Gobelet pour le niveau 2
GOBELET_YAOURT = load_scaled_image("Ressources/image/Niveau 2/Yaourt.png")

# Obstacles pour le niveau 2
AVION_OBSTACLE = load_scaled_image("Ressources/image/Niveau 2/Avion.png")
BOUTEILLE_OBSTACLE = load_scaled_image("Ressources/image/Niveau 2/Bouteille.png")
LIVRE_OBSTACLE = load_scaled_image("Ressources/image/Niveau 2/Livre.png")

# Bonus pour le niveau 2
COOKIE_BONUS = load_scaled_image("Ressources/image/Niveau 2/Cookie.png")
POULET_BONUS = load_scaled_image("Ressources/image/Niveau 2/Poulet.png")
SANDWICH_BONUS = load_scaled_image("Ressources/image/Niveau 2/Sandwich.png")

# Malus pour le niveau 2
OS_MALUS = load_scaled_image("Ressources/image/Niveau 2/Os.png")
POUBELLE_NV2_MALUS = load_scaled_image("Ressources/image/Niveau 2/Poubelle.png")



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
        self.image_orig = load_high_quality_image(f"Ressources/image/Menu/{nom}.png")
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

# Création des boutons
boutons = {
    "tutoriel":  BoutonInteractif('Tutoriel', ajustx(1480), ajusty(940), ajustx(285), ajusty(203)),
    "niveau1":   BoutonInteractif('Nv1',      ajustx(960), ajusty(450), ajustx(520), ajusty(188)),
    "niveau2":   BoutonInteractif('Nv2',      ajustx(960), ajusty(630), ajustx(520), ajusty(188)),
    "niveau3":   BoutonInteractif('Nv3',      ajustx(960), ajusty(800), ajustx(520), ajusty(188)),
    "quitter":   BoutonInteractif('Quitter',  ajustx(200), ajusty(710), ajustx(247), ajusty(247)),
    "reglage":   BoutonInteractif('Reglages', ajustx(500), ajusty(940), ajustx(325), ajusty(235)),
}

boutons_jeu = {
    "reglage2":  BoutonInteractif('Reglages2', ajustx(1000), ajusty(940), ajustx(325), ajusty(235))

}

GOBELET_COLLISION_TYPE = 0


