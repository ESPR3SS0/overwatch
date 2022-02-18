
from overwatch import HTTP, Hero
import asyncio 



async def main():
	me = "blackoutu742-1980"
	
	cli = HTTP()
	
	prof = await cli.GetHero(me, Hero.DVA)
	prof2 = await cli.GetComplete(me)
	
	print(prof)
	print(prof2)
	
	print("HERE HERE HERE HERE: {}".format(prof == prof2))

asyncio.get_event_loop().run_until_complete(main())

