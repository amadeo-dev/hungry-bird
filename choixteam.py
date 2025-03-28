import pygame
from Constantes import *


WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Bouton avec image")


fond = pygame.image.load(f"Ressources/image/selec_bckg.jpg")
fond = pygame.transform.scale(fond, (1280, 720))


def select_team():
    """Affiche l'écran de sélection des personnages."""
    selected_characters = []
    all_characters = [
        ("Adrien", "Aucun pouvoir"),
        ("Thomas", "Pouvoir X"),
        ("Amadeo", "Pouvoir Y"),
        ("Nicolas", "Pouvoir Z"),
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
        screen.fill(WHITE)
        text = font.render("Choisissez 3 personnages :", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

        for i, (name, power) in enumerate(all_characters):
            x, y = 100 + i * 250, 200
            screen.blit(bird_images[name], (x, y))

            text_name = font.render(name, True, BLACK)
            screen.blit(text_name, (x + 10, y + 110))

            text_power = font.render(power, True, (150, 0, 0))
            screen.blit(text_power, (x, y + 140))

            if pygame.Rect(x, y, 100, 100).collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, GREEN, (x, y, 100, 100), 5)

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
