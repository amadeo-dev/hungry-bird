import pygame

def lancer_tutoriel(screen):
    # Définir une taille un peu plus petite que l'écran pour afficher le tuto au centre
    largeur_tuto, hauteur_tuto = 1020, 720

    # Charger l’image de fond (le décor classique)
    fond = pygame.image.load("Ressources/image/Menu/Decors.png").convert()
    fond = pygame.transform.scale(fond, screen.get_size())  # On adapte à la taille de l’écran

    # Charger l’image du tutoriel (explications du jeu)
    image_tutoriel = pygame.image.load("Ressources/image/Menu/Instruction.png").convert_alpha()
    image_tutoriel = pygame.transform.scale(image_tutoriel, (largeur_tuto, hauteur_tuto))

    # On centre l’image tutoriel dans l’écran
    screen_rect = screen.get_rect()
    pos_x = (screen_rect.width - largeur_tuto) // 2
    pos_y = (screen_rect.height - hauteur_tuto) // 2

    clock = pygame.time.Clock()
    en_tutoriel = True  # On reste dans la boucle tant que le joueur n’a pas cliqué ou appuyé sur une touche

    while en_tutoriel:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                en_tutoriel = False  # Dès que le joueur interagit → on sort du tuto

        screen.blit(fond, (0, 0))  # On affiche le fond
        screen.blit(image_tutoriel, (pos_x, pos_y))  # On affiche le visuel tutoriel par-dessus
        pygame.display.flip()
        clock.tick(60)  # 60 FPS pour que ce soit fluide
