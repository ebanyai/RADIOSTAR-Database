import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


"""
This function calls the appropriate plotting function. The plot model contains
the necessary information (plot data, dimension, )
"""
def plot(plot_model):
    print("Started plotting... ",end="")
    if (plot_model.dimension == "2"):
        if (plot_model.multiplot):
            for d in plot_model.data:
                plot_2d(d)
        else:
            plot_2d(plot_model.data[0])
     
    elif (plot_model.dimension == "3"):
        print("3D plotting not have been fully implemented yet.",end=" ")
        if (plot_model.multiplot):
            for d in plot_model.data:
                plot_3d(d)
        else:
            plot_3d(plot_model.data[0])       
    else: 
        print("No suitable plot function was found. :(")
        return
    print("DONE")
    return

"""
Function for creating 2D plots.
"""
def plot_2d(plot_model):
    plt.figure()
    plt.xlabel(plot_model.xlabel)
    plt.ylabel(plot_model.ylabel)
    for i in range(0,plot_model.Count()):
        plt.plot(plot_model.x[i],plot_model.y[i],label=plot_model.legend[i],marker="o")
    ax = plt.gca()
    ax.set_yscale('log')
    plt.tick_params(axis='y', which='minor')
    plt.grid(which='minor',linestyle=':')
    plt.grid(which='major',linestyle='-')
    plt.title(plot_model.title)
    plt.legend()
    plt.show()


"""
Function for creating 3D plots.
"""
def plot_3d(plot_model):
    #TODO: 
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(0,plot_model.Count()):
        ax.scatter(plot_model.x[i], plot_model.y[i], plot_model.z[i],label=plot_model.legend[i],marker="o")
    
    plt.minorticks_on()
    ax.set_xlabel(plot_model.xlabel)
    ax.set_ylabel(plot_model.ylabel)
    ax.set_zlabel(plot_model.zlabel)
    ax.set_title(plot_model.title)
    plt.legend()
    return
