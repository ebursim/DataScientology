import os
import json
import pandas as pd

#file_list = []
#for file in os.listdir("./data"):
#    if file.endswith(".txt"):
#        file_list.append(json.load(open(file, encoding="utf-8")))
#with open("./data/cache", "w") as cache:
#    json.dump(file_list, cache)

data = json.load(open("./small-cache", "r", encoding="utf-8"))

# json.dump(data[:20000], open("./small-cache", "w", encoding="utf-8"))

w_m = {}
l_m = {}

row_id = 1

for row in data:

    print(f"Row {row_id} of {len(data)} rows")

    if row["chat"] == None:
        continue

    chat_data = pd.read_json(json.dumps(row["chat"]))
    if "unit" not in chat_data:
        continue

    chat_data.query("unit == unit")
    players = pd.read_json(json.dumps(row["players"]))
    won_names = players.query("win == 1")["personaname"]
    lost_names = players.query("win == 0")["personaname"]
    won_messages = chat_data[chat_data["unit"].isin(won_names)]["key"].map(lambda word : str(word).lower())
    lost_messages = chat_data[chat_data["unit"].isin(lost_names)]["key"].map(lambda word : str(word).lower())

    for x in (val for msg in won_messages for val in msg.split(" ") if len(val) >= 2 and not val.isdigit()):
        if x in w_m:
            w_m[x] += 1
        else:
            w_m[x] = 1

    for x in (val for msg in lost_messages for val in msg.split(" ") if len(val) >= 2 and not val.isdigit()):
        if x in l_m:
            l_m[x] += 1
        else:
            l_m[x] = 1
    
    row_id += 1

w_f = open("won_words.txt", "w", encoding="utf-8")
l_f = open("lost_words.txt", "w", encoding="utf-8")

w_m = sorted(((value, key) for (key,value) in w_m.items()), reverse=True)
l_m = sorted(((value, key) for (key,value) in l_m.items()), reverse=True)

w_f.write("\n".join(map(lambda val : f"{val[1]} - {val[0]}", w_m)))
l_f.write("\n".join(map(lambda val : f"{val[1]} - {val[0]}", l_m)))

w_f.close()
l_f.close()