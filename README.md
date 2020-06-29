# RADIOSTAR-Database

A python3 script that plots the Nucleosynthesis Yield data from the FRUITY database available online ([here](http://fruity.oa-teramo.inaf.it/)) and Supernova Yield from ([arxiv.org](https://arxiv.org/abs/1805.09640)). It can be used to plot and compare yield curves for all the available parameters in the FRUITY database.

Future may include:

- Adding surface composition support.
- Adding net and total yields switch.
- Adding monash and snuppat support, or perhaps coming up with a standarized form.
- Adding temporal evolution of element/isotope (surface composition with time, TP number or Total mass).

# The Code Library
The library contains 4 separate codes, one reference file, and examplary input files.

### plot.py:
Running this code creates the figure(s). At the moment, the code has to be manually edited to set the file paths.

Planned feature(s):
- Either open a choose file dialog or read input file paths from terminal arguments. E.g.:

```plot.py -i input_file.txt -d data_files_path```

- Perhaps the input file and the data files could have a related name so they would automatically match with each other. If not found, a default option could be used instead.


## Utils folder
It contains the different data processing files (import, process, plot). The idea is to separate the code by function so new features/methods can be more easily implemented in the future.

### data_reader.py
This file contains the methods for reading the reference, the input and the data files. New data reading methods can be implemented for different sources of yield data.

The reading methods can be invoked (`read_species_file()`, `read_input_file()`, `read_data_file()` etc.) separateley - e.g. for easier debugging - or by using the DataModel class which invokes some of them during initialization.

Suggested improvements:
- init DataModel class with a more complex method so `DataModel` could be assigned/initialized without any obligatory arguments, and attributes could be assigned later.
E.g.:
```
def __init__(self,input_path=None,data_path=None,species_path=None):
	self.input_dictionary = read_input_file(input_path) if input_path not None else {}
	...
```
	
### data_processor.py
This file contains methods to prepare the data for plotting. At the moment, only nucleosynthesis data processing is implemented. Note: Maybe there is no need for other methods. See the comments in the `data_processor.py` file for details.

It also contains 3 classes. `PlotModel` which is used for plotting alongside with the two `PlotDataModel`\*. The `process` function returns a `PlotModel`, containing a list of the PlotDataModels. `PlotDataModel`s are storing the data, and plotting parameteres (such as `title`, `x_label` etc.).

### data_plotter.py
This file creates the plots from the `PlotModels`. It has a function both for 2D and 3D plots.
