#!/usr/bin/env python3

'''

	Objective
	---------
		Functions to anaylze game play 
		1. First need to tame a json file 
			input => raw json, output => manipulated ow_file
'''



# New standard dataFrame structure:
#
# ----- UTC-time | blizzard_name | GameMode | Platform | Region | hero_name | ?best? | stats...
#
#
#
#
#
#
# pass a glob of series strings to the function 
#
#
#   One "series" string: { utc : "" , blizzard_name : "", GameMode : "", Platform : "", Region : "", hero_name : "", stats : {}}
#


import pandas as pd 
import numpy as np
import json

from typing import Dict, List

import pymongo

#from .db import Monodb
from db import Mongodb


#	Once I am to the point of plotting basic stats I am then going to work on...
#		1. Beefing up the plots, adding more options (commind line options/ config file options)
#		2. Getting the mongodb side of things up and running to get cool stats overtime 
#		3. Beef up the analysis, get some really cool insights/ pattern searching
#		4. Work on the CLI side of things 
#		5. Checkout the django integration 


def GenEmptyHeroDf(data, force_shape=True):
	columns = ['utc_time','blizzard_name', 'GameMode', 'Platform', 'Region', 'hero']


	if force_shape:
		if "competitiveStats" not in data.keys():
			return 
		if "careerStats" not in data["competitiveStats"].keys():
			return 
		if "topHeroes" not in data["competitiveStats"].keys():
			return 

		# Append all the bottom most keys for each player under careerStats in comp 
		for hero, hero_dict in data["competitiveStats"]["careerStats"].items():
			for sub_category, subcat_dict in hero_dict.items():
				if subcat_dict is None:
					continue
				for name in subcat_dict.keys():
					if name not in columns:
						columns.append(name)
	
		# Append all bottom most keys for each hero under top heroes
			# There is some overlap from the stats above, howevr top heroes 
			# Has some stats that the above missing, so this will add them to the cols
		for hero, hero_dict in data["competitiveStats"]["topHeroes"].items():
			for key in hero_dict.keys():
				if key not in columns:
					columns.append(key)

		if "quickPlayStats" not in data.keys():
			return 
		if "careerStats" not in data["quickPlayStats"].keys():
			return 
		if "topHeroes" not in data["quickPlayStats"].keys():
			return 

		# Append all the bottom most keys for each player under careerStats in comp 
		for hero, hero_dict in data["quickPlayStats"]["careerStats"].items():
			for sub_category, subcat_dict in hero_dict.items():
				if subcat_dict is None:
					continue
				for name in subcat_dict.keys():
					if name not in columns:
						columns.append(name)

		for hero, hero_dict in data["quickPlayStats"]["topHeroes"].items():
			for key in hero_dict.keys():
				if key not in columns:
					columns.append(key)

	hero_df = pd.DataFrame(columns=columns)
	print("here")
	return hero_df
	



def CreateHeroCompDict(data, hero):

	hero_dict = data["competitiveStats"]["topHeroes"][hero]

	for key, sub_dict in data["competitiveStats"]["careerStats"][hero].items():
		if sub_dict is None:
			continue
		for subkey, value in sub_dict.items():
			hero_dict[subkey] = value

	return hero_dict

def CreateHeroQuickDict(data, hero):

	hero_dict = data["quickPlayStats"]["topHeroes"][hero]

	for key, sub_dict in data["quickPlayStats"]["careerStats"][hero].items():
		if sub_dict is None:
			continue
		for subkey, value in sub_dict.items():
			hero_dict[subkey] = value

	return hero_dict

def HeroDf_FromMongo(data: Dict):
	'''
	nop


	Parameters
	----------
		data: Dict 
			A document object from the mongo db 
	'''

