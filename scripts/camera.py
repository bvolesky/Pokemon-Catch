import pygame


# USED TO "FOLLOW" PLAYER AROUND MAP BY CENTERING MAP TO PLAYER MOVEMENT
class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # SET UP MAP
        self.screen = pygame.display.get_surface()
        self.x = self.screen.get_size()[0] // 2
        self.y = self.screen.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.map = pygame.image.load('assets/images/screens/launch/map.png').convert()
        self.map_rect = self.map.get_rect(topleft=(0, 0))

    def adjustMapTo(self, player):
        # CREATE OFFSETS
        self.offset.x = player.hitbox.centerx - self.x
        self.offset.y = player.hitbox.centery - self.y

        # MOVE MAP
        new_map_position = self.map_rect.topleft - self.offset
        self.screen.blit(self.map, new_map_position)

        # MOVE SPRITES
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)
