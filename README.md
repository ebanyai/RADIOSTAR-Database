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
This file contains the methods for reading the referenc, the input and the data files. New data reading methods can be implemented for different source of yield data.
	
### data_processor.py

### data_plotter.py