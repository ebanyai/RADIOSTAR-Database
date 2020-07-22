import pandas as pd
import numpy as np
import os
import re
import sys

def read_input_file(file_name):
    """
    Reads the text file with the the different input values and puts it
    in a dictionary
    
    Arguments:
        file_name -- The name of the file (full path)
        
    Returns:
        A dictionary with the parameters and values for the plot
    """
    print("Reading input dictionary... ")
    input_dictionary = {}
    
    with open(file_name, "r")  as input_file:
        lines = input_file.readlines()
        for line in lines[1:]:
            key = line.split(":")[0].lower()
            values =  line.split(":")[1].split()
            input_dictionary[key]=values
    
    #TODO: check keys (not all checks are implemented -- e.g. compare)
    # This parts checks for possible errors or missing values in the input file.
    # Sets some of  values to lower case and/or makes them a single 'string' value
    # instead of 'list'
    input_dictionary["compare"] = [c.lower() for c in input_dictionary["compare"]]
    
    input_dictionary["plot_type"] = input_dictionary["plot_type"][0].lower() if input_dictionary.get("plot_type") else raise_error("Plot_type")
    input_dictionary["data_source_type"] = input_dictionary["data_source_type"][0].lower() if input_dictionary.get("data_source_type") else raise_error("Data_source_type")
    input_dictionary["axis"] = input_dictionary["axis"][0] if input_dictionary.get("axis") else raise_error("Axis")
    input_dictionary["xaxis"] = input_dictionary["xaxis"][0] if input_dictionary.get("xaxis") else raise_error("Zaxis")
    if input_dictionary["axis"] == "3":
        input_dictionary["zaxis"] = input_dictionary["zaxis"][0] if input_dictionary.get("zaxis") else raise_error("Zaxis")

    # set the multiplot value to a 'boolean'
    multiplot = False
    if input_dictionary.get("multiplot"):
        multiplot = True if input_dictionary["multiplot"][0] in ["True","true","yes","y","1"] else False
    
    input_dictionary["multiplot"] = multiplot
    
    print("DONE")
    return input_dictionary
        

def read_species_file(file_name):
    """
    Reads the species file.
    
    Arguments:
        file_name -- If no specific file was given, it uses the included
                     species.dat file from the /utils directory.
    Returns:
        A DataFrame() with the species
    """
    print("Reading species file... ")
    file_name = file_name if file_name != None else os.path.dirname(os.path.abspath(__file__))+os.sep+"species.dat"
    column_names = ["Name","A","Z","Yield"]
    species_dt = pd.read_table(file_name,sep="\s+",names=column_names)
    print("DONE")
    return species_dt

    
#NOTE: DataModel.data should be as consistent as it could be.
    # If the DataFrame is similarly built there's no need to create new
    # data processing functions later. So I suggest to use this kind of layout:
    # DataFrame(columns=["param1","param2","param3",...,"element","yield"])
    # (by Evelin)

def read_data_file(data_path,input_dictionary):
    """
    Reads yield data.
    
    Returns:
        A pandas DataFrame()
    """
    
    # For shorter referencing:
    data_source_type = input_dictionary["data_source_type"]
    plot_type = input_dictionary["plot_type"]
    
    
    data = pd.DataFrame()
    
    print("Checking for suitable data reader...")
    if (plot_type == "nucleosynthesis"):
        if (data_source_type == "fruity"):
            data = read_data_file_ns_fruity(data_path,input_dictionary)
        else:
            print("No implemented method was found.")
    elif (plot_type == "supernova"):
        if (data_source_type == "limongi"):
            data = read_data_file_sn_limongi(data_path,input_dictionary)
        else:
            print("No implemented method was found.")
    else:
        print("No implemented method was found.")
    
    return data

def read_data_file_ns_fruity(data_path,input_dictionary):
    """
    Reads fruity nucleosynthesis data.
    
    Returns:
        A pandas DataFrame()
    """
    
    elements = input_dictionary["element"]
    dataset = pd.DataFrame(columns=["mass","metalicity","c13_pocket","rotation","element","yield"])
    column_names = ["element","A","Z","Yield"]

    files = create_file_list(data_path,input_dictionary)
    print("Reading file(s)... ")
    for file_name in files:
        data = pd.read_table(data_path+os.sep+file_name,sep="\s+",names=column_names,skiprows=1)
        
        data = data.loc[data['element'].isin(elements)]
        values = [e for e in data["Yield"]]
        
        # NOTE: Regex might needed to be updated to better fit the fruity naming conventions.
        # A regex used to acquire the parameter values from the file name
        pattern= r"(?P<index>yields_tot_m(?P<mass>[0-9]+[pm][0-9]+|sun)z(?P<metalicity>[0-9]+[pm][0-9]+|sun)_(?P<pocket>T|0)(?P<rotation>[0-9]{2})_)"
        r = re.compile(pattern)
        m = r.match(file_name)
        
        index = m.group("index")
        mass = m.group("mass")
        metalicity = m.group("metalicity").replace('sun','14m3')
        pocket = m.group("pocket")
        rotation = m.group("rotation")
        
        # Each element should get a row in the Dataframe (containing its name and yield value too).
        for e, v in zip(elements,values):
            dataset.loc[index+e] = [mass,metalicity,pocket,rotation,e,v]
        
    # Converting the string values for mass/metalicity to float
    dataset["mass"] = dataset["mass"].apply(convert_values)
    dataset["metalicity"] = dataset["metalicity"].apply(convert_values)

    print("DONE")
    return dataset


