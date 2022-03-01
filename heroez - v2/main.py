import warnings
import pandas as pd
from models import NoHero, Godjira, Yokai, CyberKongz, Lyz, Etherman, Creepz, MAX_ENERGY
from utils.fc import merge_dfs

warnings.filterwarnings("ignore")
ATTACK_BONUS = 65
DEFENSE_BONUS = 23.8

if __name__ == "__main__":

    df_no_hero = df_godjira = df_yokai = df_cyber_kongz = df_lyz = df_etherman = df_creepz = pd.DataFrame()

    for _ in range(6000):
        no_hero = NoHero(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS)
        godjira = Godjira(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity='epic')
        yokai = Yokai(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity='epic')
        cyber_kongz = CyberKongz(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity='epic')
        lyz = Lyz(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity='epic')
        etherman = Etherman(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity='epic')
        creepz = Creepz(attack_bonus=ATTACK_BONUS, defense_bonus=DEFENSE_BONUS, rarity='epic')

        while no_hero.day < 6:
            no_hero.battle()
            godjira.battle()
            yokai.battle()
            cyber_kongz.battle()
            lyz.battle()
            etherman.battle()

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
        df_cyber_kongz = df_cyber_kongz.append([cyber_kongz])
        df_etherman = df_etherman.append([etherman])
        df_lyz = df_lyz.append([lyz])
        df_creepz = df_creepz.append([creepz])

    dfs = [df_no_hero, df_godjira, df_yokai, df_cyber_kongz, df_etherman, df_lyz, df_creepz]
    names = ["no_hero", 'godjira', 'yokai', 'cyber_kongz', 'etherman', 'lyz', 'creepz']
    df_goldz = merge_dfs(column='goldz', dfs=dfs, names=names).mean().rename_axis('goldz')
    df_energy = merge_dfs(column='energy', dfs=dfs, names=names).mean().rename_axis('energy')
    df_qtd_attacks = merge_dfs(column='qtd_attacks', dfs=dfs, names=names).mean().rename_axis('number_of_attacks')
    df = pd.concat([df_goldz, df_energy, df_qtd_attacks], keys=['goldz', 'remaining_energy', 'number_of_attacks'], axis=1).T
    print(df)
