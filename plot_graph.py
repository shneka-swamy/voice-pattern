# AIM: Make the graphs suitable for IEEE publication
# Requires matplotlib, multipledispatch

#TODO: Add a test mode in which the title and labels are not required
#TODO: Choose from a pallatte of colors and add designs that make the graphs visible.
#TODO: Generates a direct SVG or PDF file and stores it in the folder results (this name can be changed)
#TODO: Ability to take the values from an excel sheet or csv file and generate the graph
#TODO: Allow to adjust the x and the y axis
#TODO: Allow to choose configuration
#TODO: Consolidate all the comments to a single value
#TODO: Must change the number of parameters passed to the function

#TO check: Can one x axis be left and the other's be given


import matplotlib.pyplot as plt
from multipledispatch import dispatch

class Graphs():
	
	def __init__(self):
		self.x_label = []
		self.y_label = []
		self.title = ''
		self.legends = []

	def set_labels(self, x_label, y_label, title):	
		self.x_label = x_label
		self.y_label = y_label
		self.title += title

	def set_legends(self, legends):
		self.legends = legends

	# Truncates values to match the list length
	def truncate_y_list(self, y_list, back_trun):
		y_length = min([len(value) for value in y_list])
		for i in range(0, len(y_list)):
			if back_trun:
				y_list[i] =  y_list[i][:y_length]
			else:
				y_list[i] = y_list[i][(len(value) - y_length):]

	# Generates the x list based on whether one is provided or not
	def generate_x_list(self, y_list, x_list):
		if len(x_list) == 0:
			y_length = len(y_list[0])
			x_list.append(range(0, y_length))
		# When most of the graphs have the same x-axis
		if len(x_list) < len(y_list):
			for i in range(0, (len(y_list) - len(x_list))):
				get_value = x_list[-1]
				x_list.append(get_value)

	# Chooses the dimension of the graph based on the input
	def choose_model(self, number_of_graphs, max_limit = 5):
		# Warn that it might make the graph messy
		if number_of_graphs % 2 != 0 and number_of_graphs <= max_limit:
			return int(number_of_graphs), 1

		for i in range(1, max_limit+1):
			for  j in range(1, i+1):
				if i*j == number_of_graphs or i*j > number_of_graphs:
					return i, j
		print("Change the maximum limit")
		exit(0)

	# Gets the label if enough labels are not entered
	def _get_labels_(self, length):
		print("Want common(C) or different(D) label")
		decision = input()
		while decision!= 'C' and decision!= 'D':
			print("Please Enter a correct decision")
			decision = input()

		count = 0
		get_list = []
		while(True):
			if decision == 'C' and count == 1:
				break
			elif decision == 'D' and count == length:
				break
			else:
				get_list.append(input())
				count += 1
		return get_list, decision

	# Checks if common or different labels are required
	def _get_decision_(self, label, length, val = 0):
		get_list = []
		if len(label) == 1:
			decision = 'C'
		elif len(label) == length:
			decision = 'D'
		else:  
			if val == 0:
				print("It is mandatory to have x-axis label")
			else:
				print("It is mandatory to have y-axis label")
			get_list, decision = self._get_labels_(length - len(label))

		return decision, get_list 

	# Checks if the title for the graph is entered
	def _check_title_label_(self, length):
		if len(self.title) == 0:
			print("Title required, Please Enter the Title")
			self.title += input()

		x_decision, get_xlist = self._get_decision_(self.x_label, length)
		self.x_label += get_xlist
	
		y_decision, get_ylist = self._get_decision_(self.y_label, length, 1)
		self.y_label += get_ylist

		return x_decision, y_decision

	# Checks if there are legends - if the number of graphs is more than 1
	def _check_legends_(self, divisions):
		if divisions == 1:
			print("Legends not required - have a good title")
		else:
			if len(self.legends) != divisions:
				print("Please enter all legends to make the graph clearer")
				for i in range(0, divisions-len(self.legends)):
					self.legends.append(input())

	# Divisions here define the number of graphs in one subplot
	# TODO: More modularity will be great - Clean the code
	# TODO: How to handle the scatter plot if two points merge one above the other
	# TODO: Seperate out and as a part of the documentation write the following
	# Scatter plot cannot be superimposed on the top of a line plot. Instead if only one value needs to be marked use a marker
	# Or scatter the marker on top of the plot. 
	# This can be specified as a marker alone
	@dispatch(list, x_list= list, divisions= int, graph_type= str, marker_x= list, marker_y=list, position= str, trun_y_list= bool, back_trun= bool, mode= bool)
	def plot_graph(self, y_list, x_list =[], divisions = 1, graph_type='Line', marker_x=[], marker_y =[], position = 'upper right', trun_y_list= False, back_trun= True, mode= 'Test'):	

		count = 0
		label_count = 0	

		assert len(y_list)%divisions == 0, "In even partition - try giving divisions as list if the number of graphs vary"
		dim_1, dim_2 = self.choose_model(len(y_list)/divisions)
		print("Printing Dimensions", dim_2, dim_1)
		fig, ax = plt.subplots(dim_1, dim_2, squeeze= False)
		self.truncate_y_list(y_list, back_trun)
		self.generate_x_list(y_list, x_list)
		assert len(y_list) == len(x_list), "Error in internal functions"

		if mode == 'Final':
			x_decision, y_decision = self._check_title_label_(len(y_list)/divisions)
			self._check_legends_(divisions)
			plt.suptitle(self.title)		
		
		for i in range(0, dim_1):
			for j in range(0, dim_2):
				for k in range(0, divisions):
					if count < len(y_list):	
						if divisions == 1 or mode == 'Test':	
							if graph_type == 'Line':
								ax[i][j].plot(x_list[count], y_list[count])
							elif graph_type == 'Scatter':
								print("The x axis of the scatter plot must only contain the values for which y exist")
								ax[i][j].scatter(x_list[count], y_list[count])
						else:
							if graph_type == 'Line':
								ax[i][j].plot(x_list[count], y_list[count],label= self.legends[k])
							elif graph_type == 'Scatter':
								print("The x axis of the scatter plot must only contain the values for which y exist")
								ax[i][j].scatter(x_list[count], y_list[count], label= self.legends[k])
						count += 1

				# If markers are present scatter the markers
				if len(marker_x) != 0:
					pick_marker = ['o', 'x', '^']
					assert len(marker_x) == len(marker_y), "Number of markers must match"
					for m in range(len(marker_x)):
						assert len(marker_x[i]) == len(marker_y[i]), "Dimension mismatch in the marker values provided"
						#TODO: Must add label=''
						for n in range(0, len(marker_x[m])):
							ax[i][j].scatter(marker_x[m][n], marker_y[m][n], color='black', marker=pick_marker[m])
				
				#count += 1

				if mode == 'Final':
					if x_decision == 'D':
						ax[i][j].set_xlabel(self.x_label[label_count])
					if y_decision == 'D':
						ax[i][j].set_ylabel(self.y_label[label_count])
					label_count += 1
					if divisions != 1:
						ax[i][j].legend(loc= position)

		if mode == 'Final':
			if x_decision == 'C': 
				fig.text(0.5, 0.04, self.x_label[0], ha='center')
			else:
				fig.tight_layout(rect=[0, 0.03, 1, 0.95])
		
			if y_decision == 'C':
				fig.text(0.04, 0.5, self.y_label[0], va='center', rotation='vertical')
		
		plt.show()


	#TODO: Work on changing if the divisions given is a list
	@dispatch(list, list, list, str, bool, bool)
	def plot_graph(self, y_list, x_list, divisions, position= 'upper right', trun_y_list= False, back_trun = True):
		pass

# TODO: This function must be removed and must lead to a simpler calling funtion
def main():
	g = Graphs()
	
	# Remove this for demo.
	
	#g.set_labels(['Time in sec'], ['Linear'], "Linear graph")
	g.set_legends(['check'])
	
	#g.plot_graph([[1,2,3,4,5], [1,2,2,2,2], [1,2,3,4,5], [2,2,2,2,2]
	#			  ], mode = 'Final', divisions=2)

	#g.plot_graph([[1,2,3,4,5], [1,2,2,2,2], [1,2,3,4,5], [2,2,2,2,2]
	#			  ], mode = 'Final', divisions=2, position= 'upper left')

	#g.plot_graph([[1,2,3,4,5]], mode = 'Final', position= 'upper left', graph_type ='Scatter')

	g.plot_graph([[1,2,3,4,5], [1,2,2,2,2]], mode = 'Test', divisions=2, position= 'upper left')

if __name__ == '__main__':
	main()