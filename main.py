import pygame
import pymunk
import random

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 1280, 720
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 200, 0), (0, 0, 0)
BIRD_SIZE_DEFAULT = 50
MAX_SPEED = 1000
GRAVITY = (0, 900)
MIN_DISTANCE = 100  # Distance minimale entre les aliments

# Chargement des images
BIRD_IMG = pygame.image.load("Ressources/Jacky.png")  # Image du personnage
HOTDOG_IMG = pygame.transform.scale(pygame.image.load("Ressources/hotdog.png"), (50, 30))
BURGER_IMG = pygame.transform.scale(pygame.image.load("Ressources/burger.png"), (50, 50))
BROCOLI_IMG = pygame.transform.scale(pygame.image.load("Ressources/brocolis.png"), (40, 40))
DINDE_IMG = pygame.transform.scale(pygame.image.load("Ressources/Dinde Royale.png"), (60, 60))  # Dinde royale
RESTART_IMG = pygame.image.load("Ressources/Restart.png")
RESTART_IMG = pygame.transform.scale(RESTART_IMG, (50, 50))  # Bouton Restart
DECORS_IMG = pygame.image.load("Ressources/decor.png")  # Arrière-plan
DECORS_IMG = pygame.transform.scale(DECORS_IMG, (WIDTH, HEIGHT))  # Redimensionner l'arrière-plan

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hungry Bird")

# Initialisation de Pymunk
space = pymunk.Space()
space.gravity = GRAVITY

BIRD_SIZE = BIRD_SIZE_DEFAULT

def create_bird():
    """Crée le personnage (oiseau) avec un corps et une forme physique."""
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    body.position = (150, HEIGHT - 60)
    shape = pymunk.Circle(body, 15)
    shape.elasticity = 0.8  # Augmente le rebond
    shape.friction = 0.5  # Friction normale sauf sur le sol
    space.add(body, shape)
    return body, shape

def is_far_enough(pos, others):
    """Vérifie si une position est suffisamment éloignée des autres."""
    return all(((pos[0] - o[0]) ** 2 + (pos[1] - o[1]) ** 2) ** 0.5 > MIN_DISTANCE for o in others)

def create_food():
    """Crée les aliments à des positions aléatoires."""
    food_positions = []

    def random_pos():
        """Génère une position aléatoire pour un aliment."""
        while True:
            pos = (random.randint(WIDTH // 2, WIDTH - 100), random.randint(HEIGHT - 300, HEIGHT - 150))
            if is_far_enough(pos, food_positions):
                food_positions.append(pos)
                return pos

    return (
        [random_pos() for _ in range(3)],  # 3 Hotdogs
        [random_pos() for _ in range(1)],  # 1 Burger
        [random_pos() for _ in range(2)],  # 2 Brocolis
        [random_pos() for _ in range(1)]  # 1 Dinde Royale
    )

def create_ground():
    """Crée le sol du jeu."""
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (WIDTH // 2, HEIGHT - 20)
    shape = pymunk.Poly.create_box(body, (WIDTH, 40))
    shape.elasticity = 0.3  # Garde un léger rebond
    shape.friction = 1.5  # Augmente la friction pour éviter le glissement
    space.add(body, shape)

def create_borders():
    """Crée les bordures du jeu."""
    borders = [
        pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 5),
        pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 5),
        pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), 5)
    ]
    for border in borders:
        border.elasticity = 0.8
        space.add(border)

def limit_speed():
    """Limite la vitesse du personnage pour éviter des mouvements trop rapides."""
    vx, vy = bird_body.velocity
    speed = (vx ** 2 + vy ** 2) ** 0.5
    if speed > MAX_SPEED:
        factor = MAX_SPEED / speed
        bird_body.velocity = (vx * factor, vy * factor)

def check_collision():
    """Vérifie les collisions entre le personnage et les aliments."""
    global BIRD_SIZE, score

    for lst, points, size in [
        (hotdog_positions, 1, 8),  # Hotdog
        (burger_positions, 3, 15),  # Burger
        (brocoli_positions, -2, -5),  # Brocoli
        (dinde_positions, 10, 20)  # Dinde Royale
    ]:
        for item in lst[:]:
            if bird_body.position.get_distance(item) < 40:
                score += points
                BIRD_SIZE = max(30, BIRD_SIZE + size)  # Augmentation plus visible de la taille
                lst.remove(item)

def restart_game():
    """Réinitialise le jeu."""
    global bird_body, bird_shape, hotdog_positions, burger_positions, brocoli_positions, dinde_positions, launched, start_pos, score, BIRD_SIZE
    space.remove(bird_body, bird_shape)
    bird_body, bird_shape = create_bird()
    bird_body.position = (150, HEIGHT - 60)
    hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_food()
    launched = False
    start_pos = None
    score = 0
    BIRD_SIZE = BIRD_SIZE_DEFAULT  # Réinitialisation de la taille de l'oiseau

