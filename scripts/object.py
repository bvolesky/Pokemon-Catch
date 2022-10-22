import pygame


# CREATE INDIVIDUAL OBJECTS FOR SPRITE LAYERS
class Object(pygame.sprite.Sprite):
    def __init__(self, pos, groups, image, inflation=(0, -10)):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(inflation)
