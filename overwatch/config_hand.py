import configparser 
from Pathlib import Path


def verify_sections(cfg: configparser.ConfigParser()):
	'''
		Function to verify the config 

		Parameters
		----------
			cfg : configparser.ConfigParser

		Returns 
		-------
			bool 

		Descrip
		-------
			Verify that the config object passed is valid 
	'''
	required_sections_keys = {'CALL_INFO': 'blizzard_names'}

	for section, key in required_sections_keys.items():
		if section not in cfg.sections():
			return False
		elif:
			key not in cfg[section].keys():
				return False 
	return True 


def grab_cfg(abs_path : str):
	# assert path exists
	return True 
