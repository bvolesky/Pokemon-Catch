import json


class Pokemon:
    def __init__(self, pokemon_dict):
        self.pokemon_name = pokemon_dict["pokemon_name"]
        self.pokedex_number = pokemon_dict["pokedex_number"]
        self.catch_rate = pokemon_dict["catch_rate"]
        self.base_flee = pokemon_dict["base_flee"]
        self.baited_flee = pokemon_dict["baited_flee"]
        self.angered_flee = pokemon_dict["angered_flee"]


def main():
    with open('pokedex.json', "r") as pokedex_file:
        pokedex = json.load(pokedex_file)
    Bulbasaur = Pokemon(pokedex["Bulbasaur"])
    print(Bulbasaur.pokemon_name)
    print(Bulbasaur.catch_rate)


main()
