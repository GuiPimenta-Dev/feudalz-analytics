import warnings

from typing import List

import matplotlib.pyplot as plt
import pandas as pd

from utils.fc import simulation, merge_dfs, get_df_columns_sum, get_hero_diff


def plot_scatter(x, y, offset: tuple = (0, 10), decimal: int = 2):
    for x, y in zip(x, y):
        plt.annotate(
            round(y, decimal),
            (x, y),
            textcoords="offset points",
            xytext=offset,
            ha="center",
        )


def plot_line_with_scatter(
    ax: plt.subplots,
    df: pd.DataFrame,
    x: str,
    y: List[str],
    labels: List = ["Epic", "Rare", "Unusual", "Usual"],
    offset: tuple = (0, 10),
    mean: bool = False,
    sum: bool = False,
    decimal: int = 2,
):
    for index, item in enumerate(y):
        if mean:
            ax.plot(
                df[x],
                df[item],
                marker="o",
                label=f"{labels[index]} = {round(df[item].mean(), decimal)}",
            )
        elif sum:
            ax.plot(
                df[x],
                df[item],
                marker="o",
                label=f"{labels[index]} = {round(df[item].sum(), decimal)}",
            )
        else:
            ax.plot(df[x], df[item], marker="o", label=f"{labels[index]}")

        plot_scatter(df[x], df[item], offset=offset)


def plot_bar_with_scatter(
    ax: plt.subplots,
    df: pd.DataFrame,
    x: str,
    y: List[str],
    offset: tuple = (0, 10),
    mean: bool = False,
    sum: bool = False,
    decimal: int = 2,
):
    for item in y:
        if mean:
            ax.plot(
                df[x],
                df[item],
                marker="o",
                label=f"{item.capitalize()} = {round(df[item].mean(), decimal)}",
            )
        elif sum:
            ax.plot(
                df[x],
                df[item],
                marker="o",
                label=f"{item.capitalize()} = {round(df[item].sum(), decimal)}",
            )
        else:
            ax.plot(df[x], df[item], marker="o", label=f"{item.capitalize()}")

        plot_scatter(df[x], df[item], offset=offset)


def plot_no_hero_and_heroes_goldz_average(
    my_defense_bonus: float = 0,
    my_attack_bonus: float = 0,
    enemy_defense_bonus: float = 13.8,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    colors=["black", "red", "green", "blue", "cyan"],
    bars=["No Hero", "Common", "Uncommon", "Rare", "Epic"],
    heroes=["dicez", "urzog", "kongz", "etherman"],
    raritys=["common", "uncommon", "rare", "epic"],
    games: int = 500,
):
    df = simulation(
        my_defense_bonus=my_defense_bonus,
        my_attack_bonus=my_attack_bonus,
        enemy_defense_bonus=enemy_defense_bonus,
        group=False,
        games=games,
    )

    dfs = []
    df_heroes = []

    for hero in heroes:
        dfs.append(df)
        for rarity in raritys:
            dfs.append(
                simulation(
                    my_defense_bonus=my_defense_bonus,
                    my_attack_bonus=my_attack_bonus,
                    enemy_defense_bonus=enemy_defense_bonus,
                    hero=hero,
                    rarity=rarity,
                    group=False,
                )
            )

        df_heroes.append(merge_dfs(dfs=dfs, column="goldz", pk="day"))
        # df_heroes.append(merge_dfs(dfs=dfs, column='goldz', pk='day', limits=(20, 30)))
        dfs = []

    heroes = {}
    for i in df_heroes:
        for j in i.columns[1:]:
            heroes[j] = 0

    for i in df_heroes:
        for j in i.columns[1:]:
            heroes[j] += i[j].sum() / len(heroes)

    df = pd.DataFrame.from_dict(heroes, orient="index").T

    height = df.iloc[0].to_list()

    fig, ax = plt.subplots(figsize=(16, 9))

    plt.bar(bars, height, color=colors, width=0.4)

    for container in ax.containers:
        ax.bar_label(container, fontsize=20)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
    return df


def plot_heroes_diff(
    my_defense_bonus: float = 13.8,
    my_attack_bonus: float = 0,
    enemy_defense_bonus: float = 13.8,
    label: str = "",
    games: int = 500,
    column: str = "goldz",
    mean=False,
    sum=False,
    heroes=["dicez", "urzog", "kongz", "etherman", "lyz", "vampirao"],
    index="rarity",
):
    if not mean and not sum:
        raise BaseException("Mean and Sum empty")

    df_heroes = [
        get_hero_diff(
            my_defense_bonus=my_defense_bonus,
            my_attack_bonus=my_attack_bonus,
            enemy_defense_bonus=enemy_defense_bonus,
            hero=hero,
            mean=mean,
            sum=sum,
            games=games,
            column=column,
        ).set_index(index)
        for hero in heroes
    ]
    df = pd.concat(
        df_heroes,
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
