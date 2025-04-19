import pygame
import math
import random
import time
import pymunk
import pymunk.pygame_util

from main import *
from Constantes import *
from globals import *
from perso import select_team
from power import *


def is_far_enough(pos, others):
    return all(((pos[0] - o[0]) ** 2 + (pos[1] - o[1]) ** 2) ** 0.5 > MIN_DISTANCE for o in others)


def create_food(level):
    food_positions = []

    def random_pos():
        max_attempts = 100
        for _ in range(max_attempts):
            pos = (random.randint(screen_width // 2, screen_width - 100),
                   random.randint(screen_height - 300, screen_height - 150))
            if is_far_enough(pos, food_positions):
                food_positions.append(pos)
                return pos
        return (random.randint(screen_width // 2, screen_width - 100),
                random.randint(screen_height - 300, screen_height - 150))

    if level == 1:
        return [random_pos() for _ in range(3)], [random_pos() for _ in range(1)], [random_pos() for _ in range(2)], [
            random_pos() for _ in range(1)]
    elif level == 2:
        return [random_pos() for _ in range(5)], [random_pos() for _ in range(2)], [random_pos() for _ in range(3)], [
            random_pos() for _ in range(1)]
    elif level == 3:
        return [random_pos() for _ in range(7)], [random_pos() for _ in range(3)], [random_pos() for _ in range(4)], [
            random_pos() for _ in range(2)]


def create_ground():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (screen_width // 2, screen_height - 20)
    shape = pymunk.Poly.create_box(body, (screen_width, 40))
    shape.elasticity = 0.3
    shape.friction = 1.5
    shape.collision_type = 3
    space.add(body, shape)
    return body, shape


def create_borders():
    borders = [
        pymunk.Segment(space.static_body, (0, 0), (0, screen_height), 5),
        pymunk.Segment(space.static_body, (screen_width, 0), (screen_width, screen_height), 5),
        pymunk.Segment(space.static_body, (0, 0), (screen_width, 0), 5)
    ]
    for border in borders:
        border.elasticity = 0.8
        border.friction = 1.0
        border.collision_type = 1
        space.add(border)
    return borders


def limit_speed():
    for bird in birds:
        if hasattr(bird, 'body') and bird.body:
            vx, vy = bird.body.velocity
            speed = (vx ** 2 + vy ** 2) ** 0.5
            if speed > MAX_SPEED:
                factor = MAX_SPEED / speed
                bird.body.velocity = (vx * factor, vy * factor)


def check_collision():
    global score, end_game_time

    for bird in birds:
        if not hasattr(bird, 'launched') or not bird.launched:
            continue

        # Vérifier si l'oiseau est proche de la nourriture pour ouvrir la bouche
        bird.near_food = False  # Réinitialiser l'état de "proximité"
        for lst in [hotdog_positions, burger_positions, brocoli_positions, dinde_positions]:
            for item in lst:
                # Si l'oiseau est à moins de 100 pixels d'un aliment
                if bird.body.position.get_distance(item) < 100:
                    bird.near_food = True
                    break  # Pas besoin de vérifier plus loin
            if bird.near_food:
                break

        # Si l'oiseau mange des aliments
        for lst, points, size in [
            (hotdog_positions, 1, 8),
            (burger_positions, 3, 15),
            (brocoli_positions, -2, -5),
            (dinde_positions, 10, 20)
        ]:
            for item in lst[:]:  # Crée une copie pour pouvoir enlever des éléments
                if bird.body.position.get_distance(item) < 40:  # Distance pour "mange"
                    score += points
                    bird.size = max(50, bird.size + size)
                    lst.remove(item)
                    miam_sound.play()  # Jouer un son lorsqu'on mange


def clear_space():
    static_bodies = [body for body in space.bodies if body.body_type == pymunk.Body.STATIC]

    for body in space.bodies[:]:
        if body not in static_bodies:
            space.remove(body)

    for shape in space.shapes[:]:
        space.remove(shape)
    for constraint in space.constraints[:]:
        space.remove(constraint)


def restart_game():
    global birds, hotdog_positions, burger_positions, brocoli_positions, dinde_positions, score, current_bird_index, game_over, end_game_time

    clear_space()

    for bird in birds:
        bird.launched = False
        bird.size = 60
        bird.near_food = False

    hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_food(current_level)
    create_ground()
    create_borders()

    score = 0
    current_bird_index = 0
    game_over = False
    end_game_time = None

    # Positionnement des oiseaux de droite à gauche
    positions = [
        (screen_width - 100, screen_height - 100),  # Droite
        (screen_width // 2, screen_height - 100),  # Centre
        (100, screen_height - 100)  # Gauche
    ]

    for i, bird in enumerate(birds[:3]):  # On ne prend que les 3 premiers pour l'exemple
        bird.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
        bird.body.position = positions[i]
        bird.shape = pymunk.Circle(bird.body, bird.size / 2)
        bird.shape.elasticity = 0.8
        bird.shape.friction = 0.5
        bird.shape.collision_type = 2
        space.add(bird.body, bird.shape)


def draw_end_menu():
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
    screen.blit(RESTART_IMG, (screen_width - 150, 20))


def draw_menu_button():
    pygame.draw.rect(screen, RED, (screen_width - 150, 80, 130, 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Menu", True, WHITE)
    screen.blit(text, (screen_width - 120, 90))


def game_loop():
    global running, score, current_level, current_bird_index, start_pos, game_over, end_game_time
    dt = 1 / 60.0

    handler = space.add_collision_handler(1, 2)
    handler.begin = lambda arbiter, space, data: True

    handler = space.add_collision_handler(3, 2)
    handler.begin = lambda arbiter, space, data: True

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
                        main()
                    elif current_bird_index < len(birds):
                        start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and current_bird_index < len(birds):
                end_pos = pygame.mouse.get_pos()
                if start_pos:
                    # Ordre de lancement : droite (0), centre (1), gauche (2)
                    bird_order = [0, 1, 2]  # Index des oiseaux dans l'ordre de lancement
                    bird_index = bird_order[current_bird_index]

                    birds[bird_index].body.apply_impulse_at_local_point(
                        ((start_pos[0] - end_pos[0]) * 5, (start_pos[1] - end_pos[1]) * 5))
                    birds[bird_index].launched = True
                    current_bird_index += 1
                    start_pos = None
                    lance_sound.play()

        if start_pos and pygame.mouse.get_pressed()[0] and current_bird_index < len(birds):
            current_mouse_pos = pygame.mouse.get_pos()
            bird_order = [0, 1, 2]
            bird_index = bird_order[current_bird_index]
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
        check_collision()

        # Dessiner les oiseaux avec effet miroir si besoin
        for bird in birds:
            if hasattr(bird, 'body') and bird.body:
                vx, vy = bird.body.velocity

                # Choisir l'image selon si l'oiseau est près de la nourriture ou non
                if hasattr(bird, 'near_food') and bird.near_food:
                    bird_img = pygame.transform.scale(bird.image_o, (bird.size, bird.size))
                else:
                    bird_img = pygame.transform.scale(bird.image_n, (bird.size, bird.size))

                # Appliquer un effet miroir si l'oiseau se déplace vers la gauche
                if vx < 0:
                    bird_img = pygame.transform.flip(bird_img, True, False)

                bird_rect = bird_img.get_rect(center=(int(bird.body.position[0]), int(bird.body.position[1])))

                screen.blit(bird_img, bird_rect)

        # Dessiner la nourriture
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
    global birds, hotdog_positions, burger_positions, brocoli_positions, dinde_positions, running, score, current_level, current_bird_index, space

    space = pymunk.Space()
    space.gravity = (0, 900)

    while True:
        clear_space()
        current_level = level
        selected_team = select_team()
        past_power(selected_team)
        birds = selected_team.copy()

        hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_food(current_level)
        create_ground()
        create_borders()

        # Initialisation des oiseaux avec positions de droite à gauche
        positions = [
            (screen_width - 100, screen_height - 100),  # Droite (premier à lancer)
            (screen_width // 2, screen_height - 100),  # Centre
            (100, screen_height - 100)  # Gauche (dernier à lancer)
        ]

        for i, bird in enumerate(birds[:3]):  # On suppose qu'il y a 3 oiseaux
            bird.size = 60
            bird.launched = False
            bird.near_food = False
            bird.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
            bird.body.position = positions[i]
            bird.shape = pymunk.Circle(bird.body, bird.size / 2)
            bird.shape.elasticity = 0.8
            bird.shape.friction = 0.5
            bird.shape.collision_type = 2
            space.add(bird.body, bird.shape)

        running = True
        score = 0
        current_bird_index = 0
        start_pos = None
        game_over = False
        end_game_time = None

        game_loop()