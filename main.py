import warnings

from utils.fc import simulation

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    x = simulation(
        my_defense_bonus=0,
        my_attack_bonus=65,
        enemy_defense_bonus=13.8,
        hero="tanker",
        rarity="epic",
        group=False
    )
    print(x)
