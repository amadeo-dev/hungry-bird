import pygame

def lancer_tutoriel(screen):
    # Définir la taille réduite pour le tutoriel
    largeur_tuto, hauteur_tuto = 1020, 720

    # Charger l’image de fond (même taille que le screen)
    fond = pygame.image.load("Ressources/image/Menu/Decors.png").convert()
    fond = pygame.transform.scale(fond, screen.get_size())

    # Charger l’image tutoriel redimensionnée
    image_tutoriel = pygame.image.load("Ressources/image/Menu/Instruction.png").convert_alpha()
    image_tutoriel = pygame.transform.scale(image_tutoriel, (largeur_tuto, hauteur_tuto))

    # Calculer la position pour centrer l’image tutoriel
    screen_rect = screen.get_rect()
    pos_x = (screen_rect.width - largeur_tuto) // 2
    pos_y = (screen_rect.height - hauteur_tuto) // 2

    clock = pygame.time.Clock()
    en_tutoriel = True

    while en_tutoriel:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                en_tutoriel = False

        screen.blit(fond, (0, 0))  # Dessiner le fond
        screen.blit(image_tutoriel, (pos_x, pos_y))  # Dessiner le tutoriel par-dessus
        pygame.display.flip()
        clock.tick(60)
