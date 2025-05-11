from main import *
from power import *
from globals import *

def reset_globals():
    global birds, banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    global score, current_level, current_bird_index, game_over, end_game_time, space, running
    global cookie_positions, poulet_positions, sandwich_positions, os_malus_positions
    global selec_trois  # Ajoutez cette ligne pour réinitialiser la sélection

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
    selec_trois = []  # Réinitialise la sélection des oiseaux
    score = 0
    current_level = 1
    current_bird_index = 0
    game_over = False
    end_game_time = None
    running = True

    space = pymunk.Space()
    space.gravity = GRAVITY


def is_far_enough(pos, others,MIN_DISTANCE):
    return all(((pos[0] - o[0]) ** 2 + (pos[1] - o[1]) ** 2) ** 0.5 > MIN_DISTANCE*1.5 for o in others)


def create_food(level):
    if level == 1:
        banane_positions = [(560, 500), (970, 380)]
        hotdog_positions = [(1300, 250), (1300, 620)]
        burger_positions = [(830, 210)]
        banane_malus_positions = [(600, 350), (780, 570)]
        poubelle_positions = [(620, 200), (1300, 420)]
        return banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    elif level == 2:
        cookie_positions = [(600, 450), (1000, 300), (900, 700)]
        poulet_positions = [(600, 250), (1200, 600)]
        sandwich_positions = [(1250, 300)]
        os_malus_positions = [(700, 350), (900, 550)]
        poubelle_positions = [(650, 700), (1250, 400)]
        return cookie_positions, poulet_positions, sandwich_positions, os_malus_positions, poubelle_positions
    else:  # Niveau 3 - mêmes aliments que niveau 1
        return create_random_food(level)


