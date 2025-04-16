import pygame
import pymunk
from Constantes import *
from globals import *


power_list = ["Aucun pouvoir","Pouvoir X","Pouvoir Y","Pouvoir Z","Jacky", "Pouvoir mystère"]
ekip = []   #liste de tous les oiseaux à disposition
selec_trois = []  #selection des trois oiseaux du joueur
font = pygame.font.Font(None, 58)

selection_running = False


class Bird:
    def __init__(self, position, name, image, image_o, power):
        self.size = BIRD_SIZE_DEFAULT
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
        self.shape = pymunk.Circle(self.body, 15)
        space.add(self.body, self.shape)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        self.size = 50
        self.launched = False
        self.body.position = position
        self.name = name
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))

        self.image_o = pygame.image.load(image_o).convert_alpha()
        self.image_o = pygame.transform.scale(self.image_o, (150, 150))

        self.power = power


def create_birds():
    ekip.clear()
    selected_names = bird_name[:5]
    for i, name in enumerate(selected_names):
        image = f"Ressources/image/Personnages/{name}_n.png"
        image_o = f"Ressources/image/Personnages/{name}_o.png"
        power = power_list[i]
        bird = Bird((150 + i * 60, HEIGHT - 60), name, image,image_o, power)
        ekip.append(bird)

def select_team():
    global selec_trois, selection_running
    selection_running = True
    create_birds()
    while selection_running:
        screen.fill((255, 255, 255))

        background = pygame.image.load("Ressources/image/selec_bck.jpg")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        ship_top = screen.get_height() - background.get_height()
        ship_left = screen.get_width() / 2 - background.get_width() / 2
        screen.blit(background, (ship_left, ship_top))

        choix = pygame.image.load("Ressources/image/choix.png")
        screen.blit(choix, (WIDTH // 2 - choix.get_width() // 2, 50))

        bird_rects = []
        for i, bird in enumerate(ekip):
            x, y = 100 + i * 250, 200
            rect = pygame.Rect(x, y, 150, 150)
            bird_rects.append((rect, bird))

            screen.blit(bird.image, (x, y))

            text_name = font.render(bird.name, True, (0, 0, 0))
            screen.blit(text_name, (x + 10, y + 110))

            text_power = font.render(bird.power, True, (150, 0, 0))
            screen.blit(text_power, (x, y + 140))

            if bird in selec_trois:
                bird.image = pygame.transform.scale(bird.image_o, (150, 150))
            elif rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (0, 200, 200), rect, 5)

        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, bird in bird_rects:
                    if rect.collidepoint(event.pos):
                        if bird in selec_trois:
                            selec_trois.remove(bird)  # Désélection
                        elif len(selec_trois) < 3:
                            selec_trois.append(bird)  # Sélection

                # Vérifie si on a bien sélectionné 3 oiseaux pour sortir de la boucle
                if len(selec_trois) == 3:
                    selection_running = False  # FIN de la sélection

    return selec_trois


