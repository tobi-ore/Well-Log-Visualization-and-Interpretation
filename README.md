# Well-Log-Visualization-and-Interpretation

## Objectives
The main objective of this project is to apply tools used in data science to carry out a basic petrophysical well log analysis. This involves transforming the well log measurements into reservoir properties like porosity,  clay content etc. The uptmost goal is to have as much information about the subsurface as possible.

## Data Source
The format of the data utilized for this project is the Log ASCII Standard (LAS) is a standard file-format common in the oil-and-gas and water well industries to store well log information. This file type is formatted as shown below where the `~CURVE INFORMATION` is the column header.

```
~VERSION INFORMATION
VERS.      2.0   :CWLS LOG ASCII STANDARD--VERSION 2.0
WRAP.      NO    :ONE LINE PER DEPTH STEP
~WELL INFORMATION
#MNEM.UNIT              DATA          DESCRIPTION
#================================================
STRT.FT                        101.00000 :START DEPTH
STOP.FT                       3666.00000 :STOP DEPTH
STEP.FT                          0.50000 :STEP
NULL.                         -999.00000 :NULL VALUE
COMP.   Data output from TerraStation II         : COMPANY
WELL.   Walakpa 1                                : WELL NAME
UWI.    50-023-20013                             : WELL UWI
API.    50-023-20013                             : WELL API
LOC.    9 20N 19W                                : WELL LOCATION
DATE.   NorthSlope.W08                           : WELL DATE
FLD.    No Project Selected                      : Project NAME
~CURVE INFORMATION
#================================================
M__DEPTH.FT                  :M__DEPTH
SP      .MV                  :SP
GR      .GAPI                :GR
CALI    .IN                  :CALI
BitSize .IN                  :BitSize
LL8     .OHMM                :LL8
ILM     .OHMM                :ILM
ILD     .OHMM                :ILD
RHOB    .G/CC                :RHOB
NPHI    .%                   :NPHI
DT      .US/F                :DT
MudWgt  .LBS/GAL             :MudWgt
~PARAMETER INFORMATION
#================================================
~OTHER INFORMATION
#================================================
~A
     101.00000    -999.00000    -999.00000    -999.00000      12.25000    -999.00000    -999.00000    -999.00000    -999.00000      -0.07240    -999.00000       9.00000
     101.50000    -999.00000    -999.00000    -999.00000      12.25000    -999.00000    -999.00000    -999.00000    -999.00000      -0.07360    -999.00000       9.00000
     102.00000    -999.00000    -999.00000    -999.00000      12.25000    -999.00000    -999.00000    -999.00000    -999.00000      -0.07480    -999.00000       9.00000
```
Data of this nature is in abundance due to the high volume of oil and gas exploration. In this project, data from the Department of the Interior U.S. Geological Survey repository of Wildcat Wells in the National Petroleum Reserve in Alaska will be used (https://certmapper.cr.usgs.gov/data/PubArchives/OF00-200/WELLS/WELLIDX.HTM). However, this project is not exclusive to this data, therefore, the workflow and codes could be applied to data from other database.

## Implementation
The analysis of the well logs will be carried out using R and Python. However, bash and wget will be utilized to download and manipulate the data into the desired format.

__Software__: `GitBash`, `R` and `Python`
__Packages__: `wget`, `bash`, `tidyverse`, `ggplot2`, `lasio` and `reticulate`

To download the data, run  `bash data_download.sh` in the command line.

To convert the data format from Las to csv which will be used as the input in R, a python script is utilized. The `reticulate` package is used to run the python script from R. If you don't have Python, skip this step and use the data in the data_csv folder to run the rest of the R script.

The various manipulations and operations on the well logs in done by running the R script called `data_manipulation.R`.

## Expected Products
_Log images_
A folder that contains all the well log images named after the name of the respective wells.

_Vsh images_
A folder that contains the plot of calculated volume of shale for each wells.

_Interpreted logs_
A folder that contains the final csv for each wells with the calculated properties.

## Author

[Tobi Ore](https://github.com/tobi-ore)

## License

[This project is licensed under the MIT License](https://choosealicense.com/licenses/mit/)

## Acknowledgments

[Dr Amy Hessl](https://github.com/hessllab)
