# DataScientology
Intro to Data Science Project Work
**********************************************

#Example query to see how it is: https://api.opendota.com/api/explorer?sql=SELECT%20public_matches.match_id,public_matches.avg_mmr,%20public_matches.lobby_type,public_matches.lobby_type,public_matches.game_mode%20FROM%20public_matches%20WHERE%20public_matches.avg_mmr%20%3E%205000%20AND%20public_matches.lobby_type%20IN%20(5,6,7) AND public_matches.game_mode=22%20limit%20100\

#
# PARAMETERS\
#1) chatdata (wordcount) or take the words, wordcounts are python dictionary. How do we use wordclouds for this? 
    Maybe not predictor but just two wordclouds for win and lose situations. This is not in the code yet \
#2) We try to obtain location coordinates on the map and the map size? Not in the code yet, could not find the map size for X,Y\
#3) number of wards placed \
#4) camps stacked \
#5) denies \
#6) sum of all hero damage per minute \
#7) sum of all hero healing per minute \
#8) Regen item uses. Regen items: [tango, clarity, flask and enchanted_mango] use? \
#9) Sum of all heroes lane efficiencies \
# 
#Uses players[i]['win'] to select aggregate through above parameters. \

#Shall we look into hero wise winrate too? Might get a bit too complicated though.
#

Also, apparently the data is not that clean. There are many instances where the value of a parameter is NONE or it the key itself does not exist. It might be  due to privacy settings of the players, so they do not share certain stats but it still does not explain the selectiveness of stat existence.

