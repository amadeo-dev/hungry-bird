from main import *
from power import *
from globals import *

def reset_globals():
    """Réinitialise toutes les variables globales pour une nouvelle partie"""
    global birds, banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    global score, current_level, current_bird_index, game_over, end_game_time, space, running
    global cookie_positions, poulet_positions, sandwich_positions, os_malus_positions
    global selec_trois

    # On vide toutes les listes
    birds = []
    banane_positions = []
    hotdog_positions = []
    burger_positions = []
    banane_malus_positions = []
    poubelle_positions = []
    cookie_positions = []
    poulet_positions = []
    sandwich_positions = []
    os_malus_positions = []
    selec_trois = []  # On réinitialise la sélection des oiseaux

    # On remet les valeurs par défaut
    score = 0
    current_level = 1
    current_bird_index = 0
    game_over = False
    end_game_time = None
    running = True

    # On recrée l'espace physique
    space = pymunk.Space()
    space.gravity = GRAVITY

def is_far_enough(pos, others, MIN_DISTANCE):
    """Vérifie si une position est assez loin des autres"""
    return all(((pos[0] - o[0]) ** 2 + (pos[1] - o[1]) ** 2) ** 0.5 > MIN_DISTANCE for o in others)

def create_food(level):
    """Crée la nourriture en fonction du niveau"""
    if level == 1:
        # Niveau 1 - positions fixes
        banane_positions = [(560, 500), (970, 380)]
        hotdog_positions = [(1300, 250), (1300, 620)]
        burger_positions = [(830, 210)]
        banane_malus_positions = [(600, 350), (780, 570)]
        poubelle_positions = [(620, 200), (1300, 420)]
        return banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    elif level == 2:
        # Niveau 2 - positions fixes
        cookie_positions = [(600, 450), (1000, 300), (900, 700)]
        poulet_positions = [(600, 250), (1200, 600)]
        sandwich_positions = [(1250, 300)]
        os_malus_positions = [(700, 350), (900, 550)]
        poubelle_positions = [(650, 700)]
        return cookie_positions, poulet_positions, sandwich_positions, os_malus_positions, poubelle_positions
    else:
        # Niveau 3 - positions aléatoires
        return create_random_food(level)

