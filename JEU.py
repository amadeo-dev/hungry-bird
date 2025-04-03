import pygame
import random
import time
from Constantes import *
from map import *


# Version simplifiée de la classe Bird sans dépendre de perso.py
class Bird:
    def __init__(self, position, name):
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        physique.add(self.body, self.shape)
        self.size = BIRD_SIZE_DEFAULT
        self.launched = False
        self.name = name
        self.image = pygame.transform.scale(
            pygame.image.load(f"Ressources/image/{name}.png").convert_alpha(),
            (self.size, self.size)
        )


def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hungry Bird - Jeu Direct")
    return screen


def create_team():
    """Crée une équipe de 3 oiseaux aléatoires (sans utiliser perso.py)"""
    return random.sample(bird_name, 3)


def create_game_birds(selected_names):
    """Crée les oiseaux du jeu"""
    birds = []
    for i, name in enumerate(selected_names):
        bird = Bird((150 + i * 60, HEIGHT - 60), name)
        birds.append(bird)
    return birds


def create_food(level):
    """Crée la nourriture selon le niveau"""

    def random_pos(existing):
        for _ in range(100):
            pos = (random.randint(WIDTH // 2, WIDTH - 100), random.randint(HEIGHT - 300, HEIGHT - 150))
            if all(((pos[0] - o[0]) ** 2 + (pos[1] - o[1]) ** 2) ** 0.5 > MIN_DISTANCE for o in existing):
                existing.append(pos)
                return pos
        return (random.randint(WIDTH // 2, WIDTH - 100), random.randint(HEIGHT - 300, HEIGHT - 150))

    positions = []
    if level == 1:
        return [random_pos(positions) for _ in range(3)], [random_pos(positions) for _ in range(1)], [
            random_pos(positions) for _ in range(2)], [random_pos(positions) for _ in range(1)]
    elif level == 2:
        return [random_pos(positions) for _ in range(5)], [random_pos(positions) for _ in range(2)], [
            random_pos(positions) for _ in range(3)], [random_pos(positions) for _ in range(1)]
    elif level == 3:
        return [random_pos(positions) for _ in range(7)], [random_pos(positions) for _ in range(3)], [
            random_pos(positions) for _ in range(4)], [random_pos(positions) for _ in range(2)]


def main():
    # Initialisation
    screen = initialize_game()
    clock = pygame.time.Clock()

    # Création de l'équipe (3 oiseaux aléatoires)
    selected_names = create_team()
    birds = create_game_birds(selected_names)

    # Configuration du jeu
    current_level = 1
    foods = create_food(current_level)
    create_bordures()

    score = 0
    current_bird_index = 0
    start_pos = None
    game_over = False
    end_time = None

    # Boucle principale
    running = True
    while running:
        dt = 1 / 60.0
        screen.blit(DECORS, (0, 0))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # Réinitialisation
                    selected_names = create_team()
                    birds = create_game_birds(selected_names)
                    current_level = 1
                    foods = create_food(current_level)
                    score = 0
                    current_bird_index = 0
                    game_over = False
                    end_time = None
                elif current_bird_index < len(birds):
                    start_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and start_pos:
                end_pos = pygame.mouse.get_pos()
                bird_index = len(birds) - 1 - current_bird_index
                impulse = ((start_pos[0] - end_pos[0]) * 5, (start_pos[1] - end_pos[1]) * 5)
                birds[bird_index].body.apply_impulse_at_local_point(impulse)
                birds[bird_index].launched = True
                current_bird_index += 1
                start_pos = None

        # Mise à jour physique
        physique.step(dt)

        # Limitation de vitesse
        for bird in birds:
            vx, vy = bird.body.velocity
            speed = (vx ** 2 + vy ** 2) ** 0.5
            if speed > MAX_SPEED:
                factor = MAX_SPEED / speed
                bird.body.velocity = (vx * factor, vy * factor)

        # Vérifier collisions
        hotdogs, burgers, brocolis, dindes = foods
        for bird in birds:
            if bird.launched:
                for food_list, points in [
                    (hotdogs, 1), (burgers, 3),
                    (brocolis, -2), (dindes, 10)
                ]:
                    for food in food_list[:]:
                        if bird.body.position.get_distance(food) < 40:
                            score += points
                            food_list.remove(food)

        # Dessiner les éléments
        for bird in birds:
            screen.blit(bird.image, bird.image.get_rect(center=bird.body.position))

        for img, positions in [
            (HOTDOG, foods[0]), (BURGER, foods[1]),
            (BROCOLI, foods[2]), (DINDE, foods[3])
        ]:
            for pos in positions:
                screen.blit(img, img.get_rect(center=pos))

        # UI
        font = pygame.font.SysFont(None, 36)
        texts = [
            f"Score: {score}",
            f"Niveau: {current_level}",
            f"Équipe: {', '.join(b.name for b in birds)}"
        ]
        for i, text in enumerate(texts):
            screen.blit(font.render(text, True, (255, 0, 0)), (20, 20 + i * 40))

        screen.blit(RESTART, (WIDTH - 70, 20))

        # Fin de niveau
        all_food_collected = all(not food_list for food_list in foods)
        if current_bird_index >= len(birds) or all_food_collected:
            if end_time is None:
                end_time = time.time()

            if time.time() - end_time >= 2:
                game_over = True
                font = pygame.font.SysFont(None, 72)

                if all_food_collected and current_level < 3:
                    msg = "Niveau réussi!"
                    current_level += 1
                    birds = create_game_birds(selected_names)
                    foods = create_food(current_level)
                    current_bird_index = 0
                    game_over = False
                    end_time = None
                elif all_food_collected:
                    msg = "Victoire finale!"
                else:
                    msg = "Game Over"

                text = font.render(msg, True, (0, 255, 0) if all_food_collected else (255, 0, 0))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()