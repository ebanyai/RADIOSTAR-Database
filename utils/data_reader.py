import pandas as pd
import numpy as np
import os
import re
import sys


class DataModel():
    
    def __init__(self,input_path,data_path,species_path=None):
        self.input_dictionary = read_input_file(input_path)
        self.species = read_species_file(species_path);
        self.data_path = data_path
        self.plot_type = self.input_dictionary["plot_type"]
        self.plot_dimension = self.input_dictionary["axis"]
        self.data = self.read_data_file()
        

    """
    
    """
    def read_data_file(self):
        data_source_type = self.input_dictionary["data_source_type"]
        
        print("Checking for suitable data reader...")
        if (self.plot_type == "nucleosynthesis"):
            if (data_source_type == "fruity"):
                self.read_data_file_ns_fruity_private()
            else:
                print("No implemented method was found.")
        elif (self.plot_type == "supernova"):
            if (data_source_type == "fruity"):
                self.read_data_file_sn_furity_private()
            else:
                print("No implemented method was found.")
        else:
            print("No implemented method was found.")   
        
        return self.data
    
    """
    
    """
    def read_data_file_ns_fruity_private(self):
        elements = self.input_dictionary["element"]
        dataset = pd.DataFrame(columns=["mass","metalicity","c13_pocket","rotation","element","yield"])
        column_names = ["element","A","Z","Yield"]
    
        files = self.create_file_list_private()
        print("Reading file(s)... ",end="")
        for file_name in files:
            data = pd.read_table(self.data_path+os.sep+file_name,sep="\s+",names=column_names,skiprows=1)
            
            data = data.loc[data['element'].isin(elements)]
            values = [e for e in data["Yield"]]
            
            #TODO: this part should be done with named regex groups (mass/metallicities above 10 will screw it)
            index = file_name[11:24]
            mass = file_name[12:15].replace("sun","14m3") #this might be wrong
            metalicity = file_name[16:19].replace("sun","0.014")
            pocket = file_name[20:21]
            rotation = file_name[21:23]
            for e, v in zip(elements,values):
                dataset.loc[index+e] = [mass,metalicity,pocket,rotation,e,v]
            
        dataset["mass"] = dataset["mass"].apply(convert_values)
        dataset["metalicity"] = dataset["metalicity"].apply(convert_values)

        self.data=dataset
        print("DONE")
        return 
    
    
    def read_data_file_sn_furity_private(self):
        print("This data reading method have not been implemented yet.")
        return None
    
    """
    Returns the file list depending on the given values in the input file 
    (mass, metallicity, C13 pocket type, rotation). This function is used for fruity data set.
    """
    def create_file_list_private(self):
        print("Gather file list depending on the given values in the input dictionary... ",end="")
        all_files=os.listdir(self.data_path)
        needed_files=[]
        
        
        #TODO: Regex (might) needed to be updated for larger mass/metaliccity values (> m10/z10)
        mass = "|".join(self.input_dictionary["mass"]) if self.input_dictionary.get("mass") else "[0-9]p[0-9]"
        metalicity = "|".join(self.input_dictionary["metalicity"]) if self.input_dictionary.get("metalicity") else "z[0-9]p[0-9]|zsun"
        pocket = "|".join(self.input_dictionary["c13_pocket"]) if self.input_dictionary.get("c13_pocket") else "0|T"
        rotation = "|".join(self.input_dictionary["rotation"]) if self.input_dictionary.get("rotation") else "[0-9][0-9]"
        
        pattern_to_match = r'yields_tot_m({mass})({metalicity})_({pocket})({rotation})' \
            .format(mass=mass,metalicity=metalicity,pocket=pocket,rotation=rotation)
        
        print(pattern_to_match)
        
        r = re.compile(pattern_to_match)
        
        for file in all_files:
                if r.match(file):
                    needed_files.append(file)
        print("DONE")
        return needed_files

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
            key = line.split(":")[0].lower()
            values =  line.split(":")[1].split()
            input_dictionary[key]=values
    
    #TODO: check keys (I've partly implemented them)
    input_dictionary["compare"] = [c.lower() for c in input_dictionary["compare"]]
    
    input_dictionary["plot_type"] = input_dictionary["plot_type"][0].lower() if input_dictionary.get("plot_type") else raise_error("Plot_type")
    input_dictionary["axis"] = input_dictionary["axis"][0] if input_dictionary.get("axis") else raise_error("Axis")
    input_dictionary["data_source_type"] = input_dictionary["data_source_type"][0].lower() if input_dictionary.get("data_source_type") else raise_error("Data_source_type")
    input_dictionary["xaxis"] = input_dictionary["xaxis"][0] if input_dictionary.get("xaxis") else raise_error("Zaxis")
    if input_dictionary["axis"] == "3":
        input_dictionary["zaxis"] = input_dictionary["zaxis"][0] if input_dictionary.get("zaxis") else raise_error("Zaxis")

            
    
    multiplot = False 
    if input_dictionary.get("multiplot"):
        multiplot = True if input_dictionary["multiplot"][0] in ["True","true","yes","y","1"] else False
                
    input_dictionary["multiplot"] = multiplot
    
    print("DONE")
    return input_dictionary
        
"""
Reads the species file. If no specific file is given, it uses the included species.dat
file from the /utils directory.
"""
def read_species_file(file_name):
    print("Reading species file... ",end="")
    file_name = file_name if file_name != None else os.path.dirname(os.path.abspath(__file__))+os.sep+"species.dat"
    column_names = ["Name","A","Z","Yield"]
    species_dt = pd.read_table(file_name,sep="\s+",names=column_names)
    species_dt["Name"] = species_dt["Name"].str.casefold() 
    print("DONE")
    return species_dt


"""
This function should done the 
"""    
def convert_values(x):
    result = np.nan
    try:         
        if "p" in x :
            result = float(x.replace("p","."))        
        elif "m" in x :
            result = float(x.split("m")[0])/(10**float(x.split("m")[1]))
        else:
            result = float(x)
    except:
        raise ValueError("Could not convert value: {x}".format(x=x))
    
    return result


def raise_error(name):
    """Exception raised for errors in the input.
    
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """
    message = "{name} is not included in the input file.".format(name=name)
    sys.exit(message)