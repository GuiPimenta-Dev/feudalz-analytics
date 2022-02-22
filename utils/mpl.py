from typing import List

import matplotlib.pyplot as plt
import pandas as pd


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
