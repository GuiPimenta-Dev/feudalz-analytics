from random import randint

from models import Player, Land, History

me = Player(
    feudalz=["133", "4417", "4430"], orcz=10, elvez=6, animalz=["1563", "3243", "2132"]
)
my_land = Land(region="Grassland")

enemy = Player(
    feudalz=["4413", "3850", "2828", "2808"], orcz=5, elvez=1, animalz=["673", "671"]
)
enemy_land = Land(region="Grassland")

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


class Game:
    day: int = 1

    def __init__(self, me, my_land, enemy, enemy_land):
        me.defense_bonus = min(me.defense_bonus + my_land.defense_bonus, 65)
        enemy.defense_bonus = min(enemy.defense_bonus + enemy_land.defense_bonus, 65)
        self.me = me
        self.my_land = my_land
        self.enemy = enemy

    def attack(self, hero: str = None, rarity: str = "epic"):
        if self.my_land.attacks == 0:
            self.__wait_a_day()

        if self.my_land.energy <= 0:
            self.__heal_land()

        my_dice = randint(1, 70)
        enemy_dice = randint(1, 70)

        if hero == "urzog":
            attack_bonus, defense_bonus, energy, goldz = self.__urzog(my_dice=my_dice, enemy_dice=enemy_dice,
                                                                      rarity=rarity)
        elif hero == "tanker":
            attack_bonus, defense_bonus, energy, goldz = self.__tanker(my_dice=my_dice, enemy_dice=enemy_dice,
                                                                       rarity=rarity)
        else:
            attack_bonus, defense_bonus, energy, goldz = self.__no_hero(my_dice=my_dice, enemy_dice=enemy_dice)

        self.my_land.energy -= energy
        self.me.goldz += goldz
        self.my_land.attacks -= 1

        history = {
            "day": self.day,
            "energy": energy,
            "goldz": goldz,
            "my_defense_bonus": defense_bonus,
            "my_attack_bonus": attack_bonus,
            "my_dice": my_dice,
            "enemy_defense_bonus": self.enemy.defense_bonus,
            "enemy_dice": enemy_dice
        }

        self.me.history.append(history)

    def __wait_a_day(self):
        self.my_land.attacks = 2
        self.day += 1
        self.me.recharge_cost += 1

    def __heal_land(self):
        self.my_land.energy = self.my_land.max_energy
        self.me.heal_cost += self.my_land.heal_cost

    def __no_hero(self, my_dice, enemy_dice):
        energy = self.__self_damage(
            my_dice=my_dice, defense_bonus=self.me.defense_bonus
        )
        my_total = my_dice + self.me.attack_bonus
        enemy_total = enemy_dice + self.enemy.defense_bonus
        goldz = self.__calculate_earning(my_total, enemy_total)
        return self.me.attack_bonus, self.me.defense_bonus, energy, goldz

    def __urzog(self, my_dice, enemy_dice, rarity):
        stats = {"usual": 10, "unusual": 15, "rare": 27, "epic": 35}
        attack_bonus = self.me.attack_bonus + stats[rarity]
        my_total = my_dice + attack_bonus
        enemy_total = enemy_dice + self.enemy.defense_bonus
        energy = self.__self_damage(
            my_dice=my_dice, defense_bonus=self.me.defense_bonus
        )
        goldz = self.__calculate_earning(my_total, enemy_total)
        return attack_bonus, self.me.defense_bonus, energy, goldz

    def __tanker(self, my_dice, enemy_dice, rarity):
        stats = {"usual": 12, "unusual": 17, "rare": 32, "epic": 40}
        defense_bonus = self.me.defense_bonus + stats[rarity]
        my_total = my_dice + self.me.attack_bonus
        enemy_total = enemy_dice + self.enemy.defense_bonus
        energy = self.__self_damage(
            my_dice=my_dice, defense_bonus=defense_bonus
        )
        goldz = self.__calculate_earning(my_total, enemy_total)
        return self.me.attack_bonus, defense_bonus, energy, goldz

    @staticmethod
    def __self_damage(my_dice, defense_bonus):
        return round(my_dice * (1 - (0.008 * defense_bonus)))

    @staticmethod
    def __calculate_earning(my_total, enemy_total):
        percentage = round(my_total / enemy_total) * 100
        for item in earnings_range:
            if percentage >= item["percentage"]:
                return item["earning"]
