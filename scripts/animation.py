from scripts.interaction import *
from scripts.support import getImages


# USED TO ANIMATE GRASS AND BALLS
class Animations:
    def __init__(self, barrier_group, visible_group, grass_group, pokemon_group, overlay_group):
        # SPRITE GROUPS
        self.barrier_group = barrier_group
        self.visible_group = visible_group
        self.grass_group = grass_group
        self.pokemon_group = pokemon_group
        self.overlay_group = overlay_group

        # ANIMATION COOLDOWN
        self.animating = False
        self.animation_time = None
        self.animation_cooldown = 200

        # GRASS FRAMES
        self.grass_frames = {'grass': getImages('assets/images/sprites/map/vegetation/grass/rustle_animation')}

        # BALL FRAMES
        self.ball_frames = {'pokeball_left': getImages('assets/images/sprites/pickups/balls/pokeball/throw/left')
            , 'pokeball_right': getImages('assets/images/sprites/pickups/balls/pokeball/throw/right')
            , 'pokeball_up': getImages('assets/images/sprites/pickups/balls/pokeball/throw/up')
            , 'pokeball_down': getImages('assets/images/sprites/pickups/balls/pokeball/throw/down')
            , 'greatball_left': getImages('assets/images/sprites/pickups/balls/greatball/throw/left')
            , 'greatball_right': getImages('assets/images/sprites/pickups/balls/greatball/throw/right')
            , 'greatball_up': getImages('assets/images/sprites/pickups/balls/greatball/throw/up')
            , 'greatball_down': getImages('assets/images/sprites/pickups/balls/greatball/throw/down')
            , 'ultraball_left': getImages('assets/images/sprites/pickups/balls/ultraball/throw/left')
            , 'ultraball_right': getImages('assets/images/sprites/pickups/balls/ultraball/throw/right')
            , 'ultraball_up': getImages('assets/images/sprites/pickups/balls/ultraball/throw/up')
            , 'ultraball_down': getImages('assets/images/sprites/pickups/balls/ultraball/throw/down')}

        self.ball_close = {'pokeball': getImages('assets/images/sprites/pickups/balls/pokeball/animations/close')
            , 'greatball': getImages('assets/images/sprites/pickups/balls/greatball/animations/close')
            , 'ultraball': getImages('assets/images/sprites/pickups/balls/ultraball/animations/close')}

        self.ball_open = {'pokeball': getImages('assets/images/sprites/pickups/balls/pokeball/animations/open')
            , 'greatball': getImages('assets/images/sprites/pickups/balls/greatball/animations/open')
            , 'ultraball': getImages('assets/images/sprites/pickups/balls/ultraball/animations/open')}

        self.ball_wobble = {'pokeball': getImages('assets/images/sprites/pickups/balls/pokeball/animations/wobble')
            , 'greatball': getImages('assets/images/sprites/pickups/balls/greatball/animations/wobble')
            , 'ultraball': getImages('assets/images/sprites/pickups/balls/ultraball/animations/wobble')}

    # ANIMATIONS
    def updateGrassAnimation(self, pos, groups):
        GrassParticle(pos, groups, self.grass_frames['grass'])

    def updateThrowAnimation(self, player, groups, animation_type):
        BallParticle(player, groups, self.ball_frames[animation_type], self.barrier_group, self.visible_group, self.grass_group, self.pokemon_group, self.overlay_group, self.ball_close, self.ball_wobble, self.ball_open)
