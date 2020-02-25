import pandas as pd
import os
import re

"""
Reads the text file with the the different input values and puts it
in a dictionary
"""
def read_input_file(file_name):
    print("Reading input dictionary... ",end="")
    input_dictionary = {}
    with open(file_name, "r")  as input_file:
        lines = input_file.readlines()
        for line in lines[1:]:
            key = line.split(":")[0]
            values = line.split(":")[1].split()
            input_dictionary[key]=values
    
    #TODO: check for not accepted keys    
    print("DONE")
    return input_dictionary
        
"""
Reads the species file. If no specific file is given, it uses the included species.dat
file from the /utils directory.
"""
def read_species_file(file_name=os.path.dirname(os.path.abspath(__file__))+os.sep+"species.dat"):
    print("Reading species file... ",end="")
    column_names = ["Name","A","Z","Yield"]
    species_dt = pd.read_table(file_name,sep="\s+",names=column_names)
    print("DONE")
    return species_dt
    
def read_data_file(data_path,input_dict,source_type="fruity"):
    data = pd.DataFrame()
    plot_type = input_dict["Plot_type"][0].lower()
    
    print("Checking for suitable data reader...")
    if (plot_type == "nucleosynthesis"):
        if (source_type == "fruity"):
            data = read_data_file_ns_fruity(data_path,input_dict)
        else:
            print("No implemented method was found.")
    elif (plot_type == "supernova"):
        if (source_type == "fruity"):
            data = read_data_file_sn_furity()
        else:
            print("No implemented method was found.")
    else:
        print("No implemented method was found.")   
    
    return data

"""

"""
def read_data_file_ns_fruity(data_path,input_dict):
    dataset = pd.DataFrame(columns=["data"])
    column_names = ["Name","A","Z","Yield"]

    files = create_file_list(data_path,input_dict)
    print(files)
    print("Reading file(s)... ",end="")
    for file_name in files:
        print(data_path+os.sep+file_name)
        data = pd.read_table(data_path+os.sep+file_name,sep="\s+",names=column_names,skiprows=1)
        dataset["data"].loc[file_name[11:23]]= data
        print(file_name)
    print("DONE")
    return dataset


def read_data_file_sn_furity(data_path,input_dict):
    print("This data reading method have not been implemented yet.")
    return None

"""
Returns the file list depending on the given values in the input file 
(mass, metallicity, C13 pocket type, rotation). This function is used for fruity data set.
"""
def create_file_list(data_path,input_dict):
    print("Gather file list depending on the given values in the input dictionary... ",end="")
    all_files=os.listdir(data_path)
    needed_files=[]
    
    mass = "|".join(input_dict["Mass"]) if input_dict.get("Mass") else "[0-9]p[0-9]"
    metallicity = "|".join(input_dict["Metallicities"]) if input_dict.get("Metallicities") else "m[0-9]p[0-9]|zsun"
    pocket = "|".join(input_dict["C13_Pocket"]) if input_dict.get("C13_Pocket") else "0|T"
    rotation = "|".join(input_dict["Rotation"]) if input_dict.get("Rotation") else "[0-9][0-9]"
    
    pattern_to_match = r'yields_tot_m({mass})({metallicity})_({pocket})({rotation})' \
        .format(mass=mass,metallicity=metallicity,pocket=pocket,rotation=rotation)
    
    print(pattern_to_match)
    
    r = re.compile(pattern_to_match)
    
    for file in all_files:
            if r.match(file):
                needed_files.append(file)
    print("DONE")
    return needed_files