import warnings

import pandas as pd

from utils.models import NoHero, Godjira, Yokai, Urzog, Lyz, Etherman, Creepz, BabyDragon
from v2.utils.fc import merge_dfs

warnings.filterwarnings("ignore")
ATTACK_BONUS = 0
DEFENSE_BONUS = 0
RARITYS = ['common', 'uncommon', 'rare', 'epic']
MAX_ENERGY = 1000
if __name__ == "__main__":

    df = df_no_hero = df_godjira = df_yokai = df_cyber_kongz = df_lyz = df_etherman = df_creepz = df_baby_dragon= pd.DataFrame()
    for rarity in RARITYS:
        for _ in range(500):
            no_hero = NoHero(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS)
            godjira = Godjira(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity=rarity)
            yokai = Yokai(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity=rarity)
            urzog = Urzog(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity=rarity)
            lyz = Lyz(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity=rarity)
            etherman = Etherman(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity=rarity)
            creepz = Creepz(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity=rarity)
            baby_dragon = BabyDragon(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity=rarity)

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
                    new_no_hero = NoHero(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS)
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
        df_qtd_attacks = merge_dfs(column='qtd_attacks', dfs=dfs, names=names).mean().rename_axis('number_of_attacks')
        # df = pd.concat([df_goldz, df_energy, df_qtd_attacks], keys=['goldz', 'remaining_energy', 'number_of_attacks'], axis=1).T

        df_profit = pd.Series(
            [df_goldz.godjira + ((df_energy.godjira - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
             df_goldz.yokai + ((df_energy.yokai - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
             df_goldz.urzog + ((df_energy.urzog - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
             df_goldz.etherman + ((df_energy.etherman - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
             df_goldz.lyz + ((df_energy.lyz - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
             df_goldz.creepz + ((df_energy.creepz - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
             df_goldz.creepz + ((df_energy.creepz - df_energy.no_hero) / 100 * 2) - df_goldz.no_hero,
             ],
            index=['godjira', 'yokai', 'urzog', 'etherman', 'lyz', 'creepz'])
        # df = pd.concat([df_profit], keys=[rarity], axis=1).T
        df = df.append(pd.concat([df_profit], keys=[rarity], axis=1).T)

    print(df)
