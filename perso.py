import pygame
import pymunk
from Constantes import *


bird_images = {}
power_list = ["Aucun pouvoir","Pouvoir X","Pouvoir Y","Pouvoir Z","Jacky", "Pouvoir mystère"]
menu_running = False

pygame.font.init()

space = pymunk.Space()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 58)

ekip = []

class Bird:
    def __init__(self, position, name, image, power):
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
        self.power = power


def create_birds():
    ekip.clear()
    selected_names = bird_name[:5]
    for i, name in enumerate(selected_names):
        image = f"Ressources/image/{name}.png"
        power = power_list[i]
        bird = Bird((150 + i * 60, HEIGHT - 60), name, image, power)
        ekip.append(bird)

def select_team():
    team = []
    selection_running = True

    while selection_running:
        background = pygame.image.load("Ressources/image/selec_bck.jpg")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        ship_top = screen.get_height() - background.get_height()
        ship_left = screen.get_width() / 2 - background.get_width() / 2
        screen.blit(background, (ship_left, ship_top))

        text = font.render("Choisissez 3 personnages :", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

        for bird in ekip:
            x, y = 100 + bird_name.index(bird.name) * 250, 200

            screen.blit(bird.image, (x, y))

            text_name = font.render(bird.name, True, (0, 0, 0))
            screen.blit(text_name, (x + 10, y + 110))

            text_power = font.render(bird.power, True, (150, 0, 0))
            screen.blit(text_power, (x, y + 140))

            if pygame.Rect(x, y, 100, 100).collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (0, 200, 0), (x, y, 100, 100), 5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for bird in ekip:
                    x, y = 100 + bird_name.index(bird.name) * 250, 200
                    if pygame.Rect(x, y, 100, 100).collidepoint(event.pos) and len(ekip) < 3:
                        ekip.append(bird.name)

                if len(ekip) == 3:
                    selection_running = False

    return ekip



while menu_running:
    create_birds()
    select_team()

pygame.quit()