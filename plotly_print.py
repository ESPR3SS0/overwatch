
from overwatch import Overwatch, Requestor, JsonDataHandler, TermPrinter

import collections

from plotly.subplots import make_subplots
import plotly.graph_objects as go
	

def traverse_dict(data):
	
	temp = {item:val for item, val in data.items()}
	done = False
	options = "(1) cd (2) print key data"
	dir_str = ""

	current_key_depth = []
	
	while not done:
		
		print(options)
		opt = int(input("OPTION|{}:>".format(dir_str)))
	
		if opt == 1:
			print("Traversing, enter stop to stop")
			print("current keys: {}".format(temp.keys()))
			inp = str(input("Enter Desired Key>"))

			if inp == "stop":
				done = True 
				break
			
			if inp == "..":
				current_key_depth.pop(len(current_key_depth)-1)
				temp = {}
				temp = {item:val for item, val in data.items()}
				for key in current_key_depth:
					temp = temp[key]
				dir_str = "/".join(current_key_depth)
			elif inp not in temp.keys():
				print("Key: {} not an available key".format(inp))
				continue
			elif not isinstance(temp[inp], dict):
				print("Key results in non-dict type: {}".format(temp[inp]))
				done = True
			else:
				dir_str = dir_str + '/' + inp
				temp = temp[inp]
				current_key_depth.append(inp)
		elif opt == 2:
			for key, val in temp.items():
				print(" Key: {} Data: {}".format(key, val))
	return 

def get_highest_winrate(data):
	'''
		Within the topheroes
	'''

	highest = 0 
	topheroes = data["topHeroes"]
	
	if not topheroes:
		return ("na", "na")

	try:
		for hero_name, data in topheroes.items():
			if (int(data["winPercentage"]) > highest and int(data["winPercentage"]) < 80):
				print("Old highest: {}".format(highest))
				top_name = hero_name
				highest = int(data["winPercentage"])
				print("New highest: {} {}".format(top_name, highest))
	except KeyError as e:
		print("KeyError no data for hero")
	except NoneType as e:
		print("No data")
	
	return (top_name, highest)

overwatch = Overwatch()
printer = TermPrinter()

blizzard_names = [ "blackoutu742-1980", "Bastion-12314", "GON-12362", \
					"Chrollo-11124", "Neferpitou-21418", "Hisoka-12762",\
					"Meruem-11127", "Nac-11271" ]

names_to_remove = []
# to get to comp stats its : ["competitiveStats"]
data_dict = {}
for name in blizzard_names:
	complete = overwatch.PullComplete(name)
	if "competitiveStats" in complete.keys():
		data_dict[name] = complete["competitiveStats"]
		print("PULLED {}".format(name))
	else:
		data_dict[name] = "na"
		print("Name {} has no data".format(name))
		names_to_remove.append(name)
	#print(complete["competitiveStats"].keys())

#traverse_dict(data_dict[blizzard_names[0]])

done = False 
options = "(1) Traverse data, (2) Compare Single Stats (3) Graph 'topheroes' stats for character"
#while not done:
#	print(options)
#	opt = int(input("OPTION>"))
#	if opt == 1:
#		print("Name options are: {}".format(blizzard_names))
#		name = str(input("name>"))
#		if name not in blizzard_names:
#			print("Name: {} not an option".format(name))
#			continue
#		traverse_dict(data_dict[name])
#	elif opt == 2:
#		print("TODO")
#	elif opt == 3:
#		print("TODO")


# Lets print ana winrates 
#ana_win = {name : "na" for name in blizzard_names}
ana_win = {}

for name in blizzard_names:
	try:
		#print(data_dict[name]["careerStats"]["ana"]["heroSpecific"]["scopedAccuracy"])
		print("Name {} accr {}".format(name, data_dict[name]["careerStats"]["ana"]["heroSpecific"]["scopedAccuracy"]))
		ana_win[name] = int(str(data_dict[name]["careerStats"]["ana"]["heroSpecific"]["scopedAccuracy"]).replace("%",""))
	except TypeError as e:
		print("TypeError with name {}, not printing".format(name))
		#ana_win.pop(name)
	except KeyError as e:
		print("KeyError with name: {}, not printing".format(name))
		#ana_win.pop(name)


winrates = {}
for name in blizzard_names:
	try:
		hero, val = get_highest_winrate(data_dict[name])
		winrates[name] = hero, val
	except TypeError as e:
		print("foobar: {}".format(e))
	
print(winrates)


#fig = make_subplots(rows=1,cols=2, subplot_titles=("ScopedAccuracy"))
#names = list(ana_win.keys())
#fig.add_trace(go.Bar( name = "Accr", x = names, y = list(ana_win.values())), row=1,col=1)
#fig.show()
	

#data = { key:val for key, val in data_dict.items() if val != "na" }
#
#for name in names_to_remove:
#	blizzard_names.remove(name)
#
#options_str = "Show stats for hero"
#done = False
#while not done:
#	print(options_str)
#	hero = str(input("Hero name>"))
## Lets graph everyones stats for reaper 
##...This requires that all the values in the chart are integers
##print(data_dict["blackoutu742-1980"]["topHeroes"]["reaper"])
#	for name in blizzard_names:
#	#	print("Working on {}".format(name))
#	#	
#	#	print(data_dict.keys())
#		try:
#			data[name]["topHeroes"][hero].pop('timePlayed')
#		except TypeError as e:
#			print("Error, not going to print {}".format(name))
#			#data.pop(name)
#		except KeyError as e:
#			print("Error, not goin to print {}".format(name))
#			#data.pop(name)
#		#for key, value in data_dict[name]["topHeroes"]["reaper"].items():
#		#	if isinstance(value,str):
#		#		data_dict[name]["topHeroes"]["reaper"].pop(key)
#		#		print("Removing key {}".format(key))
#	
#	for name, key in data.items():
#		if "topHeroes" not in data[name].keys():
#			continue
#		chart = printer.easy_chart_name_value(f"{name}:{hero}", **data[name]["topHeroes"][hero])
#		print(chart)
