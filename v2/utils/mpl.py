import pandas as pd
from matplotlib import pyplot as plt

from .fc import merge_dfs
from .models import NoHero, Godjira, Yokai, Urzog, Lyz, Etherman, Creepz, BabyDragon, MAX_ENERGY

RARITYS = ['common', 'uncommon', 'rare', 'epic']


def plot_heroes_total_goldz_by_rarity(my_defense_bonus: float = 13.8,
                                      my_attack_bonus: float = 0,
                                      label: str = "",
                                      games: int = 500,
                                      ):  # sourcery no-metrics
    df = df_no_hero = df_godjira = df_yokai = df_cyber_kongz = df_lyz = df_etherman = df_creepz = df_baby_dragon = pd.DataFrame()
    for rarity in RARITYS:
        for _ in range(games):
            no_hero = NoHero(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus)
            godjira = Godjira(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            yokai = Yokai(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            urzog = Urzog(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            lyz = Lyz(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            etherman = Etherman(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            creepz = Creepz(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            baby_dragon = BabyDragon(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)

            while no_hero.day < 6:
                no_hero.battle()
                godjira.battle()
                yokai.battle()
                urzog.battle()
                lyz.battle()
                etherman.battle()
                baby_dragon.battle()

            while creepz.day < 6:
                if creepz.charges > 0:
                    creepz.battle()
                else:
                    new_no_hero = NoHero(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus)
                    new_no_hero.battle()
                    creepz.attacks -= 1
                    creepz.qtd_attacks += 1
                    creepz.goldz += new_no_hero.goldz
                    creepz.energy -= MAX_ENERGY - new_no_hero.energy
                    creepz.wait_a_day()

            df_no_hero = df_no_hero.append([no_hero])
            df_godjira = df_godjira.append([godjira])
            df_yokai = df_yokai.append([yokai])
            df_cyber_kongz = df_cyber_kongz.append([urzog])
            df_etherman = df_etherman.append([etherman])
            df_lyz = df_lyz.append([lyz])
            df_creepz = df_creepz.append([creepz])
            df_baby_dragon = df_baby_dragon.append([baby_dragon])

        dfs = [df_no_hero, df_godjira, df_yokai, df_cyber_kongz, df_etherman, df_lyz, df_creepz, df_baby_dragon]
        names = ["no_hero", 'godjira', 'yokai', 'urzog', 'etherman', 'lyz', 'creepz', 'baby_dragon']
        df_goldz = merge_dfs(column='goldz', dfs=dfs, names=names).mean().rename_axis('goldz')
        df_energy = merge_dfs(column='energy', dfs=dfs, names=names).mean().rename_axis('energy')

        # df_profit = pd.Series(
        #     [df_goldz.godjira + ((df_energy.godjira - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
        #      df_goldz.yokai + ((df_energy.yokai - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
        #      df_goldz.urzog + ((df_energy.urzog - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
        #      df_goldz.etherman + ((df_energy.etherman - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
        #      df_goldz.lyz + ((df_energy.lyz - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
        #      df_goldz.baby_dragon + ((df_energy.baby_dragon - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
        #      df_goldz.creepz + ((df_energy.creepz - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
        #      ],
        #     index=['Godjira', 'Yokai', 'Urzog', 'Etherman', 'Lyz', 'Baby Dragon', 'Creepz'])
        # df = df.append(pd.concat([df_profit], keys=[rarity], axis=1).T)

        df_profit = pd.Series(
            [df_goldz.no_hero,
             df_goldz.godjira + ((df_energy.godjira - df_energy.no_hero) / 100 * 2),
             df_goldz.yokai + ((df_energy.yokai - df_energy.no_hero) / 100 * 2),
             df_goldz.urzog + ((df_energy.urzog - df_energy.no_hero) / 100 * 2),
             df_goldz.etherman + ((df_energy.etherman - df_energy.no_hero) / 100 * 2),
             df_goldz.lyz + ((df_energy.lyz - df_energy.no_hero) / 100 * 2),
             df_goldz.baby_dragon + ((df_energy.baby_dragon - df_energy.no_hero) / 100 * 2),
             df_goldz.creepz + ((df_energy.creepz - df_energy.no_hero) / 100 * 2),
             ],
            index=['No Hero','Godjira', 'Yokai', 'Urzog', 'Etherman', 'Lyz', 'Baby Dragon', 'Creepz'])
        df = df.append(pd.concat([df_profit], keys=[rarity], axis=1).T)

    ax = df.plot.bar(figsize=(20, 10))
    for container in ax.containers:
        ax.bar_label(container, fontsize=20)


    plt.xticks(rotation=0, fontsize=30)
    # plt.yticks(color='w')
    plt.title(label, fontsize=30)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=20)
    plt.show()
    return df


def plot_heroes_goldz_by_rarity(my_defense_bonus: float = 13.8,
                                my_attack_bonus: float = 0,
                                label: str = "",
                                games: int = 500,
                                ):  # sourcery no-metrics
    df = df_no_hero = df_godjira = df_yokai = df_cyber_kongz = df_lyz = df_etherman = df_creepz = pd.DataFrame()
    for rarity in RARITYS:
        for _ in range(games):
            no_hero = NoHero(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus)
            godjira = Godjira(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            yokai = Yokai(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            urzog = Urzog(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            lyz = Lyz(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            etherman = Etherman(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)
            creepz = Creepz(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus, rarity=rarity)

            while no_hero.day < 6:
                no_hero.battle()
                godjira.battle()
                yokai.battle()
                urzog.battle()
                lyz.battle()
                etherman.battle()

            while creepz.day < 6:
                if creepz.charges > 0:
                    creepz.battle()
                else:
                    new_no_hero = NoHero(attack_bonus=my_attack_bonus, defense_bonus=my_defense_bonus)
                    new_no_hero.battle()
                    creepz.attacks -= 1
                    creepz.qtd_attacks += 1
                    creepz.goldz += new_no_hero.goldz
                    creepz.energy -= MAX_ENERGY - new_no_hero.energy
                    creepz.wait_a_day()

            df_no_hero = df_no_hero.append([no_hero])
            df_godjira = df_godjira.append([godjira])
            df_yokai = df_yokai.append([yokai])
            df_cyber_kongz = df_cyber_kongz.append([urzog])
            df_etherman = df_etherman.append([etherman])
            df_lyz = df_lyz.append([lyz])
            df_creepz = df_creepz.append([creepz])

        dfs = [df_no_hero, df_godjira, df_yokai, df_cyber_kongz, df_etherman, df_lyz, df_creepz]
        names = ["no_hero", 'godjira', 'yokai', 'urzog', 'etherman', 'lyz', 'creepz']
        df_goldz = merge_dfs(column='goldz', dfs=dfs, names=names).mean().rename_axis('goldz')

        df_profit = pd.Series(
            [df_goldz.godjira - df_goldz.no_hero,
             df_goldz.yokai - df_goldz.no_hero,
             df_goldz.urzog - df_goldz.no_hero,
             df_goldz.creepz - df_goldz.no_hero,
             ],
            index=['godjira', 'yokai', 'urzog', 'creepz'])
        df = df.append(pd.concat([df_profit], keys=[rarity], axis=1).T)

    ax = df.plot.bar(figsize=(20, 10))
    for container in ax.containers:
        ax.bar_label(container, fontsize=20)

    plt.xticks(rotation=0, fontsize=30)
    plt.title(label, fontsize=30)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=20)
    plt.show()
    return df
