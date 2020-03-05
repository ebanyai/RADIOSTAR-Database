import numpy as np
import itertools

"""
This selects the processing function depending on the plot type 
(nucleosynthesis, supernova) and the dimension (2 or 3).
"""
def process(data_model):
    if data_model.plot_type == "nucleosynthesis":
        return process_ns(data_model)
    elif data_model.plot_type == "supernova":
        return process_sn(data_model)
    return


"""
This function processes nucleosynthesis data. Both for 2D and 3D
"""
def process_ns(data_model):
	# For easier referencing
    data = data_model.data
    input_dict = data_model.input_dictionary
    
    # Initialize values:
    multiplot = input_dict["multiplot"]
    xaxis = input_dict["xaxis"] 
    dimension = input_dict["axis"] 
    zaxis = input_dict["zaxis"] if dimension == "3" else "-"
    
    
    set_parameters = data.columns.to_list()
    elements = ["yield"]
    items_to_remove = [*elements]
    items_to_remove.extend(input_dict["compare"])
    items_to_remove.extend([input_dict["xaxis"]])
    if (dimension == "3") :
        items_to_remove.extend(input_dict["zaxis"])
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
        z = []
        legend = []
        for parameters, frame in data_grouped_by_comparison:            
            x.append(frame[xaxis].tolist())
            y.append(frame["yield"].tolist())
            if (dimension == "3"):
                z.append(frame[zaxis].tolist())
            legend.append(" ".join(str(parameters)))
            
        
        title = ", ".join(["{name}: {value}".format(name=x,value=y) for x, y in zip(set_parameters,set_values)])
        
        #TODO: set up a dict for different xaxis options (e.g. xlabel_dict = {"mass": "Initial Mass [$M_{\odot}$]", "metalicity": "Metalicity"} )
        xlabel = xaxis
        zlabel = zaxis
        
        if ( dimension == "2" ):
            plot_data_models.append(PlotDataModel2D(x,y,xlabel,legend,title))
        else:
            plot_data_models.append(PlotDataModel3D(x,y,z,xlabel,zlabel,legend,title))
        
        
    return PlotModel(plot_data_models,dimension,multiplot)



"""
This function processes nucleosynthesis data.
"""
def process_sn():
    return


#NOTE: it might be better to include this part in the data_plotter.py file
    # feel free to move it, thou don't forget to add this to the beginning of 
    # this file (data_processer.py):
    # from data_processer import PlotModel(), PlotDataModel2D(), PlotDataModel3D()
"""
This class is used to store the (list of) PlotDataModels, information on the plot type and 
if it's a multiplot or not.
"""
class PlotModel():
    
    def __init__(self,data=[],dimension="2",multiplot=False):
        self.data = data
        self.dimension = dimension
        self.multiplot = multiplot
        

"""
This class contains the required data and information for one 2D plot. 
The values x, y and legend should be lists for multiline plots.
"""    
class PlotDataModel2D():
    def __init__(self,x,y,xlabel,legend,title):
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = "Yields [$M_{\odot}$]"
        self.legend = legend
        self.title = title
        
    """
    Count returns the number of lines.
    """
    def Count(self):
        return len(self.y)
    
"""
This class contains the required data and information for one 3D plot. 
The values x, y, z and legend should be lists for multiline plots.
"""
class PlotDataModel3D():
    
    #TODO: 
    def __init__(self,x,y,z,xlabel,zlabel,legend,title):
        self.x = x
        self.y = y
        self.z = z
        self.xlabel = xlabel
        self.ylabel = "Yields [$M_{\odot}$]"
        self.zlabel = zlabel
        self.legend = legend
        self.title  = title
        
        
    """
    Count returns the number of lines.
    """
    def Count(self):
        return len(self.y)