#!/usr/bin/env python3

'''

	Objective
	---------
		Functions to anaylze game play 
		1. First need to tame a json file 
			input => raw json, output => manipulated ow_file
'''


# Comp 
# Table stat stat stat stat herospecific:dict
# hero1 
# hero2
# hero3
# hero4 
# hero5
# hero6 
# hero7
# hero8


import pandas as pd 
import numpy as np
import json

from typing import Dict, List


# Thinking outloud... in a python file 
#	The json provided is heavily nested, and only has types : [int, dict, type(na), float]
#		So pretty much no lists, and I don't know what type na is just yet
#
#   I'd like to first scan for na's and set those to something known
#     --> np.NaN 
#   I'm betting pandas will handle this quite nicely for me 

#  Once some data manipulation is done, I'll probably make wrapper functions for pandas 
#		filters, then grab some basic data for now and plot it 
# 
#  TODO: Impletement plotly and matplotlib/seaborn plots, all very similar however 
#			I am sure there will be some changing to do for each one 
#  
#
#
#	Once I am to the point of plotting basic stats I am then going to work on...
#		1. Beefing up the plots, adding more options (commind line options/ config file options)
#		2. Getting the mongodb side of things up and running to get cool stats overtime 
#		3. Beef up the analysis, get some really cool insights/ pattern searching
#		4. Work on the CLI side of things 
#		5. Checkout the django integration 



def GetAvailableStats(name: str, df: pd.DataFrame) -> List:
	'''
	Parameter
	---------
		name : str 
			hero name
		df : pd.DataFrame
			pandas dataframe
	'''

	hero_df = (((df.loc[name]).to_frame()).dropna()).transpose()
	return hero_df.columns.values.tolist()

def CreateCompDf(data: Dict)-> pd.DataFrame:
	'''
		Parameter
		---------
			data: Dict
				Standart dictionary for competitive api call
		Returns
		-------
			pd.DataFrame
	'''

	flat_dict = {}
	hero_dict = {}

	# First fill the dataframe with the correct colls and hero
	for hero in data.keys():
		hero_dict = {}
		for key, value in data[hero].items():
			if value:
				for key2, val in value.items():
					hero_dict[key2] = val
		flat_dict[hero] = hero_dict


	cols = data.keys()
	index = flat_dict.keys()

	return (pd.DataFrame(flat_dict)).transpose()


def LocHeroStats(hero : str, df: pd.DataFrame, stats: List[str]) -> pd.DataFrame:
	'''
		Grab stats for hero in dataframe
		TODO: Evalute the usefulness of this function

		Parameters
		----------
			hero : str
				name of hero
			df : pd.DataFrame
				Competitive dataframe 
			stats : List[str]
				List of keywords to locate

		Returns
		-------
			pd.DataFrame 
				Including all the found stats for the passed hero 
	'''
	ret_df = pd.DataFrame(np.nan, index=[hero],
						columns=[stat for stat in stats if stat in df.columns])

	for stat in ret_df.columns:
		ret_df[stat] = df.at[hero, stat]

	ret_df = ret_df.dropna()
	return ret_df
	

def LocMany(hero: str, stats: List[str], df_list : Dict[str, pd.DataFrame]) -> pd.DataFrame:
	'''
		Another filter wrapper

		Parameters
		----------
			stats : List[str]
				keys for the wants stats 
			df_list : Dict[str, pd.DataFrame]
				blizzard_name : comp_df
	'''


	ret_df = pd.DataFrame(np.nan, index=[name for name in df_list.keys()],
						columns=stats)
	
	for blizzard_name, comp_df in df_list.items():
		for stat in stats:
			ret_df.at[blizzard_name, stat] = comp_df.at[hero, stat]
		
	return ret_df







if __name__ == "__main__":

	with open("data.json", 'r') as f:
		data = json.load(f)

	with open("data_player2.json", 'r') as f:
		data_player2 = json.load(f)



	comp_data = data["competitiveStats"]["careerStats"]
	comp_player2 = data_player2["competitiveStats"]["careerStats"]

	#print(comp_data.keys())


	comp_df = CreateCompDf(comp_data)
	comp_player2_df = CreateCompDf(comp_player2)


	#df = comp_df[comp_df["winrate"] 

	#ana_col = GetAvailableStats('ana', comp_df)

	#bp = LocHeroStats('reaper', comp_df, ['gamesPlayed', 'gamesWon'])
	#print(bp)

	bp = LocMany('reaper', ['gamesPlayed', 'gamesWon'], {"player1":comp_df, "player2":comp_player2_df})
	print(bp)

	pd.options.plotting.backend = "plotly"

	fig = bp.plot(kind="bar")
	fig.show()

	player1_played = comp_df.at['reaper', 'gamesPlayed']
	player1_won = comp_df.at['reaper', 'gamesWon']

	player2_played= comp_player2_df.at['reaper', 'gamesPlayed']
	player2_won= comp_player2_df.at['reaper', 'gamesWon']

	print("player1 ana stat-- games played : {} games won : {}".format(player1_played, player1_won))
	print("player2 ana stat-- games played : {} games won : {}".format(player2_played, player2_won))


