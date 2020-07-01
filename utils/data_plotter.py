"""
The data_plotter.py takes care of the plotting.  The plot() function selects 
the plotting method (2D or 3D) and plots the figure(s) accordingly. Though 
plot_2d() or plot3d() can be used independently as well.
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot(plot_model):
    """
    This function calls the appropriate plotting function. 
    
    Arguments:
        plot_model -- a PlotModel containing the PlotDataModel and dimension information
    """
    
    print("Started plotting... ",end="")
    if (plot_model.dimension == "2"):
        for d in plot_model.data:
            plot_2d(d)
     
    elif (plot_model.dimension == "3"):
        for d in plot_model.data:
            plot_3d(d)
    else: 
        print("No suitable plot function was found. :(")
        return
    
    print("DONE")
    return

def plot_2d(plot_data_model):
    """
    Function for creating 2D plots. 
    
    Arguments:
        plot_data_model -- a PlotDataModel2D containing all necessary info
    """
    plt.figure()
    plt.xlabel(plot_data_model.xlabel)
    plt.ylabel(plot_data_model.ylabel)
    for i in range(0,plot_data_model.count):
        plt.plot(plot_data_model.x[i],plot_data_model.y[i],label=plot_data_model.legend[i],marker="o")
    ax = plt.gca()
    ax.set_yscale('log')
    plt.tick_params(axis='y', which='minor')
    plt.grid(which='minor',linestyle=':')
    plt.grid(which='major',linestyle='-')
    plt.title(plot_data_model.title)
    plt.legend()
    plt.show()

def plot_3d(plot_data_model):
    """
    Function for creating 3D plots.
    
    Arguments:
        plot_data_model -- a PlotDataModel3D containing all necessary info
    """
    #NOTE: might need more adjustments
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(0,plot_data_model.count):
        ax.scatter(plot_data_model.x[i], plot_data_model.y[i], plot_data_model.z[i],label=plot_data_model.legend[i],marker="o")
    
    plt.minorticks_on()
    ax.set_xlabel(plot_data_model.xlabel)
    ax.set_ylabel(plot_data_model.ylabel)
    ax.set_zlabel(plot_data_model.zlabel)
    ax.set_title(plot_data_model.title)
    plt.legend()
    return
