#Yield Plotting

-A python3 script that plots the Nucleosynthesis Yield vs Mass data from the F.R.U.I.T.Y database available online (http://fruity.oa-teramo.inaf.it/) and Supernova Yield from https://arxiv.org/abs/1805.09640. It can be used to plot and compare yield curves for all the parameters in the fruity model.

-The plots can be created by editing the input file and running the code. 



-Code
	the code contains 3 parts:
	1) 2D plot for the Nucleosynthesis yield: It creates a 2D plot of yield vs mass fo different rotation, metalicities, C13 Pockets and Elements. Multiple data from a single parameter can be plotted for comparison. 
	
	2) 3D plot for Nucleosynthesis yield: It creates a 3D plot of mass (x-axis), Metalicity (y-axis) and Yield (z-axis). 
	
	3) 2D plot for Supernova yield: It creates a 2D yield vs mass plot for different elements and velocuti and z value. The user has an option to display plots for multiple elements or multiple metalicities on a single plot.

	It uses a reference file for the plotting of the Nucleosynthesis therefore it is necessary to make sure that the element must be present in the reference file before plotting.
	
	libraries: Matplotlib, glob, mpl_toolkits, copy, re and copy. The user must make sure that these libraries are installed before using the code


	
-Data
	The data for the Nucleosynthesis  Yield is taken from http://fruity.oa-teramo.inaf.it/. The file name remains the same as at the time of downloading the zipped folder containing multiple files.
	
	The name describes the parameter values for those yields. it can be broken into many parts in the following way:

	yields_tot_m1p3z2m5_000_20200102_231441 -->
	Yields_tot_ + m=1p3(1.3) + z= 2m5(0.00002) + C13_Pocket=0(Standard) + Rotation 00 + Date 2020/01/02
 	
	In the input file, the mass and the metalicity has to be written in the similar format as in the downloaded file i.e. z1m2 should be used for z=0.01 and 1p5 for mass = 1.5. 

	All the data for nucleosynthesis yield is saved in the folder named Yield data and the data for the supernova yield is saved in the file named supernova_yield in the parent directory.



-Input File
	The input file needs to be generated differently for the 3 typed of plots
	1) For Nucleosynthesis yield, 2D plot:
		Elements: List of Elements in the same format as in the reference file seperated by a space. Example He4 Al26 C12
		Plot_type:  Nucleosynthesis
		Axis: 2
		Metalicities:  Matalicity values  seperated by spaces in the same format as in the downloaded file. Example z1m2 z1m3 z1m4 
		Compare:  The parameter whose multiple plots have to be drawn on a single axis. Possible values {Elements, C13_Pocket, Metalicit,Rotation}
		C13_Pocket: T denotes extended and 0 denotes standard. Both can be given separated by a space
		Rotation:  {00,10,30,60} separated by spaces

	
	2) For Nucleosynthesis, 3D plot:
		Elements: Same as above
		Plot_type: Nucleosynthesis
		Axis: 3
		Mass: Same format as in the the of the yield files, seperated by spaces. {1p3 1p5 2p0 2p5 3p0 4p0 5p0 6p0}
		Rotation: Same as above
		C13_Pocket: Same as above
		
	3) For Supernova yields:
		Plot_type: supernova
		Elements: Same as above
		Axis: 2
		Vel: Possible values{0, 150, 300} separated by spaces
		Z: Possible values{0,-1,-2,-3} separated by space
		Compare: {Elements, Metalicities}
	
	The format is as follows:
	Parameter: Value
	Parameter name followed by ':' followed by a space and the value
	Look for example folder for examples of each type 


#end
	
