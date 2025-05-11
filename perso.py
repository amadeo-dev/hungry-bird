import pygame
import pymunk
from globals import *

# Liste des pouvoirs associés aux personnages
power_list = ["base", "bouclier", "boost", "Gourmand", "saut"]

# Liste de tous les personnages (Bird) disponibles
ekip = []

# Liste des 3 oiseaux sélectionnés par le joueur
selec_trois = []

# Police pour afficher du texte
font = pygame.font.Font(None, 58)

# Booléen pour indiquer si on est dans l’écran de sélection
selection_running = False


# Classe qui définit un oiseau (Bird) avec son corps physique, ses images et son pouvoir
class Bird:
    def __init__(self, position, name, image, image_o, power):
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
        self.shape = pymunk.Circle(self.body, 15)
        space.add(self.body, self.shape)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5

        self.size = 80
        self.launched = False
        self.body.position = position

        self.name = name
        self.image_n = load_high_quality_image(image)
        self.image_o = load_high_quality_image(image_o)
        self.power = power
        self.power_active = False
        self.power_end_time = 0
        self.can_use_power = False  # Passe à True après le tir
        self.near_food = False

        # Si l’oiseau est Amadeo, on charge une image spéciale
        if name == 'Amadeo':
            self.special_image = pygame.image.load("Ressources/image/Personnages/Amadeo_s.png").convert_alpha()
            self.special_image = pygame.transform.smoothscale(
                self.special_image,
                (self.image_n.get_width(), self.image_n.get_height())
            )

        self.shield_active = False

        # Sauvegarde des images originales avant redimensionnement
        self.original_image_n = self.image_n
        self.original_image_o = self.image_o

        # Ajustement de la taille des sprites
        original_width, original_height = self.image_n.get_size()
        scale_factor = min(250 / original_width, 250 / original_height)
        new_size = (int(original_width * scale_factor), int(original_height * scale_factor))

        self.image_n = pygame.transform.smoothscale(self.image_n, new_size)
        self.image_o = pygame.transform.smoothscale(self.image_o, new_size)

        self.power = power


# Bouton visuel associé à un oiseau (pour la sélection ou les menus)
class BirdButton:
    def __init__(self, bird, x, y, is_menu_button=False, custom_size=None):
        self.bird = bird
        self.x, self.y = x, y
        self.is_menu_button = is_menu_button

        if is_menu_button:
            self.image_n = pygame.image.load(f"Ressources/image/Choix Oiseau/{bird}.png").convert_alpha()
            self.image_o = self.image_n
        else:
            self.image_n = bird.image_n
            self.image_o = bird.image_o

        # Taille du bouton (menu ou oiseau)
        self.base_size = pygame.Vector2(custom_size) if custom_size else (
            pygame.Vector2(250, 250) if not is_menu_button else pygame.Vector2(500, 220))
        self.current_size = self.base_size.copy()
        self.rect = self.image_n.get_rect(center=(x, y))
        self.animation_timer = 0

    # Met à jour l’apparence du bouton selon la souris
    def update(self, mouse_pos, mouse_pressed):
        hover = self.rect.collidepoint(mouse_pos)
        clicked = hover and mouse_pressed

        if clicked:
            self.animation_timer = 10

        # Animation : effet de scale pendant un petit délai
        if self.animation_timer > 0:
            self.animation_timer -= 0.5
            scale = 0.95 if self.animation_timer > 5 else 1.0
        else:
            scale = 1.02 if hover else 1.0

        # Transition douce de la taille
        target_size = self.base_size * scale
        self.current_size += (target_size - self.current_size) * 0.3

        image = self.image_o if (not self.is_menu_button and self.bird in selec_trois) else self.image_n
        image = pygame.transform.smoothscale(image, self.current_size)
        self.rect = image.get_rect(center=(self.x, self.y))
        return image, self.rect


# Crée les objets Bird avec leur sprite et les ajoute dans la liste "ekip"
def create_birds():
    ekip.clear()
    selected_names = bird_name[:5]
    for i, name in enumerate(selected_names):
        image = f"Ressources/image/Personnages/{name}_n.png"
        image_o = f"Ressources/image/Personnages/{name}_o.png"
        power = power_list[i]
        bird = Bird((150 + i * 60, screen_height - 60), name, image, image_o, power)
        ekip.append(bird)


# Écran de sélection d’équipe (3 oiseaux parmi 5)
def select_team():
    global selec_trois, selection_running
    selec_trois = []  # On vide la sélection précédente
    selection_running = True
    create_birds()

    # Chargement du fond et du texte d’instruction
    background = pygame.transform.scale(
        pygame.image.load("Ressources/image/Choix Oiseau/Decors_o.png"),
        (screen_width, screen_height)
    )
    text_image = pygame.image.load("Ressources/image/Choix Oiseau/Text.png").convert_alpha()
    text_image = pygame.transform.scale(text_image, (500, 100))
    text_rect = text_image.get_rect(center=(screen_width // 2, 150))

    # Création des boutons associés aux oiseaux
    bird_buttons = []
    bird_width, bird_height = ajustx(250), ajusty(250)
    spacing = 100
    total_width = len(ekip) * bird_width + (len(ekip) - 1) * spacing
    start_x = (screen_width - total_width) // 2
    y = 400

    for i, bird in enumerate(ekip):
        x = start_x + i * (bird_width + spacing)
        bird_buttons.append(BirdButton(bird, x + bird_width // 2, y + bird_height // 2))

    # Bouton "Jouer" (uniquement affiché quand 3 oiseaux sont sélectionnés)
    jouer_btn = BirdButton("Jouer", screen_width // 2, 200, is_menu_button=True)

    # Bouton "Retour" (pour revenir au menu)
    retour_btn = BirdButton("Retour", 150, screen_height - 80, is_menu_button=True, custom_size=(200, 100))

    while selection_running:
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Affichage des boutons des oiseaux
        for button in bird_buttons:
            image, rect = button.update(mouse_pos, mouse_pressed)
            screen.blit(image, rect.topleft)

        # Affichage du bouton "Jouer" uniquement si 3 oiseaux sont choisis
        if len(selec_trois) == 3:
            jouer_img, jouer_rect = jouer_btn.update(mouse_pos, mouse_pressed)
            screen.blit(jouer_img, jouer_rect.topleft)

        # Bouton "Retour" toujours visible
        retour_img, retour_rect = retour_btn.update(mouse_pos, mouse_pressed)
        screen.blit(retour_img, retour_rect.topleft)

        # Affichage du texte si la sélection est incomplète
        if len(selec_trois) < 3:
            screen.blit(text_image, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Gestion du clic sur les oiseaux
                for button in bird_buttons:
                    if button.rect.collidepoint(event.pos):
                        bird = button.bird
                        if bird in selec_trois:
                            selec_trois.remove(bird)
                        elif len(selec_trois) < 3:
                            selec_trois.append(bird)

                # Validation de la sélection → on quitte la boucle
                if len(selec_trois) == 3 and jouer_btn.rect.collidepoint(event.pos):
                    selection_running = False

                # Retour au menu principal
                if retour_btn.rect.collidepoint(event.pos):
                    return "menu"

    return selec_trois
