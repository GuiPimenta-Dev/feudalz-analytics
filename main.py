import warnings
from pprint import pprint

import pandas as pd

from game import Game
from models import Player, Land, MockPlayer

warnings.filterwarnings('ignore')


def create_game():
    def _create_game():
        me = Player(feudalz=['133', '4417', '4430'], orcz=10, elvez=6, animalz=["1563", "3243", "2132"])
        my_land = Land(region='Grassland')
        enemy = Player(feudalz=['4413', '3850', '2828', '2808'], orcz=5, elvez=1, animalz=["673", "671"])
        enemy_land = Land(region='Grassland')
        return Game(me=me, my_land=my_land, enemy=enemy, enemy_land=enemy_land)

    df = pd.DataFrame(
        columns=['days', 'my_defense_bonus', 'my_attack_bonus', 'enemy_defense_bonus', 'goldz', 'cost', 'victories',
                 'defeats'])

    for _ in range(1000):
        game = _create_game()
        for _ in range(100):
            game.attack()
        df = df.append(
            {'days': game.days, 'my_defense_bonus': game.me.defense_bonus, 'my_attack_bonus': game.me.attack_bonus,
             'enemy_defense_bonus': game.enemy.defense_bonus, 'goldz': game.me.goldz, 'cost': game.me.cost,
             'victories': len(game.me.victories), 'defeats': len(game.me.defeats)}, ignore_index=True)

    pprint({'my_defense_bonus': round(df.my_defense_bonus.mean(), 2),
            'my_attack_bonus': round(df.my_attack_bonus.mean(), 2),
            'enemy_defense_bonus': round(df.enemy_defense_bonus.mean(), 2),
            'goldz': round(df.goldz.mean(), 2),
            'cost': round(df.cost.mean(), 2),
            'profit': round(df.goldz.mean() - df.cost.mean(), 2),
            'victories': round(df.victories.mean(), 2),
            'defeats': round(df.defeats.mean(), 2)})


def create_mock_game(my_attack_bonus: int = 0, my_defense_bonus: int = 0, my_region: str = 'Grassland',
                     enemy_defense_bonus: int = 0,
                     enemy_region: str = 'Grassland'):
    me = MockPlayer(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus)
    my_land = Land(region=my_region)
    enemy = MockPlayer(attack_bonus=0, defense_bonus=enemy_defense_bonus)
    enemy_land = Land(region=enemy_region)
    return Game(me=me, my_land=my_land, enemy=enemy, enemy_land=enemy_land)


if __name__ == "__main__":
    my_attack_bonus = my_defense_bonus = enemy_defense_bonus = 0
    df_total = df = pd.DataFrame(
        columns=['my_defense_bonus', 'my_attack_bonus', 'enemy_defense_bonus', 'goldz', 'cost', 'victories', 'defeats',
                 'efficiency'])

    for my_attack_bonus in range(66):

        for _ in range(100):
            game = create_mock_game(my_attack_bonus=my_attack_bonus, my_defense_bonus=my_defense_bonus,
                                    enemy_defense_bonus=enemy_defense_bonus)
            for _ in range(100):
                game.attack()
            df = df.append(
                {'my_defense_bonus': game.me.defense_bonus, 'my_attack_bonus': game.me.attack_bonus,
                 'enemy_defense_bonus': game.enemy.defense_bonus, 'goldz': game.me.goldz, 'cost': game.me.cost,
                 'victories': len(game.me.victories), 'defeats': len(game.me.defeats),
                 'efficiency': (len(game.me.victories) / (len(game.me.victories) + len(game.me.defeats))) * 100},
                ignore_index=True)


        df_total = df_total.append(
            {'my_defense_bonus': round(df.my_defense_bonus.mean(), 2),
             'my_attack_bonus': round(df.my_attack_bonus.mean(), 2),
             'enemy_defense_bonus': round(df.enemy_defense_bonus.mean(), 2),
             'goldz': round(df.goldz.mean(), 2),
             'cost': round(df.cost.mean(), 2),
             'profit': round(df.goldz.mean() - df.cost.mean(), 2),
             'victories': round(df.victories.mean(), 2),
             'defeats': round(df.defeats.mean(), 2),
             'efficiency': round(df.efficiency.mean(), 2),
             },
            ignore_index=True)

        df = pd.DataFrame()

    pprint({'my_defense_bonus': round(df_total.my_defense_bonus.mean(), 2),
            'my_attack_bonus': round(df_total.my_attack_bonus.mean(), 2),
            'enemy_defense_bonus': round(df_total.enemy_defense_bonus.mean(), 2),
            'goldz': round(df_total.goldz.mean(), 2),
            'cost': round(df_total.cost.mean(), 2),
            'profit': round(df_total.goldz.mean() - df_total.cost.mean(), 2),
            'victories': round(df_total.victories.mean(), 2),
            'defeats': round(df_total.defeats.mean(), 2),
            'efficiency': round(df_total.efficiency.mean(), 2),
            })
