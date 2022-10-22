import pygame.mixer

from scripts.world import WORLD_MAP
from scripts.player import Player
from scripts.pokemon import Pokemon
from scripts.hud import HUD
from scripts.camera import Camera
from scripts.animation import *


# PLAYABLE STAGE
class Level:
    def __init__(self):

        # SPRITE GROUPS
        self.visible_group = Camera()
        self.barrier_group = pygame.sprite.Group()
        self.overlay_group = pygame.sprite.Group()
        self.pokemon_group = pygame.sprite.Group()
        self.grass_group = pygame.sprite.Group()
        self.death_group = pygame.sprite.Group()

        # SPRITE LISTS
        self.grass_list = []
        self.ball_list = []
        self.shoes = []
        self.waters = []
        self.waters_picked_up = 0

        # SCREEN
        self.screen = pygame.display.get_surface()
        self.HUD = HUD()

        # POKÉMON
        self.max_pokemon_at_once = 10

        # PICKUPS
        self.pokeball_image = pygame.image.load('assets/images/sprites/pickups/balls/pokeball/throw/down/0.png').convert_alpha()
        self.greatball_image = pygame.image.load('assets/images/sprites/pickups/balls/greatball/throw/down/0.png').convert_alpha()
        self.ultraball_image = pygame.image.load('assets/images/sprites/pickups/balls/ultraball/throw/down/0.png').convert_alpha()
        self.ball_lookup = {'pokeball': self.pokeball_image, 'greatball': self.greatball_image, 'ultraball': self.ultraball_image}
        self.water_image = pygame.image.load('assets/images/sprites/pickups/water/water.png').convert_alpha()
        self.shoes_image = pygame.image.load('assets/images/sprites/pickups/shoes/shoes.png').convert_alpha()

        # OVERLAYS
        self.grass_image = pygame.image.load('assets/images/sprites/map/vegetation/grass/grass.png').convert_alpha()
        self.shrub_image = pygame.image.load('assets/images/sprites/map/vegetation/shrub/shrub.png').convert_alpha()
        self.tree_top_left_image = pygame.image.load('assets/images/sprites/map/vegetation/tree/top/left.png').convert_alpha()
        self.tree_top_center_image = pygame.image.load('assets/images/sprites/map/vegetation/tree/top/center.png').convert_alpha()
        self.tree_top_right_image = pygame.image.load('assets/images/sprites/map/vegetation/tree/top/right.png').convert_alpha()
        self.tree_bottom_left_image = pygame.image.load('assets/images/sprites/map/vegetation/tree/bottom/left.png').convert_alpha()
        self.tree_bottom_center_image = pygame.image.load('assets/images/sprites/map/vegetation/tree/bottom/center.png').convert_alpha()
        self.tree_bottom_right_image = pygame.image.load('assets/images/sprites/map/vegetation/tree/bottom/right.png').convert_alpha()
        self.log_image = pygame.image.load('assets/images/sprites/map/log/logs.png').convert_alpha()
        self.building_top_left_image = pygame.image.load('assets/images/sprites/map/building/top/left.png').convert_alpha()
        self.building_top_center_image = pygame.image.load('assets/images/sprites/map/building/top/center.png').convert_alpha()
        self.building_top_right_image = pygame.image.load('assets/images/sprites/map/building/top/right.png').convert_alpha()
        self.building_bottom_left_image = pygame.image.load('assets/images/sprites/map/building/bottom/left.png').convert_alpha()
        self.building_bottom_center_image = pygame.image.load('assets/images/sprites/map/building/bottom/center.png').convert_alpha()
        self.building_bottom_right_image = pygame.image.load('assets/images/sprites/map/building/bottom/right.png').convert_alpha()

        # ANIMATIONS
        self.animation = Animations(self.barrier_group, self.visible_group, self.grass_group, self.pokemon_group, self.overlay_group)

        # AUDIO
        self.start_of_game = False
        self.legendary_battle_sound = getSounds('legendary_battle')
        self.mewtwo_sound = getSounds('mewtwo')
        self.mew_sound = getSounds('mew')
        self.safari_music = getSounds('safari_music')
        self.ball_pickup_sound = getSounds('ball_pickup')
        self.shoes_pickup_sound = getSounds('shoes_pickup')
        self.water_pickup_sound = getSounds('water_pickup')
        self.sound_queue = []

        # MAP
        self.createMap()

    def createMap(self):

        # CREATE OBJECTS FOR EACH TILE IN WORLD
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * 64
                y = row_index * 64
                if col == 'x':
                    Barrier((x, y), [self.barrier_group])
                if col == 't':
                    Barrier((x, y), [self.death_group])
                elif col == '1':
                    g = Grass((x, y), [self.grass_group, self.visible_group], self.grass_image, (-30, -30), 1)
                    self.grass_list.append(g)
                elif col == '2':
                    g = Grass((x, y), [self.grass_group, self.visible_group], self.grass_image, (-30, -30), 2)
                    self.grass_list.append(g)
                elif col == '3':
                    g = Grass((x, y), [self.grass_group, self.visible_group], self.grass_image, (-30, -30), 3)
                    self.grass_list.append(g)
                elif col == '4':
                    g = Grass((x, y), [self.grass_group, self.visible_group], self.grass_image, (-30, -30), 4)
                    self.grass_list.append(g)
                elif col == '5':
                    g = Grass((x, y), [self.grass_group, self.visible_group], self.grass_image, (-30, -30), 5)
                    self.grass_list.append(g)
                elif col == '6':
                    wa = Object((x, y), [self.visible_group], self.water_image, (-26, -26))
                    self.waters.append(wa)
                elif col == '7':
                    sh = Object((x, y), [self.visible_group], self.shoes_image, (-26, -26))
                    self.shoes.append(sh)
                elif col == '8':
                    pb = Ball((x, y), [self.visible_group], self.pokeball_image, (-26, -26), 'pokeball')
                    self.ball_list.append(pb)
                elif col == '9':
                    gb = Ball((x, y), [self.visible_group], self.greatball_image, (-26, -26), 'greatball')
                    self.ball_list.append(gb)
                elif col == '0':
                    ub = Ball((x, y), [self.visible_group], self.ultraball_image, (-26, -26), 'ultraball')
                    self.ball_list.append(ub)
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_group], self.barrier_group, self.visible_group, self.grass_group, self.pokemon_group, self.overlay_group, self.spawnBall)
                elif col == 'q':
                    Object((x, y), [self.visible_group, self.overlay_group], self.tree_top_left_image)
                elif col == 'a':
                    Object((x, y), [self.visible_group, self.barrier_group, self.overlay_group], self.tree_bottom_left_image)
                elif col == 'w':
                    Object((x, y), [self.visible_group, self.overlay_group], self.tree_top_center_image)
                elif col == 's':
                    Object((x, y), [self.visible_group, self.barrier_group, self.overlay_group], self.tree_bottom_center_image)
                elif col == 'e':
                    Object((x, y), [self.visible_group, self.overlay_group], self.tree_top_right_image)
                elif col == 'd':
                    Object((x, y), [self.visible_group, self.barrier_group, self.overlay_group], self.tree_bottom_right_image)
                elif col == 'l':
                    Object((x, y), [self.visible_group, self.barrier_group, self.overlay_group], self.log_image)
                elif col == 'y':
                    Object((x, y), [self.visible_group, self.overlay_group], self.building_top_left_image)
                elif col == 'u':
                    Object((x, y), [self.visible_group, self.overlay_group], self.building_top_center_image)
                elif col == 'i':
                    Object((x, y), [self.visible_group, self.overlay_group], self.building_top_right_image)
                elif col == 'h':
                    Object((x, y), [self.visible_group, self.barrier_group, self.overlay_group], self.building_bottom_left_image)
                elif col == 'j':
                    Object((x, y), [self.visible_group, self.barrier_group, self.overlay_group], self.building_bottom_center_image)
                elif col == 'k':
                    Object((x, y), [self.visible_group, self.barrier_group, self.overlay_group], self.building_bottom_right_image)
                elif col == 'r':
                    Object((x, y), [self.visible_group, self.barrier_group, self.overlay_group], self.shrub_image)

        # MAKE SURE PLAYER IS ABOVE MAP SPRITES
        pushLayerToTop(self.player, self.visible_group)

        # KEEP OVERLAYS ON TOP LAYER
        for overlay in self.overlay_group:
            pushLayerToTop(overlay, self.visible_group)

    def spawnBall(self):
        status = self.player.status
        if 'idle' in self.player.status:
            status = self.player.status.split('_')[0]
        self.animation.updateThrowAnimation(self.player, [self.visible_group], '{}_{}'.format(self.player.ball.name, status))

    def rustleGrass(self, hitbox):
        for sprite in self.grass_list:
            if sprite.hitbox.colliderect(hitbox):
                pos = sprite.hitbox.center
                pos = (pos[0] - 32, pos[1] - 32)  # COMPENSATE
                self.animation.updateGrassAnimation(pos, [self.visible_group])

    # LOOPS IN MAIN.PYW
    def run(self, seconds_paused):

        # START OF GAME MUSIC
        if not self.start_of_game:
            self.start_of_game = True
            self.player.safari_music.set_volume(0.25)
            self.player.safari_music.play(615)

        # UPDATE VISIBLE SPRITES
        self.visible_group.adjustMapTo(self.player)
        self.visible_group.update()

        # CHECK IF POKÉMON NEED TO RUN AWAY OR KEEP MOVING
        for pokemon in self.pokemon_group:
            pokemon.runawayCheck()
            pokemon.fleeCheck()

        # CHECK FOR PLAYER GRASS RUSTLE
        if self.player.in_grass and 'idle' not in self.player.status:
            self.rustleGrass(self.player.hitbox)

        # CHECK FOR POKÉMON GRASS RUSTLE
        for pokemon in self.pokemon_group:
            if pokemon.in_grass:
                self.rustleGrass(pokemon.hitbox)
        self.grass_group.update()

        # CHECK IF PLAYER HAS PICKED UP ITEM
        pickup_lists = [self.ball_list, self.shoes, self.waters]
        for pickup_list in pickup_lists:
            for item in pickup_list:
                if item.hitbox.colliderect(self.player.hitbox):

                    # PLAYER PICKED UP BALL
                    if item in self.ball_list:
                        if self.sound_queue:
                            for sound in self.sound_queue:
                                sound.stop()
                            self.sound_queue.clear()
                        self.sound_queue.append(self.ball_pickup_sound)
                        self.ball_pickup_sound.set_volume(0.2)
                        self.ball_pickup_sound.play()
                        self.player.picked_up_ball = True
                        self.player.ball_name = item.name
                        self.player.ball_image = self.ball_lookup[item.name]
                        self.player.ball = item
                        self.player.stats['throw_speed'] = item.throw_speed

                    # PLAYER PICKED UP SHOES
                    elif item in self.shoes:
                        if self.sound_queue:
                            for sound in self.sound_queue:
                                sound.stop()
                            self.sound_queue.clear()
                        self.sound_queue.append(self.shoes_pickup_sound)
                        self.shoes_pickup_sound.set_volume(0.2)
                        self.shoes_pickup_sound.play()
                        self.player.picked_up_shoes = True
                        self.player.stats['speed'] = 6
                        self.player.speed = 6
                        self.player.animation_speed *= 1.2

                    # PLAYER PICKED UP WATER
                    elif item in self.waters:
                        if self.sound_queue:
                            for sound in self.sound_queue:
                                sound.stop()
                            self.sound_queue.clear()
                        self.sound_queue.append(self.water_pickup_sound)
                        self.water_pickup_sound.set_volume(0.15)
                        self.water_pickup_sound.play()
                        self.player.energy_max += 30
                        self.waters_picked_up += 1
                        self.player.energy = self.player.energy_max
                        self.player.picked_up_water = self.waters_picked_up

                    if item in pickup_list:
                        pickup_list.remove(item)
                    item.kill()
                    break

        # UPDATE HUD
        self.HUD.run(self.player, self.waters_picked_up, seconds_paused, self.player.zone_complete)

        # SPAWN POKÉMON
        if self.player.pokemon_appeared and self.player.pokemon_appeared['pokemon_name'] not in self.player.caught_pokemon and self.player.pokemon_appeared["pokemon_name"] not in self.player.pokemon_on_level and len(self.player.pokemon_on_level) < self.max_pokemon_at_once:
            self.player.pokemon_on_level.append(self.player.pokemon_appeared['pokemon_name'])
            self.player.pokemon = Pokemon((self.player.hitbox.x, self.player.hitbox.y), [self.visible_group, self.pokemon_group], self.barrier_group, self.visible_group, self.grass_group,self.death_group,self.pokemon_group,self.player.pokemon_on_level, self.player.pokemon_appeared,self.player)  # self.player.pokemon_appeared['pokemon_name'].lower()
            self.screen.blit(self.player.pokemon.image, (self.player.hitbox.x, self.player.hitbox.y))
            self.player.pokemon_appeared = False

            # POKÉMON CRIES
            if len(str(self.player.pokemon.pokedex_number)) == 1:
                modified_dex_no = "00{}".format(str(self.player.pokemon.pokedex_number))
            elif len(str(self.player.pokemon.pokedex_number)) == 2:
                modified_dex_no = "0{}".format(str(self.player.pokemon.pokedex_number))
            else:
                modified_dex_no = str(self.player.pokemon.pokedex_number)
            cry = getSounds(modified_dex_no)
            cry.set_volume(0.5)
            cry.play()

            # BATTLE SOUNDS
            if self.player.pokemon.pokemon_name.lower() == 'articuno' and not self.player.articuno_sound_started:
                pygame.mixer.stop()
                self.legendary_battle_sound.set_volume(0.3)
                self.legendary_battle_sound.play(100)
                self.player.articuno_sound_started = True

            elif self.player.pokemon.pokemon_name.lower() == 'zapdos' and not self.player.zapdos_sound_started:
                pygame.mixer.stop()
                self.legendary_battle_sound.set_volume(0.3)
                self.legendary_battle_sound.play(100)
                self.player.zapdos_sound_started = True

            elif self.player.pokemon.pokemon_name.lower() == 'moltres' and not self.player.moltres_sound_started:
                pygame.mixer.stop()
                self.legendary_battle_sound.set_volume(0.3)
                self.legendary_battle_sound.play(100)
                self.player.moltres_sound_started = True

            elif self.player.pokemon.pokemon_name.lower() == 'mewtwo' and not self.player.mewtwo_sound_started:
                pygame.mixer.stop()
                self.mewtwo_sound.set_volume(0.4)
                self.mewtwo_sound.play(100)
                self.player.mewtwo_sound_started = True

            elif self.player.pokemon.pokemon_name.lower() == 'mew' and not self.player.mew_sound_started:
                pygame.mixer.stop()
                self.mew_sound.set_volume(0.4)
                self.mew_sound.play(100)
                self.player.mew_sound_started = True

            # PUSH PLAYER AND OVERLAYS ABOVE POKÉMON SPRITE
            for i in self.overlay_group:
                pushLayerToTop(i, self.visible_group)