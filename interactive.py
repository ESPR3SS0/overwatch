
from overwatch import Overwatch, Requestor, JsonDataHandler, TermPrinter

def traverse_dict(data):
	
	temp = {item:val for item, val in data.items()}
	done = False
	options = "(1) cd (2) print key data"
	dir_str = ""
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
			
			if inp not in temp.keys():
				print("Key: {} not an available key".format(inp))
				continue
			if not isinstance(temp[inp], dict):
				print("Key results in non-dict type: {}".format(temp[inp]))
				done = True
			else:
				dir_str = dir_str + '/' + inp
				temp = temp[inp]
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
		
		
