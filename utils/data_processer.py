import itertools
import pandas as pd
#TODO: prepare the data for plotting


"""
    THIS ONE IS STILL HEAVILY UNDER CONSTRUCTION :D
"""
def process(data_reader):
	#TODO: some magic
    data = data_reader.data
    input_dict = data_reader.input_dictionary
    xaxis = input_dict["xaxis"][0]
    
    
    col_list = data.columns.to_list()
    elements = ["yield"]
    items_to_remove = [*elements]
    items_to_remove.extend(input_dict["compare"])
    items_to_remove.extend(input_dict["xaxis"])
    print("col_list:",end=" ")
    print(col_list)
    print("items_to_remove:",end=" ")
    print(items_to_remove)
    for item in items_to_remove:
        if item in col_list: col_list.remove(item)
         
    print("new col_list: ",end=" ")
    print(col_list)
    
    set_items = []
    
    for item in col_list:
        values = data[item].unique().tolist()
        set_items.append(values)
    
    parameters_to_compare = input_dict["compare"]
     
    #    items_to_compare = [input_dict[c.lower()] for c in parameters_to_compare ]
    #    print(items_to_compare)
    #    sets_to_compare = itertools.product(*items_to_compare)
    #    for p in sets_to_compare:
    #        print(p)
    
    print(set_items)
    prod = [*itertools.product(*set_items)]
    
    print(prod)

    # This will work for only one plot right now (for prod[0])
    
    
    # Might be a better way to do it, but I' just rearranged the dataframe before uploading...
    data_set = data
    for value, name in zip(prod[0],col_list):
         data_set = data_set.loc[data_set[name] == value]
    
    #print(data_set)
    

    
    
    data_grouped_by_comparison = data_set.groupby(parameters_to_compare)
    
    x = []
    y = []
    legend = []
    for state, frame in data_grouped_by_comparison:
        #print(f"First 2 entries for {state!r}")
        #print("------------------------")
        #print(frame["yield"], end="\n\n")
        
        x.append(frame[xaxis].tolist())
        y.append(frame["yield"].tolist())
        legend.append(" ".join(state))
        
    
    title = ", ".join(["{name}: {value}".format(name=x,value=y) for x, y in zip(col_list,prod[0])])
    #TODO: set up a dict for different xaxis options (e.g. xlabel_dict = {"mass": "Initial Mass [$M_{\odot}$]", "metalicity": "Metalicity"} )
    xlabel = xaxis
   
    return PlotModel2D(x,y,xlabel,legend,title)

class PlotModel2D():
    
    def __init__(self,x,y,xlabel,legend,title):
        
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = "Yields [$M_{\odot}$]"
        self.legend = legend
        self.title = title
        
    def Count(self):
        return len(self.y)