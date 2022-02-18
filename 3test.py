#! /usr/bin/env python3
from overwatch import HTTP, Hero
import asyncio 

import json


async def main():
	me = "blackoutu742-1980"
	
	cli = HTTP()
	
	#prof = await cli.GetHero(me, Hero.DVA)
	prof2 = await cli.GetComplete(me)
	
	#print(prof2)
	walk_dict(prof2[(prof2.keys())[0]], 4)

	with open("data.json", 'w') as f:
		json.dump(prof2,f, sort_keys=True, indent=4)

asyncio.get_event_loop().run_until_complete(main())

