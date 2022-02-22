import warnings
from typing import List

import pandas as pd

from utils.fc import simulation

warnings.filterwarnings("ignore")


def merge_dfs(column: str, names: List, dfs: List, pk: str = None):
    df_merged = pd.DataFrame()

    if pk:
        df_merged[pk] = dfs[0][pk]

    for index, df in enumerate(dfs):
        df_merged[names[index]] = df[column]
    return df_merged


if __name__ == "__main__":
    df = simulation(
        my_defense_bonus=0, my_attack_bonus=65, enemy_defense_bonus=13.8, group=False
    )
    df1 = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="kongz",
        rarity="usual",
        group=False,
    )
    df2 = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="kongz",
        rarity="unusual",
        group=False,
    )
    df3 = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="kongz",
        rarity="rare",
        group=False,
    )
    df4 = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="kongz",
        rarity="epic",
        group=False,
    )

    #
    # names = ['No Hero', 'Usual', 'Unusual', 'Rare', 'Epic']
    # df = df.rename(columns={'goldz': 'No Hero'})
    # df = df.rename(columns={'goldz': 'No Hero'})
    # df = df.rename(columns={'goldz': 'No Hero'})
    # df = df.rename(columns={'goldz': 'No Hero'})
    # df = df.rename(columns={'goldz': 'No Hero'})
    # pd.concat([df, df1, df2, df3, df4])[['day', 'No Hero', 'Unusual', 'Rare', 'Epic']]
    df = merge_dfs(
        "goldz",
        ["No Hero", "Usual", "Unusual", "Rare", "Epic"],
        [df, df1, df2, df3, df4],
        pk="day",
    )
    x = simulation(
        my_defense_bonus=0,
        my_attack_bonus=0,
        enemy_defense_bonus=13.8,
        hero="urzog",
        rarity="epic",
        group=True,
    )
    print(x)
