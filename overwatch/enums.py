
from enum import Enum

class Hero(Enum):
	'''
		List of all requestable overwatch heros

		NOTE: Some characters have potentially unexpected names 
				so this should help with some of that
		
	'''

	ECHO = "echo"
	DVA = "dVa"
	REAPER = "reaper"
	GENJI = "genji"
	HANZO = "hanzo"
	JUNKRAT = "junkrat"
	LUCIO = "lucio"
	MCCREE = "mccree"
	MEI = "mei"
	MERCY = "mercy"
	ORISA = "orisa"
	PHARAH = "pharah"
	REINHARDT = "reinhardt"
	ROADHOG = "roadhog"
	SOLDIER76 = "soldier76"
	SOMBRA = "sombra"
	SYMMETRA = "symmetra"
	TORBJORN = "torbjorn"
	TRACER = "tracer"
	WIDOWMAKER = "widowmaker"
	WINSTON = "winston"
	ZARYA = "zarya"
	ZENYATTA = "zenyatta"

class Platform(Enum):
	'''
		List of all possible platforms for ow-api

		NOTE: The api docs only list pc
	'''
	PC = "pc"
	

class Region(Enum):
	'''
		List of all possible regions for ow-api
	'''
	US = "us"
	EU = "eu"
	ASIA = "asia"

class APICallType(Enum):
	'''
		List of all possible call types for ow-api
	'''
	PROFILE = "profile"
	COMPLETE = "complete"
	HERO = "heroes"
