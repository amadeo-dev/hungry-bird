import pygame
#pygame.image.load(f"Ressources/image/{name}.png")

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouton avec image")


button_image1 = pygame.image.load(f"Ressources/image/hotdog.png")  # Remplacez par votre image
button_image1 = pygame.transform.scale(button_image1, (150, 50))  # Redimensionner si nécessaire
button_rect = button_image1.get_rect(center=(WIDTH // 2, HEIGHT // 2))


button_image2 = pygame.image.load(f"Ressources/image/Nicolas.png")  # Remplacez par votre image
button_image2 = pygame.transform.scale(button_image2, (150, 50))  # Redimensionner si nécessaire
button_rect2 = button_image2.get_rect(center=(WIDTH // 3, HEIGHT // 3))


button_image3 = pygame.image.load(f"Ressources/image/burger.png")  # Remplacez par votre image
button_image3 = pygame.transform.scale(button_image3, (150, 50))  # Redimensionner si nécessaire
button_rect3 = button_image3.get_rect(center=(WIDTH // 4, HEIGHT // 4))


# Boucle principale
running = True
while running:
    screen.fill((30, 30, 30))  # Fond d'écran

    # Affichage du bouton
    screen.blit(button_image1, button_rect)
    screen.blit(button_image2, button_rect)
    screen.blit(button_image3, button_rect)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Bouton cliqué !")

    pygame.display.flip()

pygame.quit()
