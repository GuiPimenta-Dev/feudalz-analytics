from random import randint, choices

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

NUMBER_OF_ATTACKS = 2
RECHARGE_COST = 1


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
            my_attack_bonus, enemy_defense_bonus, energy, goldz = self.__urzog(
                my_dice=my_dice, enemy_dice=enemy_dice, rarity=rarity
            )
        elif hero == "dicez":
            my_attack_bonus, enemy_defense_bonus, energy, goldz = self.__dicez(
                my_dice=my_dice, enemy_dice=enemy_dice, rarity=rarity
            )
        elif hero == "kongz":
            my_attack_bonus, enemy_defense_bonus, energy, goldz = self.__kongz(
                my_dice=my_dice, enemy_dice=enemy_dice, rarity=rarity
            )
        elif hero == "lyz":
            my_attack_bonus, enemy_defense_bonus, energy, goldz = self.__lyz(
                my_dice=my_dice, enemy_dice=enemy_dice, rarity=rarity
            )
        elif hero == "vampirao":
            my_attack_bonus, enemy_defense_bonus, energy, goldz = self.__vampirao(
                my_dice=my_dice, enemy_dice=enemy_dice, rarity=rarity
            )
        elif hero == "etherman":
            my_attack_bonus, enemy_defense_bonus, energy, goldz = self.__etherman(
                my_dice=my_dice, enemy_dice=enemy_dice, rarity=rarity
            )
        else:
            my_attack_bonus, enemy_defense_bonus, energy, goldz = self.__no_hero(
                my_dice=my_dice, enemy_dice=enemy_dice
            )

        self.my_land.energy -= energy
        self.me.goldz += goldz
        self.my_land.attacks -= 1

        history = {
            "day": self.day,
            "energy": -1 * energy,
            "recharge_cost": RECHARGE_COST / NUMBER_OF_ATTACKS,
            "attack": self.my_land.attacks,
            "goldz": goldz,
            "my_defense_bonus": self.me.defense_bonus,
            "my_attack_bonus": my_attack_bonus,
            "my_dice": my_dice,
            "enemy_defense_bonus": enemy_defense_bonus,
            "enemy_dice": enemy_dice,
        }

        self.me.history.append(history)

    def __wait_a_day(self):
        self.my_land.attacks = NUMBER_OF_ATTACKS
        self.day += 1
        self.me.recharge_cost += RECHARGE_COST

    def __heal_land(self):
        self.my_land.energy = self.my_land.max_energy
        self.me.heal_cost += self.my_land.heal_cost

    def __no_hero(self, my_dice, enemy_dice):
        my_total = my_dice + self.me.attack_bonus
        enemy_total = enemy_dice + self.enemy.defense_bonus
        energy = self.__self_damage(
            enemy_total=enemy_total, defense_bonus=self.me.defense_bonus
        )
        goldz = self.__calculate_earning(my_total, enemy_total)
        return self.me.attack_bonus, self.enemy.defense_bonus, energy, goldz

    def __urzog(self, my_dice, enemy_dice, rarity):
        stats = {"usual": 0.25, "unusual": 0.50, "rare": 0.75, "epic": 1}
        my_total = my_dice + self.me.attack_bonus
        enemy_defense_bonus = self.enemy.defense_bonus
        critical = choices([True, False], [stats[rarity], 1 - stats[rarity]])[0]
        if critical:
            enemy_defense_bonus = 0

        enemy_total = enemy_dice + enemy_defense_bonus
        energy = self.__self_damage(
            enemy_total=enemy_total, defense_bonus=self.me.defense_bonus
        )
        goldz = self.__calculate_earning(my_total, enemy_total)
        return self.me.attack_bonus, enemy_defense_bonus, energy, goldz

    def __dicez(self, my_dice, enemy_dice, rarity):
        stats = {"usual": 1, "unusual": 2, "rare": 3, "epic": 4}
        dices = [randint(1, 70) for _ in range(stats[rarity])]
        my_dice = max([my_dice, max(dices)])
        my_total = my_dice + self.me.attack_bonus
        enemy_total = enemy_dice + self.enemy.defense_bonus

        energy = self.__self_damage(
            enemy_total=enemy_total, defense_bonus=self.me.defense_bonus
        )
        goldz = self.__calculate_earning(my_total, enemy_total)
        return self.me.attack_bonus, self.enemy.defense_bonus, energy, goldz

    def __kongz(self, my_dice, enemy_dice, rarity):
        stats = {"usual": 0.25, "unusual": 0.50, "rare": 0.75, "epic": 1}
        my_total = my_dice + self.me.attack_bonus
        critical = choices([True, False], [stats[rarity], 1 - stats[rarity]])[0]
        if critical:
            my_total *= 2
        enemy_total = enemy_dice + self.enemy.defense_bonus
        energy = self.__self_damage(
            enemy_total=enemy_total, defense_bonus=self.me.defense_bonus
        )
        goldz = self.__calculate_earning(my_total, enemy_total)
        return my_total - 2 * my_dice, self.enemy.defense_bonus, energy, goldz

    def __lyz(self, my_dice, enemy_dice, rarity):
        stats = {"usual": 0.25, "unusual": 0.5, "rare": 0.75, "epic": 1}
        my_total = my_dice + self.me.attack_bonus
        critical = choices([True, False], [stats[rarity], 1 - stats[rarity]])[0]
        enemy_total = enemy_dice + self.enemy.defense_bonus
        if critical:
            energy = 0
        else:
            energy = self.__self_damage(
                enemy_total=enemy_total, defense_bonus=self.me.defense_bonus
            )

        goldz = self.__calculate_earning(my_total, enemy_total)
        return self.me.attack_bonus, self.enemy.defense_bonus, energy, goldz

    def __vampirao(self, my_dice, enemy_dice, rarity):
        stats = {"usual": 0.25, "unusual": 0.50, "rare": 0.75, "epic": 1}
        my_total = my_dice + self.me.attack_bonus
        critical = choices([True, False], [stats[rarity], 1 - stats[rarity]])[0]
        enemy_total = enemy_dice + self.enemy.defense_bonus
        life_steal = my_dice + self.me.defense_bonus if critical else 0
        energy = self.__self_damage(
            enemy_total=enemy_total, defense_bonus=self.me.defense_bonus
        )

        goldz = self.__calculate_earning(my_total, enemy_total)
        return (
            self.me.attack_bonus,
            self.enemy.defense_bonus,
            energy - life_steal,
            goldz,
        )

    def __etherman(self, my_dice, enemy_dice, rarity):
        attack_bonus = self.me.attack_bonus
        my_total = my_dice + attack_bonus
        enemy_total = enemy_dice + self.enemy.defense_bonus
        energy = self.__self_damage(
            enemy_total=enemy_total, defense_bonus=self.me.defense_bonus
        )
        goldz = self.__calculate_earning(my_total, enemy_total)
        if self.my_land.attacks == 1:
            stats = {"usual": 0.25, "unusual": 0.50, "rare": 0.75, "epic": 1}
            critical = choices([True, False], [stats[rarity], 1 - stats[rarity]])[0]
            if critical:
                my_new_dice = randint(1, 70)
                enemy_new_dice = randint(1, 70)
                my_new_total = my_new_dice + attack_bonus
                attack_bonus *= 2
                enemy_new_total = enemy_new_dice + self.enemy.defense_bonus
                energy += self.__self_damage(
                    enemy_total=enemy_new_total, defense_bonus=self.me.defense_bonus
                )
                goldz += self.__calculate_earning(my_new_total, enemy_new_total)

        return (
            attack_bonus,
            self.enemy.defense_bonus,
            energy,
            goldz,
        )

    @staticmethod
    def __self_damage(enemy_total, defense_bonus):
        return round(enemy_total * (1 - (0.008 * defense_bonus)))

    @staticmethod
    def __calculate_earning(my_total, enemy_total):
        percentage = round(my_total / enemy_total * 100)
        for item in earnings_range:
            if percentage >= item["percentage"]:
                return item["earning"]
