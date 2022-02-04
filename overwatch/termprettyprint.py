

class TermPrinter:

	def __init__(self):
		self.boarder = '|' 
		self.underline = '-'
		self.thick_underline = '='
		self.endline = "\n"
		self.tab = "\t"
		
	
	def chart_top(self, num):
		return (self.thick_underline*num) + self.endline
	
	def chart_bottom(self, num):
		return (self.thick_underline*num) + self.endline

	def row_name_value(self, name, pad1, value, pad2):
		return 

	def row_dividor(self, num):
		return (self.underline*num) + self.endline

	def info_piece_with_list(self, info, *args, sep = ", " ):

		info_top = self.chart_top(len(info) + 4 )
		info_row = f"{self.boarder} {info:<{len(info_top) - 5}} {self.boarder}{self.endline}"
		list_row = self.boarder + self.tab + sep.join( x for x in args)  
		list_row = f"{list_row:<{len(info_top) - 9}} {self.boarder}{self.endline}"
		info_bottom = self.chart_top(len(info) + 4 )
		
		info = info_top + info_row + list_row + info_bottom
		return info
			
	def chart_name_dict(self, title, split_name = True, printchart = False, **kwargs):
		'''
			Process will be very similar to easy chart 
				1. Find the longest row 
				2. create main rows 
				3. Create accessory rows 

		 	Expected Params...
				kwargs : { name : { x, y, x } , ... } 
		'''
			
		lname = 0 
		linfo = 0 
	
		data = {} 
		
		# First I'm going to create my data dict 
		for key, info in kwargs.items():
			if split_name:
				name = key.split('#')[0]
			else:
				name = key
			data[name] = info 
		
		# Now I'm going to find the longest name and and longest list 
		
		for key, info in data.items():
			# find the longest info 
			#f"| key: name  key: name  key: name |" 
			# So the length will be (1space + len(key) + 1colon + 1spave + len(name) + 1space) * nums items + 2 boarder 
			
			infol = 2 
			for inner_key, name in info.items():
				infol += 4 
				infol += len(str(inner_key)) + len(str(name))

			if infol > linfo:
				linfo = infol
	
			if len(name) > lname:
				lname = len(name)
	
		# now I have the longest name and longest info row 
		main_rows = ""
		for key, info in data.items():
			row = f"{self.boarder} {key:<{lname}} {self.boarder}"
			section = ""
			for inner_key, name in info.items():
				section += f" {inner_key}: {name} "

			section = f"{section:<{linfo}}" + self.boarder + self.endline

			row  += section 
			main_rows += row 

		# Get the top boarder 
		top = self.chart_top(len(row) - 1)

		#Get title 
		title_row = f"{self.boarder} {title}"
		title_row = f"{title_row:<{len(row) - 3}} {self.boarder}{self.endline}"
		
		#Underline the title 
		title_underline = self.row_dividor(len(row) - 1)
		
		# Get the top boarder 
		bottom = self.chart_top(len(row) - 1)

		chart = top + title_row + title_underline + main_rows + bottom

		return chart 
			
			

	def easy_chart_name_value(self, title, split_name = True, printchart = False, \
								highlight_leader = False, leader = None, **kwargs):
		'''
			Params: 
					{ name : value } 

		'''

		# Acouple NOTES
		#      The name passed to leader must be of the names in the rows 
		if highlight_leader:
			if not leader:
				return 
			elif leader not in kwargs.keys():
				return 

		# longest name and longest(str(value))
		lname = 0 
		lval = 0 
	
		# New Dict to store new names.
		#	New names will be made if split_name = True
		data = {}

		# First I need to now what padding the left column and right column need...
		for name, value in kwargs.items():
			# To split the name at the '#' or not to split... 
			if split_name:
				new_name = name.split('#')[0]
			else:
				new_name = name
			data[new_name] = value

			# Compare the length of the new name to the longest length so far 
			if len(new_name) > lname:
				lname = len(new_name)
			# Compare the length of the longest str of the values 
			#if isinstance(value, str):
			#	if len(value) > lval:
			#		lval = len(value)
			if len("{:.2f}".format(value)) > lval:
				lval = len("{:.2f}".format(value))
		
		# This will assure that if the leader is highlighted that the 
		# 	highlight row won't be too long
		if highlight_leader:
			if lval < len("Leader"):
				lval = len("Leader")

		# Now I know the paddings and what names to display

		# Now create all cols containing name and values
		all_cols = ""
		for name, value in data.items():
			col = f"{self.boarder} {name:<{lname}} {self.boarder} {value:<{lval}.2f} {self.boarder}{self.endline}"
			all_cols += col

		# Create the top of the chart, title row for chart, and title underline
		chart_top = self.chart_top(len(col) - 1)
		# In the following line "-3" for 2 spaces and 1 boarder, "-1" b/c yeah
		chart_title = f"{self.boarder} {title:<{len(col) - 1 - 3}}{self.boarder}{self.endline}"
		chart_underline = self.row_dividor(len(col) - 1)
 
		# put the pieces together and return the complete string
		#     Only thing remaining is the optional leader highlight and bottom 
		chart = chart_top + chart_title + chart_underline + all_cols 
		
		# Add the leader foot if passed 
		if highlight_leader:
		
			if split_name:
				leader = leader.split('#')[0]

			chart += chart_underline
			leader_row = f"{self.boarder} Leader: {leader:<{len(col) - 13}} {self.boarder}{self.endline}"
			chart += leader_row
			chart += chart_top
		else:
			chart += chart_top

		if printchart:
			print(chart)
		
		return chart
		
		

if __name__ == "__main__":
	printer = TermPrinter()
	my = { "name" : 89 }
	title = "dummy"
	chart = printer.easy_chart_name_value(title, **my)
	print(chart)
		
