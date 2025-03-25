import pygame
import pymunk


bird_images = {}
bird_name = ['Jacky', 'Thomas', 'Adrien', 'Nicolas', 'Amadeo' ]

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
space = pymunk.Space()
pygame.font.init()
space.gravity = (0, 900)

ekip = []

class Bird:
    def __init__(self, position, name):
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        space.add(self.body, self.shape)
        self.size = 50
        self.launched = False
        self.name = name

def create_birds():
    ekip.clear()
    selected_names = bird_name[:3]
    for i, name in enumerate(selected_names):
        bird = Bird((150 + i * 60, HEIGHT - 60), name)
        ekip.append(bird)

def select_team():
    """Affiche l'écran de sélection des personnages."""
    selected_characters = []
    all_characters = [
        ("Adrien", "Aucun pouvoir"),
        ("Thomas", "Pouvoir X"),
        ("Amadeo", "Pouvoir Y"),
        ("Nicolas", "Bouclier"),
        ("Jacky", "Pouvoir mystère"),
    ]

    font = pygame.font.Font(None, 40)
    selection_running = True

    for i in range(len(bird_name)):
        name = bird_name[i]
        print(name)
        bird = pygame.image.load(f"Ressources/image/{name}.png")
        bird_images[name] = pygame.transform.scale(bird, (100, 100))


    while selection_running:
        background = pygame.image.load("Ressources/image/selec_bckg.jpg")  # Chemin vers l'image de fond
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.fill(background)
        text = font.render("Choisissez 3 personnages :", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

        for i, (name, power) in enumerate(all_characters):
            x, y = 100 + i * 250, 200
            screen.blit(bird_images[name], (x, y))

            text_name = font.render(name, True, (0, 0, 0))
            screen.blit(text_name, (x + 10, y + 110))

            text_power = font.render(power, True, (150, 0, 0))
            screen.blit(text_power, (x, y + 140))

            if pygame.Rect(x, y, 100, 100).collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (0, 200, 0), (x, y, 100, 100), 5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (name, _) in enumerate(all_characters):
                    x, y = 100 + i * 250, 200
                    if pygame.Rect(x, y, 100, 100).collidepoint(event.pos) and len(selected_characters) < 3:
                        selected_characters.append(name)

                if len(selected_characters) == 3:
                    selection_running = False

    return selected_characters

menu_running = True

while menu_running:
    create_birds()
    select_team()

pygame.quit()