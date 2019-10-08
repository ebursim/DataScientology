import pandas as pd
import requests as req
import json
import os
import matplotlib.pyplot as plot
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split

data = pd.read_csv("./cache")

heroes = pd.read_json("./heroes.json")

for column in data.columns:
    print(column)

faction_column, faction_labels = data["isRadiant"].map(lambda val : "Radiant" if val == True else "Dire").factorize()

data["faction"] = faction_column

data = data[["match_id", "win", "hero_id", "faction", "radiant_win"]]

for hero_index in heroes.columns:
    data[f"radiant_hero_{hero_index}"] = 0
    data[f"dire_hero_{hero_index}"] = 0

for match_id in data["match_id"].unique():
    all_heroes = data.query(f"match_id == {match_id}")
    radiant_heroes = all_heroes.query("faction == 0")["hero_id"]
    dire_heroes = all_heroes.query(f"faction == 1")["hero_id"]

    for index in all_heroes.index:
        for hero_index in range(0, 5):
            data.at[index, f"radiant_hero_{radiant_heroes.iloc[hero_index]}"] = 1
            data.at[index, f"dire_hero_{dire_heroes.iloc[hero_index]}"] = 1

data = data.groupby("match_id").first().reset_index().drop("match_id", axis = 1)

target_variable = data["radiant_win"]

data.drop(["faction", "hero_id", "radiant_win"], axis = 1, inplace = True)

x_train, x_test, y_train, y_test = train_test_split(data, target_variable, test_size=0.2)

tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2)
tpot.fit(x_train, y_train)
print(tpot.score(x_test, y_test))