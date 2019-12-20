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

This well logs are subsurface informations and therefore have associated stratigraphic data, stored as text files. An example of this text file for the LAS file above is:
```

Dept. of the Interior
U.S. Geological Survey
Energy Resources Team

Selected Data from Fourteen Wildcat Wells in 
the National Petroleum Reserve in Alaska

USGS Open File Report 00-200 


Wildcat Well Walakpa 1 - Depths to Selected Stratigraphic Horizons

WELL NAME         ROCK UNIT                                   DEPTH, FEET
WALAKPA 1         Surficial Deposits and/or Gubik Formation      19
WALAKPA 1         Torok Formation                                50
WALAKPA 1         Pebble Shale Unit                            1700
WALAKPA 1         Kingak Shale                                 2090
WALAKPA 1         Sag River Sandstone                          3220
WALAKPA 1         Shublik Formation                            3260
WALAKPA 1         Basement Complex                             3630

Data Source
Table 15.3. - Total depth and depths to selected stratigraphic horizons
for Government-drilled wells on the North Slope of Alaska., 
in:

Gryc, George, Ed., 1988, Geology and exploration of the National Petroleum
     Reserve in Alaska, 1974 to 1982, U.S. Geological Survey Professional 
     Paper 1399, Pgs. 322 - 324.
```
The stratigraphic information is used in the interpretation of the well log data.

## Implementation
The analysis of the well logs will be carried out using Python. However, bash and wget will be utilized to download and manipulate the data into the desired format.

__Software__: `GitBash`, R and `Python`
__Packages__: `wget`, `tidyverse`, `ggplot2`, `reticulate`, and `lasio`.

To download the data, run  `bash data_download.sh` in the command line.

After downloading the files from the database, using the reticulate package convert the format of the files to csv using this command `source_python('data_conversion.py')`. check the project.Rmd file for more details.

Run the data_manipulation.R scripts to carryout the operations. check the project.Rmd file for more details.

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