# ----- UTC-time | blizzard_name | GameMode | Platform | Region | hero_name | ?best? | stats...

	# Stats include the name of EVERY stat in the dictionary inside...
		# competitiveStats.careerStats
		# competitiveStats.topHeroes
		# quickPlayStats.careerStats
		# quickPlayStats.topHeroes

	# This dat frame IGNORES the following Stat/status in dictionary:
		# competitiveStats.awards
		# competitiveStats.games
		# gamesWon
		# level
		# prestige
		# quickPlayStats.awards
		# quickPLayStats.game
		# rating
		# ratings --> which is a list 

	# THEREFORE 
	# Because these stats are structure differently, I will gave another standard 
		# DataFrame that will contion this. 
	
	# Two dataframes are HERO_DATA and GENERAL 

	# Assuming standard mongodb document to dictionary is being passed 
		# One row with game mode competitive will only be for one hero
			# and include both the data from competitive.careerStats and
			#    data from competitive.topHeroes
	

	#blizzard_name = "test"
	#utc_time = "time"
	#region = "UC"
	#platform = "PC"

	# Grab an empty dataFrame with the correct columns 

	df = GenEmptyHeroDf(data)

	heroes = data['competitiveStats']['topHeroes'].keys() 

	for hero in heroes:
		hero_dict = CreateHeroCompDict(data, hero)
		hero_dict['blizzard_name'] = data['blizzard_name']
		hero_dict['utc_time'] = data['utc_time']
		hero_dict['game_mode'] = "competitive"
		hero_dict['region'] = data['region']
		hero_dict['platform'] = data['platform']
		hero_dict['hero'] = hero

		#hero_df = pd.DataFrame(hero_dict)
		df.loc[len(df.index)] = hero_dict

		#df = pd.concat([df,pd.DataFrame(hero_dict)], ignore_index=True)
	
	for hero in heroes:
		try:
			hero_dict = CreateHeroQuickDict(data, hero)
		except KeyError as e:
			print("Key Error In Quick - No character? : {}".format(e))
			continue

		# Eeach hero needs each of the following
		hero_dict['blizzard_name'] = data['blizzard_name']
		hero_dict['utc_time'] = data['utc_time']
		hero_dict['game_mode'] = "quick"
		hero_dict['region'] = data['region']
		hero_dict['platform'] = data['platform']
		hero_dict['hero'] = hero

		df.loc[len(df.index)] = hero_dict
		#df = pd.concat([df,pd.DataFrame(hero_dict)], ignore_index=True)
	
	# Hero df for one mongodb document blob
	return df

	# Now to fill the data 
	# each new combination can only be one character and one GameMode
	# So for the typical doc...
		# Each character will have two indexes in the stand hero_dataframe
		# one for comp, one for quick 
	
	# At this point the data was structure correctly 

def CreateGeneralDf(data:Dict):
	'''
	nop
	'''
	return True






if __name__ == "__main__":


	db = Mongodb(db_name="OVERWATCH_DEFAULT")
	data = db.FetchAllDocs('NETERO-31710')
	print(data)

	#with open("../sample_complete_pulls/data.json", 'r') as f:
	#	data = json.load(f)


	#gen_cols = GenHeroDfColumns(data)

	df = HeroDf_FromMongo(data[0])


	ch = ['winRate', 'winPercentage'] 
	for x in ch:
		if x in df.columns:
			print("{} in cols".format(x))
	#print(df.columns)

	tp = df[['hero','gamesPlayed','gamesLost','gamesWon','gamesTied']]
	
	print(tp)


	#print(gen_cols.columns)

	#with open("../sample_complete_pulls/data_player2.json", 'r') as f:
	#	data_player2 = json.load(f)



	#comp_data = data["competitiveStats"]["careerStats"]
	#comp_player2 = data_player2["competitiveStats"]["careerStats"]

	##print(comp_data.keys())


	#comp_df = CreateCompDf(comp_data)
	#comp_player2_df = CreateCompDf(comp_player2)

	#with open('data_player1_pickle','wb') as f:
	#	comp_df.to_pickle(f)


	##df = comp_df[comp_df["winrate"] 

	##ana_col = GetAvailableStats('ana', comp_df)

	##bp = LocHeroStats('reaper', comp_df, ['gamesPlayed', 'gamesWon'])
	##print(bp)

	#bp = LocMany('reaper', ['gamesPlayed', 'gamesWon'], {"player1":comp_df, "player2":comp_player2_df})
	#print(bp)

	#pd.options.plotting.backend = "plotly"

	#fig = bp.plot(kind="bar")
	#fig.show()

	#player1_played = comp_df.at['reaper', 'gamesPlayed']
	#player1_won = comp_df.at['reaper', 'gamesWon']

	#player2_played= comp_player2_df.at['reaper', 'gamesPlayed']
	#player2_won= comp_player2_df.at['reaper', 'gamesWon']

	#print("player1 ana stat-- games played : {} games won : {}".format(player1_played, player1_won))
	#print("player2 ana stat-- games played : {} games won : {}".format(player2_played, player2_won))


