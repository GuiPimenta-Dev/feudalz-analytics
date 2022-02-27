from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import randint, choices

NUMBER_OF_ATTACKS = 2
RECHARGE_COST = 1
ENEMY_DEFENSE_BONUS = 23.8
MAX_ENERGY = 1000
CHARGES = 10
earnings_range = [
    {
        "percentage": 200,
        "earning": 7,
    },
    {
        "percentage": 150,
        "earning": 5,
    },
    {
        "percentage": 100,
        "earning": 3,
    },
    {
        "percentage": 50,
        "earning": 1,
    },
    {
        "percentage": 0,
        "earning": 0.5,
    },
]


@dataclass
class Land(ABC):
    day = 1
    energy_cost: int = 0
    attacks = NUMBER_OF_ATTACKS
    goldz: float = 0
    qtd_attacks: int = 0

    def __init__(self, attack_bonus, defense_bonus):
        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus

    @abstractmethod
    def battle(self):
        pass

    def attack(self):
        return randint(1, 70) + self.attack_bonus

    @staticmethod
    def defend(enemy_defense_bonus: float = ENEMY_DEFENSE_BONUS):
        return randint(1, 70) + enemy_defense_bonus

    def wait_a_day(self):
        if self.attacks == 0:
            self.attacks = NUMBER_OF_ATTACKS
            self.day += 1

    def self_damage(self, enemy_total):
        self.energy_cost += round(enemy_total * (1 - (0.008 * self.defense_bonus)), 2)

    def claim_gold(self, my_total, enemy_total):
        self.qtd_attacks += 1
        percentage = round(my_total / enemy_total * 100)
        for item in earnings_range:
            if percentage >= item["percentage"]:
                self.goldz += item["earning"]


@dataclass
class NoHero(Land):
    def __init__(self, attack_bonus, defense_bonus):
        super().__init__(attack_bonus, defense_bonus)

    def battle(self):
        my_total = self.attack()
        enemy_total = self.defend()
        self.attacks -= 1
        self.self_damage(enemy_total=enemy_total)
        self.claim_gold(my_total=my_total, enemy_total=enemy_total)
        self.wait_a_day()


@dataclass
class Godjira(Land):
    charges = CHARGES

    def __init__(self, attack_bonus, defense_bonus, rarity):
        super().__init__(attack_bonus, defense_bonus)
        self.rarity = rarity

    def battle(self):
        self.charges -= 1
        stats = {"common": 0.25, "uncommon": 0.50, "rare": 0.75, "epic": 1}
        special = choices([True, False], [stats[self.rarity], 1 - stats[self.rarity]])[0]
        enemy_defense_bonus = 0 if special else ENEMY_DEFENSE_BONUS
        my_total = self.attack()
        enemy_total = self.defend(enemy_defense_bonus=enemy_defense_bonus)
        self.attacks -= 1
        self.self_damage(enemy_total=enemy_total)
        self.claim_gold(my_total=my_total, enemy_total=enemy_total)
        self.wait_a_day()


@dataclass
class Yokai(Land):
    charges = CHARGES

    def __init__(self, attack_bonus, defense_bonus, rarity):
        super().__init__(attack_bonus, defense_bonus)
        self.rarity = rarity

    def battle(self):
        self.charges -= 1
        stats = {"common": 2, "uncommon": 3, "rare": 4, "epic": 5}
        dices = [randint(1, 70) for _ in range(stats[self.rarity])]
        my_dice = max(dices)
        my_total = my_dice + self.attack_bonus
        enemy_total = self.defend()
        self.attacks -= 1
        self.self_damage(enemy_total=enemy_total)
        self.claim_gold(my_total=my_total, enemy_total=enemy_total)
        self.wait_a_day()


@dataclass
class CyberKongz(Land):
    charges = CHARGES

    def __init__(self, attack_bonus, defense_bonus, rarity):
        super().__init__(attack_bonus, defense_bonus)
        self.rarity = rarity

    def battle(self):
        self.charges -= 1
        stats = {"common": 0.25, "uncommon": 0.50, "rare": 0.75, "epic": 1}
        my_total = self.attack()
        special = choices([True, False], [stats[self.rarity], 1 - stats[self.rarity]])[0]
        if special:
            my_total *= 2
        enemy_total = self.defend()
        self.attacks -= 1
        self.self_damage(enemy_total=enemy_total)
        self.claim_gold(my_total=my_total, enemy_total=enemy_total)
        self.wait_a_day()


@dataclass
class Lyz(Land):
    charges = CHARGES

    def __init__(self, attack_bonus, defense_bonus, rarity):
        super().__init__(attack_bonus, defense_bonus)
        self.rarity = rarity

    def battle(self):
        self.charges -= 1
        stats = {"common": 0.25, "uncommon": 0.50, "rare": 0.75, "epic": 1}
        my_total = self.attack()
        special = choices([True, False], [stats[self.rarity], 1 - stats[self.rarity]])[0]
        enemy_total = self.defend()
        if not special:
            self.self_damage(enemy_total=enemy_total)
        self.attacks -= 1
        self.claim_gold(my_total=my_total, enemy_total=enemy_total)
        self.wait_a_day()


@dataclass
class Etherman(Land):
    charges = CHARGES

    def __init__(self, attack_bonus, defense_bonus, rarity):
        super().__init__(attack_bonus, defense_bonus)
        self.rarity = rarity

    def battle(self):
        self.charges -= 1
        stats = {"common": 0.25, "uncommon": 0.50, "rare": 0.75, "epic": 1}
        my_dice = randint(1, 70)
        my_total = my_dice + self.attack_bonus
        special = choices([True, False], [stats[self.rarity], 1 - stats[self.rarity]])[0]
        if special:
            self.energy_cost -= my_dice + self.defense_bonus
        enemy_total = self.defend()
        self.self_damage(enemy_total=enemy_total)
        self.attacks -= 1
        self.claim_gold(my_total=my_total, enemy_total=enemy_total)
        self.wait_a_day()


@dataclass
class Creepz(Land):
    charges = CHARGES

    def __init__(self, attack_bonus, defense_bonus, rarity):
        super().__init__(attack_bonus, defense_bonus)
        self.rarity = rarity

    def battle(self):
        self.charges -= 1
        stats = {"common": 0.25, "uncommon": 0.50, "rare": 0.75, "epic": 1}
        my_total = self.attack()
        enemy_total = self.defend()
        special = choices([True, False], [stats[self.rarity], 1 - stats[self.rarity]])[0]
        if not special:
            self.attacks -= 1
        self.self_damage(enemy_total=enemy_total)
        self.claim_gold(my_total=my_total, enemy_total=enemy_total)
        self.wait_a_day()
