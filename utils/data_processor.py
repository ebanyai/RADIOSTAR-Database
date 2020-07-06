"""
The imported data get processed here, data_processer.py contains the functions
and classes related to this process. The process() function can select the
required method.
"""

'''
def process(data_model):
    """
    This selects the processing function depending on the plot type
    (nucleosynthesis, supernova).
    
    Arguments:
        data_model -- a DataModel with the data and the input dictionary.
        
    Returns:
        PlotModel() -- containing the processed data and information for the plotting
    """
    
    if data_model.plot_type == "nucleosynthesis":
        return process_ns(data_model)
    elif data_model.plot_type == "supernova":
        return process_sn(data_model)
    return

'''
def process(data_model):
    """
    This function processes nucleosynthesis data. Both for 2D and 3D plots.
    
    Arguments:
        data_model -- a DataModel with the data and the input dictionary.
        
    Returns:
        PlotModel() -- containing the processed data and information for the plotting
    """
    # For easier referencing
    data = data_model.data
    input_dict = data_model.input_dictionary
    
    # Initialize values:
    multiplot = input_dict["multiplot"]
    xaxis = input_dict["xaxis"]
    dimension = input_dict["axis"]
    zaxis = input_dict["zaxis"] if dimension == "3" else "-"
    comparison_parameters = input_dict["compare"]
    
    # Here the function creates 'sets' depending on the values given in the
    # input file. Compared parameter(s), yield, and xaxis plus zaxis in case of a 3D
    # plot won't be included.
    set_parameters = data.columns.tolist()
    items_to_remove = ["yield"]
    items_to_remove.extend(comparison_parameters)
    items_to_remove.append(xaxis)
    if (dimension == "3") :
        items_to_remove.append(zaxis)
        
    set_parameters = [item for item in set_parameters if item not in items_to_remove]
         
    # Init a list fo the PlotDataModels
    plot_data_models = []
    
    # Group the data in to sets depending on the parameters in the
    # set_parameters variable.
    data_sets = data.groupby(set_parameters)
    
    for set_values, data_set in data_sets:
        
        # Group data by the given comparison parameter(s) in the input file (e.g.: element)
        data_grouped_by_comparison = data_set.groupby(comparison_parameters)
    
        # Initialize variables for PlotDataModel2D and PlotDataModel3D
        xx = []
        yy = []
        zz = []
        legend = []
        
        # Itarate through the sets
        for parameters, frame in data_grouped_by_comparison:
            xx.append(frame[xaxis].tolist())
            yy.append(frame["yield"].tolist())
            if (dimension == "3"):
                zz.append(frame[zaxis].tolist())
            legend.append(" ".join(str(parameters)))
            
        
        title = ", ".join(["{name}: {value}".format(name=x,value=y) for x, y in zip(set_parameters,set_values)])
        
        #TODO: set up a dict for different xaxis options (e.g. xlabel_dict = {"mass": "Initial Mass [$M_{\odot}$]", "metalicity": "Metalicity"} )
        xlabel = xaxis
        zlabel = zaxis
        
        if ( dimension == "2" ):
            plot_data_models.append(PlotDataModel2D(xx,yy,xlabel,legend,title))
        else:
            plot_data_models.append(PlotDataModel3D(xx,yy,zz,xlabel,zlabel,legend,title))
        
        if not multiplot: break
    
    return PlotModel(plot_data_models,dimension)

'''
#TODO: Implement
#NOTE: I'm not sure if this function is really necessary. Might depend on the
    # part where the data gets imported. I would suggest the DataFrame to be
    # similar to the one used for the supernova data if possible. Then process_sn()
    # and process() functions could be removed and porcess_ns() renamed to process().
    # Also dat_reader.ModelData won't need plot_type anymore.
    # (by Evelin)
def process_sn(data_model):
    """
    This function processes nucleosynthesis data.
    
    Arguments:
        data_model -- a DataModel with the data and the input dictionary.
        
    Returns:
        PlotModel() -- containing the processed data and information for the plotting
    """
    print("Supernova data processing has not been implemented yet.")
    return
'''

#NOTE: it might be better to include this part in the data_plotter.py file.
    # I couldn't decide. feel free to move it, thou don't forget to add
    # this to the beginning of this file (data_processer.py):
    # from data_processer import PlotModel(), PlotDataModel2D(), PlotDataModel3D()
    # (by Evelin)

class PlotModel():
    """
    This class is used to store the (list of) PlotDataModels and information on
    the plot dimension.
    
    Attributes:
        data -- Contains a list of PlotDataModel3D or PlotDataModel2D
        dimension -- dimension of the plot (2 or 3)
    """
    
    def __init__(self,data,dimension):
        self.data = data
        self.dimension = dimension
        

class PlotDataModel2D():
    """
    This class contains the required data and information for a 2D plot.
    
    Attributes:
        x -- x values
        y -- Yiel values
        xlabel -- label of the x axis
        ylabel -- label of the y axis
        legend -- legend list
        title -- title of the figure
        count -- returns the number of lines
    """
    
    def __init__(self,x,y,xlabel,legend,title):
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = "Yields [$M_{\odot}$]"
        self.legend = legend
        self.title = title
        self.count = len(self.y)
        
    
class PlotDataModel3D():
    """
    This class contains the required data and information for a 3D plot.
    
    Attributes:
        x -- x values
        y -- y values
        z -- Yield values
        xlabel -- label of the x axis
        ylabel -- label of the y axis
        zlable -- label of the z axis
        legend -- legend list
        title -- title of the figure
        count -- returns the number of lines
    """
    
    def __init__(self,x,y,z,xlabel,zlabel,legend,title):
        self.x = x
        self.y = z
        self.z = y
        self.xlabel = xlabel
        self.ylabel = zlabel
        self.zlabel = "Yields [$M_{\odot}$]"
        self.legend = legend
        self.title  = title
        self.count = len(self.y)
        
        
