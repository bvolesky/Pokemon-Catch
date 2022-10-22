from scripts.support import *
from scripts.object import Object
from scripts.entity import Entity


# WALLS THAT THE ENTITIES CANNOT PASS
class Barrier(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.rect = pygame.rect.Rect(pos[0], pos[1], 64, 64)
        self.hitbox = self.rect.inflate(0, -10)


# OBJECT THAT ALLOWS POKÉMON TO SPAWN
class Grass(Object):
    def __init__(self, pos, groups, image, inflation, zone):
        super().__init__(pos, groups, image, inflation)
        self.zone = zone


# GRASS RUSTLING ANIMATION OBJECT
class GrassParticle(pygame.sprite.Sprite):
    def __init__(self, pos, groups, animation_frames):
        super().__init__(groups)
        # BOUNDARIES
        self.sprite_type = 'grass'
        self.image = animation_frames[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate((0, 0))

        # ANIMATION
        self.frame_index = 0
        self.frames = animation_frames
        self.backup_frames = animation_frames
        self.animation_speed = 0.1
        self.triggered = False

    def update(self):
        self.animate()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            # END OF FRAMES
            self.kill()
            self.animation_speed = 0.1
            self.frames = self.backup_frames

        else:
            # LOAD NEXT FRAME
            self.image = self.frames[int(self.frame_index)]


# ITEM THAT CAN BE PICKED UP TO CAPTURE POKÉMON
class Ball(Object):
    def __init__(self, pos, groups, image, inflation, ball_name):
        super().__init__(pos, groups, image, inflation)
        self.name = ball_name
        self.ball_lookup = {'pokeball': {'rate': 1, 'throw_speed': 7}, 'greatball': {'rate': 2, 'throw_speed': 9}, 'ultraball': {'rate': 4, 'throw_speed': 12}}
        self.rate = self.ball_lookup[self.name]['rate']
        self.throw_speed = self.ball_lookup[self.name]['throw_speed']


# THROWABLE OBJECT THAT CAN CAPTURE POKÉMON
class BallParticle(Entity):
    def __init__(self, player, groups, animation_frames, barrier_group, visible_group, grass_group, pokemon_group, overlay_group, ball_close, ball_wobble, ball_open):
        super().__init__(groups, barrier_group, visible_group, grass_group)

        # SPRITES
        self.barrier_group = barrier_group
        self.visible_group = visible_group
        self.grass_group = grass_group
        self.pokemon_sprites = pokemon_group
        self.overlay_sprites = overlay_group
        self.sprite_type = 'ball'
        self.backup_sprite = None
        self.player = player

        # BOUNDARIES
        self.pos = (player.rect.centerx - 32, player.rect.centery - 32)
        self.image = animation_frames[0]
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate((-30, -30))
        self.hitting_object = False
        self.barrier_direction = (0, 0)

        # ANIMATION
        self.frame_index = 0
        self.animation_speed = 0.1
        self.frames = animation_frames
        self.backup_frames = animation_frames
        self.ball_open = ball_open
        self.ball_close = ball_close
        self.ball_wobble = ball_wobble

        # MOVEMENT
        self.direction = getDirection(self.player.status)
        self.ball_speed = player.stats['throw_speed']

        # COOLDOWN
        self.hit_time = None
        self.hit_cooldown = 3000

        # BOOL FLAGS
        self.pokemon_broke_out = False
        self.ball_opened = False
        self.close_animation_complete = False
        self.hit_pokemon = player.hit_pokemon

        # LAYERS
        self.pushLayerToBottom(self.player)

        # AUDIO
        self.ball_open_sound = getSounds('ball_open')
        self.ball_wobble_sound = getSounds('ball_wobble')
        self.ball_wobble_sound_playing = False
        self.jigglypuff_singing_started = False
        self.pokeflute_sound_started = False

    def pushLayerToBottom(self, player):
        pushLayerToTop(player, self.visible_group)
        for pokemon in self.pokemon_sprites:
            pushLayerToTop(pokemon, self.visible_group)
        for i in self.overlay_sprites:
            pushLayerToTop(i, self.visible_group)

    def update(self):
        if not self.hit_pokemon and not self.pokemon_broke_out:
            if self.direction.magnitude():
                self.direction = self.direction.normalize()
            self.move(self.ball_speed)
        self.animate()
        self.cooldown()
