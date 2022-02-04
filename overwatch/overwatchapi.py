'''
	Wrapper for a basic requestor class with Overwatch specific values
'''

from .requestor import Requestor

import json

class Overwatch:

	hero_list = [ 'bastion', 'dVa', 'genji' , 'hanzo' , 'junkrat' , 'lucio' , \
					'mccree' , 'mei' , 'mercy' , 'orisa' , 'pharah' , 'reaper' , \
                    'reinhardt' , 'roadhog' , 'soldier76' , 'sombra' , 'symmertra' , \
                    'torbjorn' , 'tracer' , 'widowmaker' , 'winston' , 'zarya' , \
                    'zenyatta' ]

	def __init__(self):
		self.api = Requestor()
		self.base_url = "http://ow-api.com/v1/stats/pc/us/"
	
	def PullComplete(self, blizzard_name):
		'''
			GET https://ow-api.com/v1/stats/{blizzard_name}/complete
		'''

		# This is the raw return from request.get
		url = self.base_url + blizzard_name + "/complete"

		# This is the raw return from request.get
		ret = self.api.send(url)
		data = json.loads(ret.text)
		return data

	def PullProfile(self, blizzard_name):
		'''
			GET https://ow-api.com/v1/stats/{blizzard_name}/profile
		'''
		ret = self.api.send("http://ow-api.com/v1/stats/{}/profile".format(blizzard_name))
		data = json.loads(r.text)
		return data

	def PullHeroStats(self, blizzard_name, *hero_list):
		'''
			GET https://ow-api.com/v1/stats/{blizzard_name}/heroes/hero1,hero2,hero3
		'''

		heroes = ",".join(x for x in hero_list)
		for hero in heroes:
			if hero not in hero_list:
				return

		ret = self.api.send("http://ow-api.com/v1/stats/{}/heroes/{}".format(blizzard_name, heroes))
		data = json.loads(r.text)
		return data


if __name__ == "__main__":
	api = Requestor()
	overwatch = Overwatch()
	
	name = "blackoutu742-1980"
	data = overwatch.PullComplete(name)
	print(data)
	
	
