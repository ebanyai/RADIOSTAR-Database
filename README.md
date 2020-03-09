# RADIOSTAR-Database

A python3 script that plots the Nucleosynthesis Yield data from the F.R.U.I.T.Y database available online ([here](http://fruity.oa-teramo.inaf.it/)) and Supernova Yield from [arxiv.org](https://arxiv.org/abs/1805.09640)). It can be used to plot and compare yield curves for all the parameters in the fruity model.

# The Code Library
The library contains 4 separate codes, one reference file, and examplary input files.

### plot.py: 
Running this code creates the figure(s). At the moment the code have to be manually edited to set the file paths.

Planned feature(s):
- Read input file paths from argument. E.g.:
```plot.py. -i input_file.txt -d data_files_path```



## Utils folder
It contains the different data processing files (import, process, plot). 

`data_reader.py`
	
`data_processer.py`

`data_plotter.py`