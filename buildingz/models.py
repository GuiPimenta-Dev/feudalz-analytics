from dataclasses import dataclass
from random import choice

import pandas as pd

HOLDERS = 1225
LANDZ_MINTED = 4071
LAND_ID = 0


@dataclass
class Land:
    id: int
    attacks_received: int = 0
    attacks = 2


@dataclass
class Player:
    id: int
    total_of_landz: int
    landz = []
    landz_ids = []
    total_attacks_received: int = 0

    def __init__(self, id, landz, landz_ids):
        self.id = id
        self.landz = landz
        self.landz_ids = landz_ids
        self.total_of_landz = len(landz_ids)


players = []
for i in range(HOLDERS):
    if i <= 25:
        NUMBER_OF_LANDZ = 35
    elif 25 < i <= 50:
        NUMBER_OF_LANDZ = 25
    elif 50 < i <= 200:
        NUMBER_OF_LANDZ = 8
    elif 200 < i <= 512:
        NUMBER_OF_LANDZ = 2
    else:
        NUMBER_OF_LANDZ = 1
        if LANDZ_MINTED <= 0:
            break
    LANDZ_MINTED -= NUMBER_OF_LANDZ
    landz = []
    landz_ids = []
    for _ in range(NUMBER_OF_LANDZ):
        LAND_ID += 1
        landz_ids.append(LAND_ID)
        landz.append(Land(id=LAND_ID))
    players.append(Player(id=i, landz=landz, landz_ids=landz_ids))

for player in players:
    for land in player.landz:
        for _ in range(land.attacks):
            target_player = choice([i for i in range(len(players)) if i not in player.landz_ids])
            players[target_player].total_attacks_received += 1
            target_land = choice(players[target_player].landz_ids)
            for land in players[target_player].landz:
                if land.id == target_land:
                    land.attacks_received += 1

df = pd.DataFrame(players)
for i in df.groupby('total_of_landz'):
    print(
        f'Total of Landz: {i[0]} - Attacks Received: {(i[1].total_attacks_received.mean())}')
