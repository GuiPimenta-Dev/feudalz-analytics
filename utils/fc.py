import warnings

import pandas as pd

from game import Game
from models import Land, MockPlayer

warnings.filterwarnings("ignore")


def create_mock_game(
        my_attack_bonus: float,
        my_defense_bonus: float = 0,
        my_region: str = "Grassland",
        enemy_defense_bonus: float = 0,
        enemy_region: str = "Grassland",
):
    me = MockPlayer(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus)
    my_land = Land(region=my_region)
    enemy = MockPlayer(attack_bonus=0, defense_bonus=enemy_defense_bonus)
    enemy_land = Land(region=enemy_region)
    return Game(me=me, my_land=my_land, enemy=enemy, enemy_land=enemy_land)


def get_df_over_increase(
        enemy_defense_bonus: float,
        my_attack_bonus: int = 0,
        my_defense_bonus: float = 0,
        min_var: int = 0,
        cap: int = 70,
        step: int = 5,
        variation: str = "attack",
        games: int = 100,
        attacks: int = 100,
):
    df1 = df = pd.DataFrame(
        columns=[
            "my_defense_bonus",
            "my_attack_bonus",
            "enemy_defense_bonus",
            "goldz",
            "heal_cost",
            "recharge_cost",
            "total_cost",
        ]
    )

    for var in range(min_var, cap, step):

        for _ in range(games):
            if variation == "attack":
                game = create_mock_game(
                    my_attack_bonus=var,
                    my_defense_bonus=my_defense_bonus,
                    enemy_defense_bonus=enemy_defense_bonus,
                )
            else:
                game = create_mock_game(
                    my_attack_bonus=my_attack_bonus,
                    my_defense_bonus=var,
                    enemy_defense_bonus=enemy_defense_bonus,
                )
            for _ in range(attacks):
                game.attack()
            df = df.append(
                {
                    "my_defense_bonus": game.me.defense_bonus,
                    "my_attack_bonus": game.me.attack_bonus,
                    "enemy_defense_bonus": game.enemy.defense_bonus,
                    "goldz": game.me.goldz,
                    "heal_cost": game.me.heal_cost,
                    "recharge_cost": game.me.recharge_cost,
                    "total_cost": game.me.heal_cost + game.me.recharge_cost,
                },
                ignore_index=True,
            )

        df1 = df1.append(
            {
                "my_defense_bonus": round(df.my_defense_bonus.mean(), 2),
                "my_attack_bonus": round(df.my_attack_bonus.mean(), 2),
                "enemy_defense_bonus": round(df.enemy_defense_bonus.mean(), 2),
                "goldz": round(df.goldz.mean(), 2),
                "heal_cost": round(df.heal_cost.mean(), 2),
                "recharge_cost": round(df.recharge_cost.mean(), 2),
                "total_cost": round(df.total_cost.mean(), 2),
                "profit": round(df.goldz.mean() - (df.total_cost.mean()), 2),
            },
            ignore_index=True,
        )

        df = pd.DataFrame()

    return df1


def simulation(
        my_defense_bonus: float,
        my_attack_bonus: float,
        enemy_defense_bonus: float,
        use: int = 20,
        hero: str = None,
        rarity: str = "usual",
        games=100,
        attacks: int = 100,
        days: int = 5,
        recharge=10,
        group: bool = False,
):
    df_total = df = pd.DataFrame(
        columns=[
            "day",
            "energy",
            "goldz",
            "my_defense_bonus",
            "my_attack_bonus",
            "my_dice",
            "enemy_defense_bonus",
            "enemy_dice",
        ]
    )

    for _ in range(games):
        game = create_mock_game(
            my_attack_bonus=my_attack_bonus,
            my_defense_bonus=my_defense_bonus,
            enemy_defense_bonus=enemy_defense_bonus,
        )
        for i in range(attacks):
            if hero and use <= i < use + recharge:
                game.attack(hero=hero, rarity=rarity)
            else:
                game.attack()
        df = df.append(game.me.history, ignore_index=True)

    for i in df.groupby("day"):
        df_total = df_total.append(
            {
                "day": i[0],
                "energy": round(i[1].energy.mean(), 2),
                "my_defense_bonus": round(i[1].my_defense_bonus.mean(), 2),
                "my_attack_bonus": round(i[1].my_attack_bonus.mean(), 2),
                "enemy_defense_bonus": round(i[1].enemy_defense_bonus.mean(), 2),
                "goldz": round(i[1].goldz.mean(), 2),
                "my_dice": round(i[1].my_dice.mean(), 2),
                "enemy_dice": round(i[1].enemy_dice.mean(), 2),
            },
            ignore_index=True,
        )

    df_grouped = pd.DataFrame(
        [[0, None, 0, None, None, None, None, None]],
        columns=[
            "day",
            "energy",
            "goldz",
            "my_defense_bonus",
            "my_attack_bonus",
            "my_dice",
            "enemy_defense_bonus",
            "enemy_dice",
        ],
    )
    if group:
        for i in range(days, attacks // 2 + days, days):
            data = df_total[i - days: i]

            df_grouped = df_grouped.append(
                {
                    "day": i,
                    "energy": round(data.energy.sum(), 2),
                    "my_defense_bonus": round(data.my_defense_bonus.mean(), 2),
                    "my_attack_bonus": round(data.my_attack_bonus.mean(), 2),
                    "enemy_defense_bonus": round(data.enemy_defense_bonus.mean(), 2),
                    "goldz": round(data.goldz.sum(), 2),
                    "my_dice": round(data.my_dice.mean(), 2),
                    "enemy_dice": round(data.enemy_dice.mean(), 2),
                },
                ignore_index=True,
            )
        return df_grouped

    return df_total
