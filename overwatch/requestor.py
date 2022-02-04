'''

	Wrapper class for request class 
	
'''

import requests


class Requestor:
	def send(self, msg):
		'''
			So this is just a long way to say "requests.get(msg)"
			... but maybe more funcationality will be implemented later

			returns the raw return from the api call
		'''
		url = msg 
		ret = requests.get(url)
		return ret 
