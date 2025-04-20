import pygame
import pymunk
from globals import *


power_list = ["Chiefetoilé","bavoir","chienem","base","Gourmand"]
ekip = []   #liste de tous les oiseaux à disposition
selec_trois = []  #selection des trois oiseaux du joueur
font = pygame.font.Font(None, 58)

selection_running = False


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
        self.image_n = pygame.image.load(image).convert_alpha()
        self.image_n = pygame.transform.smoothscale(self.image_n, (250, 250))

        self.image_o = pygame.image.load(image_o).convert_alpha()
        self.image_o = pygame.transform.smoothscale(self.image_o, (250, 250))

        self.power = power


class BirdButton:
    def __init__(self, bird, x, y):
        self.bird = bird
        self.x, self.y = x, y
        self.base_size = pygame.Vector2(250, 250)
        self.current_size = self.base_size.copy()
        self.rect = bird.image_n.get_rect(center=(x, y))
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
        image = self.bird.image_o if self.bird in selec_trois else self.bird.image_n
        image = pygame.transform.smoothscale(image, self.current_size)
        self.rect = image.get_rect(center=(self.x, self.y))
        return image, self.rect


def create_birds():
    ekip.clear()
    selected_names = bird_name[:5]  # Par exemple, sélectionne les 5 premiers oiseaux

    for i, name in enumerate(selected_names):
        image = f"Ressources/image/Personnages/{name}_n.png"
        image_o = f"Ressources/image/Personnages/{name}_o.png"
        power = power_list[i]
        # Création de l'oiseau
        bird = Bird((150 + i * 60, screen_height - 60), name, image, image_o, power)
        ekip.append(bird)


def select_team():
    global selec_trois, selection_running
    selection_running = True
    create_birds()

    # Chargement d'éléments graphiques une seule fois
    background = pygame.image.load("Ressources/image/selec_bck.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    choix_image = pygame.image.load("Ressources/image/choix.png")

    # Création des boutons pour les oiseaux
    bird_buttons = []
    bird_width, bird_height = ajustx(250), ajusty(250)
    spacing = 100
    total_width = len(ekip) * bird_width + (len(ekip) - 1) * spacing
    start_x = (screen_width - total_width) // 2
    y = 400

    for i, bird in enumerate(ekip):
        x = start_x + i * (bird_width + spacing)
        bird_buttons.append(BirdButton(bird, x + bird_width//2, y + bird_height//2))

    while selection_running:
        # Affichage du fond
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(choix_image, (screen_width // 2 - choix_image.get_width() // 2, 50))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # Dessin des boutons d'oiseaux
        for button in bird_buttons:
            image, rect = button.update(mouse_pos, mouse_pressed)
            screen.blit(image, rect.topleft)

        pygame.display.flip()

        # Gestion des événements utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in bird_buttons:
                    if button.rect.collidepoint(event.pos):
                        bird = button.bird
                        if bird in selec_trois:
                            selec_trois.remove(bird)
                        elif len(selec_trois) < 3:
                            selec_trois.append(bird)

                if len(selec_trois) == 3:
                    selection_running = False

    return selec_trois