def create_random_food(level):
    """Crée de la nourriture avec des positions aléatoires"""
    food_positions = []

    def random_pos():
        """Génère une position aléatoire qui ne chevauche pas les autres"""
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(500, screen_width - 200)
            y = random.randint(100, screen_height - 200)
            pos = (x, y)
            if is_far_enough(pos, food_positions, int(MIN_DISTANCE * 1.5)):
                food_positions.append(pos)
                return pos
        return (screen_width // 2, screen_height // 2)  # Si on trouve pas, on met au centre

    # On crée la nourriture avec les bonnes quantités
    hotdog = [random_pos() for _ in range(2)]
    banane = [random_pos() for _ in range(2)]
    burger = [random_pos()]
    poubelle = [random_pos()]
    banane_malus = [random_pos() for _ in range(2)]

    return banane, hotdog, burger, banane_malus, poubelle

def create_ground():
    """Crée le sol physique"""
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (screen_width // 2, screen_height - 20)
    shape = pymunk.Poly.create_box(body, (screen_width, 40))
    shape.elasticity = 0.3
    shape.friction = 1.5
    shape.collision_type = 3
    space.add(body, shape)
    return body, shape

def create_gobelets(level):
    """Crée les gobelets en fonction du niveau"""
    gobelets = []
    if level == 1:
        # Niveau 1 - gobelets colorés
        positions = [
            (90, screen_height - 70),  # Bleu
            (210, screen_height - 60),  # Rouge
            (330, screen_height - 70)   # Vert
        ]
        images = [GOBELET_BLEU, GOBELET_ROUGE, GOBELET_VERT]
    else:
        # Niveau 2 et 3 - yaourts
        positions = [
            (90, screen_height - 70),
            (210, screen_height - 60),
            (330, screen_height - 70)
        ]
        images = [GOBELET_YAOURT] * 3  # Même image pour les 3

    for img, pos in zip(images, positions):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos

        # On crée une forme qui correspond à l'image
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
    """Crée les obstacles en fonction du niveau"""
    obstacles = []
    if level == 1:
        # Obstacle Jus
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 550, screen_height - 190)
        mask = pygame.mask.from_surface(JUS_OBSTACLE)
        outline = mask.outline()
        simplified = [outline[i] for i in range(0, len(outline), 5)]
        vertices = [(x - JUS_OBSTACLE.get_width() / 2, y - JUS_OBSTACLE.get_height() / 2) for (x, y) in simplified]
        shape = pymunk.Poly(body, vertices)
        shape.elasticity = 0.5
        shape.friction = 1.0
        space.add(body, shape)
        obstacles.append((body, shape, JUS_OBSTACLE, None))

        # Obstacle Jouet (en haut)
        jouet_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        jouet_body.position = (screen_width - 800, screen_height - 710)

        radius_x = 5
        radius_y = 50
        segments = 20

        top_vertices = []
        for i in range(segments + 1):
            angle = math.pi * i / segments
            x = radius_x * math.cos(angle) - 10
            y = -radius_y * math.sin(angle) - 30
            top_vertices.append((x, y))
        top_shape = pymunk.Poly(jouet_body, top_vertices)
        top_shape.elasticity = 0.7
        top_shape.friction = 0.3
        top_shape.collision_type = 4
        space.add(jouet_body, top_shape)

        # Obstacle Jouet (en bas)
        jouet2_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        jouet2_body.position = (screen_width - 800, screen_height - 720)

        bottom_vertices = []
        for i in range(segments + 1):
            angle = math.pi * i / segments
            x = radius_x * math.cos(angle) - 10
            y = radius_y * math.sin(angle) + 130
            bottom_vertices.append((x, y))
        bottom_shape = pymunk.Poly(jouet2_body, bottom_vertices)
        bottom_shape.elasticity = 0.7
        bottom_shape.friction = 0.3
        bottom_shape.collision_type = 4
        space.add(jouet2_body, bottom_shape)

        obstacles.append((jouet_body, top_shape, JOUET_OBSTACLE))
        obstacles.append((jouet2_body, bottom_shape, JOUET2_OBSTACLE))

    elif level == 2:
        # Niveau 2 - Avion
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 400, 150)
        mask = pygame.mask.from_surface(AVION_OBSTACLE)
        outline = mask.outline()
        simplified = [outline[i] for i in range(0, len(outline), 3)]
        vertices = [(x - AVION_OBSTACLE.get_width() / 2, y - AVION_OBSTACLE.get_height() / 2) for (x, y) in simplified]
        shape = pymunk.Poly(body, vertices)
        space.add(body, shape)
        obstacles.append((body, shape, AVION_OBSTACLE))

        # Bouteille (dynamique)
        mass = 2
        size = (BOUTEILLE_OBSTACLE.get_width() * 0.7, BOUTEILLE_OBSTACLE.get_height() * 0.7)
        moment = pymunk.moment_for_box(mass, size)

        body = pymunk.Body(mass, moment)
        body.position = (screen_width // 2, screen_height - 150)

        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 1.2
        shape.collision_type = 4

        space.add(body, shape)
        obstacles.append((body, shape, BOUTEILLE_OBSTACLE))

        # Livre
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 150, screen_height - 200)
        mask = pygame.mask.from_surface(LIVRE_OBSTACLE)
        outline = mask.outline()
        simplified = [outline[i] for i in range(0, len(outline), 3)]
        vertices = [(x - LIVRE_OBSTACLE.get_width() / 2, y - LIVRE_OBSTACLE.get_height() / 2) for (x, y) in simplified]
        shape = pymunk.Poly(body, vertices)
        space.add(body, shape)
        obstacles.append((body, shape, LIVRE_OBSTACLE))

    return obstacles

