from random import randint

from models import Player, Land, History

me = Player(feudalz=['133', '4417', '4430'], orcz=10, elvez=6, animalz=["1563", "3243", "2132"]
            )
my_land = Land(region='Grassland')

enemy = Player(feudalz=['4413', '3850', '2828', '2808'], orcz=5, elvez=1, animalz=["673", "671"]
               )
enemy_land = Land(region='Grassland')

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
    days: int = 1

    def __init__(self, me, my_land, enemy, enemy_land):
        me.defense_bonus = min(me.defense_bonus + my_land.defense_bonus, 65)
        enemy.defense_bonus = min(enemy.defense_bonus + enemy_land.defense_bonus, 65)
        self.me = me
        self.my_land = my_land
        self.enemy = enemy

    def attack(self):
        if self.my_land.attacks == 0:
            self.__wait_a_day()

        if self.my_land.energy <= 0:
            self.__heal_land()

        my_dice = randint(1, 70)
        enemy_dice = randint(1, 70)
        self.__combat(my_dice=my_dice, enemy_dice=enemy_dice)

    def __wait_a_day(self):
        self.my_land.attacks = 2
        self.days += 1
        self.me.cost += 1

    def __heal_land(self):
        self.my_land.energy = 1000
        self.me.cost += 10

    def __combat(self, my_dice, enemy_dice):
        my_total = my_dice + self.me.attack_bonus
        enemy_total = enemy_dice + self.enemy.defense_bonus
        energy = self.__self_damage(my_total=my_total,
                                    defense_bonus=self.me.defense_bonus)
        goldz = self.__calculate_earning(my_total, enemy_total)
        self.my_land.energy -= energy
        self.me.goldz += goldz
        self.my_land.attacks -= 1
        history = History(energy=energy, goldz=goldz, my_total=my_total, enemy_total=enemy_total)
        if my_total > enemy_total:
            self.me.victories.append(history)
        else:
            self.me.defeats.append(history)

    @staticmethod
    def __self_damage(my_total, defense_bonus):
        return round(my_total * (1 - (0.008 * defense_bonus)))

    @staticmethod
    def __calculate_earning(my_total, enemy_total):
        percentage = round(my_total / enemy_total) * 100
        for item in earnings_range:
            if percentage >= item["percentage"]:
                return item['earning']

    def __repr__(self):
        return f"\nGoldz: {self.me.goldz}\n" \
               f"Cost: {self.me.cost}\n" \
               f"Victories: {len(self.me.victories)}\n" \
               f"Defeats: {len(self.me.defeats)}\n" \
               f"Days: {self.days}"
