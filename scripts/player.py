import pygame.mixer

from scripts.animation import Animations
from scripts.interaction import *
from random import randint


# CONTROLLABLE ENTITY USED TO PLAY GAME
class Player(Entity):
    def __init__(self, pos, groups, barrier_group, visible_group, grass_group, pokemon_group, overlay_group, throwBall):
        super().__init__(groups, barrier_group, visible_group, grass_group)

        # SPRITES
        self.sprite_type = 'player'
        self.pokemon_group = pokemon_group
        self.overlay_group = overlay_group

        # GRAPHICS
        self.image = pygame.image.load('assets/images/sprites/player/up_idle/0.png').convert_alpha()
        self.animations = getPlayerSprites()

        # AUDIO
        self.captured_sound = getSounds('captured')
        self.collision_sound = getSounds('collision')
        self.ball_throw_sound = getSounds('ball_throw')
        self.safari_music = getSounds('safari_music')
        self.pre_mew_sound = getSounds('pre_mew')
        self.articuno_sound_started = False
        self.zapdos_sound_started = False
        self.moltres_sound_started = False
        self.articuno_sound_completed = False
        self.zapdos_sound_completed = False
        self.moltres_sound_completed = False
        self.mewtwo_sound_started = False
        self.pre_mew_sound_started = False
        self.mew_sound_started = False

        # BOUNDARIES
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-5, -27)

        # MOVEMENT
        self.status = 'up'
        self.picked_up_shoes = False
        self.player_lookup = {'up': {'key': pygame.K_UP, 'direction': (0, -1), 'speed_increase': False}, 'down': {'key': pygame.K_DOWN, 'direction': (0, 1), 'speed_increase': True}, 'left': {'key': pygame.K_LEFT, 'direction': (-1, 0), 'speed_increase': False}, 'right': {'key': pygame.K_RIGHT, 'direction': (1, 0), 'speed_increase': True}}
        self.keys = []
        self.key_list = [pygame.K_BACKSPACE,pygame.K_TAB,pygame.K_CLEAR,pygame.K_PAUSE,pygame.K_ESCAPE,pygame.K_SPACE,pygame.K_EXCLAIM,pygame.K_QUOTEDBL,pygame.K_HASH,pygame.K_DOLLAR,pygame.K_AMPERSAND,pygame.K_QUOTE,pygame.K_LEFTPAREN,pygame.K_RIGHTPAREN,pygame.K_ASTERISK,pygame.K_PLUS,pygame.K_COMMA,pygame.K_MINUS,pygame.K_PERIOD,pygame.K_SLASH,pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_COLON,pygame.K_SEMICOLON,pygame.K_LESS,pygame.K_EQUALS,pygame.K_GREATER,pygame.K_QUESTION,pygame.K_AT,pygame.K_LEFTBRACKET,pygame.K_BACKSLASH,pygame.K_RIGHTBRACKET,pygame.K_CARET,pygame.K_UNDERSCORE,pygame.K_BACKQUOTE,pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_DELETE,pygame.K_KP0,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_KP_PERIOD,pygame.K_KP_DIVIDE,pygame.K_KP_MULTIPLY,pygame.K_KP_MINUS,pygame.K_KP_PLUS,pygame.K_KP_ENTER,pygame.K_KP_EQUALS,pygame.K_INSERT,pygame.K_HOME,pygame.K_END,pygame.K_PAGEUP,pygame.K_PAGEDOWN,pygame.K_F1,pygame.K_F2,pygame.K_F3,pygame.K_F4,pygame.K_F5,pygame.K_F6,pygame.K_F7,pygame.K_F8,pygame.K_F9,pygame.K_F10,pygame.K_F11,pygame.K_F12,pygame.K_F13,pygame.K_F14,pygame.K_NUMLOCK,pygame.K_CAPSLOCK,pygame.K_SCROLLOCK,pygame.K_RSHIFT,pygame.K_LSHIFT,pygame.K_RCTRL,pygame.K_LCTRL,pygame.K_RALT,pygame.K_LALT,pygame.K_RMETA,pygame.K_LMETA,pygame.K_LSUPER,pygame.K_RSUPER,pygame.K_MODE,pygame.K_HELP,pygame.K_PRINT,pygame.K_SYSREQ,pygame.K_BREAK,pygame.K_MENU,pygame.K_POWER,pygame.K_EURO]

        # BASE STATS
        self.base_energy = 100
        self.base_speed = 4.3
        self.base_throw_speed = 6
        self.base_animation_speed = 0.18
        self.stats = {'energy': self.base_energy, 'speed': self.base_speed, 'throw_speed': self.base_throw_speed, 'animation_speed': self.base_animation_speed}

        # CURRENT STATS
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.throw_speed = self.stats['throw_speed']
        self.animation_speed = self.stats['animation_speed']

        # ENERGY REGENERATION
        self.energy_max = 100
        self.regenerating_energy = False
        self.regeneration_time = None
        self.regeneration_cooldown = 1000
        self.regeneration_amount = 4
        self.speed_compensation = 1.2  # NORMALIZE DOWN AND RIGHT MOVEMENTS
        self.energy_drain = 10
        self.picked_up_water = False

        # GRASS
        self.in_grass = False
        self.grass_steps = 0
        self.minimum_encounter_steps = 5
        self.encounter_rate = 0.035

        # POKÉMON
        self.pokedex = getPokedex()
        self.dex_no = None
        self.pokemon = None
        self.pokemon_appeared = False
        self.pokemon_on_level = []
        self.zone_complete = False
        self.pokemon_toast = False
        self.zone_1 = ['9', '12', '15', '18', '20', '22', '26', '40', '42', '49', '51', '59', '68', '73', '128']  # Z1 = ['Caterpie', 'Weedle', 'Pidgey', 'Rattata', 'Spearow', 'Ekans', 'Sandshrew', 'Zubat', 'Oddish', 'Diglett', 'Meowth', 'Poliwag', 'Bellsprout', 'Geodude', 'Magikarp']
        self.zone_2 = ['24', '28', '31', '36', '45', '47', '53', '55', '57', '62', '71', '76', '78', '80', '83', '85', '87', '89', '91', '95', '97', '99', '103', '108', '115', '117', '119', '132']  # Z2 = ['Pikachu', 'Nidoran♀', 'Nidoran♂', 'Vulpix', 'Paras', 'Venonat', 'Psyduck', 'Mankey', 'Growlithe', 'Abra', 'Tentacool', 'Ponyta', 'Slowpoke', 'Magnemite', 'Doduo', 'Seel', 'Grimer', 'Shellder', 'Gastly', 'Drowzee', 'Krabby', 'Voltorb', 'Cubone', 'Koffing', 'Horsea', 'Goldeen', 'Staryu', 'Eevee']
        self.zone_3 = ['0', '3', '6', '10', '11', '13', '14', '16', '19', '21', '23', '25', '27', '29', '32', '34', '37', '38', '41', '43', '46', '48', '52', '54', '56', '60', '63', '65', '66', '69', '74', '79', '82', '86', '88', '92', '96', '101', '104', '110', '113', '116', '121', '122', '123', '124', '125', '126', '127', '133', '134', '135', '137', '139', '146']  # Z3 = ['Bulbasaur', 'Charmander', 'Squirtle', 'Metapod', 'Butterfree', 'Kakuna', 'Beedrill', 'Pidgeotto', 'Raticate', 'Fearow', 'Arbok', 'Raichu', 'Sandslash', 'Nidorina', 'Nidorino', 'Clefairy', 'Ninetales', 'Jigglypuff', 'Golbat', 'Gloom', 'Parasect', 'Venomoth', 'Persian', 'Golduck', 'Primeape', 'Poliwhirl', 'Kadabra', 'Machop', 'Machoke', 'Weepinbell', 'Graveler', 'Slowbro', "Farfetch'd", 'Dewgong', 'Muk', 'Haunter', 'Hypno', 'Exeggcute', 'Marowak', 'Rhyhorn', 'Tangela', 'Seadra','Mr.Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Vaporeon', 'Jolteon', 'Flareon', 'Omanyte', 'Kabuto', 'Dratini']
        self.zone_4 = ['1', '2', '4', '5', '7', '8', '17', '30', '33', '39', '44', '50', '61', '64', '67', '70', '72', '75', '77', '81', '84', '90', '93', '94', '98', '100', '102', '105', '106', '107', '109', '111', '118', '120', '129', '130', '138', '140']  # Z4 = ['Ivysaur', 'Venusaur', 'Charmeleon', 'Charizard', 'Wartortle', 'Blastoise', 'Pidgeot', 'Nidoqueen', 'Nidoking', 'Wigglytuff', 'Vileplume', 'Dugtrio', 'Poliwrath', 'Alakazam', 'Machamp', 'Victreebel', 'Tentacruel', 'Golem', 'Rapidash', 'Magneton', 'Dodrio', 'Cloyster', 'Gengar', 'Onix', 'Kingler', 'Electrode', 'Exeggutor', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 'Weezing', 'Rhydon', 'Seaking', 'Starmie', 'Gyarados', 'Lapras', 'Omastar', 'Kabutops']
        self.zone_5 = ['35', '58', '112', '114', '131', '136', '141', '142', '143', '144', '145', '147', '148', '149', '150']  # Z5 = ['Clefable', 'Arcanine', 'Chansey', 'Kangaskhan', 'Ditto', 'Porygon', 'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew']
        self.caught_pokemon = []
        self.finalize = False  # USED TO KEEP PACE FOR END OF GAME

        # BALL
        self.throw_animation = Animations(self.barrier_group, self.visible_group, self.grass_group, self.pokemon_group, self.overlay_group)
        self.ball_name = None
        self.ball_image = None
        self.ball = None
        self.picked_up_ball = False
        self.cost = 10
        self.throwing = False
        self.throw_time = None
        self.throw_cooldown = 700
        self.balls_thrown = 0
        self.throw_ball = throwBall
        self.hit_pokemon = False
        self.hit_name = False
        self.balls_hit = 0

    def actions(self):
        # PREVENT PLAYER FROM MOVING DIAGONAL
        if self.direction.magnitude() not in [-1, 1, 0, 0]:
            self.direction = pygame.math.Vector2()

        # PLAYER NOT THROWING
        if not self.throwing:
            # RESET THROW STATUS
            if 'throw' in self.status:
                self.status = self.status.replace('_throw', '')

            # ARROW KEY LOGIC
            keys = pygame.key.get_pressed()
            for arrow in self.player_lookup.keys():
                # UPDATE STATUS FROM ARROWS
                py_key = self.player_lookup[arrow]['key']
                if keys[py_key]:
                    if arrow not in self.keys:
                        self.keys.append(arrow)
                else:
                    if arrow in self.keys:
                        self.keys.remove(arrow)

                # ASSIGN STATUS BASED ON LAST ARROW KEY PRESS
                if self.keys and self.status != self.keys[-1]:
                    self.status = self.keys[-1]

                # ADJUST DIRECTION AND SPEED
                arrow_direction = self.player_lookup[arrow]['direction']
                speed_increase = self.player_lookup[arrow]['speed_increase']
                if self.status == arrow and self.direction != pygame.Vector2(arrow_direction[0], arrow_direction[1]):
                    self.direction = pygame.Vector2(arrow_direction[0], arrow_direction[1])
                    if speed_increase:
                        if not self.picked_up_shoes:
                            self.stats['speed'] = self.speed * self.speed_compensation

                    else:
                        if not self.picked_up_shoes:
                            self.stats['speed'] = self.speed

            # IDLE LOGIC
            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                self.keys = []
                self.direction.x = 0
                self.direction.y = 0
                if 'idle' not in self.status and 'throw' not in self.status:
                    self.status = self.status + '_idle'
                    if self.hitting_object:
                        self.hitting_object = False

            # THROW LOGIC, USER PRESSED ANY KEY
            for key in self.key_list:
                if keys[key]:
                    self.throwing = True
                    self.throw_time = pygame.time.get_ticks()
                    if self.energy - self.cost >= 0 and self.picked_up_ball:
                        self.ball_throw_sound.set_volume(0.2)
                        self.ball_throw_sound.play()
                        self.energy -= self.cost
                        self.throw_ball()
                        self.balls_thrown += 1

        # PLAYER IS THROWING
        else:
            self.direction = pygame.Vector2()
            if 'throw' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_throw')
                else:
                    self.status = self.status + '_throw'
            elif self.hitting_object:
                self.hitting_object = False

        # ENERGY REGENERATION
        if not self.regenerating_energy and not self.direction.magnitude():
            if self.energy + self.regeneration_amount <= self.energy_max:
                self.energy += self.regeneration_amount
            else:
                self.energy = self.energy_max
            self.regenerating_energy = True
            self.regeneration_time = pygame.time.get_ticks()

    def grass(self):
        # RESET GRASS STEPS BEFORE MEW, START HUNTING MUSIC
        if len(self.caught_pokemon) == 150 and not self.pre_mew_sound_started:
            self.grass_steps = 0
            pygame.mixer.stop()
            self.pre_mew_sound.set_volume(0.3)
            self.pre_mew_sound.play(100)
            self.pre_mew_sound_started = True

        # PLAYER IN GRASS, CHECK IF PLAYER STEPS OUT OF GRASS
        if self.in_grass and self.direction.magnitude() and not self.hitting_object:
            for visible in self.visible_group:
                if visible.hitbox.colliderect(self.hitbox):
                    self.in_grass = False
                    break

        # PLAYER OUT OF GRASS, CHECK IF PLAYER STEPS INTO GRASS
        if not self.in_grass:
            for grass_sprite in self.grass_group:
                if grass_sprite.hitbox.colliderect(self.hitbox):
                    self.in_grass = True

                    # IF PLAYER IS MOVING AND NOT HITTING BARRIERS
                    if self.direction.magnitude() and not self.hitting_object:
                        # COUNT STEPS IN GRASS
                        self.grass_steps += round(self.encounter_rate, 2)
                        self.grass_steps = round(self.grass_steps, 2)

                        # IF REACHED MINIMUM ENCOUNTER STEPS
                        if self.grass_steps > self.minimum_encounter_steps:
                            grass_toss = randint(0, 100)
                            if grass_toss == 1:  # IF WIN CHANCE TOSS
                                # CHECK ZONE, RANDOMLY PICK POKÉMON FROM ZONE LIST TO GET DEX NUMBER
                                zones = {1: self.zone_1, 2: self.zone_2, 3: self.zone_3, 4: self.zone_4, 5: self.zone_5}
                                zone_list = zones[grass_sprite.zone]
                                if len(zone_list) > 0:
                                    random_number = randint(0, len(zone_list) - 1)
                                    if zone_list[random_number] in ['149', '150']:  # IF PULLED MEWTWO OR MEW FROM ZONE5
                                        # CHECK IF DEX HAS BEEN COMPLETED
                                        if len(self.caught_pokemon) == 149:
                                            # PLAY MEWTWO SOUND
                                            self.dex_no = '149'  # SET MEWTWO
                                        elif len(self.caught_pokemon) == 150:
                                            # PLAY MEW SOUND
                                            self.dex_no = '150'
                                    else:
                                        self.dex_no = zone_list[random_number]

                                # POKÉMON SPAWN TOSS
                                if self.dex_no:
                                    pokemon = self.pokedex[str(self.dex_no)]
                                    self.dex_no = False
                                    if pokemon['pokemon_name'] not in self.caught_pokemon:
                                        # HAVEN'T ALREADY CAUGHT POKÉMON
                                        spawn_toss = randint(0, 254)
                                        if pokemon['catch_rate'] >= spawn_toss:
                                            # WON SPAWN TOSS, ASSIGN POKÉMON TO SPAWN IN LEVEL
                                            self.pokemon_appeared = pokemon
                                            self.grass_steps = 0
                                            break

    def update(self):
        self.cooldown()
        self.actions()
        self.move(self.stats['speed'])
        self.animate()
        self.grass()
