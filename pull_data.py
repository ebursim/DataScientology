import pandas as pd
import requests as req
import json
import time
import os

if not os.path.isfile("./cache"):
    r = req.get("https://api.opendota.com/api/explorer?sql=SELECT%20public_matches.match_id%20FROM%20public_matches%20WHERE%20public_matches.avg_mmr%20%3E%205500%20AND%20public_matches.lobby_type%20IN%20(5,6,7)%20AND%20public_matches.game_mode=22%20limit%20100000").text
    parsed = json.loads(r)["rows"]
    match_ids = list(map(lambda obj : obj["match_id"], parsed))

    dfs = []

    i = 1
    for match_id in match_ids:
        print(f"Match: {i}")
        i += 1
        while True:
            time.sleep(1.5)
            r = req.get('https://api.opendota.com/api/matches/' + str(match_id))
            if r.status_code != 200:
                continue
            dmr = json.loads(r.text)
            if "players" in dmr:
                pdata = dmr['players']
                dfs.append(pd.DataFrame(pdata))
                break
            else:
                continue

        if i % 100 == 0:
            if not os.path.isfile("./cache"):
                data_out = pd.concat(dfs, ignore_index=True, join="inner", sort=False).to_csv()
                cache = open("cache", "w", encoding="utf-8")
                cache.write(data_out)
                cache.close()
            else:
                data_out = pd.concat([pd.read_csv("./cache")] + dfs, ignore_index=True, join="inner", sort=False).to_csv()
                cache = open("cache", "w", encoding="utf-8")
                cache.write(data_out)
                cache.close()
            dfs.clear()

    if not os.path.isfile("./cache"):
        data_out = pd.concat(dfs, ignore_index=True, join="inner", sort=False).to_csv()
        cache = open("cache", "w", encoding="utf-8")
        cache.write(data_out)
        cache.close()
    else:
        data_out = pd.concat([pd.read_csv("./cache")] + dfs, ignore_index=True, join="inner", sort=False).to_csv()
        cache = open("cache", "w", encoding="utf-8")
        cache.write(data_out)
        cache.close()

data = pd.read_csv("./cache")