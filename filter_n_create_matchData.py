import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


data = json.load(open("small-cache2","r"))
match_data = pd.DataFrame()


variable_list = ['WardCount','CampStack','Denies','THeroDmg','THeroHeal','RegItemUse','TLaneEff', 'TPings', 'TDeaths' , 'TKills', 'TGPM', 'TXPM', 'Win']
#dset = pd.DataFrame(dset, columns=['matchID'])
match_data = pd.DataFrame(columns=variable_list)

#for i in range(len(dset)):
#    match_req = req.get('https://api.opendota.com/api/publicMatches/'+dset['matchID'][i])

#mr = req.get('https://api.opendota.com/api/matches/5051327209').text
#dmr = json.loads(mr)
W_APM=W_WardCount=W_CampStack=W_Denies=W_THeroDmg=W_THeroHeal=W_RegItemUse=W_TLaneEff = W_Pings = W_Deaths = W_Kills = W_TGPM = W_TXPM = 0
L_APM=L_WardCount=L_CampStack=L_Denies=L_THeroDmg=L_THeroHeal=L_RegItemUse=L_TLaneEff = L_Pings = L_Deaths = L_Kills = W_TGPM = W_TXPM = 0

def sum_regits(pdata):
    sum = 0
    if 'tango' in pdata:
        sum += pdata['tango']
    if 'clarity' in pdata:
        sum += pdata['clarity']
    if 'flask' in pdata:
        sum += pdata['flask']
    if 'enchanted_mango' in pdata:
        sum += pdata['enchanted_mango']
    return sum
def sum_wards(pdata):
    sum = 0
    if 'obs_placed' in pdata:
        sum += pdata['obs_placed']
    if 'sen_placed' in pdata:
        sum += pdata['sen_placed']
    return sum

#def check_exist(pdata):
#    return pdata['lane_efficiency'] if pdata['lane_efficiency'] in pdata else break


def pparam_from_match(dmr, match_data):
    W_WardCount=W_CampStack=W_Denies=W_THeroDmg=W_THeroHeal=W_RegItemUse=W_TLaneEff = W_Pings = W_Deaths = W_Kills = W_TGPM = W_TXPM = 0
    L_WardCount=L_CampStack=L_Denies=L_THeroDmg=L_THeroHeal=L_RegItemUse=L_TLaneEff = L_Pings = L_Deaths = L_Kills = L_TGPM = L_TXPM = 0
    for i in range(len(dmr['players'])):
        if dmr['players'][i]['win'] == 1:
            minutes = float(dmr['duration']/60)
#            W_APM += dmr['players'][i]['actions_per_min']
            W_WardCount += float(dmr['players'][i]['obs_placed']+dmr['players'][i]['sen_placed'])/minutes
            W_CampStack += float(dmr['players'][i]['camps_stacked'])/minutes
            W_Denies += float(dmr['players'][i]['denies'])/minutes
            W_THeroDmg += float(dmr['players'][i]['hero_damage'])/minutes
            W_THeroHeal += float(dmr['players'][i]['hero_healing'])/minutes
            W_RegItemUse += float(sum_regits(dmr['players'][i]['item_uses']))/minutes
            W_TLaneEff += dmr['players'][i]['lane_efficiency']
            W_Pings += float(dmr['players'][i]['pings'])/minutes
            W_Deaths += float(dmr['players'][i]['deaths'])/minutes
            W_Kills += float(dmr['players'][i]['kills'])/minutes
            W_TGPM += float(dmr['players'][i]['total_gold'])/minutes
            W_TXPM += float(dmr['players'][i]['total_xp'])/minutes
        if dmr['players'][i]['win'] == 0:
            minutes = float(dmr['duration']/60)
#            L_APM += dmr['players'][i]['actions_per_min']
            L_WardCount += float(dmr['players'][i]['obs_placed']+dmr['players'][i]['sen_placed'])/minutes
            L_CampStack += float(dmr['players'][i]['camps_stacked'])/minutes
            L_Denies += float(dmr['players'][i]['denies'])/minutes
            L_THeroDmg += float(dmr['players'][i]['hero_damage'])/minutes
            L_THeroHeal += float(dmr['players'][i]['hero_healing'])/minutes
            L_RegItemUse += float(sum_regits(dmr['players'][i]['item_uses']))/minutes
            L_TLaneEff += dmr['players'][i]['lane_efficiency']
            L_Pings += float(dmr['players'][i]['pings'])/minutes
            L_Deaths += float(dmr['players'][i]['deaths'])/minutes
            L_Kills += float(dmr['players'][i]['kills'])/minutes
            L_TGPM += float(dmr['players'][i]['total_gold'])/minutes
            L_TXPM += float(dmr['players'][i]['total_xp'])/minutes

    wmd = pd.DataFrame([[ W_WardCount, W_CampStack, W_Denies, W_THeroDmg, W_THeroHeal, W_RegItemUse, W_TLaneEff, W_Pings, W_Deaths, W_Kills, W_TGPM, W_TXPM,  1]], columns=['WardCount','CampStack','Denies','THeroDmg','THeroHeal','RegItemUse','TLaneEff', 'TPings', 'TDeaths', 'TKills', 'TGPM', 'TXPM', 'Win'])
    lmd = pd.DataFrame([[ L_WardCount, L_CampStack, L_Denies, L_THeroDmg, L_THeroHeal, L_RegItemUse, L_TLaneEff, L_Pings, L_Deaths, L_Kills, L_TGPM, L_TXPM, 0]], columns=['WardCount','CampStack','Denies','THeroDmg','THeroHeal','RegItemUse','TLaneEff', 'TPings', 'TDeaths', 'TKills', 'TGPM', 'TXPM', 'Win'])
    match_data = match_data.append(wmd)
    match_data = match_data.append(lmd)
    return match_data

i = 0
match_data = pd.DataFrame(columns=variable_list)

while i < len(data):
    dmr = data[i]
    pdata = dmr["players"]
    nullvaluecheck = []
    for j in range(10): ##Reason for this checks are because I realized data is not that clean. There are many occasions where these values are NONE rather than 0.
        checklist = [pdata[j].get('obs_placed'), pdata[j].get('sen_placed'), pdata[j].get('camps_stacked'), pdata[j].get('denies'), pdata[j].get('hero_damage'), pdata[j].get('hero_healing'), pdata[j].get('deaths'), pdata[j].get('kills'), pdata[j].get('pings'), pdata[j].get('total_gold'), pdata[j].get('total_xp'), pdata[j].get('lane_efficiency'), sum_regits(pdata[j])]
        print(i)
        if all(x for x in checklist if x is None):
            nullvaluecheck.append(1)
        else:
            nullvaluecheck.append(0)
    if 0 in nullvaluecheck:
        i+=1
        print('There are NONE values, skipping matchID')
    else:
        match_data = pparam_from_match(dmr, match_data)
        i+=1

match_data.to_csv('filtered_match_data20k.csv', index=False)
