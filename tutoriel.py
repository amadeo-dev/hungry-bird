import pygame

def lancer_tutoriel(screen):
    # Charger l’image
    image_tutoriel = pygame.image.load("/Users/jackyzhang/PycharmProjects/hungry-bird/Ressources/image/Menu/Tutoriel.png").convert()
    image_tutoriel = pygame.transform.scale(image_tutoriel, screen.get_size())

    clock = pygame.time.Clock()
    en_tutoriel = True

    while en_tutoriel:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                en_tutoriel = False  # Quitte le tutoriel quand on clique ou appuie sur une touche

        screen.blit(image_tutoriel, (0, 0))
        pygame.display.flip()
        clock.tick(60)