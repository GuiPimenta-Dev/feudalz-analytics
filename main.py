import warnings
from typing import List

import pandas as pd

from utils.fc import simulation, merge_dfs, plot_heroes_mean_diff, plot_heroes_sum_diff

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
    x = simulation(
            my_defense_bonus=0,
            my_attack_bonus=0,
            enemy_defense_bonus=0,
            games=100,
            hero='kongz',
        rarity='epic',
            attacks= 30,
    )
    pass
    # )
    # y = simulation(
    #     my_defense_bonus=0,
    #     my_attack_bonus=65,
    #     enemy_defense_bonus=13.8,
    #     hero="etherman",
    #     rarity="epic",
    #     group=False,
    #     games=2000,
    # )
    # print(x)
