# -*- coding: utf-8 -*-
import pygame
from os import walk
import json
import threading

pokemon_dict = {}


def getImages(path, *pokemon):
    # IMPORTS DIRECTORY OF IMAGES, USED BY getPlayerSprites and getPokemonSprites
    surface_list = []
    for _, __, img_files in walk(path):
        for image in sorted(img_files):
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            if pokemon:
                image_surf = pygame.transform.scale(image_surf, (image_surf.get_width() * 3, image_surf.get_height() * 3))  # TRIPLE SPRITE SIZE
            surface_list.append(image_surf)
    return surface_list


def getPlayerSprites():
    # IMPORTS PLAYER IMAGES
    character_path = 'assets/images/sprites/player/'
    animations = {'up': [], 'down': [], 'left': [], 'right': [], 'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [], 'up_throw': [], 'down_throw': [], 'left_throw': [], 'right_throw': []}
    for animation in animations.keys():
        full_path = character_path + animation
        animations[animation] = getImages(full_path)
    return animations


def getPokemonSprites(name):
    # IMPORTS INDIVIDUAL POKÉMON IMAGES
    main_path = f'assets/images/sprites/pokemon/{name}/'
    animations = {'left': getImages(main_path + 'move/left', True),
                  'right': getImages(main_path + 'move/right', True),
                  'up': getImages(main_path + 'move/up', True),
                  'down': getImages(main_path + 'move/down', True),
                  }
    _name = name.capitalize()
    if name == 'mr.mime':
        _name = 'Mr.Mime'

    pokemon_dict[_name] = animations


def createPokemonSpriteDictionary():
    pokemon_names = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff",
                     "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton",
                     "Farfetch'd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr.Mime", "Scyther", "Jynx", "Electabuzz", "Magmar",
                     "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew"]
    threads = []
    for pokemon in pokemon_names:
        x = threading.Thread(target=getPokemonSprites, args=(pokemon.lower(),))
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()

    return pokemon_dict


def loadPickupGraphics(pickups):
    # IMPORTS ITEM IMAGES
    pickup_graphics = {}
    for k, v in pickups.items():
        pickup = pygame.image.load(v).convert_alpha()
        pickup_graphics[k] = pickup
    return pickup_graphics


def getPokedex():
    # GETS POKÉMON DATA
    with open('assets/data/pokedex.json', "r", encoding="utf-8") as pokedex_file:
        pokedex = json.load(pokedex_file)
    return pokedex


def pushLayerToTop(layer, group):
    # MODIFIES LAYER ORDER
    group.remove(layer)
    group.add(layer)


