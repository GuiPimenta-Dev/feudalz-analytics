import json
from dataclasses import dataclass

import pandas as pd

rarity_table = json.load(open("utils/rarity_table.json"))
humanz_table = json.load(open("utils/humanz.json"))
animalz_table = json.load(open("utils/animalz.json"))

unique_feudalz_idz = [
    "177",
    "1055",
    "133",
    "3023",
    "2275",
    "4310",
    "4433",
    "3467",
    "3964",
    "3910",
    "1088",
    "745",
    "3399",
    "2595",
    "3797",
]

region_bonus = {
    "Snowy": 28,
    "Grassland": 10,
    "Forest": 16,
    "Arid": 22,
    "Unique": 35,
}


@dataclass
class Land:
    max_energy = 1000
    energy: int = max_energy
    heal_cost = 10
    attacks: int = 2

    def __init__(self, region):
        self.defense_bonus = region_bonus[region]


@dataclass
class History:
    energy: float
    goldz: float
    my_total: float
    enemy_total: float


@dataclass
class Player:
    attack_bonus: float
    defense_bonus: float
    goldz: float = 0
    cost: float = 0

    def __init__(self, feudalz, orcz, elvez, animalz):
        self.victories = []
        self.defeats = []
        self.get_attack_bonus(feudalz=feudalz, orcz=orcz, animalz=animalz)
        self.get_defense_bonus(feudalz=feudalz, elvez=elvez, animalz=animalz)

    def get_attack_bonus(self, feudalz, orcz, animalz):
        bonus = 0
        for id in feudalz:
            if id in unique_feudalz_idz:
                bonus += 6
            else:
                rarity = int(rarity_table[id])
                if rarity <= 250:
                    bonus += 5
                elif rarity <= 999:
                    bonus += 3
                elif rarity <= 2222:
                    bonus += 1
                else:
                    bonus += 0.1

        bonus += min(orcz, 30)
        dragonz = sum(
            self.__count_traits("Dragonz", animalz_table, id=id) for id in animalz
        )
        bonus += dragonz * 10
        self.attack_bonus = min(bonus, 65)

    def get_defense_bonus(self, feudalz, elvez, animalz):
        bonus = 0

        for id in feudalz:
            traits = humanz_table[id]["traits"]
            for trait in traits:
                trait_rarity = round(trait["trait_count"] / 4444) * 100
                if trait_rarity <= 3:
                    bonus += 2
                elif trait_rarity == 4:
                    bonus += 1

        male_bonus = sum(
            self.__count_traits("Human Male", humanz_table, id=id) for id in feudalz
        )

        bonus += min(male_bonus, 10)
        bonus += min(elvez * 1.5, 30)
        bonus += min(len(animalz) * 0.2, 10)

        duck_bonus = sum(
            self.__count_traits("Pure Gold", animalz_table, id=id) for id in animalz
        )
        bonus += duck_bonus * 10

        self.defense_bonus = min(bonus, 65)

    def __count_traits(self, value, table, id):
        for i in table[id]["traits"]:
            if i["value"] == value:
                return 1
        return 0


@dataclass
class MockPlayer:
    attack_bonus: float
    defense_bonus: float
    goldz = 0
    heal_cost = 0
    recharge_cost = 0

    def __init__(self, attack_bonus, defense_bonus):
        # self.history = pd.DataFrame(columns=['day', 'energy', 'goldz', 'my_total', 'enemy_total', 'result'])
        self.history = []
        self.attack_bonus = min(attack_bonus, 65)
        self.defense_bonus = min(defense_bonus, 65)
