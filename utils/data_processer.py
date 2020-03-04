import itertools
import pandas as pd
#TODO: prepare the data for plotting


"""
    THIS ONE IS STILL HEAVILY UNDER CONSTRUCTION :D
"""
def process(data_reader):
	# For easier referencing
    data = data_reader.data
    input_dict = data_reader.input_dictionary
    
    # Initialize values:
    plot_type = input_dict["plot_type"][0].lower()
    multiplot = input_dict["multiplot"]
    xaxis = input_dict["xaxis"][0]
    
    
    set_parameters = data.columns.to_list()
    elements = ["yield"]
    items_to_remove = [*elements]
    items_to_remove.extend(input_dict["compare"])
    items_to_remove.extend(input_dict["xaxis"])
    print("col_list:",end=" ")
    print(set_parameters)
    print("items_to_remove:",end=" ")
    print(items_to_remove)
    for item in items_to_remove:
        if item in set_parameters: set_parameters.remove(item)
         
    print("new col_list: ",end=" ")
    print(set_parameters)
    
    comparison_parameters = input_dict["compare"]
    
    plot_data_models = []
    data_sets = data.groupby(set_parameters)
    
    print("works")
    for set_values, data_set in data_sets:
        
        # Group data by the given comparison parameter(s) in the input file (e.g.: element)
        data_grouped_by_comparison = data_set.groupby(comparison_parameters)
    
        # Initialize variables for PlotDataModel2D
        x = []
        y = []
        legend = []
        for parameters, frame in data_grouped_by_comparison:            
            x.append(frame[xaxis].tolist())
            y.append(frame["yield"].tolist())
            legend.append(" ".join(parameters))
            
        
        title = ", ".join(["{name}: {value}".format(name=x,value=y) for x, y in zip(set_parameters,set_values)])
        #TODO: set up a dict for different xaxis options (e.g. xlabel_dict = {"mass": "Initial Mass [$M_{\odot}$]", "metalicity": "Metalicity"} )
        xlabel = xaxis
       
        plot_data_models.append(PlotDataModel2D(x,y,xlabel,legend,title))
    
    
    return PlotModel(plot_data_models,plot_type,multiplot)

class PlotModel():
    
    def __init__(self,data,plot_type,multiplot=False):
        self.data = data
        self.plot_type = plot_type
        self.multiplot = multiplot
        
    
class PlotDataModel2D():
    def __init__(self,x,y,xlabel,legend,title):
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = "Yields [$M_{\odot}$]"
        self.legend = legend
        self.title = title
        
    def Count(self):
        return len(self.y)