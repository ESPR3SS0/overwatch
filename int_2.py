
from overwatch import Overwatch, Requestor, JsonDataHandler, TermPrinter
	

#def get_inp(input_str):
#	inp = input(input_str)
#	return inp

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


overwatch = Overwatch()
printer = TermPrinter()


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
while not done:
	print(options)
	opt = int(input("OPTION>"))
	if opt == 1:
		print("Name options are: {}".format(blizzard_names))
		name = str(input("name>"))
		if name not in blizzard_names:
			print("Name: {} not an option".format(name))
			continue
		traverse_dict(data_dict[name])
	elif opt == 2:
		print("TODO")
	elif opt == 3:
		print("TODO")
		
		

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
