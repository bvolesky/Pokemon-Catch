import pygame
import time
import sys
from scripts.level import Level
from scripts.support import getSounds


# ORIGIN THAT SETS UP APPLICATION AND RUNS PLAYABLE GAME
class Game:
    def __init__(self):
        pygame.mixer.quit()  # BYPASSES PYGAME MIXER BUG
        pygame.mixer.init(44100, -16, 1, 512)
        pygame.init()

        # TIME
        self.clock = pygame.time.Clock()
        self.game_paused = False
        self.ticks = 0
        self.time_passed = 0
        self.seconds_passed = 0

        # APPLICATION WINDOW
        self.caption = "Pokémon Catch!"
        self.app_icon = pygame.image.load('assets/images/screens/launch/icon.ico')
        pygame.display.set_icon(self.app_icon)
        self.screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)
        pygame.display.set_caption(self.caption)

        # LOADING SCREEN
        self.loading_background = pygame.image.load('assets/images/screens/loading/loading.png')
        self.addToScreen(self.loading_background)

        # SOUND
        self.title_sound = getSounds('title')
        self.kangaskhan = getSounds('115')
        self.a_sound = getSounds('a')
        self.countdown_number_sound = getSounds('countdown_number')
        self.go_sound = getSounds('go')

        # TUTORIAL
        self.tutorial_background = pygame.image.load('assets/images/screens/tutorial/background.png')
        self.tutorial_pokedex = pygame.image.load('assets/images/screens/tutorial/pokedex.png')
        self.countdown_ready = pygame.image.load('assets/images/screens/tutorial/countdown/ready.png')
        self.countdown_3 = pygame.image.load('assets/images/screens/tutorial/countdown/3.png')
        self.countdown_2 = pygame.image.load('assets/images/screens/tutorial/countdown/2.png')
        self.countdown_1 = pygame.image.load('assets/images/screens/tutorial/countdown/1.png')
        self.countdown_go = pygame.image.load('assets/images/screens/tutorial/countdown/go.png')

        # CREATE LEVEL
        self.max_frames = 1 / 60
        self.frames_remaining = 0
        self.lap_1 = time.perf_counter()
        self.pause_background = pygame.image.load('assets/images/screens/pause/pause.png')
        self.level = Level()  # This instantiation also creates the map and loads images - this is what takes time during the loading screen.

    def run(self, restarting_game=False):
        # PLAY SOUND
        self.title_sound.set_volume(0.30)
        self.title_sound.play(100, 0, 3000)

        # SET UP APPLICATION WINDOW
        self.screen = pygame.display.set_mode((800, 600))  # Add frame to app window

        # TUTORIAL SCREEN
        if not restarting_game:
            self.screen.blit(self.tutorial_background, (0, 0))
            self.screen.blit(self.tutorial_pokedex, (0, 12))
            pygame.display.update()

            # WAIT FOR USER INPUT
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.mixer.quit()
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                # USER PRESSED KEY
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_BACKSPACE,pygame.K_TAB,pygame.K_CLEAR,pygame.K_PAUSE,pygame.K_ESCAPE,pygame.K_SPACE,pygame.K_EXCLAIM,pygame.K_QUOTEDBL,pygame.K_HASH,pygame.K_DOLLAR,pygame.K_AMPERSAND,pygame.K_QUOTE,pygame.K_LEFTPAREN,pygame.K_RIGHTPAREN,pygame.K_ASTERISK,pygame.K_PLUS,pygame.K_COMMA,pygame.K_MINUS,pygame.K_PERIOD,pygame.K_SLASH,pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_COLON,pygame.K_SEMICOLON,pygame.K_LESS,pygame.K_EQUALS,pygame.K_GREATER,pygame.K_QUESTION,pygame.K_AT,pygame.K_LEFTBRACKET,pygame.K_BACKSLASH,pygame.K_RIGHTBRACKET,pygame.K_CARET,pygame.K_UNDERSCORE,pygame.K_BACKQUOTE,pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_DELETE,pygame.K_KP0,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9,pygame.K_KP_PERIOD,pygame.K_KP_DIVIDE,pygame.K_KP_MULTIPLY,pygame.K_KP_MINUS,pygame.K_KP_PLUS,pygame.K_KP_ENTER,pygame.K_KP_EQUALS,pygame.K_INSERT,pygame.K_HOME,pygame.K_END,pygame.K_PAGEUP,pygame.K_PAGEDOWN,pygame.K_NUMLOCK,pygame.K_CAPSLOCK,pygame.K_SCROLLOCK,pygame.K_RSHIFT,pygame.K_LSHIFT,pygame.K_RCTRL,pygame.K_LCTRL,pygame.K_RALT,pygame.K_LALT]:  # This bypasses a bug where pygame would press F15 for you randomly (fun, right?)
                        # START COUNTDOWN
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            pygame.mixer.quit()
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit()

                        # TITLE FINISHED
                        self.title_sound.set_volume(0.1)
                        self.kangaskhan.set_volume(0.75)
                        self.kangaskhan.play()
                        pygame.time.wait(2000)

                        # START COUNTDOWN
                        self.countdown_number_sound.set_volume(0.2)
                        for i in [self.countdown_ready, self.countdown_3, self.countdown_2, self.countdown_1]:
                            if i != self.countdown_ready:
                                self.countdown_number_sound.play()
                            self.addToScreen(i, 1)
                        break

        # GO SCREEN
        self.title_sound.stop()
        self.go_sound.set_volume(0.25)
        self.go_sound.play()
        self.addToScreen(self.countdown_go, 1)

        # MAIN LOOP
        while True:
            # MANAGE FRAME RATE
            can_render = False
            lap_2 = time.perf_counter()
            frames_passed = lap_2 - self.lap_1
            self.frames_remaining += frames_passed
            self.lap_1 = lap_2
            while self.frames_remaining >= self.max_frames:
                self.frames_remaining -= self.max_frames
                can_render = True

            # RENDER GAME
            if can_render:
                # CHECK FOR USER INPUT
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.mixer.quit()
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        # BUTTON PRESS SOUND
                        self.a_sound.set_volume(0.15)
                        self.a_sound.play()

                        # USER PAUSED GAME
                        if not self.game_paused:
                            self.game_paused = True
                            self.time_passed = 0
                            self.ticks = pygame.time.get_ticks()
                            self.addToScreen(self.pause_background)

                        # USER UNPAUSED GAME
                        else:
                            self.game_paused = False
                            self.time_passed = (pygame.time.get_ticks() - self.ticks) / 1000
                            self.seconds_passed += self.time_passed

                # RUN LEVEL
                if not self.game_paused:
                    self.level.run(self.seconds_passed)
                    pygame.display.update()

    def addToScreen(self, image, seconds_to_wait=0, position=(0, 0)):
        self.screen.blit(image, position)
        pygame.display.update()
        if seconds_to_wait != 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.quit()
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
            pygame.time.wait(seconds_to_wait * 1000)  # CONVERT SECONDS TO MILLISECONDS


if __name__ == '__main__':
    game = Game()
    game.run()