def create_borders():
    """Crée les bords de l'écran"""
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
    """Limite la vitesse des oiseaux"""
    for bird in birds:
        if hasattr(bird, 'body') and bird.body:
            # Thomas peut aller plus vite avec son pouvoir
            if bird.name == 'Thomas' and bird.power_active:
                continue

            vx, vy = bird.body.velocity
            speed = (vx ** 2 + vy ** 2) ** 0.5
            if speed > MAX_SPEED:
                factor = MAX_SPEED / speed
                bird.body.velocity = (vx * factor, vy * factor)

def check_collision():
    """Vérifie les collisions entre les oiseaux et la nourriture"""
    global score, end_game_time

    for bird in birds:
        if not hasattr(bird, 'launched') or not bird.launched:
            continue

        bird.near_food = False

        # Distance pour détecter la nourriture
        BASE_PROXIMITY = 100
        PROXIMITY_THRESHOLD = BASE_PROXIMITY * (1.8 if bird.name == 'Amadeo' else 1)
        COLLISION_THRESHOLD = 40

        # Liste de toute la nourriture selon le niveau
        if current_level == 1:
            all_items = banane_positions + hotdog_positions + burger_positions + banane_malus_positions + poubelle_positions
        elif current_level == 2:
            all_items = cookie_positions + poulet_positions + sandwich_positions + os_malus_positions + poubelle_positions
        else:
            all_items = banane_positions + hotdog_positions + burger_positions + banane_malus_positions + poubelle_positions

        # On vérifie si l'oiseau est près de la nourriture
        for pos in all_items:
            dx = abs(bird.body.position.x - pos[0])
            dy = abs(bird.body.position.y - pos[1])

            if bird.name == 'Amadeo':
                if dx < PROXIMITY_THRESHOLD * 1.5 and dy < PROXIMITY_THRESHOLD * 1.2:
                    bird.near_food = True
                    break
            else:
                if dx < PROXIMITY_THRESHOLD and dy < PROXIMITY_THRESHOLD:
                    bird.near_food = True
                    break

        # On définit les effets de chaque nourriture
        food_data = []
        if current_level == 1:
            food_data = [
                (banane_positions, 20, 5, BANANE_BONUS, None),
                (hotdog_positions, 40, 10, HOTDOG_BONUS, None),
                (burger_positions, 100, 20, BURGER_BONUS, None),
                (banane_malus_positions, -20, -5, BANANE_MALUS, (100, 255, 100)),
                (poubelle_positions, -50, -10, POUBELLE_MALUS, (50, 255, 50))
            ]
        elif current_level == 2:
            food_data = [
                (cookie_positions, 30, 8, COOKIE_BONUS, None),
                (poulet_positions, 50, 12, POULET_BONUS, None),
                (sandwich_positions, 80, 15, SANDWICH_BONUS, None),
                (os_malus_positions, -30, -8, OS_MALUS, (100, 255, 100)),
                (poubelle_positions, -60, -15, POUBELLE_NV2_MALUS, (50, 255, 50))
            ]
        else:
            food_data = [
                (banane_positions, 20, 5, BANANE_BONUS, None),
                (hotdog_positions, 40, 10, HOTDOG_BONUS, None),
                (burger_positions, 100, 20, BURGER_BONUS, None),
                (banane_malus_positions, -20, -5, BANANE_MALUS, (100, 255, 100)),
                (poubelle_positions, -50, -10, POUBELLE_MALUS, (50, 255, 50))
            ]

        # On vérifie les collisions
        for lst, points, size, img, color_effect in food_data:
            for item_pos in lst[:]:
                distance = ((bird.body.position.x - item_pos[0]) ** 2 +
                           (bird.body.position.y - item_pos[1]) ** 2) ** 0.5

                if distance < COLLISION_THRESHOLD:
                    if color_effect is not None and bird.shield_active:
                        continue

                    score += points
                    bird.size = max(50, bird.size + size)
                    if color_effect:
                        bird.color_effect = color_effect
                        pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                    lst.remove(item_pos)
                    miam_sound.play()
                    bird.near_food = True
                    break

