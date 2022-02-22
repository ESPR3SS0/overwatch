'''
	Unsure if this will be usefull but the idea sounds cool 
	
	Objective 
	---------
		Make a dataclass object for each hero 
		TODO: Test overhead for make the dataclass objects

	Note
	----
		Standard JSON dict for any given hero follows:
		<hero_name> : { assists : <>,
						average : <>,
						best : <>
						combat : <>.
						deaths : <>,
						heroSpecific : <>,
						game : <>
						matchAwards : <>,
						miscellaneous : <>
						}
'''

from dataclasses import dataclass 
from typing import List, Optional, Dict


@dataclass 
class 

@dataclass 
class Hero:
	name: str 
	assists : Dict
	average : Dict
	best : Dict 
	combat : Dict
	deaths : Dict
	heroSpecific : Dict
	game : Dict
	matchAwards : Dict
	miscellaneous : Dict


