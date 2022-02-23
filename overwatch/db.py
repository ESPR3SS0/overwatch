#!/usr/bin/env python3

import pymongo
from pymongo import MongoClient
import time
import subprocess

import json

import pandas as pd 
import numpy as np

from typing import List, Dict

from enums import Hero, Region, Platform



# STRUCTURE OF DATABASE 
#
#     database :: OVERWATCH_DEFAULT
#		This is the name of the default overwatch database
#
#     collection :: blizzard_name 
#		Each collection will be named after a blizzard name 
#	  
#	TODO: In addition to id'ing each document, include a timestamp and 
#			pull type ['complete', 'competitive', or ...]
#     doc :: complete_pull ; right now I'm only setting up the db for 'complete pulls'
#           complete stat json pulled from ow-api site
#
# Thinking out loud... onto a python script again 
#
# Now I have a problem but it's a good problem...
#	How to split up the data manipulation between pymongo and pandas 
#   Originally the idea was to store the raw json inside of pymongo 
#   And leave all data manipulation to pandas 
#
#   However now that I've been playing with pymongo some, selecting 
#		documents is very easy 
#
#	
#	I think I am going to shoot for a happy medium...
#
#      1. Do the filtering that I can in pymongo, so what that means to me 
#			as of now is selecting the smallest dictionary possible
#			from collections and returning those 
#
#		2. Once the smallest dictionaries necessary have been pulled from the 
#			database leave the computations and higher level filtering/plotting 
#			ect., to pandas
#
#		NOTICE: This will make same manipulating with pandas more difficult 
#				now that I no longer will always be passing a standard dictionary 
#				set up. I do believe I will be able to construct generalized functions 
#				that work non-the-less


# TODO: use shlex or some other form of running os cmds? 
# TODO: windows/mac support?? Though this is liked a loaded question
class MongoServer:
	def __init__(self):
		self.is_running = False

	def start(self):
		cmd = "mongod  >/dev/null 2>&1"
		subprocess.Popen(cmd, shell=True)
		return 
	
	def stop(self):
		cmd = "pkill mongod"
		subprocess.Popen(cmd, shell=True)
		return 

class MongoQuery:
	def __init__(self, server, database):
		self._server = server
		self.client = MongoClient()

		self.db = self.client[database]

		if not self._server.is_running:
			self._server.start()
	

	def _formatquery(self, keys: List[str]):
		'''
			Wrapper, latter I will add checking here 

		'''
		return ".".join(x for x in keys)

	def QueryStat(self, blizzard_name: str, keys: List[str]):
		'''
			Parameters
			----------
				blizzard_name: str
					blizzard_name, this will be the name of the collection

				keys: List[str]
					keys for the desired query 
		'''
		query_str = self._formatquery(keys)

		collection = self.db[blizzard_name]


		docs = []
		for doc in collection.find({}, {query_str:1}):
				docs.append(doc)
		return docs



	def CollectFromFilter(blizzard_names: List[str], 
			keys: List[str])-> Dict[str,pymongo.collection]:
		'''
			Use the same document filter/query str from multiple players
		'''
		query_str = self._formatquery(keys)
		doc_dict = {}
		for name in blizzard_names:
			docs = [doc for doc in (self.db[blizzard_name].find({}, {query_str:1}))]
			doc_dict[name] = docs
		return doc_dict

	def CollectFromFilters(blizzard_names: List[str], nested_keys: List[List[keys]]):
		'''
			Use the same multiple queries for multiple players
		'''
		doc_dict = {}
		for keys in nested_keys:
			keys_dict = self.CollectFromFilter(blizzard_name, keys)

		# Return like this maybe--
		# dict = {
		#     player1 : {
		#			query_string : result,
		#			query_strng2 : res2
		#			}
		#	 player2 : {
		#
		#
		#			}

	def CollectUniqueFilters(name_filter_pairs: Dict[str,List[List[str]]]):
		'''
			I want this to be the highest level filter for pulling from mongodb so far 

			the filter must be in the form:
				"{<collection_name/blizzard_name>: [['key','key1']['key2','key3']], ...}

			Parameters
			----------
					name_filter_pairs : Dict[str, List[List[str]]
						An example may serve the best explanation here...
							filter = {"my_blizard_name": [['competitive','careerStats'],
														['competitive','careerStats','ana'],
													['quickPlay','careerStats', 'topHeroes']}
		'''

		# Need to make sure the filter parameter is well constructed

	def ConvertDocData(blizzard_name, gameMode, region=Region.US, platform=Platform.PC):
		'''
			Convert the Data to the format that the standard DataFrame expects 

			{UTC_time: "", blizzard_name : "", GameMode : "", Platform : "", Region : "",\
					hero : "", *stats

			This means the final returned data is only the data for a SINLGE hero, SINGLE
				player, SINGLE mode and so on


			competitiveStats.careerStats.ana
			competitiveStats.topHeroes.ana
			quickPlay.careerStats.reaper
			topHeroes.blizzard_name
		'''

	def RawPullToDoc(blizzard_name, pull_time_utc, pull_type, region=Region.US, 
			platform=Platform.PC, json_data):
			'''
				Edit the json return from OW-API. 
				Append the time, region, platform, blizzard_name, pull type to json. 
			'''

			json_data['blizzard_name'] = blizzard_name
			json_data['utc_time'] = pull_time_utc
			json_data['pull_type'] = pull_type
			json_data['region'] = region
			json_data['platform'] = platform
			return json_data





if __name__ == "__main__":
	server = MongoServer()
	server.start()
	
	time.sleep(3)

	database = 'test_data'

	mongosh = MongoQuery(server, database)

	reaps_data = mongosh.QueryStat('player1', ['competitiveStats','careerStats','reaper'])
	for reaps in reaps_data:
		print(reaps)



	#with open("../sample_complete_pulls/player1_data2.json", 'r') as f:
	#	data = json.load(f)


	#collection.insert_one(data)

	#cur = collection.find({})
	#print(cur[0])
	#for doc in cur:
	#	print(doc)

	#print(collection['careerStats']['competitiveStats']['ana'])

	#print(db['player1'])
	#print('hjere')

