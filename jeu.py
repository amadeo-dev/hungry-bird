from main import *
from power import *

def reset_globals():
    global birds, hotdog_positions, burger_positions, brocoli_positions, dinde_positions
    global score, current_level, current_bird_index, game_over, end_game_time, space, running

    # Réinitialiser les variables globales
    birds = []
    hotdog_positions = []
    burger_positions = []
    brocoli_positions = []
    dinde_positions = []
    score = 0
    current_level = 1
    current_bird_index = 0
    game_over = False
    end_game_time = None
    running = True

    # Réinitialiser l'espace physique
    space = pymunk.Space()
    space.gravity = GRAVITY


def is_far_enough(pos, others):
    return all(((pos[0] - o[0]) ** 2 + (pos[1] - o[1]) ** 2) ** 0.5 > MIN_DISTANCE for o in others)


def create_food(level):
    if level == 1:
        # Positions fixes pour le niveau 1
        banane_positions = [(800, 500), (900, 550), (1000, 500)]  # +20 points chacun
        hotdog_positions = [(850, 450)]  # +40 points
        burger_positions = [(950, 400)]  # +100 points
        banane_malus_positions = [(700, 500), (1100, 500)]  # -20 points chacun
        poubelle_positions = [(750, 450)]  # -50 points

        return banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    elif level == 2:
        # Structure similaire pour les autres niveaux (à adapter plus tard)
        return create_random_food(level)
    elif level == 3:
        return create_random_food(level)


def create_random_food(level):
    # Ancienne fonction pour les niveaux 2 et 3 (à adapter plus tard)
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


def create_obstacles(level):
    obstacles = []
    if level == 1:
        # Obstacle Jus (position fixe)
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width // 2, screen_height - 100)
        shape = pymunk.Poly.create_box(body, (150, 150))
        shape.elasticity = 0.5
        shape.friction = 1.0
        shape.collision_type = 4  # Nouveau type de collision pour les obstacles
        space.add(body, shape)
        obstacles.append((body, shape, JUS_OBSTACLE))

        # Obstacle Jouet (position fixe)
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width // 2, screen_height // 2)
        shape = pymunk.Poly.create_box(body, (200, 100))
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

        # Vérifier la proximité avec la nourriture
        for lst in [banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions]:
            for item in lst:
                if bird.body.position.get_distance(item) < 100:
                    bird.near_food = True
                    break
            if bird.near_food:
                break

        # Collision avec la nourriture
        for lst, points, size, img in [
            (banane_positions, 20, 5, BANANE_BONUS),  # +20 points
            (hotdog_positions, 40, 8, HOTDOG_BONUS),  # +40 points
            (burger_positions, 100, 15, BURGER_BONUS),  # +100 points
            (banane_malus_positions, -20, -5, BANANE_MALUS),  # -20 points
            (poubelle_positions, -50, -10, POUBELLE_MALUS)  # -50 points
        ]:
            for item in lst[:]:
                if bird.body.position.get_distance(item) < 40:
                    score += points
                    bird.size = max(50, bird.size + size)
                    lst.remove(item)
                    miam_sound.play()


def clear_space():
    global space
    for body in space.bodies[:]:
        space.remove(body)
    for shape in space.shapes[:]:
        space.remove(shape)
    for constraint in space.constraints[:]:
        space.remove(constraint)
    # Réinitialiser l'espace proprement
    space = pymunk.Space()
    space.gravity = GRAVITY


def restart_game():
    global birds, hotdog_positions, burger_positions, brocoli_positions, dinde_positions, score, current_bird_index, game_over, end_game_time

    clear_space()

    for bird in birds:
        bird.launched = False
        bird.size = 100
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
        (300, screen_height - 80),  # Troisième oiseau devient le premier
        (200, screen_height - 80),  # Deuxième oiseau reste au milieu
        (100, screen_height - 80)  # Premier oiseau devient le dernier
    ]

    for i, bird in enumerate(birds[:3]):  # On aligne les 3 premiers oiseaux avec l'inversion et rapprochement
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

def update_bird_angle():
    for bird in birds:
        if hasattr(bird, 'body') and bird.body:
            # Récupérer la vitesse de l'oiseau
            vx, vy = bird.body.velocity

            # Calculer l'angle pour l'orientation de l'oiseau
            angle = math.degrees(math.atan2(vy, vx)) if vx != 0 or vy != 0 else 0

            # Charger l'image correcte (near_food ou non)
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

            # Gestion de l'effet miroir pour les mouvements vers la gauche (vx < 0)
            if vx < 0:
                bird_img = pygame.transform.flip(bird_img, True, False)
                angle = 180 + angle  # Compense l'effet miroir pour garder une inclinaison correcte

            # Ne pas effecter de rotation si la vitesse est trop faible (on garde l'angle 0 par défaut)
            if abs(vx) > 0.1 or abs(vy) > 0.1:
                bird_img = pygame.transform.rotate(bird_img, -angle)

            # Centrer l'image sur la position actuelle de l'oiseau
            bird_rect = bird_img.get_rect(center=(int(bird.body.position[0]), int(bird.body.position[1])))

            # Dessiner l'image sur l'écran
            screen.blit(bird_img, bird_rect)


