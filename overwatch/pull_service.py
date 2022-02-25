from .db import Mongodb
from .ow_http import HTTP

import configparser
from pathlib import Path

import asyncio
import datetime

import time

from .errors import HTTPException


class PullService:
	'''
		Make pull using ow_http
		Save pulls using mongodb 

		Pull according to the given config 
	'''
	

	def __init__(self, config_path_abs):


		with open(config_path_abs) as f: 
			config = configparser.ConfigParser()
			config.read_file(f)
			self.cfg = config
			self.max_mongo_start_attempt = 3

			if "database" in config["SERVICE"].keys():
				self.mongo = Mongodb(config["SERVICE"]["database"])
			else:
				self.mongo = Mongodb()
		self.HTTP = HTTP()
		self._service_running = False
		self.loop = asyncio.get_event_loop()

	async def Service(self):
		'''
			Loop to run service until kill is sent
		'''

		blizzard_names = [x for x in (self.cfg["GENERAL"]["blizzard_names"]).split("\n") if\
				"-" in x]
		print("blizzard name", blizzard_names)
	
		while True:
			for name in blizzard_names:
				print("Pulling data for {}".format(name))
				mongo_start_attempt = 0
				while not self.mongo.checkServer():
					self.mongo.startServer()
					time.sleep(1)
					mongo_start_attempt += 1
					if mongo_start_attempt > self.max_mongo_start_attempt:
						self.loop.close()

				try: 
					data = await self.HTTP.GetComplete(name)
					print(type(data))
					pull_time = datetime.datetime.now(datetime.timezone.utc)
					data = self.mongo.ConvertPull(data, name, pull_time, "complete")
					self.mongo.InsertData(data, name)
					print("inserted data for {}".format(name))
				except HTTPException as e:
					print(e)
					print("Skipping name {}".format(name))

			time.sleep(60*15)

	def Start(self):
		self.loop.create_task(self.Service())
		self.loop.run_forever()


if __name__ == "__main__":

	cfg_file = Path("tmp_config.cfg")
	cfg_file = cfg_file.resolve()

	service = PullService(cfg_file)
	service.Start()


	