def create_random_food(level):
    food_positions = []

    def random_pos():
        max_attempts = 100
        for _ in range(max_attempts):
            # Zone plus large et mieux répartie
            x = random.randint(500, screen_width - 200)  # De la gauche à la droite
            y = random.randint(100, screen_height - 200)  # Du haut vers le bas
            pos = (x, y)
            # Distance minimale augmentée de 50%
            if is_far_enough(pos, food_positions, int(MIN_DISTANCE * 1.5)):
                food_positions.append(pos)
                return pos
        return (screen_width // 2, screen_height // 2)  # Fallback

    # Quantités exactes demandées
    hotdog = [random_pos() for _ in range(2)]
    banane = [random_pos() for _ in range(2)]
    burger = [random_pos()]
    poubelle = [random_pos()]
    banane_malus = [random_pos() for _ in range(2)]

    return banane, hotdog, burger, banane_malus, poubelle


def create_ground():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (screen_width // 2, screen_height - 20)
    shape = pymunk.Poly.create_box(body, (screen_width, 40))
    shape.elasticity = 0.3
    shape.friction = 1.5
    shape.collision_type = 3
    space.add(body, shape)
    return body, shape


def create_gobelets(level):
    gobelets = []
    if level == 1:
        positions = [
            (90, screen_height - 70),  # Gobelet bleu
            (210, screen_height - 60),  # Gobelet rouge
            (330, screen_height - 70)   # Gobelet vert
        ]
        images = [GOBELET_BLEU, GOBELET_ROUGE, GOBELET_VERT]
    else:  # Niveau 2 et 3
        positions = [
            (90, screen_height - 70),   # Yaourt position 1
            (210, screen_height - 60),  # Yaourt position 2
            (330, screen_height - 70)   # Yaourt position 3
        ]
        images = [GOBELET_YAOURT] * 3  # Même image pour les 3 positions

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
        # Obstacle Jus - Hitbox précise
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 550, screen_height - 190)

        # Création de la hitbox basée sur le contour de l'image
        mask = pygame.mask.from_surface(JUS_OBSTACLE)
        outline = mask.outline()
        if outline:
            simplified = [v for i, v in enumerate(outline) if i % 5 == 0]  # Simplifier le contour
            vertices = [(x - JUS_OBSTACLE.get_width() / 2, y - JUS_OBSTACLE.get_height() / 2) for (x, y) in simplified]
            shape = pymunk.Poly(body, vertices)
        else:
            shape = pymunk.Poly.create_box(body, (JUS_OBSTACLE.get_width() * 0.9, JUS_OBSTACLE.get_height() * 0.9))

        shape.elasticity = 0.5
        shape.friction = 1.0
        space.add(body, shape)
        obstacles.append((body, shape, JUS_OBSTACLE))

        # Obstacle Jouet avec VOS VALEURS EXACTES
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 800, screen_height - 710)
        space.add(body)

        # Vos paramètres exacts du trou
        radius_x = 5  # Largeur du trou
        radius_y = 50  # Hauteur du trou
        segments = 20  # Nombre de segments pour l'ovale

        # Demi-cercle supérieur (comme dans votre code)
        top_vertices = []
        for i in range(segments + 1):
            angle = math.pi * i / segments
            x = radius_x * math.cos(angle) - 10
            y = -radius_y * math.sin(angle) - 30
            top_vertices.append((x, y))
        top_shape = pymunk.Poly(body, top_vertices)

        # Demi-cercle inférieur (comme dans votre code)
        bottom_vertices = []
        for i in range(segments + 1):
            angle = math.pi * i / segments
            x = radius_x * math.cos(angle) - 10
            y = radius_y * math.sin(angle) + 130
            bottom_vertices.append((x, y))
        bottom_shape = pymunk.Poly(body, bottom_vertices)

        # Propriétés physiques
        for shape in [top_shape, bottom_shape]:
            shape.elasticity = 0.7
            shape.friction = 0.3
            shape.collision_type = 4
            space.add(shape)

        # Stockage simple avec l'image
        obstacles.append((body, [top_shape, bottom_shape], JOUET_OBSTACLE))
    elif level == 2:
        # Avion (statique avec hitbox précise)
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 400, 150)
        mask = pygame.mask.from_surface(AVION_OBSTACLE)
        outline = mask.outline()
        simplified = [outline[i] for i in range(0, len(outline), 3)]  # Simplifier le contour
        vertices = [(x - AVION_OBSTACLE.get_width() / 2, y - AVION_OBSTACLE.get_height() / 2) for (x, y) in simplified]
        shape = pymunk.Poly(body, vertices)
        space.add(body, shape)
        obstacles.append((body, shape, AVION_OBSTACLE))

        # Bouteille (dynamique avec hitbox rectangulaire simple)
        body = pymunk.Body(1, pymunk.moment_for_box(1, (
        BOUTEILLE_OBSTACLE.get_width() * 0.7, BOUTEILLE_OBSTACLE.get_height() * 0.7)))
        body.position = (screen_width // 2, screen_height - 150)
        shape = pymunk.Poly.create_box(body,
                                       (BOUTEILLE_OBSTACLE.get_width() * 0.7, BOUTEILLE_OBSTACLE.get_height() * 0.7))
        shape.elasticity = 0.7
        shape.friction = 0.5
        space.add(body, shape)
        obstacles.append((body, shape, BOUTEILLE_OBSTACLE))

        # Livre (statique avec hitbox précise)
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (screen_width - 150, screen_height - 200)
        mask = pygame.mask.from_surface(LIVRE_OBSTACLE)
        outline = mask.outline()
        simplified = [outline[i] for i in range(0, len(outline), 3)]  # Simplifier le contour
        vertices = [(x - LIVRE_OBSTACLE.get_width() / 2, y - LIVRE_OBSTACLE.get_height() / 2) for (x, y) in simplified]
        shape = pymunk.Poly(body, vertices)
        space.add(body, shape)
        obstacles.append((body, shape, LIVRE_OBSTACLE))

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

        # Proximité avec nourriture (tous les éléments)
        bird.near_food = False
        food_lists = []
        if current_level == 1:
            food_lists = [banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions]
        elif current_level == 2:
            food_lists = [cookie_positions, poulet_positions, sandwich_positions, os_malus_positions, poubelle_positions]
        else:  # Niveau 3 - TOUS les éléments interactifs
            food_lists = [banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions]

        for lst in food_lists:
            for item in lst:
                if ((bird.body.position[0] - item[0])**2 + (bird.body.position[1] - item[1])**2)**0.5 < 50:
                    bird.near_food = True
                    break
            if bird.near_food:
                break

        # Collisions
        if current_level == 1 or current_level == 3:  # Mêmes règles pour 1 et 3
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

        for lst, points, size, img, color_effect in food_data:
            for item_pos in lst[:]:
                if ((bird.body.position[0] - item_pos[0])**2 + (bird.body.position[1] - item_pos[1])**2)**0.5 < 50:
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
    global cookie_positions, poulet_positions, sandwich_positions, os_malus_positions
    global score, current_bird_index, game_over, end_game_time

    clear_space()

    # Réinitialiser les oiseaux
    for bird in birds:
        bird.launched = False
        bird.size = 100
        bird.near_food = False
        bird.color_effect = None

    # Recréer la nourriture
    if current_level == 1:
        banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_food(current_level)
    elif current_level == 2:
        cookie_positions, poulet_positions, sandwich_positions, os_malus_positions, poubelle_positions = create_food(current_level)
    else:  # Niveau 3
        banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_random_food(current_level)

    create_ground()
    create_borders()
    obstacles = create_obstacles(current_level)
    gobelets = create_gobelets(current_level)

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

            # Déterminer la taille cible en fonction de si l'oiseau est près de la nourriture
            if bird.near_food:
                base_size = int(bird.size * 1.05)
            else:
                base_size = bird.size

            # Appliquer un effet de gourmandise si l'oiseau a ce pouvoir
            if hasattr(bird, 'power') and bird.power == 'Gourmand' and bird.near_food:
                target_size = (base_size * 1.5, base_size * 1.5)
            else:
                target_size = (base_size, base_size)

            if not hasattr(bird, 'cached_images'):
                bird.cached_images = {}

            size_key = tuple(target_size) + (bird.near_food,)
            if size_key not in bird.cached_images:
                base_image = bird.image_o if bird.near_food else bird.image_n

                # Appliquer l'effet de couleur si nécessaire (modification ici)
                if hasattr(bird, 'color_effect') and bird.color_effect:
                    # Créer une copie de l'image pour ne pas modifier l'originale
                    colored_image = base_image.copy()
                    # Créer une surface pour la teinte
                    tint = pygame.Surface(colored_image.get_size(), pygame.SRCALPHA)
                    tint.fill(bird.color_effect)
                    # Appliquer la teinte seulement aux pixels non transparents
                    colored_image.blit(tint, (0, 0), special_flags=pygame.BLEND_MULT)
                    base_image = colored_image

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

    reglage_btn = BoutonInteractif('Reglages2', ajustx(screen_width), ajusty(60), ajustx(162), ajusty(117))
    restart_btn = pygame.Rect(screen_width - 150, 20, 130, 50)
    menu_btn = pygame.Rect(screen_width - 150, 80, 130, 50)

    while running:
        # Afficher le décor approprié selon le niveau
        if current_level == 1:
            screen.blit(DECORS_NV1, (0, 0))
        elif current_level == 2:
            screen.blit(DECORS_NV2, (0, 0))
        else:
            screen.blit(DECORS_IMG, (0, 0))

        # Dessiner les obstacles s'ils existent
        if obstacles:
            for obstacle in obstacles:
                body, shape, img = obstacle
                if body.body_type == pymunk.Body.DYNAMIC:  # Seulement pour la bouteille
                    # Rotation en fonction de l'angle du corps physique
                    rotated_img = pygame.transform.rotate(img, -math.degrees(body.angle))
                    pos = int(body.position.x), int(body.position.y)
                    screen.blit(rotated_img, rotated_img.get_rect(center=pos))
                else:
                    # Obstacles statiques (affichage normal)
                    screen.blit(img, img.get_rect(center=(int(body.position.x), int(body.position.y))))

        # Dessiner les gobelets
        if gobelets:
            for body, shape, img in gobelets:
                img_rect = img.get_rect(center=(int(body.position.x), int(body.position.y)))
                screen.blit(img, img_rect)

        # Dessiner la nourriture selon le niveau
        if current_level == 1 :
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
        else:  # Niveau 3
            for img, positions in [
                (BANANE_BONUS, banane_positions),
                (HOTDOG_BONUS, hotdog_positions),
                (BURGER_BONUS, burger_positions),
                (BANANE_MALUS, banane_malus_positions),
                (POUBELLE_MALUS, poubelle_positions)
            ]:
                for pos in positions:
                    screen.blit(img, img.get_rect(center=pos))

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
                        return  # Retour au menu principal
                elif current_bird_index < len(birds):
                    start_pos = mouse_pos
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
            elif event.type == pygame.USEREVENT + 1:  # Réinitialiser l'effet de couleur
                for bird in birds:
                    if hasattr(bird, 'color_effect'):
                        bird.color_effect = None

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
        draw_restart_button()  # Dessine le bouton Restart
        draw_menu_button() # Dessine le bouton Menu

        # Gestion fin de partie
        if current_bird_index >= len(birds) or (end_game_time is not None and time.time() - end_game_time >= 2):
            if end_game_time is None:
                end_game_time = time.time()
            if time.time() - end_game_time >= (2 if len(hotdog_positions) == 0 else 4):
                if not game_over:
                    menu_sound.play()
                game_over = True
                restart_button, menu_button = draw_end_menu()  # On stocke les rect des boutons

        pygame.display.flip()
        pygame.time.delay(int(dt * 1000))


def jeu(level):
    global birds, banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions
    global cookie_positions, poulet_positions, sandwich_positions, os_malus_positions, brocoli_positions, dinde_positions
    global running, score, current_level, current_bird_index, space, selec_trois

    while True:
        reset_globals()
        space = pymunk.Space()
        space.gravity = (0, 900)
        clear_space()

        current_level = level
        selected_team = select_team()
        if selected_team == "menu":  # Si l'utilisateur a cliqué sur Retour
            return "menu"  # Retourne au menu principal

        past_power(selected_team)
        birds = selected_team.copy()

        if level == 1:
            banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_food(
                level)
            screen.blit(DECORS_NV1, (0, 0))
        elif level == 2:
            cookie_positions, poulet_positions, sandwich_positions, os_malus_positions, poubelle_positions = create_food(
                level)
            screen.blit(DECORS_NV2, (0, 0))
        else:  # Niveau 3
            banane_positions, hotdog_positions, burger_positions, banane_malus_positions, poubelle_positions = create_random_food(
                level)
            brocoli_positions = banane_malus_positions
            dinde_positions = poubelle_positions
            screen.blit(DECORS_IMG, (0, 0))

        create_ground()
        create_borders()
        obstacles = create_obstacles(level)
        gobelets = create_gobelets(level)

        gobelet_positions = [
            (330, screen_height - 70),
            (210, screen_height - 60),
            (90, screen_height - 70)
        ]

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

        running = True
        score = 0
        current_bird_index = 0
        start_pos = None
        game_over = False
        end_game_time = None

        result = game_loop(obstacles, gobelets)
        if result == "menu":
            return "menu"