from typing import Union


class OverwatchException(Exception):
	"""Base exception class for Overwatch.py"""
	pass

class HTTPException(OverwatchException):
	"""
	Exception for HTTP operation failures
	
	Parameters
	----------
	status: int
		HTTP status code of request
	res: dict
		Response for HTTP request
	"""

	def __init__(self, status: int, res: Union[dict,list,str]):
		if isinstance(res, dict):
			try:
				message: Union[dict,list,str] = res["data"].get("message", res)
			except KeyError:
				message = "No Data Recievced"
		else:
			message: Union[dict, list, str] = res
		super().__init__(f"HTTP {status} - {message}")
