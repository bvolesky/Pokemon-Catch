from scripts.entity import Entity
from scripts.support import *
import pygame
import random


# ENTITY THAT PLAYER CAPTURES
class Pokemon(Entity):
    def __init__(self, pos, groups, barrier_group, visible_group, grass_group,death_group,pokemon_sprites,pokemon_on_level,pokemon,player,animations):
        super().__init__(groups, barrier_group, visible_group, grass_group,death_group,pokemon_on_level)

        # GRAPHICS
        self.animations = animations
        self.image = self.animations['down'][0]

        # BOUNDARIES
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-26, -26)

        # MOVEMENT
        self.status = 'down'
        self.fleeing = False
        self.fleeing_time = None
        self.flee_cooldown = 3000
        self.base_animation_speed = 0.22
        self.animation_speed = self.base_animation_speed
        self.speed_compensation = 0.8
        self.runaway_duration = 45

        # GRASS
        self.in_grass = True

        # POKÉMON
        self.pokemon_sprites = pokemon_sprites
        self.sprite_type = 'pokemon'
        self.pokemon_name = pokemon["pokemon_name"]
        self.pokedex_number = pokemon["pokedex_number"]
        self.catch_rate = pokemon["catch_rate"]
        self.spawn_time = pygame.time.get_ticks()
        
        # SPEED
        self.base_speed = self.getSpeedFromZone()
        self.speed = self.base_speed
        
        # PLAYER
        self.player = player

    def getSpeedFromZone(self):
        modified_dex_no = str(int(self.pokedex_number) - 1)
        # ZONE 1
        if modified_dex_no in ['9', '12', '15', '18', '20', '22', '26', '40', '42', '49', '51', '59', '68', '73', '128']:
            return 3
        # ZONE 2
        elif modified_dex_no in ['24', '28', '31', '36', '45', '47', '53', '55', '57', '62', '71', '76', '78', '80', '83', '85', '87', '89', '91', '95', '97', '99', '103', '108', '115', '117', '119', '132']:
            return 4
        # ZONE 3
        elif modified_dex_no in ['0', '3', '6', '10', '11', '13', '14', '16', '19', '21', '23', '25', '27', '29', '32', '34', '37', '38', '41', '43', '46', '48', '52', '54', '56', '60', '63', '65', '66', '69', '74', '79', '82', '86', '88', '92', '96', '101', '104', '110', '113', '116', '121', '122', '123', '124', '125', '126', '127', '133', '134', '135', '137', '139', '146']:
            return 5
        # ZONE 4
        elif modified_dex_no in ['1', '2', '4', '5', '7', '8', '17', '30', '33', '39', '44', '50', '61', '64', '67', '70', '72', '75', '77', '81', '84', '90', '93', '94', '98', '100', '102', '105', '106', '107', '109', '111', '118', '120', '129', '130', '138', '140']:
            return 6
        # ZONE 5
        elif modified_dex_no in ['35', '58', '112', '114', '131', '136', '141', '142', '143', '144', '145', '147', '148', '149', '150']:
            return 7
        else:
            return 1

    def fleeCheck(self):
        # CHECKS TO SEE IF POKÉMON MOVEMENT NEEDS TO BE UPDATED
        if not self.fleeing:
            self.fleeing_time = pygame.time.get_ticks()
            self.fleeing = True
            card_list = ['left', 'right', 'up', 'down']
            if self.hitting_object:
                # DON'T ALLOW RANDOM MOVEMENT IN DIRECTION OF BARRIER
                self.hitting_object = False
                if self.status in card_list:
                    card_list.remove(self.status)

            # SET RANDOM DIRECTION FOR MOVE
            self.status = random.choice(card_list)
            self.direction = getDirection(self.status)
            if self.status in ['left', 'up']:
                self.speed = self.base_speed * self.speed_compensation
            else:
                self.speed = self.base_speed

    def runawayCheck(self):
        # ALLOW POKÉMON TO BE REMOVED FROM LEVEL AFTER SPECIFIED TIME
        runtime = pygame.time.get_ticks()
        if ((runtime - self.spawn_time)/1000) >= self.runaway_duration:
            if self.pokemon_name in self.pokemon_on_level:
                self.pokemon_on_level.remove(self.pokemon_name)
            self.player.pokemon_toast = 'runaway_{}'.format(self.pokemon_name)
            self.kill()
            runaway_sound = getSounds('runaway')
            runaway_sound.set_volume(0.5)
            runaway_sound.play()

    def update(self):
        self.cooldown()
        self.move(self.speed)
        self.animate()
