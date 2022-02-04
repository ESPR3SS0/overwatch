'''

	Wrapper to json library

'''

import json
from pathlib import Path
import datetime

class JsonDataHandler:
	'''
		Handler for json data. Save passed data, read data from path
	
		Requires definition of root json path	

		This is meant to ONLY handle JSON. Therefore with calls such as get dir data, 
			the function will ignore any files that don't end in '.json'
	'''

	def __init__(self, root_dir):
		self.root = root_dir
		return


	def GetDirData(self, directory = None):
		'''
			Return a dictionary of files in the passed dir [ default is to return all root files ]
				{ filename : json_content , filename : json_content }
		'''

		if directory is None:
			directory = self.root
		
		ret_data = {}
		
		glob = Path(directory).glob('**/*')
		files = [ x for x in glob if ( x.is_file() and (".json" in x.name))]
		for x in files:
			ret_data[x.name] = self.read(x)
		return ret_data
	
	def ReadData(self, path):
		'''
			Returns a dictionary => { filename : json_contents }	
		'''
		ret_data = {} 
		with open(path, 'r') as f:
			data[f.name] = json.load(f)
		return data

	
	def write(self, path, data, absolute = False):
		'''
			Write the passed data to passed path
		'''
		with open(path, "w+") as f:
			json.dump(data, f, sort_keys = True, indent = 4)
		return
		
	def read(self, path, absolute = False):
		'''
			Read json file from passed path
		'''
		with open(path, 'r') as f:
			data = json.load(f)
		return data

	#def _getUtcTime(self):
	#	time = datetime.datetime.now(datetime.timezone.utc)
	#	time_str = time.strftime("%m_%d_%Y::%H:%M:%S")
	#	return time_str
	


if __name__ == "__main__":
	dummy = 4 
