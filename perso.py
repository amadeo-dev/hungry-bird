import pygame
import pymunk

class Tete:
    def __init__(self, name, img, position, space):
        self.name = name
        self.image = pygame.transform.scale(img, (70, 70))
        self.body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 15)
        self.shape.elasticity = 0.8
        self.shape.friction = 0.5
        space.add(self.body, self.shape)  # On passe l'espace comme argument
        self.launched = False

    def launch(self, impulse):
        if not self.launched:
            self.body.apply_impulse_at_local_point(impulse)
            self.launched = True

    def draw(self, screen):
        pos = self.body.position
        screen.blit(self.image, (pos.x - 35, pos.y - 35))