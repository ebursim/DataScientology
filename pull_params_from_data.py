# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import requests as req
import json
import time

N = 100
r = req.get('https://api.opendota.com/api/explorer?sql=SELECT%20public_matches.match_id%20FROM%20public_matches%20WHERE%20public_matches.avg_mmr%20%3E%205500%20AND%20public_matches.lobby_type%20IN%20(5,6,7) AND public_matches.game_mode=22%20limit%20'+str(N)).text
r = r.split('"rows"')[1]
r = r.split(',"fields"')[0]
r = r.split('[')[1].split(']')[0].split(',')

dset = list()
for line in r:
    dset.append(line.split(':')[1].split('}')[0])

variable_list = ['WardCount','CampStack','Denies','THeroDmg','THeroHeal','RegItemUse','TLaneEff', 'Win']
dset = pd.DataFrame(dset, columns=['matchID'])
match_data = pd.DataFrame(columns=variable_list)

#for i in range(len(dset)):
#    match_req = req.get('https://api.opendota.com/api/publicMatches/'+dset['matchID'][i])
    
#mr = req.get('https://api.opendota.com/api/matches/5051327209').text
#dmr = json.loads(mr)
W_APM=W_WardCount=W_CampStack=W_Denies=W_THeroDmg=W_THeroHeal=W_RegItemUse=W_TLaneEff = 0
L_APM=L_WardCount=L_CampStack=L_Denies=L_THeroDmg=L_THeroHeal=L_RegItemUse=L_TLaneEff = 0

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
    W_WardCount=W_CampStack=W_Denies=W_THeroDmg=W_THeroHeal=W_RegItemUse=W_TLaneEff = 0
    L_WardCount=L_CampStack=L_Denies=L_THeroDmg=L_THeroHeal=L_RegItemUse=L_TLaneEff = 0
    for i in range(len(dmr['players'])):
        if dmr['players'][i]['win'] == 1:
#            W_APM += dmr['players'][i]['actions_per_min']
            W_WardCount += dmr['players'][i]['obs_placed']+dmr['players'][i]['sen_placed']
            W_CampStack += dmr['players'][i]['camps_stacked']
            W_Denies += dmr['players'][i]['denies']
            W_THeroDmg += dmr['players'][i]['hero_damage']
            W_THeroHeal += dmr['players'][i]['hero_healing']
            W_RegItemUse += sum_regits(dmr['players'][i]['item_uses'])
            W_TLaneEff += dmr['players'][i]['lane_efficiency']
        if dmr['players'][i]['win'] == 0:
#            L_APM += dmr['players'][i]['actions_per_min']
            L_WardCount += dmr['players'][i]['obs_placed']+dmr['players'][i]['sen_placed']
            L_CampStack += dmr['players'][i]['camps_stacked']
            L_Denies += dmr['players'][i]['denies']
            L_THeroDmg += dmr['players'][i]['hero_damage']
            L_THeroHeal += dmr['players'][i]['hero_healing']
            L_RegItemUse += sum_regits(dmr['players'][i]['item_uses'])
            L_TLaneEff += dmr['players'][i]['lane_efficiency']
    
    wmd = pd.DataFrame([[ W_WardCount, W_CampStack, W_Denies, W_THeroDmg, W_THeroHeal, W_RegItemUse, W_TLaneEff, 1]], columns=['WardCount','CampStack','Denies','THeroDmg','THeroHeal','RegItemUse','TLaneEff', 'Win'])
    lmd = pd.DataFrame([[ L_WardCount, L_CampStack, L_Denies, L_THeroDmg, L_THeroHeal, L_RegItemUse, L_TLaneEff, 0]], columns=['WardCount','CampStack','Denies','THeroDmg','THeroHeal','RegItemUse','TLaneEff', 'Win'])
    match_data = match_data.append(wmd)
    match_data = match_data.append(lmd)
    return match_data

#match_data = pd.DataFrame(columns=['APM','WardCount','CampStack','Denies','THeroDmg','THeroHeal','RegItemUse','TLaneEff', 'Win'])

i = 0
match_data = pd.DataFrame(columns=variable_list)

while i < N:
    time.sleep(2)
    mr = req.get('https://api.opendota.com/api/matches/'+dset['matchID'][i]).text
    dmr = json.loads(mr)
    pdata = dmr['players']
    nullvaluecheck = []
    for j in range(10):
        checklist = [pdata[j]['obs_placed'], pdata[j]['sen_placed'], pdata[j]['camps_stacked'], pdata[j]['denies'], pdata[j]['hero_damage'], pdata[j]['hero_healing'], sum_regits(pdata[j])]
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
    

match_data.to_csv('dota_match_data')

