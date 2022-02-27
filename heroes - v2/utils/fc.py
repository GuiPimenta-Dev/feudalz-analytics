import warnings
from typing import List

import pandas as pd

warnings.filterwarnings("ignore")


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
