import warnings
from typing import List

import pandas as pd

from game import Game
from models import Land, MockPlayer
import matplotlib.pyplot as plt

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


def merge_dfs(
        column: str,
        dfs: List,
        pk: str = None,
        limits: tuple = (None, None),
        names=["no_hero", "usual", "unusual", "rare", "epic"],
):
    df_merged = pd.DataFrame()
    if pk:
        df_merged[pk] = dfs[0][pk]
    for index, df in enumerate(dfs):
        df_merged[names[index]] = df[column]
    return df_merged[limits[0]: limits[1]]


def get_df_columns_mean(
        df: pd.DataFrame, columns=["no_hero", "usual", "unusual", "rare", "epic"]
):
    df = df[columns].mean(axis=0)
    return df.to_frame().T


def get_df_columns_sum(
        df: pd.DataFrame, columns=["no_hero", "usual", "unusual", "rare", "epic"]
):
    df = df[columns].sum(axis=0)
    return df.to_frame().T


def get_diff(
        df: pd.DataFrame,
        column: str = "no_hero",
        pk: str = "day",
        names=["no_hero", "usual", "unusual", "rare", "epic"],
        column_names=["usual", "unusual", "rare", "epic"],
):
    df2 = pd.DataFrame()
    if pk:
        df2[pk] = df[pk]
    for index, name in enumerate(names):
        if index < len(column_names):
            df2[column_names[index]] = df[names[index + 1]] - df[column]

    return df2


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
        attacks: int = 40,
        days: int = 5,
        recharge=10,
        group: bool = False,
):
    df_total = df = pd.DataFrame(
        columns=[
            "day",
            "attack",
            "energy",
            "goldz",
            # "heal_cost",
            # "recharge_cost",
            # "total_cost",
            # "profit",
            # "my_defense_bonus",
            "my_attack_bonus",
            # "my_dice",
            # "enemy_defense_bonus",
            # "enemy_dice",
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

    # max_energy = Land.max_energy
    for i in df.groupby("day"):
        for j in i[1].groupby("attack"):
            energy = round(j[1].energy.mean(), 2)
            # max_energy, heal_cost = calculate_heal_cost(
            #     max_energy=max_energy, energy=energy
            # )
            # recharge_cost = j[1].recharge_cost.mean()
            # total_cost = heal_cost + recharge_cost
            goldz = round(j[1].goldz.mean(), 2)
            df_total = df_total.append(
                {
                    "day": i[0],
                    "attack": j[0],
                    "energy": energy,
                    "goldz": goldz,
                    # "heal_cost": heal_cost,
                    # "recharge_cost": recharge_cost,
                    # "profit": goldz - total_cost,
                    # "total_cost": total_cost,
                    # "my_defense_bonus": round(j[1].my_defense_bonus.mean(), 2),
                    "my_attack_bonus": round(j[1].my_attack_bonus.mean(), 2),
                    # "enemy_defense_bonus": round(j[1].enemy_defense_bonus.mean(), 2),
                    # "my_dice": round(j[1].my_dice.mean(), 2),
                    # "enemy_dice": round(j[1].enemy_dice.mean(), 2),
                },
                ignore_index=True,
            )

    if group:
        df_grouped = pd.DataFrame(
            [[0, None, 0, None, None, None, None, None, None, None, None, None, None]],
            columns=[
                "day",
                "energy",
                "attack",
                "goldz",
                # "recharge_cost",
                # "total_cost",
                # "heal_cost",
                # "profit",
                # "my_defense_bonus",
                # "my_attack_bonus",
                # "my_dice",
                # "enemy_defense_bonus",
                # "enemy_dice",
            ],
        )
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
                    "recharge_cost": data.recharge_cost.sum(),
                    "total_cost": data.total_cost.sum(),
                    "heal_cost": data.heal_cost.sum(),
                    "profit": round(data.profit.sum(), 2),
                    "my_dice": round(data.my_dice.mean(), 2),
                    "enemy_dice": round(data.enemy_dice.mean(), 2),
                },
                ignore_index=True,
            )
        return df_grouped

    return df_total


def calculate_heal_cost(max_energy, energy):
    heal_cost = 0
    if max_energy <= 0:
        heal_cost, max_energy = Land.heal_cost, Land.max_energy
    max_energy -= energy
    return max_energy, heal_cost


