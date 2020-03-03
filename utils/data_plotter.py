#TODO: This python file is supposed to do the plotting
import matplotlib.pyplot as plt

def plot(plot_model):
    #TODO: switch case for diff. plots
    plot_ns_2d(plot_model)
    return

def plot_ns_2d(plot_model):
    plt.figure()
    plt.xlabel('Initial Mass [$M_{\odot}$]')
    plt.ylabel('Yields [$M_{\odot}$]')
    plt.xlabel(plot_model.xlabel)
    plt.ylabel(plot_model.ylabel)
    for i in range(0,plot_model.Count()):
        plt.plot(x=plot_model.x[i],y=plot_model.y[i],label=plot_model.label[i])
        plt.scatter(x=plot_model.x[i],y=plot_model.y[i],label=plot_model.label[i])
    ax = plt.gca()
    ax.set_yscale('log')
    plt.tick_params(axis='y', which='minor')
    plt.grid(which='minor',linestyle=':')
    plt.grid(which='major',linestyle='-')
    plt.title(plot_model.title)
    plt.legend()
    plt.show()

def plot_ns_3d():
    return

def plot_sn():
    return
    

