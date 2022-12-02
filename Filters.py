import Visualise_Fourier as vf
import plot_graph as pg

# TODO: Understand the effects of applying filters -- Integrate with the original class.
# TODO: Low pass filter, High pass filter, Curve fitting (Linear and non linear)
# TODO: Fourier of a Fourier and see the graph that it produces
# TODO: Effect of ----- (check in the notes)
class Filter:
    # Visualise the effects of the filter using graph
    def visualise_filter(self, y_select, x_select):
        g_obj = pg.Graphs()
        g_obj.set_labels(['Frequency'],['Amplitude'], 'Low pass Filter')
        print("Selected length", len(x_select), len(y_select))
        g_obj.plot_graph([y_select], x_list=[x_select], mode='Final')
    
    # Calculates general average -- no weights considered
    def calc_average(self, x_axis, y_axis):
        maximum = max(y_axis)
        minimum = min(y_axis)
        average = (maximum + minimum)/2

        return average
    
    # TODO: Can weighted average be calculated and what will be the difference
    def weighted_average(self, x_axis, y_axis):
        pass

    # Implements a low pass filter to understand the effect of this frequencies in voice
    def low_pass_filter(self, x_axis, y_axis, graph = False):
        x_select = []
        y_select = []

        print("Actual length", len(x_axis), len(y_axis))
        average = self.calc_average(x_axis, y_axis)
        print("value of average is ", average)
        for i in range(0, len(y_axis)):
            if y_axis[i] <= average:
                x_select.append(x_axis[i])
                y_select.append(y_axis[i])
        
        if graph:
            self.visualise_filter(y_select, x_select)

    # Implements a high pass filter to understand the effect of high frequencies 
    def high_pass_filter(self, x_axis, y_axis, graph = False):
        x_select = []
        y_select = []

        print("Actual length", len(x_axis), len(y_axis))
        average = self.calc_average(x_axis, y_axis)
        for i in range(0, len(y_axis)):
            if y_axis[i] >= average:
                x_select.append(x_axis[i])
                y_select.append(y_axis[i])

        if graph:
            self.visualise_filter(y_select, x_select)


    # Implements the effects of removing very high and very low frequencies	
    def band_pass_filter(self, x_axis, y_axis, graph = False):
        x_select = []
        y_select = []

        print("Actual length", len(x_axis), len(y_axis))
        average = self.calc_average(x_axis, y_axis)
        # TODO: This must be changed based on the requirement
        range_factor = 0.5
        for i in range(0, len(y_axis)):
            if y_axis[i] >= (average - range_factor) and y_axis[i] <= (average + range_factor):
                x_select.append(x_axis[i])
                y_select.append(y_axis[i])
        
        if graph:
            self.visualise_filter(y_select, x_select)