def get_hero_diff(
        my_defense_bonus: float,
        my_attack_bonus: float,
        enemy_defense_bonus: float,
        hero: str,
        mean: bool = False,
        sum: bool = False,
        limits: tuple = (20, 30),
        column: str = 'goldz',
        key: str = "rarity",
        pk: str = "day",
        columns=["usual", "unusual", "rare", "epic"],
        games: int = 100,
):
    if not mean and not sum:
        raise BaseException("Mean and Sum empty")

    df = simulation(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        group=False,
        games=games,
    )
    df['profit'] = df['goldz'] + (df['energy'] / Land.max_energy) * 10
    df1 = simulation(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero=hero,
        rarity="usual",
        group=False,
        games=games,
    )
    df1['profit'] = df1['goldz'] + (df1['energy'] / Land.max_energy) * 10

    df2 = simulation(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero=hero,
        rarity="unusual",
        group=False,
        games=games,
    )
    df2['profit'] = df2['goldz'] + (df2['energy'] / Land.max_energy) * 10

    df3 = simulation(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero=hero,
        rarity="rare",
        group=False,
        games=games,
    )
    df3['profit'] = df3['goldz'] + (df3['energy'] / Land.max_energy) * 10

    df4 = simulation(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero=hero,
        rarity="epic",
        group=False,
        games=games,
    )
    df4['profit'] = df4['goldz'] + (df4['energy'] / Land.max_energy) / 10

    df_hero = merge_dfs(
        dfs=[df, df1, df2, df3, df4], column=column, pk=pk, limits=limits
    )

    df_hero = get_diff(df=df_hero)

    if sum:
        df_hero = get_df_columns_sum(df_hero, columns)
    if mean:
        df_hero = get_df_columns_mean(df_hero, columns)
    return pd.DataFrame({key: df_hero.columns, hero: df_hero.iloc[0].to_list()})


def plot_heroes_sum_diff(
        my_defense_bonus: float,
        my_attack_bonus: float,
        enemy_defense_bonus: float,
        label: str,
        games: int = 100,
        column: str = 'goldz'
):
    df_urzog_sum = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="urzog",
        sum=True,
        games=games,
        column=column
    )
    df_dicez_sum = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="dicez",
        sum=True,
        games=games,
        column=column
    )
    df_lyz_sum = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="lyz",
        sum=True,
        games=games,
        column=column
    )

    df_vampirao_sum = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="vampirao",
        sum=True,
        games=games,
        column=column
    )
    df_kongz_sum = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="kongz",
        sum=True,
        games=games,
        column=column
    )
    df_etherman_sum = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="etherman",
        sum=True,
        games=games,
        column=column
    )
    df = pd.concat(
        [

            df_urzog_sum.set_index("rarity"),
            df_dicez_sum.set_index("rarity"),
            df_kongz_sum.set_index("rarity"),
            df_etherman_sum.set_index("rarity"),
            df_lyz_sum.set_index("rarity"),
            df_vampirao_sum.set_index("rarity"),
        ],
        axis=1,
    )
    ax = df.plot.bar(figsize=(20, 10))
    for container in ax.containers:
        ax.bar_label(container, fontsize=20)
    plt.xticks(rotation=0, fontsize=30)
    plt.title(label, fontsize=30)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=20)
    plt.show()
    return df


def plot_heroes_mean_diff(
        my_defense_bonus: float,
        my_attack_bonus: float,
        enemy_defense_bonus: float,
        label: str,
        games: int = 100,
        column: str = 'goldz'
):
    df_urzog_mean = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="urzog",
        mean=True,
        games=games,
        column=column
    )
    df_dicez_mean = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="dicez",
        mean=True,
        games=games,
        column=column
    )
    df_lyz_mean = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="lyz",
        mean=True,
        games=games,
        column=column
    )

    df_vampirao_mean = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="vampirao",
        mean=True,
        games=games,
        column=column
    )
    df_kongz_mean = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="kongz",
        mean=True,
        games=games,
        column=column
    )
    df_etherman_mean = get_hero_diff(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        hero="etherman",
        mean=True,
        games=games,
        column=column
    )
    df = pd.concat(
        [
            df_dicez_mean.set_index("rarity"),
            df_urzog_mean.set_index("rarity"),
            df_kongz_mean.set_index("rarity"),
            df_lyz_mean.set_index("rarity"),
            df_etherman_mean.set_index("rarity"),
            df_vampirao_mean.set_index("rarity"),
        ],
        axis=1,
    )
    ax = df.plot.bar(figsize=(20, 10))
    for container in ax.containers:
        ax.bar_label(container, fontsize=20)

    plt.xticks(rotation=0, fontsize=30)
    plt.title(label, fontsize=30)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=20)
    plt.show()
    return df
