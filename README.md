# RADIOSTAR-Database

A python3 script that plots the Nucleosynthesis Yield data from the F.R.U.I.T.Y database available online ([here](http://fruity.oa-teramo.inaf.it/)) and Supernova Yield from [arxiv.org](https://arxiv.org/abs/1805.09640)). It can be used to plot and compare yield curves for all the parameters in the fruity model.

# The Code Library
The library contains 4 separate codes, one reference file, and examplary input files.

### plot.py: 
Running this code creates the figure(s). At the moment the code have to be manually edited to set the file paths.

Planned feature(s):
- Read input file paths from terminal arguments. E.g.:

```plot.py. -i input_file.txt -d data_files_path```



## Utils folder
It contains the different data processing files (import, process, plot). The idea was to separete the code by function so new features/methods can be more easily implemented in the future.

### data_reader.py
This file contains the methods for reading the reference, the input and the data files. New data reading methods can be implemented for different source of yield data. 

The reading methods can be invoked (´read_species_file()´, ´read_inputfile()´, ´read_data_file()´ etc.) separateley - e.g. for debugging - or by using the DataModel class which invokes them during initialization.

Suggested improvements:
- init DataModel class with a more complex method so DataModel could be assigned/initialized without any obligatory argument and attributes could be assigned later.
E.g.:
´´´
def _init(self,input_path=None,data_path=None,species_path=None):
	self.input_dictionary = read_input_file(input_path) if input_path not None else {}
	...
´´´
	
### data_processor.py

### data_plotter.py