def clear_space():
    """Vide l'espace physique de tous les objets."""
    for body in space.bodies:
        space.remove(body)
    for shape in space.shapes:
        space.remove(shape)
    for constraint in space.constraints:
        space.remove(constraint)

def draw_restart_button():
    """Dessine le bouton Restart avec une image."""
    screen.blit(RESTART_IMG, (WIDTH - 150, 20))

def draw_menu_button():
    """Dessine le bouton Menu."""
    pygame.draw.rect(screen, RED, menu_button)
    font = pygame.font.Font(None, 36)
    text = font.render("Menu", True, WHITE)
    screen.blit(text, (WIDTH - 120, 90))

def game_loop():
    """Boucle principale du jeu."""
    global running, launched, start_pos, score
    dt = 1 / 60.0

    while running:
        screen.blit(DECORS_IMG, (0, 0))  # Dessine l'arrière-plan

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    restart_game()
                elif menu_button.collidepoint(event.pos):
                    return
                else:
                    start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and not launched and start_pos:
                end_pos = pygame.mouse.get_pos()
                bird_body.apply_impulse_at_local_point(
                    ((start_pos[0] - end_pos[0]) * 5, (start_pos[1] - end_pos[1]) * 5))
                launched = True

        space.step(dt)
        limit_speed()
        check_collision()

        BIRD_IMG_RESIZED = pygame.transform.scale(BIRD_IMG, (BIRD_SIZE, BIRD_SIZE))
        bird_rect = BIRD_IMG_RESIZED.get_rect(center=(int(bird_body.position[0]), int(bird_body.position[1])))
        screen.blit(BIRD_IMG_RESIZED, bird_rect)

        for img, positions in [
            (HOTDOG_IMG, hotdog_positions),
            (BURGER_IMG, burger_positions),
            (BROCOLI_IMG, brocoli_positions),
            (DINDE_IMG, dinde_positions)  # Dinde Royale
        ]:
            for pos in positions:
                screen.blit(img, img.get_rect(center=pos))

        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f"Score: {score}", True, RED), (20, 20))
        draw_restart_button()
        draw_menu_button()
        pygame.display.flip()
        pygame.time.delay(int(dt * 1000))

def select_team():
    """Affiche l'écran de sélection des personnages."""
    selected_characters = []
    all_characters = [
        ("Adrien", "Aucun pouvoir"),
        ("Thomas", "Pouvoir X"),
        ("Amadéo", "Pouvoir Y"),
        ("Nicolas", "Pouvoir Z"),
        ("Jacky", "Pouvoir mystère"),
    ]

    font = pygame.font.Font(None, 40)
    selection_running = True

    # Charge une seule image (Jacky.png) pour tous les personnages
    char_img = pygame.image.load("Ressources/Jacky.png")
    char_img = pygame.transform.scale(char_img, (100, 100))

    while selection_running:
        screen.fill(WHITE)
        text = font.render("Choisissez 3 personnages :", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

        for i, (name, power) in enumerate(all_characters):
            x, y = 100 + i * 250, 200
            screen.blit(char_img, (x, y))

            text_name = font.render(name, True, BLACK)
            screen.blit(text_name, (x + 10, y + 110))

            text_power = font.render(power, True, (150, 0, 0))
            screen.blit(text_power, (x, y + 140))

            # Effet visuel si la souris survole un personnage
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

    return selected_characters  # ✅ Retourne les personnages choisis

def show_menu():
    """Affiche le menu principal et permet de sélectionner les personnages."""
    menu_running = True
    font = pygame.font.Font(None, 60)
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

    while menu_running:
        screen.fill(WHITE)
        title = font.render("Hungry Bird", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        pygame.draw.rect(screen, GREEN, play_button)
        pygame.draw.rect(screen, RED, quit_button)

        play_text = font.render("Jouer", True, WHITE)
        quit_text = font.render("Quitter", True, WHITE)
        screen.blit(play_text, (play_button.x + 50, play_button.y + 5))
        screen.blit(quit_text, (quit_button.x + 35, quit_button.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    selected_team = select_team()  # ✅ Récupère les personnages choisis
                    print("Équipe sélectionnée :", selected_team)  # (debug)
                    menu_running = False  # ✅ Sort du menu et lance le jeu
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

restart_button = pygame.Rect(WIDTH - 150, 20, 130, 50)
menu_button = pygame.Rect(WIDTH - 150, 80, 130, 50)

def main():
    """Fonction principale du programme."""
    global bird_body, bird_shape, hotdog_positions, burger_positions, brocoli_positions, dinde_positions, running, launched, start_pos, score, BIRD_SIZE
    while True:
        show_menu()
        clear_space()  # Vide l'espace physique avant de relancer le jeu
        BIRD_SIZE = BIRD_SIZE_DEFAULT  # Réinitialisation de la taille de l'oiseau
        bird_body, bird_shape = create_bird()
        hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_food()
        create_ground()
        create_borders()
        running, launched, start_pos, score = True, False, None, 0
        game_loop()

if __name__ == "__main__":
    main()
    pygame.quit()