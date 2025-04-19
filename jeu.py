import pygame
import random
import time
import math

from main import *
from Constantes import *
from globals import *
from perso import select_team
from power import *

def is_far_enough(pos, others):
    """Vérifie si une position est suffisamment éloignée des autres."""
    return all(((pos[0] - o[0]) ** 2 + (pos[1] - o[1]) ** 2) ** 0.5 > MIN_DISTANCE for o in others)

def create_food(level):
    """Crée les aliments à des positions aléatoires en fonction du niveau."""
    food_positions = []

    def random_pos():
        """Génère une position aléatoire pour un aliment."""
        max_attempts = 100
        for _ in range(max_attempts):
            pos = (random.randint(screen_width // 2, screen_width - 100), random.randint(screen_height - 300, screen_height - 150))
            if is_far_enough(pos, food_positions):
                food_positions.append(pos)
                return pos
        return (random.randint(screen_width // 2, screen_width - 100), random.randint(screen_height - 300, screen_height - 150))

    if level == 1:
        return [random_pos() for _ in range(3)], [random_pos() for _ in range(1)], [random_pos() for _ in range(2)], [random_pos() for _ in range(1)]
    elif level == 2:
        return [random_pos() for _ in range(5)], [random_pos() for _ in range(2)], [random_pos() for _ in range(3)], [random_pos() for _ in range(1)]
    elif level == 3:
        return [random_pos() for _ in range(7)], [random_pos() for _ in range(3)], [random_pos() for _ in range(4)], [random_pos() for _ in range(2)]

def create_ground():
    """Crée le sol du jeu."""
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (screen_width // 2, screen_height - 20)
    shape = pymunk.Poly.create_box(body, (screen_width, 40))
    shape.elasticity = 0.3
    shape.friction = 1.5
    space.add(body, shape)

def create_borders():
    """Crée les bordures du jeu."""
    borders = [
        pymunk.Segment(space.static_body, (0, 0), (0, screen_height), 5),
        pymunk.Segment(space.static_body, (screen_width, 0), (screen_width, screen_height), 5),
        pymunk.Segment(space.static_body, (0, 0), (screen_width, 0), 5)
    ]
    for border in borders:
        border.elasticity = 0.8
        space.add(border)

def limit_speed():
    """Limite la vitesse des oiseaux pour éviter des mouvements trop rapides."""
    for bird in birds:
        vx, vy = bird.body.velocity
        speed = (vx ** 2 + vy ** 2) ** 0.5
        if speed > MAX_SPEED:
            factor = MAX_SPEED / speed
            bird.body.velocity = (vx * factor, vy * factor)

def check_collision():
    """Vérifie les collisions entre les oiseaux et les aliments."""
    global score, end_game_time

    for bird in birds:
        if not bird.launched:
            continue

        for lst, points, size in [
            (hotdog_positions, 1, 8),
            (burger_positions, 3, 15),
            (brocoli_positions, -2, -5),
            (dinde_positions, 10, 20)
        ]:
            for item in lst[:]:
                if bird.body.position.get_distance(item) < 40:
                    score += points
                    bird.size = max(30, bird.size + size)
                    lst.remove(item)

    if len(hotdog_positions) == 0 and len(burger_positions) == 0 and len(brocoli_positions) == 0 and len(dinde_positions) == 0:
        if end_game_time is None:
            end_game_time = time.time()

def restart_game():
    """Réinitialise le jeu."""
    global birds, hotdog_positions, burger_positions, brocoli_positions, dinde_positions, score, current_bird_index, game_over, end_game_time
    for bird in birds:
        space.remove(bird.body, bird.shape)
    birds = selected_team
    hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_food(current_level)
    score = 0
    current_bird_index = 0
    game_over = False
    end_game_time = None

def clear_space():
    """Vide l'espace physique de tous les objets."""
    for body in space.bodies:
        space.remove(body)
    for shape in space.shapes:
        space.remove(shape)
    for constraint in space.constraints:
        space.remove(constraint)

def draw_end_menu():
    """Dessine le menu de fin de jeu."""
    font = pygame.font.Font(None, 74)
    text = font.render("Bravo !", True, GREEN)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    screen.blit(text, text_rect)

    restart_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
    menu_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 80, 200, 50)

    pygame.draw.rect(screen, GREEN, restart_button)
    pygame.draw.rect(screen, RED, menu_button)

    font = pygame.font.Font(None, 36)
    restart_text = font.render("Restart", True, WHITE)
    menu_text = font.render("Menu", True, WHITE)
    screen.blit(restart_text, (restart_button.x + 50, restart_button.y + 5))
    screen.blit(menu_text, (menu_button.x + 70, menu_button.y + 5))

    return restart_button, menu_button

def draw_restart_button():
    """Dessine le bouton Restart avec une image."""
    screen.blit(RESTART_IMG, (screen_width - 150, 20))

def draw_menu_button():
    """Dessine le bouton Menu."""
    pygame.draw.rect(screen, RED, (screen_width - 150, 80, 130, 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Menu", True, WHITE)
    screen.blit(text, (screen_width - 120, 90))

def game_loop():
    """Boucle principale du jeu."""
    global running, score, current_level, current_bird_index, start_pos, game_over, end_game_time
    dt = 1 / 60.0

    while running:
        screen.blit(DECORS_IMG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    restart_button, menu_button = draw_end_menu()
                    if restart_button.collidepoint(event.pos):
                        restart_game()
                    elif menu_button.collidepoint(event.pos):
                        main()
                else:
                    if screen_width - 150 <= event.pos[0] <= screen_width - 20 and 20 <= event.pos[1] <= 70:
                        restart_game()
                    elif screen_width - 150 <= event.pos[0] <= screen_width - 20 and 80 <= event.pos[1] <= 130:
                        return
                    elif current_bird_index < len(birds):
                        start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and current_bird_index < len(birds):
                end_pos = pygame.mouse.get_pos()
                if start_pos:
                    if current_bird_index == 0:
                        bird_index = 2
                    elif current_bird_index == 1:
                        bird_index = 1
                    elif current_bird_index == 2:
                        bird_index = 0

                    birds[bird_index].body.apply_impulse_at_local_point(
                        ((start_pos[0] - end_pos[0]) * 5, (start_pos[1] - end_pos[1]) * 5))
                    birds[bird_index].launched = True
                    current_bird_index += 1
                    start_pos = None

                    lance_sound.play()

        if start_pos and pygame.mouse.get_pressed()[0] and current_bird_index < len(birds):
            current_mouse_pos = pygame.mouse.get_pos()
            bird_index = 2 - current_bird_index
            bird = birds[bird_index]
            bird_pos = (int(bird.body.position[0]), int(bird.body.position[1]))


            dx = (start_pos[0] - current_mouse_pos[0]) * 5
            dy = (start_pos[1] - current_mouse_pos[1]) * 5

            speed = (dx ** 2 + dy ** 2) ** 0.5
            if speed > MAX_SPEED:
                factor = MAX_SPEED / speed
                dx *= factor
                dy *= factor

            pygame.draw.line(screen, (0, 255, 0), bird_pos, (bird_pos[0] + dx * 0.1, bird_pos[1] + dy * 0.1), 4)
            pygame.draw.circle(screen, (0, 255, 0), bird_pos, 10, 2)

        space.step(dt)
        limit_speed()

        for bird in birds:
            if not bird.launched:
                continue

            for lst, points, size in [
                (hotdog_positions, 1, 8),
                (burger_positions, 3, 15),
                (brocoli_positions, -2, -5),
                (dinde_positions, 10, 20)
            ]:
                for item in lst[:]:
                    if bird.body.position.get_distance(item) < 40:
                        score += points
                        bird.size = max(30, bird.size + size)
                        lst.remove(item)
                        miam_sound.play()  # Son de manger

        if len(hotdog_positions) == 0 and len(burger_positions) == 0 and len(brocoli_positions) == 0 and len(dinde_positions) == 0:
            if end_game_time is None:
                end_game_time = time.time()

        for bird in birds:
            BIRD_IMG_RESIZED = pygame.transform.scale(bird.image, (bird.size, bird.size))  # Utilisation de l'image spécifique à chaque oiseau
            bird_rect = BIRD_IMG_RESIZED.get_rect(center=(int(bird.body.position[0]), int(bird.body.position[1])))
            screen.blit(BIRD_IMG_RESIZED, bird_rect)

        for img, positions in [
            (HOTDOG_IMG, hotdog_positions),
            (BURGER_IMG, burger_positions),
            (BROCOLI_IMG, brocoli_positions),
            (DINDE_IMG, dinde_positions)
        ]:
            for pos in positions:
                screen.blit(img, img.get_rect(center=pos))

        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f"Score: {score}", True, RED), (20, 20))
        screen.blit(font.render(f"Niveau: {current_level}", True, RED), (20, 60))

        draw_restart_button()
        draw_menu_button()

        if current_bird_index >= len(birds) or (end_game_time is not None and time.time() - end_game_time >= 2):
            if end_game_time is None:
                end_game_time = time.time()
            if time.time() - end_game_time >= (2 if len(hotdog_positions) == 0 else 4):
                if not game_over:
                    menu_sound.play()
                game_over = True
                draw_end_menu()

        pygame.display.flip()
        pygame.time.delay(int(dt * 1000))



def jeu(level):
    global birds, hotdog_positions, burger_positions, brocoli_positions, dinde_positions, running, score, current_level, current_bird_index
    while True:
        clear_space()
        current_level = level
        birds = select_team()
        past_power(birds)
        hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_food(current_level)
        create_ground()
        create_borders()
        running, score, current_bird_index = True, 0, 0
        game_loop()
