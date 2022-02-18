
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


	def gen_row_str_dict(self, data):
		str_list = [f"{key}:{value}" for key, value in data.items()]
		return " ".join(x for x in str_list)

	def gen_row_str_list(self, data):
		return ",".join(x for x in data)

	def nested_dict_chart(self, title, data):
		'''
			Params
			------
				title: str
					Title of chart
				data : { name : { x, y, x } , ... } 
		'''
			
		lname = max([len(str(x)) for x in data.keys()])
		linfo = max([len(str(self.gen_row_str_dict(info))) for info in data.values()])

	
		# now I have the longest name and longest info row 
		main_rows = ""
		
		row_list = [ f"{self.boarder} {name:<{lname}} {self.boarder} " +
					 f"{self.gen_row_str_dict(info):>{linfo}} {self.boarder}{self.endline}"\
							for name, info in data.items()]
		row_len = len(row_list[0])
		
		main_rows = "".join(x for x in row_list)
		#for key, info in data.items():
		#	row = f"{self.boarder} {key:<{lname}} {self.boarder}"
		#	section = ""
		#	for inner_key, name in info.items():
		#		section += f" {inner_key}: {name} "

		#	section = f"{section:<{linfo}}" + self.boarder + self.endline

		#	row  += section 
		#	main_rows += row 

		# Get the top boarder 
		top = self.chart_top(row_len- 1)

		#Get title 
		title_row = f"{self.boarder} {title}"
		title_row = f"{title_row:<{row_len- 3}} {self.boarder}{self.endline}"
		
		#Underline the title 
		title_underline = self.row_dividor(row_len- 1)
		
		# Get the top boarder 
		bottom = self.chart_top(row_len- 1)

		chart = top + title_row + title_underline + main_rows + bottom

		return chart 
			

	def dictionary_to_chart(self, title: str, data)-> str: 
		'''
			Params: 
			-------
				title: str
					Title for the chart 

				kwargs: dict
					{ name : value } 

			TODO: Find a way to handle iterables 
			-----

		'''

		# The longest name and longest value ( as in string length ) 
			# This will be used for padding the string later
		lname = max([len(str(x)) for x in data.keys()])
		lval = max([len(str(x)) for x in data.values()])

		max_row_len = 0

		# The following creates a list each row for the body of the chart based 
			#on the key:pair values
		row_list = [ f"{self.boarder} {name:<{lname}} {self.boarder} " +
					 f"{value:>{lval}} {self.boarder}{self.endline}"\
							 for name, value in data.items()]

		# Create a single string for chart body
		chart_body = "".join(x for x in row_list)

		# Max row len will be used for padding the title
		max_row_len = max([len(x) for x in row_list])

		# Create the top of the chart, title row for chart, and title underline
		chart_top = self.chart_top(max_row_len - 1)

		# Create chart title row
			# In the following line "-3" for 2 spaces and 1 boarder,
		chart_title = f"{self.boarder} {title:<{max_row_len - 1 - 3}}{self.boarder}{self.endline}"
		chart_underline = self.row_dividor(max_row_len- 1)
 
		# Put all chart pieces together
		chart = chart_top + chart_title + chart_underline + chart_body + chart_top
		
		return chart
		
		

if __name__ == "__main__":
	printer = TermPrinter()
	my = { "strtest" : '89' , "hookaccuracy" : 902523, 
			'booltest' : True, 1 : "reverseint test"}
	title = "dummy"
	nested = { "first" : {"inner1" : 4 , "inner2" : 5}}
	#chart = printer.dictionary_to_chart(title, my)
	chart = printer.nested_dict_chart(title, nested)
	print(chart)
		