def game_loop(obstacles=None):
    global running, score, current_level, current_bird_index, start_pos, game_over, end_game_time
    dt = 1 / 60.0

    # Initialisation du bouton "Réglages" en haut à droite
    reglage_btn = BoutonInteractif('Reglages2', ajustx(screen_width - 300), ajusty(20), ajustx(250), ajusty(70))

    while running:
        screen.blit(DECORS_NV1 if current_level == 1 else DECORS_IMG, (0, 0))

        if current_level == 1:
            # Dessiner les gobelets
            screen.blit(GOBELET_BLEU, (100 - 40, screen_height - 150 - 50))
            screen.blit(GOBELET_ROUGE, (200 - 40, screen_height - 150 - 50))
            screen.blit(GOBELET_VERT, (300 - 40, screen_height - 150 - 50))

            # Dessiner les obstacles si ils existent
            if obstacles:
                for body, shape, img in obstacles:
                    screen.blit(img, (int(body.position.x) - img.get_width() // 2,
                                      int(body.position.y) - img.get_height() // 2))

            # Dessiner la nourriture spécifique au niveau
        if current_level == 1:
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
            # Ancien système de dessin pour les niveaux 2 et 3
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
                if event.key == pygame.K_r:  # Ajout de la touche "r" pour redémarrer
                    restart_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifie les clics sur le bouton "Réglages"
                if reglage_rect.collidepoint(event.pos):
                    reglages()  # Appelle la fonction des réglages

                elif game_over:  # Si le jeu est terminé, gérer les clics sur les options de fin
                    restart_button, menu_button = draw_end_menu()
                    if restart_button.collidepoint(event.pos):
                        restart_game()
                    elif menu_button.collidepoint(event.pos):
                        clear_space()  # Nettoyer les ressources physiques
                        main()
                else:
                    # Logique standard pour le lancement d'un oiseau
                    if current_bird_index < len(birds):
                        start_pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP and current_bird_index < len(birds):
                # Gérer le lancer de l'oiseau
                end_pos = pygame.mouse.get_pos()
                if start_pos:
                    bird_index = current_bird_index  # L'oiseau actuellement sélectionné
                    bird = birds[bird_index]
                    impulse = ((start_pos[0] - end_pos[0]) * 5, (start_pos[1] - end_pos[1]) * 5)
                    bird.body.apply_impulse_at_local_point(impulse)
                    bird.launched = True
                    current_bird_index += 1
                    start_pos = None
                    lance_sound.play()

        if start_pos and pygame.mouse.get_pressed()[0] and current_bird_index < len(birds):
            # Dessiner la trajectoire de lancement
            current_mouse_pos = pygame.mouse.get_pos()
            bird_index = current_bird_index
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

        # Mise à jour des éléments du jeu
        space.step(dt)
        limit_speed()
        check_collision()

        # Gérer les oiseaux (orientation, animation)
        update_bird_angle()

        # Dessiner la nourriture
        for img, positions in [
            (HOTDOG_IMG, hotdog_positions),
            (BURGER_IMG, burger_positions),
            (BROCOLI_IMG, brocoli_positions),
            (DINDE_IMG, dinde_positions)
        ]:
            for pos in positions:
                screen.blit(img, img.get_rect(center=pos))

        # Mettre à jour le score et le niveau
        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f"Score: {score}", True, RED), (20, 20))
        screen.blit(font.render(f"Niveau: {current_level}", True, RED), (20, 60))

        # Dessiner le bouton "Réglages"
        reglage_img, reglage_rect = reglage_btn.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
        screen.blit(reglage_img, reglage_rect)

        # Dessiner d'autres boutons ou éléments d'interface
        draw_restart_button()
        draw_menu_button()

        # Gestion de la fin de la partie
        if current_bird_index >= len(birds) or (end_game_time is not None and time.time() - end_game_time >= 2):
            if end_game_time is None:
                end_game_time = time.time()
            if time.time() - end_game_time >= (2 if len(hotdog_positions) == 0 else 4):
                if not game_over:
                    menu_sound.play()
                game_over = True
                draw_end_menu()

        # Rafraîchir l'écran
        pygame.display.flip()
        pygame.time.delay(int(dt * 1000))


def jeu(level):
    reset_globals()
    global birds, banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions, running, score, current_level, current_bird_index, space

    space = pymunk.Space()
    space.gravity = (0, 900)

    while True:
        clear_space()
        current_level = level
        selected_team = select_team()
        past_power(selected_team)
        birds = selected_team.copy()

        if level == 1:
            banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_food(level)
            screen.blit(DECORS_NV1, (0, 0))
        else:
            hotdog_positions, burger_positions, brocoli_positions, dinde_positions = create_random_food(level)
            screen.blit(DECORS_IMG, (0, 0))

        create_ground()
        create_borders()
        obstacles = create_obstacles(level)  # Création des obstacles

        # Positions des gobelets pour les oiseaux
        gobelet_positions = [
            (100, screen_height - 150),  # Gobelet bleu
            (200, screen_height - 150),  # Gobelet rouge
            (300, screen_height - 150)   # Gobelet vert
        ]

        for i, bird in enumerate(birds[:3]):
            bird.size = 100
            bird.launched = False
            bird.near_food = False
            bird.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
            bird.body.position = (gobelet_positions[i][0], gobelet_positions[i][1] - 50)
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

        game_loop(obstacles)  # Passez les obstacles à game_loop