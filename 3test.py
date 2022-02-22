#! /usr/bin/env python3
from overwatch import HTTP, Hero
import asyncio 

import json


async def main():
	me = 
	
	cli = HTTP()
	
	#prof = await cli.GetHero(me, Hero.DVA)
	prof2 = await cli.GetComplete(me)
	
	#print(prof2)
#	walk_dict(prof2[(prof2.keys())[0]], 4)

	with open("data_gon.json", 'w') as f:
		json.dump(prof2,f, sort_keys=True, indent=4)



	dict_of_keys = {}

	for hero, data in prof2['competitiveStats']["careerStats"].items():
		if "heroSpecific" in data.keys():
			if data['heroSpecific']:
				if isinstance(data['heroSpecific'], dict):
					dict_of_keys[hero] = data['heroSpecific'].keys()
				else:
					dict_of_keys[hero] = data['heroSpecific']
	

	list_stat = []
	for hero, stat_name in dict_of_keys.items():
		if stat_name not in list_stat:
			list_stat.append(stat_name)
		else:
			print("There is a duplicate {} {}".format(hero, stat_name))
			return 

	print(dict_of_keys)
	print("No dups")
	#print(prof2["competitiveStats"]["careerStats"]["ana"])




asyncio.get_event_loop().run_until_complete(main())

