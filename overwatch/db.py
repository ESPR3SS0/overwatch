#!/usr/bin/env python3

import asyncio

import pymongo
from pymongo import MongoClient
import time
import subprocess

import json

import pandas as pd 
import numpy as np

from typing import List, Dict

from .enums import Hero, Region, Platform
#from enums import Hero, Region, Platform


#from .ow_http import HTTP

from .errors import MongoException

import time


# STRUCTURE OF DATABASE 
#
#     database :: OVERWATCH_DEFAULT
#		This is the name of the default overwatch database
#
#     collection :: blizzard_name 
#		Each collection will be named after a blizzard name 
#	  
#     doc :: data
#           stat data pulled from ow-api site
#			NOTE: This data is NEARLY untouched, acouple new key
#					pair values are appended to the db


# TODO: use shlex or some other form of running os cmds? 
# TODO: windows/mac support?? Though this is likly a loaded question
class Mongodb:

	def __init__(self, db_name="OVERWATCH_DEFAULT"):

		self._server_is_running = False
		self.client = MongoClient()

		self.db = self.client[db_name]

		if not self._server_is_running:
			self.startServer()

	def startServer(self):
		'''
		Check that the mongodb service is running
		'''
		cmd = "mongod  >/dev/null 2>&1"
		subprocess.Popen(cmd, shell=True)

		self._server_is_running = True
		return 
	
	def stopServer(self):
		'''
		Check that the mongodb service is running
		'''
		cmd = "pkill mongod"
		subprocess.Popen(cmd, shell=True)
		self._server_is_running = False
		return 

	def checkServer(self):
		'''
		Check that the mongodb service is running
		'''
		cmd = "ps -aux | grep mongo"
		proc = subprocess.run(cmd, shell=True, capture_output=True)
		if "mongod" in proc.stdout.decode('utf-8'):
			return True
		return False 

	def _formatquery(self, keys: List[str])-> str:
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

	def FetchAllDocs(self, blizzard_name: str) -> List:
		'''
		Parameters			
		----------
		blizzard_name : str 
			name in blizzard, this will be the name of the collection

		Returns 
		-------
		List
			a list of all the Document in the Collection
		'''
		return list((self.db[blizzard_name]).find())



	#def CollectFromFilter(blizzard_names: List[str], 
	#		keys: List[str])-> Dict[str, pymongo.collection]:
	#	'''
	#		Use the same document filter/query str from multiple players
	#	'''
	#	query_str = self._formatquery(keys)
	#	doc_dict = {}
	#	for name in blizzard_names:
	#		docs = [doc for doc in (self.db[blizzard_name].find({}, {query_str:1}))]
	#		doc_dict[name] = docs
	#	return doc_dict

	def CollectFromFilters(self, blizzard_names: List[str], nested_keys: List[List[str]]):
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

	def CollectUniqueFilters(self, name_filter_pairs: Dict[str,List[List[str]]]):
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

	def ConvertDocData(self, blizzard_name, gameMode, region=Region.US, platform=Platform.PC):
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

	def ConvertPull(self, json_data, blizzard_name, pull_time_utc, pull_type, region=Region.US, 
			platform=Platform.PC):
			'''
				Edit the json return from OW-API. 
				Append the time, region, platform, blizzard_name, pull type to json. 
			'''

			data = dict(json_data)
			data['blizzard_name'] = blizzard_name
			data['utc_time'] = pull_time_utc
			data['pull_type'] = pull_type
			data['region'] = str(region)
			data['platform'] = str(platform)
			return data

	def InsertData(self, data, blizzard_name):
		'''
		Parameters
		----------
			data: dict
				json from ow_http pull

			blizzard_name: str
				blizzard name   <name>-<vals>
		'''

		if not self.AssertCollectionExists(blizzard_name):
			raise MongoExcpetion

		collection = self.db[blizzard_name]

		collection.insert_one(data)
		return 

	def AssertCollectionExists(self, collection_name: str) -> bool:
		'''
		Assert that a given collection exitsts 

		Parameters
		----------
			collection_name: str
				Name of a collection (This will be the same as blizzard_name)
		'''

		# Check that Mongodb is running first?
		if not self.checkServer(self):
			return False

		# TODO: Check that db connection is good first?

		if collection_name in self.db.list_collection_names():
			return True
		return False



if __name__ == "__main__":

	mongo = Mongodb(db_name='test_data')

	#mongosh = MongoQuery(server, database)

	#reaps_data = mongo.QueryStat('player1', ['competitiveStats','careerStats','reaper'])
	#for reaps in reaps_data:
		#print(reaps)
	print('here')

	print(mongo.checkServer())

	print(mongo.FetchAllDocs('player1'))


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

