import warnings
from typing import List

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


def merge_dfs(
    column: str,
    dfs: List,
    pk: str = None,
    names=["no_hero", "common", "uncommon", "rare", "epic"],
):
    df_merged = pd.DataFrame()
    if pk:
        df_merged[pk] = dfs[0][pk]
    for index, df in enumerate(dfs):
        df_merged[names[index]] = df[column]
    return df_merged


def get_df_columns_mean(
    df: pd.DataFrame, columns=["no_hero", "common", "uncommon", "rare", "epic"]
):
    df = df[columns].mean(axis=0)
    return df.to_frame().T


def get_df_columns_sum(
    df: pd.DataFrame, columns=["no_hero", "common", "uncommon", "rare", "epic"]
):
    df = df[columns].sum(axis=0)
    return df.to_frame().T


def get_diff(
    df: pd.DataFrame,
    column: str = "no_hero",
    pk: str = "day",
    names=["no_hero", "common", "uncommon", "rare", "epic"],
    column_names=["common", "uncommon", "rare", "epic"],
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
    use: int = 0,
    hero: str = None,
    rarity: str = "common",
    games=100,
    attacks: int = 10,
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
            "my_attack_bonus",
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
        for j in i[1].groupby("attack"):
            energy = round(j[1].energy.mean(), 2)
            goldz = round(j[1].goldz.mean(), 2)
            df_total = df_total.append(
                {
                    "day": i[0],
                    "attack": j[0],
                    "energy": energy,
                    "goldz": goldz,
                    "my_attack_bonus": round(j[1].my_attack_bonus.mean(), 2),
                },
                ignore_index=True,
            )

    if group:
        df_grouped = pd.DataFrame(
            [[0, None, 0, None]],
            columns=[
                "day",
                "energy",
                "attack",
                "goldz",
            ],
        )
        for i in range(days, attacks // 2 + days, days):
            data = df_total[i - days : i]

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


def get_hero_diff(
    my_defense_bonus: float,
    my_attack_bonus: float,
    enemy_defense_bonus: float,
    hero: str,
    mean: bool = False,
    sum: bool = False,
    column: str = "goldz",
    key: str = "rarity",
    pk: str = "day",
    columns=["common", "uncommon", "rare", "epic"],
    raritys=["common", "uncommon", "rare", "epic"],
    games: int = 100,
):
    if not mean and not sum:
        raise BaseException("Mean and Sum empty")

    dfs = []
    df = simulation(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        group=False,
        games=games,
    )
    df["profit"] = df["goldz"] + (df["energy"] / Land.max_energy) * 10
    dfs.append(df)
    for rarity in raritys:
        df = simulation(
            my_defense_bonus=my_defense_bonus,
            my_attack_bonus=my_attack_bonus,
            enemy_defense_bonus=enemy_defense_bonus,
            hero=hero,
            rarity=rarity,
            group=False,
            games=games,
        )
        df["profit"] = df["goldz"] + (df["energy"] / Land.max_energy) * 10
        dfs.append(df)

    df_hero = merge_dfs(dfs=dfs, column=column, pk=pk)

    df_hero = get_diff(df=df_hero)

    if sum:
        df_hero = get_df_columns_sum(df_hero, columns)
    if mean:
        df_hero = get_df_columns_mean(df_hero, columns)
    return pd.DataFrame({key: df_hero.columns, hero: df_hero.iloc[0].to_list()})