def clear_space():
    """Vide l'espace physique"""
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
    """Redémarre la partie"""
    global birds, banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    global cookie_positions, poulet_positions, sandwich_positions, os_malus_positions
    global score, current_bird_index, game_over, end_game_time

    clear_space()

    # On réinitialise les oiseaux
    for bird in birds:
        bird.launched = False
        bird.size = 100
        bird.near_food = False
        bird.color_effect = None
        bird.power_active = False
        bird.can_use_power = False
        bird.shield_active = False
        if hasattr(bird, 'power_end_time'):
            bird.power_end_time = 0
        if bird.name == 'Amadeo':
            bird.image_n = bird.original_image_n
            bird.image_o = bird.original_image_o

    # On recrée la nourriture
    if current_level == 1:
        banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_food(current_level)
    elif current_level == 2:
        cookie_positions, poulet_positions, sandwich_positions, os_malus_positions, poubelle_positions = create_food(current_level)
    else:
        banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_random_food(current_level)

    # On recrée les éléments physiques
    create_ground()
    create_borders()
    obstacles = create_obstacles(current_level)
    gobelets = create_gobelets(current_level)

    # On replace les oiseaux dans les gobelets
    gobelet_positions = [
        (330, screen_height - 70),
        (210, screen_height - 60),
        (90, screen_height - 70)
    ]

    for i, bird in enumerate(birds[:3]):
        bird.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
        bird.body.position = (gobelet_positions[i][0], gobelet_positions[i][1] - bird.size / 2 - 10)
        bird.shape = pymunk.Circle(bird.body, bird.size / 2)
        bird.shape.elasticity = 0.8
        bird.shape.friction = 0.5
        bird.shape.collision_type = 2
        space.add(bird.body, bird.shape)

    # On réinitialise les variables de jeu
    score = 0
    current_bird_index = 0
    game_over = False
    end_game_time = None
    return obstacles, gobelets

def update_bird_angle():
    """Met à jour l'angle et l'apparence des oiseaux"""
    for bird in birds:
        if hasattr(bird, 'body') and bird.body:
            vx, vy = bird.body.velocity
            angle = math.degrees(math.atan2(vy, vx)) if vx != 0 or vy != 0 else 0

            # On ajuste la taille selon si l'oiseau est près de la nourriture
            if bird.near_food:
                base_size = int(bird.size * 1.05)
            else:
                base_size = bird.size

            # Effet spécial pour les oiseaux gourmands
            size_factor = 1.2 if bird.near_food else 1.0
            if hasattr(bird, 'power') and bird.power == 'Gourmand' and bird.power_active:
                size_factor *= 1.5

            target_size = (int(base_size * size_factor), int(base_size * size_factor))

            if not hasattr(bird, 'cached_images'):
                bird.cached_images = {}

            size_key = tuple(target_size) + (bird.near_food,)
            if size_key not in bird.cached_images:
                base_image = bird.image_o if bird.near_food else bird.image_n

                # Effet de couleur si nécessaire
                if hasattr(bird, 'color_effect') and bird.color_effect:
                    colored_image = base_image.copy()
                    tint = pygame.Surface(colored_image.get_size(), pygame.SRCALPHA)
                    tint.fill(bird.color_effect)
                    colored_image.blit(tint, (0, 0), special_flags=pygame.BLEND_MULT)
                    base_image = colored_image

                bird.cached_images[size_key] = pygame.transform.smoothscale(base_image, target_size)

            bird_img = bird.cached_images[size_key]

            # On retourne l'image si l'oiseau va vers la gauche
            if vx < 0:
                bird_img = pygame.transform.flip(bird_img, True, False)
                angle = 180 + angle

            # On fait tourner l'image selon la direction
            if abs(vx) > 0.1 or abs(vy) > 0.1:
                bird_img = pygame.transform.rotate(bird_img, -angle)

            bird_rect = bird_img.get_rect(center=(int(bird.body.position[0]), int(bird.body.position[1])))
            screen.blit(bird_img, bird_rect)

            # On affiche le bouclier de Nicolas si actif
            if bird.name == 'Nicolas' and bird.shield_active:
                shield_surface = pygame.Surface((bird.size * 1.5, bird.size * 1.5), pygame.SRCALPHA)
                pygame.draw.circle(shield_surface, SHIELD_COLOR,
                                 (int(bird.size * 0.75), int(bird.size * 0.75)),
                                 int(bird.size * 0.7), 5)
                shield_rect = shield_surface.get_rect(center=bird_rect.center)
                screen.blit(shield_surface, shield_rect)

