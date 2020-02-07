"""
Reads the text file with the the different input values and puts it
in a dictionary
"""
def read_input_file(file_name):
    input_dictionary = {}
    with open(file_name, "r")  as input_file:
        lines = input_file.readlines()
        for line in lines[1:]:
            key = line.split(":")[0]
            values = line.split(":")[1].split()
            input_dictionary[key]=values
    
    #TODO: check for not accepted keys of values         
    return input_dictionary
        

def read_data_file(file_name):
    #TODO: everything :-D
    return