#TODO: This one should do the magic, and be as simple as it can.

# 0. import files from the utils folder
import utils.data_reader as dr
# data_processer.py
# data_plotter.py

# 1. read the data 
# 1.1 grab inputfiles' paths from command line ? - though this could be implemented later
# usage could be something like this: 
# plot.py -i input_file.txt -d data_file.txt -r rerence_file.txt
# -r could be optional (maybe? I guess it's not changes much)
# 1.2 read the data
# input = read_input(input_file)
# data = read_data(data_file)
# reference = read_reference(reference_file)

species = dr.read_species_file()
print(species)

input_dictionary = dr.read_input_file(r"D:\Projects\Python\RadiostarDB\inputfile_2D_N.txt")

files = dr.create_file_list(r"D:\Projects\Python\RadiostarDB\fruityYields",input_dictionary)

d = dr.read_data_file(r"D:\Projects\Python\RadiostarDB\fruityYields",input_dictionary)

# 2. process the data for the plots
# data_to_plot = process(input,data,reference)

# 3. plot the data
# plot(processed_data,input) 

# that's should be all.