def draw_end_menu():
    """Affiche le menu de fin de partie"""
    global best_scores
    if score > best_scores.get(current_level, 0):
        best_scores[current_level] = score

    # Overlay semi-transparent
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Polices
    title_font = pygame.font.Font(None, 74)
    score_font = pygame.font.Font(None, 48)
    button_font = pygame.font.Font(None, 36)
    hint_font = pygame.font.Font(None, 32)

    # Messages selon le score
    if score >= 75:
        messages = [
            "Bravo !", "Tu t'es bien régalé !",
            "Gros Gourmand !", "Il n'en reste plus une miette !"
        ]
        color = GREEN
    else:
        messages = [
            "Tu peux mieux faire !", "Encore un effort !",
            "Tu n'avais pas un grand appetit...", "Tu n'as pas faim ?"
        ]
        color = ORANGE

    # Message aléatoire
    current_time = pygame.time.get_ticks()
    random.seed(current_time // 10000)
    title_text = random.choice(messages)

    # Astuce pour les pouvoirs
    hint_text = hint_font.render("Appuie sur 'Espace' Pour activer les pouvoirs des Personnages !", True, WHITE)
    hint_rect = hint_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150))
    screen.blit(hint_text, hint_rect)

    # Affichage des textes
    texts = [
        (title_text, title_font, color, -100),
        (f"Score actuel: {score}", score_font, WHITE, -30),
        (f"Meilleur score: {best_scores.get(current_level, 0)}", score_font, WHITE, 20)
    ]

    for text, font, color, y_offset in texts:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
        screen.blit(text_surface, text_rect)

    # Boutons
    button_width, button_height = 200, 50
    buttons = [
        ("Restart", GREEN, 200),
        ("Menu", RED, 290)
    ]

    button_rects = []
    for text, color, y_offset in buttons:
        button_rect = pygame.Rect(
            screen_width // 2 - button_width // 2,
            screen_height // 2 + y_offset,
            button_width,
            button_height
        )
        pygame.draw.rect(screen, color, button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=10)

        text_surface = button_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        button_rects.append(button_rect)

    return button_rects[0], button_rects[1]

def draw_restart_button():
    """Dessine le bouton restart"""
    screen.blit(RESTART_IMG, (screen_width - 150, 20))

def draw_menu_button():
    """Dessine le bouton menu"""
    pygame.draw.rect(screen, RED, (screen_width - 150, 80, 130, 50))
    font = pygame.font.Font(None, 36)
    text = font.render("Menu", True, WHITE)
    screen.blit(text, (screen_width - 120, 90))

