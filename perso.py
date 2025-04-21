import pygame
import pymunk
from globals import *

power_list = ["Chiefetoilé", "bavoir", "chienem", "base", "Gourmand"]
ekip = []  # liste de tous les oiseaux à disposition
selec_trois = []  # selection des trois oiseaux du joueur
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

        self.base_size = pygame.Vector2(custom_size) if custom_size else (
            pygame.Vector2(250, 250) if not is_menu_button else pygame.Vector2(500, 220))
        self.current_size = self.base_size.copy()
        self.rect = self.image_n.get_rect(center=(x, y))
        self.animation_timer = 0

    def update(self, mouse_pos, mouse_pressed):
        hover = self.rect.collidepoint(mouse_pos)
        clicked = hover and mouse_pressed

        if clicked:
            self.animation_timer = 10

        if self.animation_timer > 0:
            self.animation_timer -= 0.5
            scale = 0.95 if self.animation_timer > 5 else 1.0
        else:
            scale = 1.02 if hover else 1.0

        target_size = self.base_size * scale
        self.current_size += (target_size - self.current_size) * 0.3

        image = self.image_o if (not self.is_menu_button and self.bird in selec_trois) else self.image_n
        image = pygame.transform.smoothscale(image, self.current_size)
        self.rect = image.get_rect(center=(self.x, self.y))
        return image, self.rect


def create_birds():
    ekip.clear()
    selected_names = bird_name[:5]
    for i, name in enumerate(selected_names):
        image = f"Ressources/image/Personnages/{name}_n.png"
        image_o = f"Ressources/image/Personnages/{name}_o.png"
        power = power_list[i]
        bird = Bird((150 + i * 60, screen_height - 60), name, image, image_o, power)
        ekip.append(bird)


def select_team():
    global selec_trois, selection_running
    selection_running = True
    create_birds()

    background = pygame.transform.scale(pygame.image.load("Ressources/image/Choix Oiseau/Decors_o.png"),
                                        (screen_width, screen_height))
    text_image = pygame.image.load("Ressources/image/Choix Oiseau/Text.png").convert_alpha()
    text_image = pygame.transform.scale(text_image, (500, 100))
    text_rect = text_image.get_rect(center=(screen_width // 2, 150))  # Texte plus bas

    bird_buttons = []
    bird_width, bird_height = ajustx(250), ajusty(250)
    spacing = 100
    total_width = len(ekip) * bird_width + (len(ekip) - 1) * spacing
    start_x = (screen_width - total_width) // 2
    y = 400

    for i, bird in enumerate(ekip):
        x = start_x + i * (bird_width + spacing)
        bird_buttons.append(BirdButton(bird, x + bird_width // 2, y + bird_height // 2))

    # Bouton Jouer en haut
    jouer_btn = BirdButton("Jouer", screen_width // 2, 200, is_menu_button=True)  # Position remontée

    # Bouton Retour/Sortir plus bas
    retour_btn = BirdButton("Retour", 150, screen_height - 80, is_menu_button=True, custom_size=(200, 80))

    while selection_running:
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for button in bird_buttons:
            image, rect = button.update(mouse_pos, mouse_pressed)
            screen.blit(image, rect.topleft)

        if len(selec_trois) == 3:
            jouer_img, jouer_rect = jouer_btn.update(mouse_pos, mouse_pressed)
            screen.blit(jouer_img, jouer_rect.topleft)

        retour_img, retour_rect = retour_btn.update(mouse_pos, mouse_pressed)
        screen.blit(retour_img, retour_rect.topleft)

        if len(selec_trois) < 3:
            screen.blit(text_image, text_rect)

        pygame.display.flip()

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

                if len(selec_trois) == 3 and jouer_btn.rect.collidepoint(event.pos):
                    selection_running = False

                if retour_btn.rect.collidepoint(event.pos):
                    return "menu"

    return selec_trois