def getDirection(entity_status):
    # GETS TUPLE FROM STATUS
    status = entity_status
    if '_' in entity_status:
        status = entity_status.split('_')[0]
    return pygame.math.Vector2({'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[status])


def getSounds(sound=False):
    # RETURNS LOADED SOUND FILE
    if sound == 'collision':
        return pygame.mixer.Sound('assets/audio/sound_effects/collision.wav')
    elif sound == 'a':
        return pygame.mixer.Sound('assets/audio/sound_effects/a.wav')
    elif sound == 'ball_pickup':
        return pygame.mixer.Sound('assets/audio/sound_effects/ball_pickup.wav')
    elif sound == 'shoes_pickup':
        return pygame.mixer.Sound('assets/audio/sound_effects/shoes_pickup.wav')
    elif sound == 'water_pickup':
        return pygame.mixer.Sound('assets/audio/sound_effects/water_pickup.wav')
    elif sound == 'countdown_number':
        return pygame.mixer.Sound('assets/audio/sound_effects/countdown_number.wav')
    elif sound == 'go':
        return pygame.mixer.Sound('assets/audio/sound_effects/go.wav')
    elif sound == 'ball_open':
        return pygame.mixer.Sound('assets/audio/sound_effects/ball_open.wav')
    elif sound == 'ball_throw':
        return pygame.mixer.Sound('assets/audio/sound_effects/ball_throw.wav')
    elif sound == 'ball_wobble':
        return pygame.mixer.Sound('assets/audio/sound_effects/ball_wobble.wav')
    elif sound == 'captured':
        return pygame.mixer.Sound('assets/audio/sound_effects/captured.wav')
    elif sound == 'runaway':
        return pygame.mixer.Sound('assets/audio/sound_effects/runaway.mp3')
    elif sound == 'safari_pa':
        return pygame.mixer.Sound('assets/audio/sound_effects/safari_pa.wav')
    elif sound == 'pokedex_rating':
        return pygame.mixer.Sound('assets/audio/sound_effects/pokedex_rating.wav')
    elif sound == 'confetti':
        return pygame.mixer.Sound('assets/audio/sound_effects/confetti.wav')
    elif sound == 'title':
        return pygame.mixer.Sound('assets/audio/music/title.mp3')
    elif sound == 'safari_music':
        return pygame.mixer.Sound('assets/audio/music/safari.ogg')
    elif sound == 'jigglypuff_singing':
        return pygame.mixer.Sound('assets/audio/music/jigglypuff.mp3')
    elif sound == 'pokeflute':
        return pygame.mixer.Sound('assets/audio/music/pokeflute.mp3')
    elif sound == 'legendary_battle':
        return pygame.mixer.Sound('assets/audio/music/legendary_battle.mp3')
    elif sound == 'mewtwo':
        return pygame.mixer.Sound('assets/audio/music/mewtwo.mp3')
    elif sound == 'pre_mew':
        return pygame.mixer.Sound('assets/audio/music/pre_mew.mp3')
    elif sound == 'mew':
        return pygame.mixer.Sound('assets/audio/music/mew.mp3')
    elif sound == 'results':
        return pygame.mixer.Sound('assets/audio/music/results.mp3')
    elif sound == 'fanfare':
        return pygame.mixer.Sound('assets/audio/music/fanfare.mp3')
    elif sound == 'epilogue':
        return pygame.mixer.Sound('assets/audio/music/epilogue.mp3')

    # POKÉMON CRIES BY DEX NUMBER
    elif sound == '001':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/001.ogg')
    elif sound == '002':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/002.ogg')
    elif sound == '003':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/003.ogg')
    elif sound == '004':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/004.ogg')
    elif sound == '005':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/005.ogg')
    elif sound == '006':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/006.ogg')
    elif sound == '007':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/007.ogg')
    elif sound == '008':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/008.ogg')
    elif sound == '009':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/009.ogg')
    elif sound == '010':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/010.ogg')
    elif sound == '011':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/011.ogg')
    elif sound == '012':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/012.ogg')
    elif sound == '013':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/013.ogg')
    elif sound == '014':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/014.ogg')
    elif sound == '015':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/015.ogg')
    elif sound == '016':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/016.ogg')
    elif sound == '017':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/017.ogg')
    elif sound == '018':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/018.ogg')
    elif sound == '019':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/019.ogg')
    elif sound == '020':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/020.ogg')
    elif sound == '021':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/021.ogg')
    elif sound == '022':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/022.ogg')
    elif sound == '023':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/023.ogg')
    elif sound == '024':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/024.ogg')
    elif sound == '025':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/025.ogg')
    elif sound == '026':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/026.ogg')
    elif sound == '027':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/027.ogg')
    elif sound == '028':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/028.ogg')
    elif sound == '029':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/029.ogg')
    elif sound == '030':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/030.ogg')
    elif sound == '031':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/031.ogg')
    elif sound == '032':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/032.ogg')
    elif sound == '033':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/033.ogg')
    elif sound == '034':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/034.ogg')
    elif sound == '035':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/035.ogg')
    elif sound == '036':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/036.ogg')
    elif sound == '037':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/037.ogg')
    elif sound == '038':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/038.ogg')
    elif sound == '039':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/039.ogg')
    elif sound == '040':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/040.ogg')
    elif sound == '041':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/041.ogg')
    elif sound == '042':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/042.ogg')
    elif sound == '043':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/043.ogg')
    elif sound == '044':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/044.ogg')
    elif sound == '045':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/045.ogg')
    elif sound == '046':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/046.ogg')
    elif sound == '047':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/047.ogg')
    elif sound == '048':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/048.ogg')
    elif sound == '049':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/049.ogg')
    elif sound == '050':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/050.ogg')
    elif sound == '051':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/051.ogg')
    elif sound == '052':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/052.ogg')
    elif sound == '053':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/053.ogg')
    elif sound == '054':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/054.ogg')
    elif sound == '055':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/055.ogg')
    elif sound == '056':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/056.ogg')
    elif sound == '057':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/057.ogg')
    elif sound == '058':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/058.ogg')
    elif sound == '059':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/059.ogg')
    elif sound == '060':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/060.ogg')
    elif sound == '061':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/061.ogg')
    elif sound == '062':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/062.ogg')
    elif sound == '063':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/063.ogg')
    elif sound == '064':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/064.ogg')
    elif sound == '065':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/065.ogg')
    elif sound == '066':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/066.ogg')
    elif sound == '067':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/067.ogg')
    elif sound == '068':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/068.ogg')
    elif sound == '069':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/069.ogg')
    elif sound == '070':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/070.ogg')
    elif sound == '071':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/071.ogg')
    elif sound == '072':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/072.ogg')
    elif sound == '073':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/073.ogg')
    elif sound == '074':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/074.ogg')
    elif sound == '075':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/075.ogg')
    elif sound == '076':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/076.ogg')
    elif sound == '077':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/077.ogg')
    elif sound == '078':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/078.ogg')
    elif sound == '079':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/079.ogg')
    elif sound == '080':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/080.ogg')
    elif sound == '081':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/081.ogg')
    elif sound == '082':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/082.ogg')
    elif sound == '083':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/083.ogg')
    elif sound == '084':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/084.ogg')
    elif sound == '085':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/085.ogg')
    elif sound == '086':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/086.ogg')
    elif sound == '087':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/087.ogg')
    elif sound == '088':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/088.ogg')
    elif sound == '089':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/089.ogg')
    elif sound == '090':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/090.ogg')
    elif sound == '091':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/091.ogg')
    elif sound == '092':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/092.ogg')
    elif sound == '093':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/093.ogg')
    elif sound == '094':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/094.ogg')
    elif sound == '095':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/095.ogg')
    elif sound == '096':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/096.ogg')
    elif sound == '097':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/097.ogg')
    elif sound == '098':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/098.ogg')
    elif sound == '099':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/099.ogg')
    elif sound == '100':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/100.ogg')
    elif sound == '101':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/101.ogg')
    elif sound == '102':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/102.ogg')
    elif sound == '103':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/103.ogg')
    elif sound == '104':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/104.ogg')
    elif sound == '105':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/105.ogg')
    elif sound == '106':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/106.ogg')
    elif sound == '107':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/107.ogg')
    elif sound == '108':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/108.ogg')
    elif sound == '109':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/109.ogg')
    elif sound == '110':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/110.ogg')
    elif sound == '111':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/111.ogg')
    elif sound == '112':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/112.ogg')
    elif sound == '113':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/113.ogg')
    elif sound == '114':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/114.ogg')
    elif sound == '115':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/115.ogg')
    elif sound == '116':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/116.ogg')
    elif sound == '117':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/117.ogg')
    elif sound == '118':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/118.ogg')
    elif sound == '119':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/119.ogg')
    elif sound == '120':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/120.ogg')
    elif sound == '121':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/121.ogg')
    elif sound == '122':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/122.ogg')
    elif sound == '123':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/123.ogg')
    elif sound == '124':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/124.ogg')
    elif sound == '125':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/125.ogg')
    elif sound == '126':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/126.ogg')
    elif sound == '127':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/127.ogg')
    elif sound == '128':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/128.ogg')
    elif sound == '129':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/129.ogg')
    elif sound == '130':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/130.ogg')
    elif sound == '131':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/131.ogg')
    elif sound == '132':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/132.ogg')
    elif sound == '133':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/133.ogg')
    elif sound == '134':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/134.ogg')
    elif sound == '135':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/135.ogg')
    elif sound == '136':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/136.ogg')
    elif sound == '137':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/137.ogg')
    elif sound == '138':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/138.ogg')
    elif sound == '139':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/139.ogg')
    elif sound == '140':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/140.ogg')
    elif sound == '141':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/141.ogg')
    elif sound == '142':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/142.ogg')
    elif sound == '143':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/143.ogg')
    elif sound == '144':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/144.ogg')
    elif sound == '145':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/145.ogg')
    elif sound == '146':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/146.ogg')
    elif sound == '147':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/147.ogg')
    elif sound == '148':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/148.ogg')
    elif sound == '149':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/149.ogg')
    elif sound == '150':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/150.ogg')
    elif sound == '151':
        return pygame.mixer.Sound('assets/audio/sound_effects/cries/151.ogg')


def debug(info, y=10, x=10):
    # DISPLAYS VALUES ON SCREEN
    display_surface = pygame.display.get_surface()
    debug_surf = pygame.font.Font(None, 30).render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surface, 'Black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)