def game_loop(obstacles=None, gobelets=None):
    """Boucle principale du jeu"""
    global running, score, current_level, current_bird_index, start_pos, game_over, end_game_time
    dt = 1 / 60.0

    # Boutons
    reglage_btn = BoutonInteractif('Reglages2', ajustx(screen_width), ajusty(60), ajustx(162), ajusty(117))
    reglage_img, reglage_rect = None, None
    restart_btn = pygame.Rect(screen_width - 150, 20, 130, 50)
    menu_btn = pygame.Rect(screen_width - 150, 80, 130, 50)

    while running:
        # Affichage du décor selon le niveau
        if current_level == 1:
            screen.blit(DECORS_NV1, (0, 0))
        elif current_level == 2:
            screen.blit(DECORS_NV2, (0, 0))
        else:
            screen.blit(DECORS_IMG, (0, 0))

        # Affichage des obstacles
        if obstacles:
            for obstacle in obstacles:
                if len(obstacle) >= 3 and obstacle[2] != JOUET2_OBSTACLE:
                    body, shape, img = obstacle[:3]
                    if hasattr(body, 'angle') and body.body_type == pymunk.Body.DYNAMIC:
                        rotated_img = pygame.transform.rotate(img, -math.degrees(body.angle))
                        screen.blit(rotated_img, rotated_img.get_rect(center=(int(body.position.x), int(body.position.y))))
                    else:
                        screen.blit(img, img.get_rect(center=(int(body.position.x), int(body.position.y))))

        # Affichage des gobelets
        if gobelets:
            for body, shape, img in gobelets:
                img_rect = img.get_rect(center=(int(body.position.x), int(body.position.y)))
                screen.blit(img, img_rect)

        # Affichage de la nourriture selon le niveau
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
        elif current_level == 2:
            for img, positions in [
                (COOKIE_BONUS, cookie_positions),
                (POULET_BONUS, poulet_positions),
                (SANDWICH_BONUS, sandwich_positions),
                (OS_MALUS, os_malus_positions),
                (POUBELLE_NV2_MALUS, poubelle_positions)
            ]:
                for pos in positions:
                    screen.blit(img, img.get_rect(center=pos))
        else:
            for img, positions in [
                (BANANE_BONUS, banane_positions),
                (HOTDOG_BONUS, hotdog_positions),
                (BURGER_BONUS, burger_positions),
                (BANANE_MALUS, banane_malus_positions),
                (POUBELLE_MALUS, poubelle_positions)
            ]:
                for pos in positions:
                    screen.blit(img, img.get_rect(center=pos))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if reglage_rect.collidepoint(event.pos):
                    reglages()
                elif restart_btn.collidepoint(mouse_pos):
                    obstacles, gobelets = restart_game()
                elif menu_btn.collidepoint(mouse_pos):
                    clear_space()
                    reset_globals()
                    return "menu"
                elif game_over:
                    restart_button, menu_button = draw_end_menu()
                    if restart_button.collidepoint(mouse_pos):
                        obstacles, gobelets = restart_game()
                    elif menu_button.collidepoint(mouse_pos):
                        clear_space()
                        reset_globals()
                        return "menu"
                elif current_bird_index < len(birds):
                    start_pos = mouse_pos
            elif event.type == pygame.MOUSEBUTTONUP and current_bird_index < len(birds):
                end_pos = pygame.mouse.get_pos()
                if start_pos:
                    bird = birds[current_bird_index]
                    impulse = ((start_pos[0] - end_pos[0]) * 15, (start_pos[1] - end_pos[1]) * 15)
                    bird.body.apply_impulse_at_local_point(impulse)
                    bird.launched = True
                    bird.can_use_power = True
                    current_bird_index += 1
                    start_pos = None
                    lance_sound.play()
            elif event.type == pygame.USEREVENT + 1:  # Réinitialiser l'effet de couleur
                for bird in birds:
                    if hasattr(bird, 'color_effect'):
                        bird.color_effect = None

        # Trajectoire avant le lancer
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

            num_points = 30
            trajectory_length = 0.4

            for i in range(1, num_points + 1):
                t = i / num_points * trajectory_length

                x = bird_pos[0] + dx * t
                y = bird_pos[1] + dy * t + 0.5 * space.gravity[1] * t ** 2

                point_size = max(1, 6 * (1 - t / trajectory_length))
                alpha = int(200 * (1 - (t / trajectory_length) ** 2))
                color = (255, 0, 255, alpha)

                if point_size > 1.5:
                    pygame.draw.circle(screen, color, (int(x), int(y)), int(point_size))
                else:
                    screen.set_at((int(x), int(y)), color[:3])

            # Cercle autour de l'oiseau
            pygame.draw.circle(screen, (100, 255, 100), bird_pos, 18, 2)
            pygame.draw.circle(screen, (200, 255, 200), bird_pos, 10, 1)
            pygame.draw.circle(screen, (50, 200, 50), bird_pos, 5)

        # Mise à jour du jeu
        handle_power_input(birds)
        check_power_duration(birds)
        space.step(dt)
        limit_speed()
        check_collision()
        update_bird_angle()

        # Affichage des obstacles spéciaux
        if obstacles and current_level == 1:
            for obstacle in obstacles:
                if len(obstacle) >= 3 and obstacle[2] == JOUET2_OBSTACLE:
                    body, shape, img = obstacle[:3]
                    screen.blit(img, img.get_rect(center=(int(body.position.x), int(body.position.y))))

        # Affichage du score et du niveau
        font = pygame.font.Font(None, 36)
        screen.blit(font.render(f"Score: {score}", True, RED), (20, 20))
        screen.blit(font.render(f"Niveau: {current_level}", True, RED), (20, 60))

        # Affichage des boutons
        reglage_img, reglage_rect = reglage_btn.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])
        screen.blit(reglage_img, reglage_rect)
        draw_restart_button()
        draw_menu_button()

        # Gestion de la fin de partie
        if current_bird_index >= len(birds) or (end_game_time is not None and time.time() - end_game_time >= 4):
            if end_game_time is None:
                end_game_time = time.time()
            if time.time() - end_game_time >= (4 if len(hotdog_positions) == 0 else 4):
                if not game_over:
                    menu_sound.play()
                game_over = True
                restart_button, menu_button = draw_end_menu()

                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()[0]

                if mouse_pressed:
                    if restart_button.collidepoint(mouse_pos):
                        obstacles, gobelets = restart_game()
                        game_over = False
                        end_game_time = None
                    elif menu_button.collidepoint(mouse_pos):
                        clear_space()
                        reset_globals()
                        return "menu"

        pygame.display.flip()
        pygame.time.delay(int(dt * 1000))

