#import logging 
import urllib.parse
from typing import Dict, List, Union, Optional

import asyncio

from httpx import AsyncClient, Response

from .enums import Platform, Region, APICallType

#import httpx

from .errors import HTTPException 

#import json

# Need to fix the issue with old lib always expecting json
async def ResponseJSONorTEXT(resp: Response) -> Union[dict, list, str]:
	"""
		Determine type of response
	"""

	json_headers: List[str] = ["application/json;charset=utf-8", "application/json"]

	if resp.headers["Content-Type"].lower() in json_headers:
		return resp.json()
	else:
		return resp.text

class Request:
	"""
		Request Object

		Parameters
		----------
		blizzard_name: str
			The blizzard profile name. Must follow format: {name}-{numbers}
		desired_content: str
			can only be the following: [ "profile", "complete", "hero" ] 
			TODO: implement heroes desired_content type to reduce api calls
	"""
	baseUrl: str = "https://ow-api.com/v1/stats/pc/us/"
	acceptable_content = ["profile", "complete", "hero" ]
	
	def __init__(self, endpoint: str):
		self.endpoint: str = endpoint

		if endpoint is not None:
			self.url = f"{self.baseUrl}{endpoint}"
		else:
			self.url = self.baseUrl

# The new requesotr
class HTTP:
	"""
		Handling of sending the http calls
	"""

	def __init__(self):
		self.session: httpx.AsyncClient = AsyncClient()


	async def Send(self,req):
		"""
			Send the request
		"""
		#async with self.session as client:
		#	resp = await client.request( "GET", req.url )
		resp = await self.session.request( "GET", req.url )
		
		data: Union[dict, list, str] = await ResponseJSONorTEXT(resp)

		# Check for error status
		if isinstance(data, dict):
			status: Optional[str] = data.get("status")
		
			if status == "error":
				raise HTTPException(resp.status_code, data)

		# HTTP 2xx: Success
		if resp.status_code >= 200 and resp.status_code < 300:
			return data
		
		# 400: Bad Request
		if resp.status_code == 400:	
			raise HTTPExcpetion(resp.status_code, data)
		
		# 404: Not Found
		if resp.status_code == 404:
			raise HTTPException(resp.status_code, data)
		
		# 406: Not Acceptable
		if resp.status_code == 406:
			raise HTTPException(resp.status_code, data)
			
		# 500: Internal Server Error
		if resp.status_code == 500:
			raise HTTPException(resp.status_code, data)

		# 503: Service Unavailable
		if resp.status_code == 503:
			raise HTTPException(resp.status_code, data)

		return 

	async def GetProfile(self, blizzard_name):
		return await self.Send(Request(f"{blizzard_name}/profile"))

	async def GetComplete(self, blizzard_name):
		return await self.Send(Request(f"{blizzard_name}/complete"))

	#TODO: This pulls the same thing as the complete  url?
	async def GetHero(self, blizzard_name, hero):
		return await self.Send(Request(f"{blizzard_name}/heroes/{hero}"))
	

if __name__ == "__main__":

	cli  = HTTP()
	bliz_name = "blackoutu742-1980"
	
	prof = asyncio.run(cli.GetProfile(bliz_name))
	print(prof)
	
		
