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

    # Font plus petite pour texte
    small_font = pygame.font.SysFont(None, 40)

    while selection_running:
        # Affichage du fond
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(choix_image, (screen_width // 2 - choix_image.get_width() // 2, 50))

        bird_rects = []

        # Placement dynamique
        bird_width, bird_height = ajustx(250), ajusty(250)
        spacing = 100
        total_width = len(ekip) * bird_width + (len(ekip) - 1) * spacing
        start_x = (screen_width - total_width) // 2
        y = 400

        # Dessin des oiseaux
        for i, bird in enumerate(ekip):
            x = start_x + i * (bird_width + spacing)
            rect = pygame.Rect(x, y, bird_width, bird_height)
            bird_rects.append((rect, bird))

            # Sélectionner l'image correcte (bouche ouverte ou fermée)
            bird.image = bird.image_o if bird in selec_trois else bird.image_n

            # Afficher les éléments associés
            screen.blit(bird.image, rect.topleft)
            text_name = small_font.render(bird.name, True, (0, 0, 0))
            text_power = small_font.render(bird.power, True, (150, 0, 0))

            screen.blit(text_name, (rect.x + bird_width // 2 - text_name.get_width() // 2, rect.y + bird_height + 10))
            screen.blit(text_power, (rect.x + bird_width // 2 - text_power.get_width() // 2, rect.y + bird_height + 40))

        pygame.display.flip()

        # Gestion des événements utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, bird in bird_rects:
                    if rect.collidepoint(event.pos):
                        if bird in selec_trois:
                            selec_trois.remove(bird)
                        elif len(selec_trois) < 3:
                            selec_trois.append(bird)

                if len(selec_trois) == 3:
                    selection_running = False

    return selec_trois