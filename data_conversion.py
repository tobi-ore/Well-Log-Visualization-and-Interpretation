import os
import lasio

directory = r".\data"  #Directory containing the well data in .las format

###creates a folder to save the new csv data files
###checks if a folder called data_csv already exists to avoid error
if os.path.exists(os.path.join(os.path.split(directory)[0], "data_csv")):
    pass
else:
    os.mkdir(os.path.join(os.path.split(directory)[0], "data_csv")) 

#loops through all the files in the directory, reads the las and converts it to csv
for file in os.listdir(directory):
    las = (lasio.read(os.path.join(directory, file)))  #load the LAS file
    well_data = las.df() #convert the LAS file to a panda DataFrame
    well_data['well_name'] = file[:-4]
    well_data['DEPTH'] = well_data.index
    well_data.rename_axis("DEPT", axis='index', inplace=True)  #rename the index M_DEPTH to DEPT
    well_data.to_csv(r'{}\data_csv\{}.csv'.format(os.path.split(directory)[0], file[:-4]))