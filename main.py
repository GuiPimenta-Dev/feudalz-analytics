import warnings
from typing import List

import pandas as pd

from utils.fc import simulation, merge_dfs

warnings.filterwarnings("ignore")


def get_diff(
    df: pd.DataFrame,
    column: str,
    names=["no_hero", "usual", "unusual", "rare", "epic"],
    column_names=["usual_diff", "unusual_diff", "rare_diff", "epic_diff"],
    pk: str = "day",
):
    df2 = pd.DataFrame()
    if pk:
        df2[pk] = df[pk]
    for index, name in enumerate(names):
        if index < len(column_names):
            df2[column_names[index]] = df[names[index + 1]] - df[column]

    return df2


if __name__ == "__main__":
    # df = simulation(
    #     my_defense_bonus=0, my_attack_bonus=65, enemy_defense_bonus=13.8, group=False
    # )
    # df1 = simulation(
    #     my_defense_bonus=0,
    #     my_attack_bonus=65,
    #     enemy_defense_bonus=13.8,
    #     hero="double",
    #     rarity="usual",
    #     group=False,
    # )
    # df2 = simulation(
    #     my_defense_bonus=0,
    #     my_attack_bonus=65,
    #     enemy_defense_bonus=13.8,
    #     hero="kongz",
    #     rarity="unusual",
    #     group=False,
    # )
    # df3 = simulation(
    #     my_defense_bonus=0,
    #     my_attack_bonus=65,
    #     enemy_defense_bonus=13.8,
    #     hero="kongz",
    #     rarity="rare",
    #     group=False,
    # )
    # df4 = simulation(
    #     my_defense_bonus=0,
    #     my_attack_bonus=65,
    #     enemy_defense_bonus=13.8,
    #     hero="kongz",
    #     rarity="epic",
    #     group=False,
    # )

    df = simulation(
        my_defense_bonus=0, my_attack_bonus=65, enemy_defense_bonus=13.8, group=False
    )
    df1 = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="urzog",
        rarity="usual",
        group=False,
    )
    df2 = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="urzog",
        rarity="unusual",
        group=False,
    )
    df3 = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="urzog",
        rarity="rare",
        group=False,
    )
    df4 = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="urzog",
        rarity="epic",
        group=False,
    )
    df = merge_dfs(
        dfs=[df, df1, df2, df3, df4],
        column="goldz",
        names=["no_hero", "usual", "unusual", "rare", "epic"],
        pk="day",
        limits=(20, 30),
    )

    df = get_diff(df=df, column="no_hero")
    pass
# x = simulation(
#     my_defense_bonus=0,
#     my_attack_bonus=0,
#     enemy_defense_bonus=13.8,
#     group=False,
# )
# y = simulation(
#     my_defense_bonus=0,
#     my_attack_bonus=65,
#     enemy_defense_bonus=13.8,
#     hero="urzog",
#     rarity="epic",
#     group=False,
#     games=1
# )
# print(x)
