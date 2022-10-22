import pygame
import random
from scripts.support import getSounds


# USED TO CREATE A PLAYER, POKÉMON, AND BALLS
class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, barrier_group=None, visible_group=None, grass_group=None, death_group=None, pokemon_on_level=None):
        super().__init__(groups)

        # SPRITES
        self.barrier_group = barrier_group
        self.visible_group = visible_group
        self.grass_group = grass_group
        self.death_group = death_group

        # ENTITY BOUNDARIES
        self.direction = pygame.math.Vector2()
        self.hitting_object = False
        self.barrier_direction = (0, 0)

        # ANIMATION
        self.frame_index = 0

        # DEATH
        self.pokemon_on_level = pokemon_on_level

    def cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.sprite_type == 'player':
            # IF COOLDOWN HAS EXPIRED, ALLOW MOVEMENT
            if self.throwing and current_time - self.throw_time >= self.throw_cooldown:
                self.throwing = False

            # IF REGEN TIME PASSED, REGEN HEALTH
            elif self.regenerating_energy and current_time - self.regeneration_time >= self.regeneration_cooldown:
                self.regenerating_energy = False

        elif self.sprite_type == 'pokemon':
            # IF FLEE TIME PASSED, READY TO FLEE
            if (self.fleeing and current_time - self.fleeing_time >= self.flee_cooldown) or self.hitting_object:
                self.fleeing = False

        elif self.sprite_type == 'ball':
            # HIT POKÉMON AND WOBBLE ANIMATION COMPLETED
            if self.hit_pokemon and ((current_time - self.hit_time) >= self.hit_cooldown):
                chance = ((self.backup_sprite.catch_rate / 255) * self.player.ball.rate) * 100
                lucky_number = random.randint(1, 100)
                if lucky_number < chance:
                    # WON CAPTURE TOSS
                    dex_no = str(self.backup_sprite.pokedex_number - 1)
                    zone_lists = [self.player.zone_1, self.player.zone_2, self.player.zone_3, self.player.zone_4, self.player.zone_5]
                    for i in zone_lists:
                        if dex_no in i:
                            index = int(zone_lists.index(i)) + 1
                            i.remove(dex_no)  # REMOVE POKÉMON FROM ZONE LIST
                            if len(i) == 0:
                                self.player.zone_complete = index  # ZONE CLEAR FLAG

                    # REGENERATE HEALTH
                    if self.player.energy + self.player.regeneration_amount <= self.player.energy_max:
                        self.player.energy += self.player.regeneration_amount
                    else:
                        self.player.energy = self.player.energy_max

                    # REMOVE POKÉMON FROM LEVEL
                    if self.backup_sprite.pokemon_name in self.player.pokemon_on_level:
                        self.player.pokemon_on_level.remove(self.backup_sprite.pokemon_name)

                    # SET CAPTURE ATTRIBUTES, KILL BALL
                    self.player.caught_pokemon.append(self.backup_sprite.pokemon_name)
                    self.player.pokemon_toast = 'capture'
                    self.player.hit_name = self.backup_sprite.pokemon_name
                    self.player.captured_sound.set_volume(0.5)
                    self.player.captured_sound.play()
                    self.hit_pokemon = False
                    self.kill()

                    # JIGGLYPUFF SONG
                    if self.backup_sprite.pokemon_name.lower() == 'jigglypuff' and not self.jigglypuff_singing_started:
                        jigglypuff_singing_sound = getSounds('jigglypuff_singing')
                        jigglypuff_singing_sound.set_volume(0.3)
                        jigglypuff_singing_sound.play()
                        self.jigglypuff_singing_started = True

                    # POKÉFLUTE SONG
                    elif self.backup_sprite.pokemon_name.lower() == 'snorlax' and not self.pokeflute_sound_started:
                        pokeflute_sound = getSounds('pokeflute')
                        pokeflute_sound.set_volume(0.3)
                        pokeflute_sound.play()
                        self.pokeflute_sound_started = True

                    # RESUME FROM LEGENDARY BATTLE
                    elif self.backup_sprite.pokemon_name.lower() in ['articuno', 'zapdos', 'moltres']:
                        pygame.mixer.stop()
                        self.player.safari_music.set_volume(0.25)
                        self.player.safari_music.play(615)

                    # CAPTURED MEW, FADEOUT MUSIC FOR RESULTS SCREEN
                    elif self.backup_sprite.pokemon_name.lower() == 'mew':
                        pygame.mixer.fadeout(2000)
                        self.player.captured_sound.set_volume(0.5)
                        self.player.captured_sound.play()

                else:
                    # LOST TOSS
                    self.ball_wobble_sound_playing = False
                    self.ball_open_sound.set_volume(0.75)
                    self.ball_open_sound.play()
                    self.ball_opened = True
                    self.player.pokemon_toast = 'fail'
                    self.player.hit_name = self.backup_sprite.pokemon_name

    def move(self, speed):
        # UPDATE HITBOX
        self.hitbox.x += self.direction.x * speed
        self.hitbox.y += self.direction.y * speed
        self.rect.center = self.hitbox.center

        if self.sprite_type == 'player' and self.direction.magnitude() and self.energy - 1 >= 0:
            # ENERGY DRAINS LESS THE MORE WATER THE PLAYER DRINKS
            if self.picked_up_water == 1:
                self.energy -= 0.010
            elif self.picked_up_water == 2:
                self.energy -= 0.005
            elif self.picked_up_water == 3:
                self.energy -= 0.003
            else:
                self.energy -= 0.015

        # COLLISION WITH DEATH TILE - PREVENTS POKÉMON FROM BLITTING OUT OF BOUNDS
        if self.sprite_type == 'pokemon':
            for death_tile in self.death_group:
                if death_tile.hitbox.colliderect(self.hitbox):
                    if self.pokemon_name in self.pokemon_on_level:
                        self.pokemon_on_level.remove(self.pokemon_name)
                    self.player.pokemon_toast = 'runaway_{}'.format(self.pokemon_name)
                    self.kill()

                    # POKÉMON RUNS AWAY
                    runaway_sound = getSounds('runaway')
                    runaway_sound.set_volume(0.5)
                    runaway_sound.play()

        # COLLISION WITH BARRIER
        barriers = False
        for barrier in self.barrier_group:
            if barrier.hitbox.colliderect(self.hitbox):
                self.direction = pygame.math.Vector2(0, 0)  # PREVENTS TELEPORTATION
                barriers = True
                if (self.sprite_type == 'player' or self.sprite_type == 'pokemon') and not self.hitting_object:
                    self.hitting_object = True
                    if self.sprite_type == 'player':
                        self.collision_sound.set_volume(0.2)
                        self.collision_sound.play()
                self.barrier_direction = self.direction

                # BALL HIT BARRIER
                if self.sprite_type == 'ball':
                    self.kill()

                # COLLISION LOGIC
                else:
                    if self.status == 'up':  # MOVE ENTITY DOWN
                        self.hitbox.top = barrier.hitbox.bottom

                    elif self.status == 'down':  # MOVE ENTITY UP
                        self.hitbox.bottom = barrier.hitbox.top

                    elif self.status == 'left':  # MOVE ENTITY RIGHT
                        self.hitbox.left = barrier.hitbox.right

                    elif self.status == 'right':  # MOVE ENTITY LEFT
                        self.hitbox.right = barrier.hitbox.left
                    self.rect.center = self.hitbox.center

        # UPDATE HITTING STATUS
        if not barriers:
            self.hitting_object = False

        # POKÉBALL HITS POKÉMON
        if self.sprite_type == 'ball' and self in self.visible_group and not self.hit_pokemon:
            for pokemon in self.pokemon_sprites:
                if pokemon.hitbox.colliderect(self.hitbox):
                    self.backup_sprite = pokemon
                    self.player.balls_hit += 1
                    pokemon.in_grass = False
                    self.hit_pokemon = True
                    self.hit_time = pygame.time.get_ticks()
                    pokemon.kill()
                    break

        # RESET HITTING STATUS IF MOVEMENT CHANGES
        if self.barrier_direction != self.direction:
            self.hitting_object = False

    def animate(self):
        if self.sprite_type == 'player' or self.sprite_type == 'pokemon':
            # WHEN STATUS CHANGES, UPDATE SPRITE
            animation = self.animations[self.status]
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
            self.image = animation[int(self.frame_index)]  # ROUNDED FRAME INDEX TO ANIMATION SPEED
            self.rect = self.image.get_rect(center=self.hitbox.center)  # WAS CENTER

        elif self.sprite_type == 'ball':
            self.frame_index += self.animation_speed
            # BALL TIMED OUT
            if self.frame_index >= len(self.frames) and not self.hit_pokemon:
                self.kill()
                self.animation_speed = 0.1
                self.frames = self.backup_frames

                # POKÉMON BROKE OUT
                if self.pokemon_broke_out:
                    # RESPAWN POKÉMON
                    self.visible_group.add(self.backup_sprite)
                    self.pokemon_sprites.add(self.backup_sprite)
                    self.player.pokemon = self.backup_sprite
                    self.player.pokemon.in_grass = True
                    pygame.display.get_surface().blit(self.player.pokemon.image, self.rect.center)
                    self.pushLayerToBottom(self.player)
                    self.player.pokemon.spawn_time = pygame.time.get_ticks()

            # BALL IS ALIVE
            else:
                if not self.ball_opened:
                    # POKÉMON HAS NOT BROKEN OUT
                    if self.hit_pokemon:
                        if not self.close_animation_complete:
                            self.frames = self.ball_close[self.player.ball.name]  # LOAD BALL CLOSE FRAMES
                            self.animation_speed = 0.07
                            if self.frame_index >= len(self.frames):  # BALL CLOSING COMPLETED
                                self.frames = self.ball_wobble[self.player.ball.name]  # LOAD WOBBLE FRAMES
                                self.close_animation_complete = True
                            else:
                                self.animation_speed = 0.1
                                self.image = self.frames[int(self.frame_index)]  # LOAD NEXT BALL FRAME
                        else:
                            if self.frame_index >= len(self.frames):
                                self.frame_index = 0

                            if int(self.frame_index) in [2, 4] and not self.ball_wobble_sound_playing:  # KEEP WOBBLE SOUND PACE
                                self.ball_wobble_sound.set_volume(0.5)
                                self.ball_wobble_sound.play()
                                self.ball_wobble_sound_playing = True
                            elif int(self.frame_index) in [0, 1, 3]:
                                self.ball_wobble_sound.stop()
                                self.ball_wobble_sound_playing = False
                            self.image = self.frames[int(self.frame_index)]
                    else:
                        self.image = self.frames[int(self.frame_index)]  # KEEP LOADING THROWN BALL FRAMES

                # POKÉMON BROKE OUT
                else:
                    if not self.pokemon_broke_out:
                        self.pokemon_broke_out = True
                        self.hit_pokemon = False  # THIS IS WHAT TRIGGERS THE POKÉMON TO RESPAWN
                        self.frames = self.ball_open[self.player.ball.name]  # LOAD BALL OPEN FRAMES
                        self.animation_speed = 0.07
                    else:
                        if self.frame_index >= len(self.frames):
                            self.animation_speed = 0.1
                            self.frames = self.backup_frames  # KEEP WOBBLING

                        else:
                            self.image = self.frames[int(self.frame_index)]
