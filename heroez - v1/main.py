import warnings

import pandas as pd

from utils.fc import get_hero_diff, simulation
from utils.mpl import plot_heroes_diff

warnings.filterwarnings("ignore")


def get_diff(
    df: pd.DataFrame,
    column: str,
    names=["no_hero", "common", "uncommon", "rare", "epic"],
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
    # y = plot_heroes_sum_diff(0,0,0,'')
    # x = get_hero_diff(sum=True)

    # )
    y = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="kongz",
        rarity="epic",
        group=False,
    )
    # print(x)