def read_data_file_sn_limongi(data_path,input_dictionary):
    """
    Reads limongi supernova data.
    
    Returns:
        A pandas DataFrame()
    """
    print('Reading File...')
    column_names=['Element','13','15','20','25','30','40','60','80','120']

    dataset = pd.DataFrame(columns=["mass","metalicity","rotation","element","yield"])
    
    data = pd.read_table(data_path,sep="\s+& ",names=column_names)
    title_list=[]
    #create a list of the subtitles in with file with their index
    for i in range (0,data.shape[0]):
        if data['Element'].astype(str).str[0][i]=='\\':
            title_list.append((data['Element'][i],i))
            print(data['Element'][i])
    

    rotation = (input_dictionary["rotation"]) if input_dictionary.get("rotation") else ['0','150','300']
    metalicity = (input_dictionary["metalicity"]) if input_dictionary.get("metalicity") else ['0','-1','-2','-3']
    mass = (input_dictionary["mass"]) if input_dictionary.get("mass") else ['13', '15', '20', '25', '30', '40', '60', '80', '120']
    elements = input_dictionary["element"]
    #I didn't use regex as the subtitles in the file had too many brackets and back slashes
    #making it a little complex
    #so i used a nested loos which creates a string using the input values
    #and looks for the string and its index from title_list #
    #and slices the dataframe to read the data
    for i in mass:
        for j in metalicity:
            for k in rotation:
                index='\cutinhead{v=%s km/s - [Fe/H]=%s}' %(k,j)
                for l in range(len(title_list)):
                    if title_list[l][0]==index:
                        sub_data=data[title_list[l][1]+1:title_list[l+1][1]]
                        sub_data['120']=sub_data['120'].apply(lambda x: float(x.replace("\\",'').replace(' ',''))) #remove the '\\' in the end
                        sub_data = sub_data.loc[data['Element'].isin(elements)]
                        values = [e for e in sub_data[i]]
                        #adding the values in the dataframe
                        for e, v in zip(elements,values):
                            dataset.loc[index+i+e] = [i,j,k,e,v]
    return dataset

def create_file_list(data_path,input_dictionary):
    """
    Returns the file list depending on the given (or not given) values in the input file
    (mass, metallicity, C13 pocket type, rotation). This function is used for fruity data set.
    
    Returns:
        A 'list' with the file names.
    """
    
    print("Gather file list depending on the given values in the input dictionary... ")
    
    # Gathers all the available file names.
    all_files=os.listdir(data_path)
    
    #NOTE: This part might need some modification. Depending on the fruity naming
        # conventions:
        #   - for mass: m[0-9][p][0-9]|msun --> m[0-9][pm][0-9]|msun or
        #     the middle [] extended with other chars
        #   - for metalicty: z[0-9][m][0-9]|zsun --> z[0-9][pm][0-9]|zsun or
        #     the midle [] extended with other possible chars
        #   - I don't know if mass/metalicity values can get higher than 9?
        # (by Evelin)
    mass = "|".join(input_dictionary["mass"]) if input_dictionary.get("mass") else "m[0-9][p][0-9]|msun"
    metalicity = "|".join(input_dictionary["metalicity"]) if input_dictionary.get("metalicity") else "z[0-9][m][0-9]|zsun"
    pocket = "|".join(input_dictionary["c13_pocket"]) if input_dictionary.get("c13_pocket") else "0|T"
    rotation = "|".join(input_dictionary["rotation"]) if input_dictionary.get("rotation") else "[0-9][0-9]"
    
    # Creates the regex
    pattern_to_match = r'yields_tot_({mass})({metalicity})_({pocket})({rotation})' \
        .format(mass=mass,metalicity=metalicity,pocket=pocket,rotation=rotation)
    r = re.compile(pattern_to_match)
    print(pattern_to_match)
    # Selects the matching files
    needed_files = [file for file in all_files if r.match(file)]
    
    print("DONE")
    return needed_files

#NOTE: I'm not sure if it's fully implemented. Sorry, I'm not fully aware of the
    # fruity naming conventions. Adjusments might needed.
    # (by Evelin)
def convert_values(x):
    """
    Converts fruity parameter values (mass, metalicity) to float.
    
    Arguments:
        x -- the number to converted
        
    Returns:
        Float
    
    """
    
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
    """
    Stops running the code if the input file has missing parameter(s).
    
    Attributes:
        name -- name of the parameter missing from the input file
    """
    message = "{name} is not included in the input file.".format(name=name)
    sys.exit(message)

class DataModel():
    """
    This class contains the imported data, species, and input dictionary and
    methods for importing the data
    
    Attributes:
        input_dictionary -- Dictionary with the input values
        species -- DataFrame with the species data (Name, A, Z, Yield)
        plot_type -- type of the plot (nucleosynthesis, supernova)
        data -- DataFrame with the imported models data (e.g. metalicity, mass,
                element, yield).
        
    """
    
    def __init__(self,input_path,data_path,species_path=None):
        self.input_dictionary = read_input_file(input_path)
        self.species = read_species_file(species_path);
        self.plot_type = self.input_dictionary["plot_type"]
        self.data = read_data_file(data_path,self.input_dictionary)

