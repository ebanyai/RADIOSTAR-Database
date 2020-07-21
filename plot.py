from utils.data_reader import DataModel 
import utils.data_plotter as dp
import utils.data_processor as dpr
import sys, os


#NOTE:
# grab  files' paths from command line ? this would be a really nice addition and 
# the plot.py file could be left unchanged when running on different data located
# elsewhere. Usage could be something like this: 
# plot.py -i input_file.txt -d data_file.txt -r rerence_file.txt
# -r could be optional
# (by Evelin)

file_name = input('what file would you like open?')
with open(file_name)as input:
    lines = input.readlines()
    lines_output = ''.join(lines)
    #print(lines_output)
    print(file_name)

with open(sys.argv[1], 'r') as file:
    for line in file:
        print(line)
        
# Getting the data model ready. It includes the species, input_dictionar and 
# a DataFrame with the imported yield data.
#data_model = DataModel(r"D:\Projects\Python\RadiostarDB\inputfile_2D_N.txt",r"D:\Projects\Python\RadiostarDB\fruityYields")
data_model = DataModel(r"inputfile.txt", r"fruityYields")

# Process the data for the plots
data_to_plot = dpr.process(data_model)

# Create figure(s)
dp.plot(data_to_plot)


    
    