from main import *
from power import *


def reset_globals():
    global birds, banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    global brocoli_positions, dinde_positions, score, current_level, current_bird_index, game_over, end_game_time, space, running

    birds = []
    banane_positions = []
    hotdog_positions = []
    burger_positions = []
    banane_malus_positions = []
    poubelle_positions = []
    brocoli_positions = []
    dinde_positions = []
    score = 0
    current_level = 1
    current_bird_index = 0
    game_over = False
    end_game_time = None
    running = True

    space = pymunk.Space()
    space.gravity = GRAVITY


def is_far_enough(pos, others):
    return all(((pos[0] - o[0]) ** 2 + (pos[1] - o[1]) ** 2) ** 0.5 > MIN_DISTANCE for o in others)


def create_food(level):
    if level == 1:
        banane_positions = [(560, 500), (970, 380)]
        hotdog_positions = [(1300, 250), (1300, 620)]
        burger_positions = [(870, 190)]
        banane_malus_positions = [(600, 350), (780, 570)]
        poubelle_positions = [(620, 200),(1300, 420)]
        return banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    else:
        return create_random_food(level)


def create_random_food(level):
    food_positions = []

    def random_pos():
        max_attempts = 100
        for _ in range(max_attempts):
            pos = (random.randint(screen_width // 2, screen_width - 100),
                   random.randint(screen_height // 2, screen_height - 150))
            if is_far_enough(pos, food_positions):
                food_positions.append(pos)
                return pos
        return (random.randint(screen_width // 2, screen_width - 100),
                random.randint(screen_height // 2, screen_height - 150))

    if level == 2:
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


def create_gobelets():
    gobelets = []
    positions = [
        (90, screen_height - 70),  # Gobelet bleu (1ère position)
        (210, screen_height - 60),  # Gobelet rouge (2ème position)
        (330, screen_height - 70)  # Gobelet vert (3ème position)
    ]
    images = [GOBELET_BLEU, GOBELET_ROUGE, GOBELET_VERT]

    for img, pos in zip(images, positions):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos

        mask = pygame.mask.from_surface(img)
        outline = mask.outline()
        if outline:
            simplified = [v for i, v in enumerate(outline) if i % 5 == 0]
            vertices = [(x - img.get_width() / 2, y - img.get_height() / 2) for (x, y) in simplified]
            shape = pymunk.Poly(body, vertices)
        else:
            shape = pymunk.Poly.create_box(body, (img.get_width(), img.get_height()))

        shape.elasticity = 0.3
        shape.friction = 1.0
        shape.collision_type = 5
        space.add(body, shape)
        gobelets.append((body, shape, img))

    return gobelets


def create_obstacles(level):
    obstacles = []
    if level == 1:
        # Obstacle Jus avec hitbox réduite
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 550, screen_height - 190)

        # Réduire la taille de la hitbox à 90%
        scaled_size = (int(JUS_OBSTACLE.get_width() * 0.9), int(JUS_OBSTACLE.get_height() * 0.9))
        scaled_img = pygame.transform.scale(JUS_OBSTACLE, scaled_size)

        mask = pygame.mask.from_surface(scaled_img)
        outline = mask.outline()
        if outline:
            simplified = [v for i, v in enumerate(outline) if i % 5 == 0]
            vertices = [(x - scaled_size[0] / 2, y - scaled_size[1] / 2) for (x, y) in simplified]
            shape = pymunk.Poly(body, vertices)
        else:
            shape = pymunk.Poly.create_box(body, scaled_size)

        shape.elasticity = 0.5
        shape.friction = 1.0
        shape.collision_type = 4
        space.add(body, shape)
        obstacles.append((body, shape, JUS_OBSTACLE))

        # Obstacle Jouet avec hitbox réduite
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 800, screen_height - 720)

        scaled_size = (int(JOUET_OBSTACLE.get_width() * 0.9), int(JOUET_OBSTACLE.get_height() * 0.9))
        scaled_img = pygame.transform.scale(JOUET_OBSTACLE, scaled_size)

        mask = pygame.mask.from_surface(scaled_img)
        outline = mask.outline()
        if outline:
            simplified = [v for i, v in enumerate(outline) if i % 5 == 0]
            vertices = [(x - scaled_size[0] / 2, y - scaled_size[1] / 2) for (x, y) in simplified]
            shape = pymunk.Poly(body, vertices)
        else:
            shape = pymunk.Poly.create_box(body, scaled_size)

        shape.elasticity = 0.7
        shape.friction = 0.3
        shape.collision_type = 4
        space.add(body, shape)
        obstacles.append((body, shape, JOUET_OBSTACLE))

    return obstacles


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

        bird.near_food = False

        # Créer un masque pour l'oiseau (avec une taille légèrement réduite)
        bird_img = bird.image_o if getattr(bird, 'near_food', False) else bird.image_n
        scaled_bird_size = (int(bird_img.get_width() * 0.9), int(bird_img.get_height() * 0.9))
        scaled_bird_img = pygame.transform.scale(bird_img, scaled_bird_size)
        bird_mask = pygame.mask.from_surface(scaled_bird_img)
        bird_rect = scaled_bird_img.get_rect(center=(int(bird.body.position.x), int(bird.body.position.y)))

        for lst, points, size, img in [
            (banane_positions, 20, 5, BANANE_BONUS),
            (hotdog_positions, 40, 8, HOTDOG_BONUS),
            (burger_positions, 100, 15, BURGER_BONUS),
            (banane_malus_positions, -20, -5, BANANE_MALUS),
            (poubelle_positions, -50, -10, POUBELLE_MALUS)
        ]:
            for item_pos in lst[:]:
                # Créer un masque réduit pour la nourriture (90% de la taille originale)
                scaled_food_size = (int(img.get_width() * 0.3), int(img.get_height() * 0.3))
                scaled_food = pygame.transform.scale(img, scaled_food_size)
                food_mask = pygame.mask.from_surface(scaled_food)
                food_rect = scaled_food.get_rect(center=item_pos)

                # Calculer le décalage
                offset_x = food_rect.x - bird_rect.x
                offset_y = food_rect.y - bird_rect.y

                # Vérifier la collision
                if bird_mask.overlap(food_mask, (offset_x, offset_y)):
                    score += points
                    bird.size = max(50, bird.size + size)
                    lst.remove(item_pos)
                    miam_sound.play()
                    bird.near_food = True


def clear_space():
    global space
    for body in space.bodies[:]:
        space.remove(body)
    for shape in space.shapes[:]:
        space.remove(shape)
    for constraint in space.constraints[:]:
        space.remove(constraint)
    space = pymunk.Space()
    space.gravity = GRAVITY


def restart_game():
    global birds, banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    global brocoli_positions, dinde_positions, score, current_bird_index, game_over, end_game_time

    clear_space()

    # Réinitialiser les oiseaux
    for bird in birds:
        bird.launched = False
        bird.size = 100
        bird.near_food = False

    # Recréer la nourriture selon le niveau
    if current_level == 1:
        banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_food(
            current_level)
    else:
        hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_random_food(current_level)

    create_ground()
    create_borders()
    obstacles = create_obstacles(current_level)
    gobelets = create_gobelets()

    gobelet_positions = [
        (330, screen_height - 70),  # 3ème gobelet (vert) - premier oiseau choisi
        (210, screen_height - 60),  # 2ème gobelet (rouge) - deuxième oiseau choisi
        (90, screen_height - 70)  # 1er gobelet (bleu) - troisième oiseau choisi
    ]

    for i, bird in enumerate(birds[:3]):
        bird.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
        bird.body.position = (gobelet_positions[i][0], gobelet_positions[i][1] - bird.size / 2 - 10)
        bird.shape = pymunk.Circle(bird.body, bird.size / 2)
        bird.shape.elasticity = 0.8
        bird.shape.friction = 0.5
        bird.shape.collision_type = 2
        space.add(bird.body, bird.shape)

    score = 0
    current_bird_index = 0
    game_over = False
    end_game_time = None
    return obstacles, gobelets


def update_bird_angle():
    for bird in birds:
        if hasattr(bird, 'body') and bird.body:
            vx, vy = bird.body.velocity
            angle = math.degrees(math.atan2(vy, vx)) if vx != 0 or vy != 0 else 0

            target_size = (bird.size * 5, bird.size * 5) if bird.power == 'Gourmand' and getattr(bird, 'near_food',
                                                                                                 True) else (
            bird.size, bird.size)
            if not hasattr(bird, 'cached_images'):
                bird.cached_images = {}

            size_key = tuple(target_size) + (bird.near_food,)
            if size_key not in bird.cached_images:
                base_image = bird.image_o if bird.near_food else bird.image_n
                bird.cached_images[size_key] = pygame.transform.smoothscale(base_image, target_size)

            bird_img = bird.cached_images[size_key]

            if vx < 0:
                bird_img = pygame.transform.flip(bird_img, True, False)
                angle = 180 + angle

            if abs(vx) > 0.1 or abs(vy) > 0.1:
                bird_img = pygame.transform.rotate(bird_img, -angle)

            bird_rect = bird_img.get_rect(center=(int(bird.body.position[0]), int(bird.body.position[1])))
            screen.blit(bird_img, bird_rect)


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


def game_loop(obstacles=None, gobelets=None):
    global running, score, current_level, current_bird_index, start_pos, game_over, end_game_time
    dt = 1 / 60.0

    reglage_btn = BoutonInteractif('Reglages2', ajustx(screen_width - 300), ajusty(20), ajustx(250), ajusty(70))

    while running:
        screen.blit(DECORS_NV1 if current_level == 1 else DECORS_IMG, (0, 0))

        # Dessiner les gobelets
        if gobelets:
            for body, shape, img in gobelets:
                screen.blit(img, (int(body.position.x) - img.get_width() // 2,
                                  int(body.position.y) - img.get_height() // 2))

        if current_level == 1:
            # Dessiner les obstacles
            if obstacles:
                for body, shape, img in obstacles:
                    screen.blit(img, (int(body.position.x) - img.get_width() // 2,
                                      int(body.position.y) - img.get_height() // 2))

            # Dessiner la nourriture niveau 1
            for img, positions in [
                (BANANE_BONUS, banane_positions),
                (HOTDOG_BONUS, hotdog_positions),
                (BURGER_BONUS, burger_positions),
                (BANANE_MALUS, banane_malus_positions),
                (POUBELLE_MALUS, poubelle_positions)
            ]:
                for pos in positions:
                    screen.blit(img, img.get_rect(center=pos))
        else:
            # Dessiner nourriture niveaux 2 et 3
            for img, positions in [
                (HOTDOG_IMG, hotdog_positions),
                (BURGER_IMG, burger_positions),
                (BROCOLI_IMG, brocoli_positions),
                (DINDE_IMG, dinde_positions)
            ]:
                for pos in positions:
                    screen.blit(img, img.get_rect(center=pos))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Touche R pour redémarrer
                    obstacles, gobelets = restart_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reglage_rect.collidepoint(event.pos):
                    reglages()
                elif game_over:
                    restart_button, menu_button = draw_end_menu()
                    if restart_button.collidepoint(event.pos):
                        obstacles, gobelets = restart_game()
                    elif menu_button.collidepoint(event.pos):
                        clear_space()
                        main()
                elif current_bird_index < len(birds):
                    start_pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP and current_bird_index < len(birds):
                end_pos = pygame.mouse.get_pos()
                if start_pos:
                    bird = birds[current_bird_index]
                    impulse = ((start_pos[0] - end_pos[0]) * 15, (start_pos[1] - end_pos[1]) * 15)
                    bird.body.apply_impulse_at_local_point(impulse)
                    bird.launched = True
                    current_bird_index += 1
                    start_pos = None
                    lance_sound.play()

        if start_pos and pygame.mouse.get_pressed()[0] and current_bird_index < len(birds):
            current_mouse_pos = pygame.mouse.get_pos()
            bird = birds[current_bird_index]
            bird_pos = (int(bird.body.position[0]), int(bird.body.position[1]))

            dx = (start_pos[0] - current_mouse_pos[0]) * 15
            dy = (start_pos[1] - current_mouse_pos[1]) * 15

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
        update_bird_angle()

        # Affichage score et niveau
        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f"Score: {score}", True, RED), (20, 20))
        screen.blit(font.render(f"Niveau: {current_level}", True, RED), (20, 60))

        # Boutons
        reglage_img, reglage_rect = reglage_btn.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
        screen.blit(reglage_img, reglage_rect)
        draw_restart_button()
        draw_menu_button()

        # Fin de partie
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
    reset_globals()
    global birds, banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    global brocoli_positions, dinde_positions, running, score, current_level, current_bird_index, space

    space = pymunk.Space()
    space.gravity = (0, 900)

    while True:
        clear_space()
        current_level = level
        selected_team = select_team()
        past_power(selected_team)
        birds = selected_team.copy()

        if level == 1:
            banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_food(
                level)
            screen.blit(DECORS_NV1, (0, 0))
        else:
            hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_random_food(level)
            screen.blit(DECORS_IMG, (0, 0))

        create_ground()
        create_borders()
        obstacles = create_obstacles(level)
        gobelets = create_gobelets()

        # Positionnement initial des oiseaux au-dessus des gobelets
        gobelet_positions = [
            (330, screen_height - 70),  # 3ème gobelet (vert) - premier oiseau choisi
            (210, screen_height - 60),  # 2ème gobelet (rouge) - deuxième oiseau choisi
            (90, screen_height - 70)  # 1er gobelet (bleu) - troisième oiseau choisi
        ]

        for i, bird in enumerate(birds[:3]):
            bird.size = 100
            bird.launched = False
            bird.near_food = False
            bird.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
            bird.body.position = (gobelet_positions[i][0], gobelet_positions[i][1] - bird.size / 2 - 10)
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

        game_loop(obstacles, gobelets)