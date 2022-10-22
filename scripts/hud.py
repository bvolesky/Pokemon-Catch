# -*- coding: utf-8 -*-
import sys
import datetime
from scripts.support import *


# HEADS UP DISPLAY THAT LIES ON TOP OF PLAYING SCREEN
class HUD:
    def __init__(self):

        # SCREEN
        self.display_surface = pygame.display.get_surface()

        # FONTS
        self.poke_font = 'assets/font/pokefont.ttf'
        self.font = pygame.font.Font(self.poke_font, 30)
        self.energy_font = pygame.font.Font(self.poke_font, 25)

        # COLORS
        self.colors = {'raisin_black': '#222222'
            , 'bright_gray': '#EEEEEE'
            , 'light_cobalt_blue': '#84A5dE'
            , 'cyber_yellow': '#FED000'
            , 'axolotl_green': '#637B5B'
            , 'amazon_green': '#387845'
            , 'emerald_green': '#5FCC74'}

        # GRAPHICS
        self.pickups = {'pokeball': 'assets/images/sprites/pickups/balls/pokeball/pokeball.png'
            , 'greatball': 'assets/images/sprites/pickups/balls/greatball/greatball.png'
            , 'ultraball': 'assets/images/sprites/pickups/balls/ultraball/ultraball.png'
            , 'shoes': 'assets/images/sprites/pickups/shoes/shoes_ui.png'
            , 'fresh_water': 'assets/images/sprites/pickups/water/water.png'}
        self.pickup_graphics = loadPickupGraphics(self.pickups)

        # SOUNDS
        self.safari_pa_sound = getSounds('safari_pa')
        self.pokedex_rating_sound = getSounds('pokedex_rating')
        self.results_sound = getSounds('results')
        self.fanfare_sound = getSounds('fanfare')
        self.confetti_sound = getSounds('confetti')
        self.epilogue_sound = getSounds('epilogue')
        self.countdown_sound = getSounds('countdown_number')
        self.go_sound = getSounds('go')
        self.legend_list = ['articuno', 'zapdos', 'moltres']

        # ENERGY BAR
        self.energy_bar = pygame.Rect(10, 20, 250, 20)

        # POKÉMON TOAST
        self.pokemon_toast_duration = 1
        self.pokemon_toast_y_pos = 620
        self.pokemon_toast_new_time = None
        self.pokemon_toast_triggered = False
        self.pokemon_toast_appeared = False
        self.pokemon_capture_changed = False

        # ZONE TOAST
        self.zone_toast_duration = 2
        self.zone_toast_triggered = False
        self.zone_toast_new_time = None
        self.zone_toast_appeared = False
        self.zone_toast_y_pos = -20

        # TIME REMAINING
        self.minutes_to_end = 35
        self.seconds = 0
        self.countdown_seconds = 10
        self.time_remaining = None
        self.start_ticks = None
        self.origin_tick_started = False

        # RESULTS
        self.border = pygame.image.load('assets/images/screens/results/results.png').convert_alpha()
        self.confetti = pygame.image.load('assets/images/screens/results/confetti.png')
        self.zone_result_duration = 8

    def updateEnergyBar(self, current, max_amount, energy_bar_rect, color):
        # CONVERT PIXELS
        ratio = current / max_amount
        current_width = energy_bar_rect.width * ratio
        current_rect = energy_bar_rect.copy()
        current_rect.width = current_width

        # DRAW ENERGY BAR
        pygame.draw.rect(self.display_surface, self.colors['raisin_black'], energy_bar_rect)  # BACKGROUND
        pygame.draw.rect(self.display_surface, self.colors['amazon_green'], energy_bar_rect, 3)  # ENERGY LEVEL
        pygame.draw.rect(self.display_surface, color, current_rect)  # ENERGY MODE
        energy_text = self.energy_font.render('E          N          E          R          G          Y', False, "dark green")
        energy_rect = energy_text.get_rect(topleft=(25, 18))
        self.display_surface.blit(energy_text, energy_rect)
        pygame.draw.rect(self.display_surface, 'black', energy_bar_rect, 2)  # ENERGY OUTLINE

    def updateCapturedCount(self, num):
        # CAUGHT COUNT
        captured_text = self.font.render(' CAPTURED: {} '.format(str(int(num))), False, self.colors['bright_gray'])
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        captured_rect = captured_text.get_rect(bottomright=(x, y))
        pygame.draw.rect(self.display_surface, self.colors['raisin_black'], captured_rect.inflate(10, 10))  # Exp level
        self.display_surface.blit(captured_text, captured_rect)

    def updateTimeRemaining(self):
        # TIME TEXT
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        pygame.draw.rect(self.display_surface, "black", self.font.render('00:00', False, 'black').get_rect(bottomright=(x, y)).inflate(10, 10), 3)

        # TIME REMAINING
        if self.time_remaining > 600:
            time_left = ':'.join(str(datetime.timedelta(seconds=self.time_remaining)).split(':'))[2:][:5]
            time_remaining_text = self.font.render(' TIME REMAINING: {} '.format(time_left), False, self.colors['bright_gray'])
            time_rect_text = self.font.render(' TIME REMAINING: 99:99 ', False, 'black')
        elif 600 > self.time_remaining >= 60:
            time_left = ':'.join(str(datetime.timedelta(seconds=self.time_remaining)).split(':'))[3:][:4]
            time_remaining_text = self.font.render(' TIME REMAINING: {} '.format(time_left), False, self.colors['bright_gray'])
            time_rect_text = self.font.render(' TIME REMAINING: 9:99 ', False, 'black')
        else:
            time_left = ':'.join(str(datetime.timedelta(seconds=self.time_remaining)).split(':'))[5:][:5]
            time_remaining_text = self.font.render(' TIME REMAINING: {} '.format(time_left), False, 'red')
            time_rect_text = self.font.render(' TIME REMAINING: 99:99 ', False, 'black')

        time_remaining_rect = time_rect_text.get_rect(topright=(x, 20))
        pygame.draw.rect(self.display_surface, self.colors['raisin_black'], time_remaining_rect.inflate(10, 10))  # Exp level
        self.display_surface.blit(time_remaining_text, time_remaining_rect)
        pygame.draw.rect(self.display_surface, "black", time_remaining_rect.inflate(10, 10), 3)  # TIME REMAINING BORDER
        if (10 > self.time_remaining > 0) and self.countdown_seconds != int(self.time_remaining):
            self.countdown_seconds = int(self.time_remaining)
            pygame.mixer.stop()
            time_remaining_text = self.font.render(' TIME REMAINING: 00:00 '.format(time_left), False, 'red')
            self.display_surface.blit(time_remaining_text, time_remaining_rect)
            pygame.draw.rect(self.display_surface, "black", time_remaining_rect.inflate(10, 10), 3)  # TIME REMAINING BORDER
            self.countdown_sound.set_volume(0.2)
            self.countdown_sound.play()

    def updateItemBox(self, player):
        # ADD BALL TO BOX
        if player.picked_up_ball:
            box_rect = self.drawItemBox(10, 505, player)
            pickup_surface = self.pickup_graphics[player.ball_name]
            ball_box_rect = pickup_surface.get_rect(center=box_rect.center)
            self.display_surface.blit(pickup_surface, ball_box_rect)

        # ADD SHOES TO BOX
        if player.picked_up_shoes:
            box_rect = self.drawItemBox(75, 510, player)
            pickup_surface = self.pickup_graphics["shoes"]
            shoes_box_rect = pickup_surface.get_rect(center=box_rect.center)
            self.display_surface.blit(pickup_surface, shoes_box_rect)

    def updateFleeBox(self, player):
        # FLEEING BOX
        if player.pokemon_on_level:
            flee_surf = pygame.Surface((100, 280))
            flee_surf.set_alpha(128)
            flee_surf.fill('black')
            self.display_surface.blit(flee_surf, (10, 80))
            fleeing_text = self.energy_font.render('FLEEING:', False, self.colors['bright_gray'])
            self.display_surface.blit(fleeing_text, (15, 85))
            for index, name in enumerate(player.pokemon_on_level):
                if name == 'Nidoran♀':
                    name = 'Nidoran [f]'
                elif name == 'Nidoran♂':
                    name = 'Nidoran [m]'
                pokemon_text = self.energy_font.render('{}'.format(name), False, self.colors['bright_gray'])
                self.display_surface.blit(pokemon_text, (15, 110 + (index * 25)))

    def drawItemBox(self, left, top, player):
        # PRESS ANY NOTIFICATION
        if player.picked_up_ball and player.balls_thrown == 0:
            a_notification_text = self.energy_font.render(' PRESS ', False, "white")
            a_rect = a_notification_text.get_rect(bottomleft=(23, 500))
            pygame.draw.rect(self.display_surface, self.colors['raisin_black'], a_rect.inflate(0, 5))
            self.display_surface.blit(a_notification_text, a_rect)

        # DRAW BOX
        box_rect = pygame.Rect(left, top, 80, 80)
        pygame.draw.rect(self.display_surface, self.colors['raisin_black'], box_rect)
        pygame.draw.rect(self.display_surface, "black", box_rect, 3)
        return box_rect

    def updateZoneToast(self, zone, time_remaining, player):

        # START ZONE TOAST, GET NEW TIME
        if not self.zone_toast_triggered:
            self.zone_toast_triggered = True
            self.zone_toast_new_time = time_remaining - 4  # SET ZONE TOAST DURATION

        # ZONE TOAST STARTED
        if self.zone_toast_triggered:
            if time_remaining >= self.zone_toast_new_time:

                # POP IN
                if self.zone_toast_y_pos + 1 <= 20 and not self.zone_toast_appeared:
                    self.zone_toast_y_pos += 1

                else:  # REACHED APEX, WAIT DURATION
                    if (time_remaining - self.zone_toast_new_time) >= self.zone_toast_duration:
                        self.zone_toast_appeared = True
                        self.zone_toast_y_pos = 20
                    else:
                        # DURATION HAS PASSED, SO RETRACT TOAST BOX
                        if self.zone_toast_y_pos >= -40:
                            self.zone_toast_y_pos -= 1

                # DRAW ZONE TOAST BOX WITH UPDATED COORDINATES
                zone_toast_text = self.font.render(' ZONE {} CLEAR ! '.format(str(int(zone))), False, self.colors['bright_gray'])
                zone_toast_rect = zone_toast_text.get_rect(midtop=(self.display_surface.get_size()[0] / 2, self.zone_toast_y_pos))  # CREATE TEXT
                pygame.draw.rect(self.display_surface, self.colors['raisin_black'], zone_toast_rect.inflate(10, 10))  # CREATE BACKGROUND
                self.display_surface.blit(zone_toast_text, zone_toast_rect)  # ADD TO SCREEN
            else:
                # ZONE ANIMATION FINISHED, RESET VARIABLES
                self.zone_toast_y_pos = -20
                self.zone_toast_appeared = False
                self.zone_toast_triggered = False
                self.zone_toast_new_time = None
                player.zone_complete = False

    def pokemonToast(self, player, time_remaining):

        # START POKÉMON TOAST, GET NEW TIME
        if player.hit_name and not self.pokemon_toast_triggered or self.pokemon_capture_changed != player.hit_name:
            self.pokemon_capture_changed = player.hit_name
            self.pokemon_toast_appeared = False
            self.pokemon_toast_triggered = True
            self.pokemon_toast_new_time = time_remaining - 2

        # START RUNAWAY TOAST
        elif 'runaway' in player.pokemon_toast and not self.pokemon_toast_triggered:
            self.pokemon_toast_appeared = False
            self.pokemon_toast_triggered = True
            self.pokemon_toast_new_time = time_remaining - 2

        # POKÉMON TOAST STARTED
        if self.pokemon_toast_triggered:
            if time_remaining >= self.pokemon_toast_new_time:
                # POP IN
                if self.pokemon_toast_y_pos - 1 >= 550 and not self.pokemon_toast_appeared:
                    self.pokemon_toast_y_pos -= 5

                else:  # REACHED APEX, WAIT DURATION
                    if (time_remaining - self.pokemon_toast_new_time) >= self.pokemon_toast_duration:
                        self.pokemon_toast_appeared = True
                        self.pokemon_toast_y_pos = 550
                    else:
                        # DURATION HAS PASSED, SO RETRACT POKÉMON TOAST BOX
                        if self.pokemon_toast_y_pos <= self.display_surface.get_size()[1] + 20:
                            self.pokemon_toast_y_pos += 5

                # SET TEXT, DRAW POKÉMON TOAST BOX
                if player.pokemon_toast and player.hit_name:
                    if player.hit_name == 'Nidoran♀':
                        player.hit_name = 'Nidoran [f]'
                    elif player.hit_name == 'Nidoran♂':
                        player.hit_name = 'Nidoran [m]'

                    # SET TOAST TEXT BASED ON WIN OR LOSS TOAST
                    if player.pokemon_toast == 'capture':
                        self.pokemon_text = self.font.render(' Captured {} ! '.format(player.hit_name), False, 'green')
                    elif player.pokemon_toast == 'fail':
                        self.pokemon_text = self.font.render(' {} broke out ! '.format(player.hit_name), False, 'red')

                # SET TOAST TEXT FOR RUNAWAY
                elif player.pokemon_toast and 'runaway' in player.pokemon_toast:
                    name = str(player.pokemon_toast).split('_')[-1]
                    if name == 'Nidoran♀':
                        name = 'Nidoran [f]'
                    elif name == 'Nidoran♂':
                        name = 'Nidoran [m]'
                    self.pokemon_text = self.font.render(' {} got away ! '.format(name), False, 'yellow')

                # ADD TO SCREEN
                pokemon_toast_rect = self.pokemon_text.get_rect(midtop=(self.display_surface.get_size()[0] / 2, self.pokemon_toast_y_pos))  # CREATE TEXT AT X AND Y
                pygame.draw.rect(self.display_surface, self.colors['raisin_black'], pokemon_toast_rect.inflate(10, 10))  # CREATE BACKGROUND
                self.display_surface.blit(self.pokemon_text, pokemon_toast_rect)  # ADD TO SCREEN

            else:
                # POKÉMON TOAST ANIMATION FINISHED, RESET VARIABLES
                self.pokemon_toast_y_pos = 620
                self.pokemon_toast_appeared = False
                self.pokemon_toast_triggered = False
                self.pokemon_toast_new_time = None
                player.pokemon_toast = False
                player.hit_name = False

                # SET GAME TO END
                if len(player.caught_pokemon) == 151:
                    player.finalize = True

    def playZoneLoadingBar(self, zone, player):
        # SET VARIABLES
        length = 0
        player_zone = 0
        pos = None

        # SET VARIABLES
        if zone == 1:
            length = 15
            player_zone = player.zone_1
            pos = (192, 223)

        elif zone == 2:
            length = 28
            player_zone = player.zone_2
            pos = (345, 223)

        elif zone == 3:
            length = 55
            player_zone = player.zone_3
            pos = (496, 223)

        elif zone == 4:
            length = 38
            player_zone = player.zone_4
            pos = (259, 335)

        elif zone == 5:
            length = 15
            player_zone = player.zone_5
            pos = (424, 335)

        # CALCULATE BAR DATA
        amount_captured = length - len(player_zone)
        if amount_captured > 0:
            if len(player.caught_pokemon) != 151:
                for i in range(1, amount_captured + 1):
                    if amount_captured != 151:
                        pygame.time.wait(self.zone_result_duration)  # SKIP ANIMATION FOR WIN
                    self.drawZoneResultBar(pos, (109, 10), i / length)
                    pygame.display.update()

                # NORMALIZE ANIMATION TIMES ACROSS ALL ZONES
                leftover = 60 - length
                for i in range(leftover):
                    pygame.time.wait(self.zone_result_duration)

            else:
                # ANIMATE ZONE
                self.drawZoneResultBar(pos, (109, 10), amount_captured / length)
                pygame.display.update()
        else:
            # NO POKÉMON CAPTURED
            pygame.draw.rect(self.display_surface, self.colors['axolotl_green'], (pos, (109, 10)), 4)  # BORDER

    def drawZoneResultBar(self, pos, size, progress):
        # USED TO ANIMATE RESULTS SCREEN ZONE BARS
        pygame.draw.rect(self.display_surface, self.colors['axolotl_green'], (*pos, *size), 4)  # BORDER
        pygame.draw.rect(self.display_surface, self.colors['light_cobalt_blue'], (*(pos[0] + 4, pos[1] + 4), *((size[0] - 8) * progress, size[1] - 8)))  # BAR

    def run(self, player, waters_picked_up, seconds_paused, zone_complete):
        # TIME REMAINING
        if not self.origin_tick_started:
            self.start_ticks = pygame.time.get_ticks()
            self.origin_tick_started = True
        self.seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.time_remaining = (60 * self.minutes_to_end - self.seconds) + seconds_paused
        self.updateTimeRemaining()

        # ZONE TOAST
        if player.zone_complete:
            # FILL UP PLAYER ENERGY
            player.energy = player.energy_max
            self.updateEnergyBar(player.energy, player.energy_max, self.energy_bar, self.colors['emerald_green'])
            self.updateZoneToast(zone_complete, self.time_remaining, player)

        # POKÉMON TOAST
        if player.pokemon_toast:
            self.pokemonToast(player, self.time_remaining)

        # CAPTURED COUNT
        self.updateCapturedCount(len(player.caught_pokemon))

        # ENERGY BAR OUTLINE
        if waters_picked_up == 1:
            self.updateEnergyBar(player.energy_max, player.energy_max, self.energy_bar.inflate(10, 10), "yellow")
        if waters_picked_up == 2:
            self.updateEnergyBar(player.energy_max, player.energy_max, self.energy_bar.inflate(12, 12), "orange")
        if waters_picked_up == 3:
            self.updateEnergyBar(player.energy_max, player.energy_max, self.energy_bar.inflate(15, 15), "purple")

        # ENERGY BAR COLOR
        if player.energy >= 60:
            color = self.colors['emerald_green']
        elif 60 > player.energy >= 20:
            color = self.colors['cyber_yellow']
        else:
            color = 'red'

        # UPDATE ENERGY BAR
        self.updateEnergyBar(player.energy, player.energy_max, self.energy_bar, color)

        # ITEM BOX
        self.updateItemBox(player)

        # FLEE BOX
        self.updateFleeBox(player)

        # END OF GAME, RESULTS SCREEN
        if self.time_remaining <= 0 or player.finalize:
            self.safari_pa_sound.set_volume(0.1)
            self.safari_pa_sound.play()
            pygame.time.wait(3000)
            pygame.mixer.stop()

            # ADD BACKGROUND
            self.display_surface.fill('white')
            self.display_surface.blit(self.border, (0, 0))
            x = self.display_surface.get_size()[0] / 2
            y = self.display_surface.get_size()[1] / 2

            # RESULTS TITLE
            font_80 = pygame.font.Font(self.poke_font, 80)
            if len(player.caught_pokemon) == 151:
                results_text = font_80.render('CONGRATULATIONS', False, 'white', )
                self.display_surface.blit(self.confetti, (0, 0))
            else:
                results_text = font_80.render('RESULTS', False, 'white', )
            results_rect = results_text.get_rect(midtop=(self.display_surface.get_size()[0] / 2, 75))
            self.display_surface.blit(results_text, results_rect)

            # POKÉMON CAPTURED
            pokemon_captured_text = self.font.render('{}  out  of  151 ! '.format(str(len(player.caught_pokemon))), False, 'white')
            captured_rect = pokemon_captured_text.get_rect(center=(x + 135, y + 79))
            self.display_surface.blit(pokemon_captured_text, captured_rect)

            # THROW ACCURACY
            if int(player.balls_thrown) != 0:
                throw_text = self.font.render('{}%'.format(int(player.balls_hit / player.balls_thrown * 100)), False, 'white')
            else:
                throw_text = self.font.render('0%', False, 'white')
            throw_rect = throw_text.get_rect(center=(x + 140, y + 115))
            self.display_surface.blit(throw_text, throw_rect)

            # TIME REMAINING
            time_remaining = self.time_remaining
            if self.time_remaining <= 0:
                time_left = '00:00'
            else:
                time_left = str(datetime.timedelta(seconds=time_remaining)).split('.')[0][-4:]
            time_remaining_text = self.font.render('{}'.format(time_left), False, 'white')
            time_rect = time_remaining_text.get_rect(center=(x + 136, y + 151))
            self.display_surface.blit(time_remaining_text, time_rect)

            # ZONE PROGRESS BARS
            self.playZoneLoadingBar(1, player)
            self.playZoneLoadingBar(2, player)
            self.playZoneLoadingBar(3, player)
            self.playZoneLoadingBar(4, player)
            self.playZoneLoadingBar(5, player)

            # OAKS RATING
            font_25 = pygame.font.Font(self.poke_font, 25)
            amount = len(player.caught_pokemon)
            if amount < 10:
                oak_quote = '"You still have lots to do. Look for Pokémon in grass!"'
            elif 10 <= amount < 20:
                oak_quote = '"You\'re on the right track. Explore more areas!"'
            elif 20 <= amount < 30:
                oak_quote = '"You still need more Pokémon. Don\'t let them flee!"'
            elif 30 <= amount < 40:
                oak_quote = '"Good, you\'re trying hard. Throw quick and accurate!"'
            elif 40 <= amount < 50:
                oak_quote = '"Looking good. Keep up the work and hone your skills!"'
            elif 50 <= amount < 60:
                oak_quote = '"You finally got a least 50 species. That\'s a great!"'
            elif 60 <= amount < 70:
                oak_quote = '"Oh! This is getting even better. You\'re coming along!"'
            elif 70 <= amount < 80:
                oak_quote = '"Very good. You\'re understanding how to capture Pokémon!"'
            elif 80 <= amount < 90:
                oak_quote = '"Wonderful! Do you like to collect things? It appears so!"'
            elif 90 <= amount < 100:
                oak_quote = '"I\'m impressed! That must have been difficult to do!"'
            elif 100 <= amount < 110:
                oak_quote = '"100 Pokémon!? I can\'t believe how good you are!"'
            elif 110 <= amount < 120:
                oak_quote = '"You even have the evolved forms of Pokémon! Super!"'
            elif 120 <= amount < 130:
                oak_quote = '"Excellent! There are stronger Pokémon out there!'
            elif 130 <= amount < 140:
                oak_quote = '"Outstanding! You\'ve become a real pro at this!"'
            elif 140 <= amount < 150:
                oak_quote = '"I have nothing left to say! You\'re the authority now!"'
            elif len(player.caught_pokemon) == 150:
                oak_quote = '"The legends are true...go and complete your destiny!"'
            elif len(player.caught_pokemon) == 151:
                oak_quote = '"I\'m so proud...your Pokédex is entirely complete!"'
            else:
                oak_quote = '"Go catch \'em all!"'
            oak_text = font_25.render('OAK: {}'.format(oak_quote), False, 'white')
            oak_rect = oak_text.get_rect(center=(x, y + 190))
            self.display_surface.blit(oak_text, oak_rect)

            # UPDATE SCREEN
            pygame.display.update()

            # TIME RAN OUT
            if len(player.caught_pokemon) != 151:
                self.pokedex_rating_sound.set_volume(0.15)
                self.pokedex_rating_sound.play()
                pygame.time.wait(2000)
                self.results_sound.set_volume(0.15)
                self.results_sound.play()
            else:
                # PLAYER CAPTURED ALL 151
                pygame.mixer.stop()
                self.confetti_sound.set_volume(1.5)
                self.fanfare_sound.set_volume(0.8)
                self.fanfare_sound.play()
                self.confetti_sound.play()
                pygame.time.wait(5000)
                self.epilogue_sound.set_volume(0.2)
                self.epilogue_sound.play()

            # GET USER INPUT FOR QUIT OR RESTART
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.mixer.quit()
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_HOME:
                            # RESTART
                            from main import Game
                            Game().run(True)  # RESTART GAME, SKIP TUTORIAL
                        elif event.key == pygame.K_ESCAPE:
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit()
