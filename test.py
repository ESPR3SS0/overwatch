
from overwatch import Overwatch, Requestor, JsonDataHandler, TermPrinter

overwatch = Overwatch()
printer = TermPrinter()

blizzard_names = []

# to get to comp stats its : ["competitiveStats"]
data_dict = {}
for name in blizzard_names:
	complete = overwatch.PullComplete(name)
	if "competitiveStats" in complete.keys():
		data_dict[name] = complete["competitiveStats"]
		print("PULLED {}".format(name))
	else:
		data_dict[name] = "na"
	#print(complete["competitiveStats"].keys())


# Lets graph everyones stats for reaper 
#...This requires that all the values in the chart are integers
print(data_dict["blackoutu742-1980"]["topHeroes"]["reaper"])
for name in blizzard_names: 
	print("Working on {}".format(name))
	
	print(data_dict.keys())
	try:
		data_dict[name]["topHeroes"]["reaper"].pop('timePlayed')
	except TypeError as e:
		print("Error, not going to print {}".format(name))
		data_dict.pop(name)
	except KeyError as e:
		print("Error, not goin to print {}".format(name))
		data_dict.pop(name)
	#for key, value in data_dict[name]["topHeroes"]["reaper"].items():
	#	if isinstance(value,str):
	#		data_dict[name]["topHeroes"]["reaper"].pop(key)
	#		print("Removing key {}".format(key))



for name, key in data_dict.items():
	print("Working on {}".format(name))
	if "topHeroes" not in data_dict[name].keys():
		continue
	chart = printer.easy_chart_name_value("Reaper", **data_dict[name]["topHeroes"]["reaper"])
	print(chart)