def jeu(level):
    """Fonction principale du jeu"""
    reset_globals()
    global birds, banane_positions, hotdog_positions, burger_positions, poubelle_positions
    global cookie_positions, poulet_positions, sandwich_positions, os_malus_positions
    global running, score, current_level, current_bird_index, space, selec_trois

    while True:
        # Réinitialisation pour chaque partie
        selec_trois = []
        current_level = level
        selected_team = select_team()
        if selected_team == "menu":
            return "menu"

        past_power(selected_team)
        birds = selected_team.copy()

        # Création de la nourriture selon le niveau
        if level == 1:
            banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_food(level)
            screen.blit(DECORS_NV1, (0, 0))
        elif level == 2:
            cookie_positions, poulet_positions, sandwich_positions, os_malus_positions, poubelle_positions = create_food(level)
            screen.blit(DECORS_NV2, (0, 0))
        else:
            banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_random_food(level)
            brocoli_positions = banane_malus_positions
            dinde_positions = poubelle_positions
            screen.blit(DECORS_IMG, (0, 0))

        # Création des éléments physiques
        create_ground()
        create_borders()
        obstacles = create_obstacles(level)
        gobelets = create_gobelets(level)

        # Position des gobelets
        gobelet_positions = [
            (330, screen_height - 70),
            (210, screen_height - 60),
            (90, screen_height - 70)
        ]

        # Placement des oiseaux dans les gobelets
        for i, bird in enumerate(birds[:3]):
            bird.size = 100
            bird.launched = False
            bird.near_food = False
            bird.color_effect = None
            bird.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 30))
            bird.body.position = (gobelet_positions[i][0], gobelet_positions[i][1] - bird.size / 2 - 10)
            bird.shape = pymunk.Circle(bird.body, bird.size / 2)
            bird.shape.elasticity = 0.8
            bird.shape.friction = 0.5
            bird.shape.collision_type = 2
            space.add(bird.body, bird.shape)

        # Initialisation des variables de jeu
        running = True
        score = 0
        current_bird_index = 0
        start_pos = None
        game_over = False
        end_game_time = None

        # Lancement de la boucle de jeu
        result = game_loop(obstacles, gobelets)
        if result == "menu":
            return "menu"