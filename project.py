# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 09:34:14 2019

@author: Tobi

description: This project involves using an open source tool to visualize and analysize well logs. 

"""
# import required packages and libraries
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import lasio

#%% Data Loading
# load the well data into one DataFrame
data = pd.DataFrame()  #empty DataFrame to serve as container for the data

directory = r"C:\Users\Tobi\Documents\Open_Data_Science\Project\data"  #Directory containing the well data in .las format

#loops through all the files in the directory, reads the csv and appends it to the data DataFrame
for file in os.listdir(directory):
    las = (lasio.read(os.path.join(directory, file)))  #load the LAS file
    well_data = las.df() #convert the LAS file to a panda DataFrame
    well_data['well_name'] = file[:-4]
    well_data['DEPTH'] = well_data.index
    well_data.rename_axis("DEPT", axis='index', inplace=True)  #rename the index M_DEPTH to DEPT
    data = data.append(well_data, sort=False,ignore_index=True)

#%% Cross match tables
#A table that shows the count of valid well log measurements for each wells
cross_match_1 = data.groupby('well_name').count()
cross_match_1.to_excel(r'cross_match_1.xls')

#A table that shows the percentage of valid well log measurements
cross_match_2 = cross_match_1.div(cross_match_1['DEPTH'], axis=0)*100
cross_match_2 = round(cross_match_2, ndigits=1)  #rounds the values to 1 decimal place
cross_match_2.to_excel(r'cross_match_2.xls')

#A table that puts "X" where there is at least one measurement of the logs for each well in the dataset
cross_match_3 = cross_match_2.replace(0,np.nan)
cross_match_3[cross_match_3>0] = 'X'
cross_match_3.to_excel(r'cross_match_3.xls')


#%% PHASE 2
#check for wells with BS and CALI
well_BS_CALI = []
for well in cross_match_3.index:
    if cross_match_3.loc[well]['CALI'] == "X" and cross_match_3.loc[well]['BITSIZE'] == "X":
        well_BS_CALI.append(well)
#%%
###creates a folder to save the log images
###checks if a folder called Log_Images already exists to avoid error
if os.path.exists(os.path.join(os.path.split(directory)[0], "Log_Images")):
    pass
else:
    os.mkdir(os.path.join(os.path.split(directory)[0], "Log_Images")) 

#plot for each well
for well in well_BS_CALI:
    MD = data[data['well_name']==well]['DEPTH']
    BS = data[data['well_name']==well]['BITSIZE']
    CALI = data[data['well_name']==well]['CALI']
    GR = data[data['well_name']==well]['GR']
    SP = data[data['well_name']==well]['SP']
    RHOB = data[data['well_name']==well]['RHOB']
    NPHI = data[data['well_name']==well]['NPHI']
    LL8 = data[data['well_name']==well]['LL8']
    ILM = data[data['well_name']==well]['ILM']
    ILD= data[data['well_name']==well]['ILD']
    DT= data[data['well_name']==well]['DT']
    
    
    fig, ax = plt.subplots(nrows=1, ncols=5,figsize=(20,30), sharey=True)
    fig.suptitle("Well {} Log Display".format(well), fontsize=25)
    #fig.subplots_adjust(top=0.93)
    
    ax[0].invert_yaxis()
    ax[0].set_ylabel('MD (M)',fontsize=20)
    ax[0].yaxis.grid(True)
    
    ##Track 1
    ##Bit_size and Caliper
    ax_BS = ax[0].twiny()
    ax_BS.plot(BS,MD, color='brown')
    ax_BS.set_xlabel('BS (in)',color='brown',fontsize=15)
    ax_BS.tick_params('x',colors='brown')  ##change the color of the x-axis tick label
    ax_BS.set_xlim([5,25])

    ax_CALI = ax[0].twiny()
    ax_CALI.plot(CALI,MD, color='red',ls=':')
    ax_CALI.set_xlabel('CALI (in)',color='red',fontsize=15)
    ax_CALI.tick_params('x',colors='red')
    ax_CALI.set_xlim([5,25])
    ax_CALI.spines['top'].set_position(('outward',40)) ##move the x-axis up

    ax_BS.fill_betweenx(MD,BS,CALI, color='yellow')
    ax_BS.grid(True,alpha=0.5)

    ax[0].get_xaxis().set_visible(False) #removing the x-axis label at the bottom of the fig

    ##Track 2
    ##Gamma_ray and SP 
    ax_GR = ax[1].twiny()
    ax_GR.plot(GR,MD, color='black')
    ax_GR.set_xlabel('GR (API)',color='black',fontsize=15)
    ax_GR.tick_params('x',colors='black')  ##change the color of the x-axis tick label
    ax[1].get_xaxis().set_visible(False)
    ax[1].yaxis.grid(True)

    #ax_GR.fill_betweenx(MD,GR,75, where = GR>75, color='brown')
    #ax_GR.fill_betweenx(MD,GR,75, where = GR<75, color='yellow')
    ax_GR.grid(True,alpha=0.5)
    
    ax_SP = ax[1].twiny()
    ax_SP.plot(SP,MD, color='blue')
    ax_SP.set_xlabel('GR (API)',color='blue',fontsize=15)
    ax_SP.tick_params('x',colors='blue')  ##change the color of the x-axis tick label
    ax_SP.spines['top'].set_position(('outward',40)) ##move the x-axis up
    

    ##Track 3
    ##Resistivities
    ax_ILD = ax[2].twiny()
    ax_ILD.set_xlim(0.1,100)
    ax_ILD.set_xscale('log')
    ax_ILD.grid(True)
    ax_ILD.spines['top'].set_position(('outward',80))
    ax_ILD.set_xlabel('ILD[m.ohm]', color='red')
    ax_ILD.plot(ILD,MD, label='ILD[m.ohm]', color='red')
    ax_ILD.tick_params(axis='x', colors='red')    
    
    ax_ILM = ax[2].twiny()
    ax_ILM.set_xlim(0.1,100)
    ax_ILM.set_xscale('log')
    ax_ILM.plot(ILM, MD, label='ILM[m.ohm]', color='purple') 
    ax_ILM.spines['top'].set_position(('outward',40))
    ax_ILM.set_xlabel('ILM[m.ohm]', color='purple')    
    ax_ILM.tick_params(axis='x', colors='purple')
    
    ax_LL8 = ax[2].twiny()
    ax_LL8.set_xlim(0.1,100)
    ax_LL8.set_xscale('log')
    ax_LL8.plot(LL8,MD, '--',label='LL8[m.ohm]', color='black') 
    ax_LL8.spines['top'].set_position(('outward',0))
    ax_LL8.set_xlabel('LL8[m.ohm]',color='black')
    ax_LL8.tick_params(axis='x', colors='black')
    
    ax[2].get_xaxis().set_visible(False)
    ax[2].yaxis.grid(True)
    ax_LL8.grid(True,alpha=0.5)
    
    #Track 4
    ##NPHI and RHOB
    ax_NPHI = ax[3].twiny()
    ax_NPHI.set_xlim(40,-15)
    ax_NPHI.invert_xaxis()
    ax_NPHI.plot(NPHI, MD, label='NPHI[%]', color='green') 
    ax_NPHI.spines['top'].set_position(('outward',0))
    ax_NPHI.set_xlabel('NPHI[%]', color='green')    
    ax_NPHI.tick_params(axis='x', colors='green')
    
    ax_RHOB = ax[3].twiny()
    ax_RHOB.set_xlim(1.95,2.95)
    ax_RHOB.plot(RHOB, MD,label='RHOB[g/cc]', color='red') 
    ax_RHOB.spines['top'].set_position(('outward',40))
    ax_RHOB.set_xlabel('RHOB[g/cc]',color='red')
    ax_RHOB.tick_params(axis='x', colors='red')
    
    ax[3].get_xaxis().set_visible(False)
    ax[3].yaxis.grid(True)
    ax_RHOB.grid(True,alpha=0.5)
    
    #Track 5
    ##DT
    ax_DT = ax[4].twiny()
    ax_DT.grid(True)
    ax_DT.set_xlim(300,0)
    ax_DT.spines['top'].set_position(('outward',0))
    ax_DT.set_xlabel('DT[us/ft]')
    ax_DT.plot(DT, MD, label='DT[us/ft]', color='blue')
    ax_DT.set_xlabel('DT[us/ft]', color='blue')    
    ax_DT.tick_params(axis='x', colors='blue')
    
    ax[4].get_xaxis().set_visible(False)
    ax[4].yaxis.grid(True)
    ax_DT.grid(True,alpha=0.5)
    
    fig.savefig(r'{}\Log_Images\{}.png'.format(os.path.split(directory)[0], well), dpi=300)
    plt.close()
    
#%%
#Petrophysical calculations

#organize the data by wells in a dictionary
data_dict = {}
for well in well_BS_CALI:
    data_dict[well] = data[data['well_name']==well]

##Volume of Shale
for well in well_BS_CALI:
    data_dict[well]['VSH_linear'] = (data_dict[well]['GR'] - data_dict[well]['GR'].min())/(data_dict[well]['GR'].max() - data_dict[well]['GR'].min()) #Linear Gamma Ray
    data_dict[well]['VSH_larionov_young']=0.083*(2**(3.7*data_dict[well]['VSH_linear'])-1)   #Larionov (1969) - Tertiary rocks
    data_dict[well]['VSH_larionov_old']=0.33*(2**(2*data_dict[well]['VSH_linear'])-1)        #Larionov (1969) - Older rocks
    data_dict[well]['VSH_clavier']=1.7-(3.38-(data_dict[well]['VSH_linear']+0.7)**2)**0.5    #Clavier (1971)
    data_dict[well]['VSH_steiber']=0.5*data_dict[well]['VSH_linear']/(1.5-data_dict[well]['VSH_linear'])               #Steiber (1969) - Tertiary rocks

###creates a folder to save the VSH images
###checks if a folder called Vsh_Images already exists to avoid error
if os.path.exists(os.path.join(os.path.split(directory)[0], "Vsh_Images")):
    pass
else:
    os.mkdir(os.path.join(os.path.split(directory)[0], "Vsh_Images")) 

#plot for each well
for well in well_BS_CALI:
    MD = data_dict[well]['DEPTH']
    GR = data_dict[well]['GR']
    VSH_linear = data_dict[well]['VSH_linear']
    VSH_larionov_young = data_dict[well]['VSH_larionov_young']
    VSH_larionov_old = data_dict[well]['VSH_larionov_old']
    VSH_clavier = data_dict[well]['VSH_clavier']
    VSH_steiber = data_dict[well]['VSH_steiber']
    
    
    fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(20,30), sharey=True)
    fig.suptitle("Well {} Log Display".format(well), fontsize=25)
    #fig.subplots_adjust(top=0.93)
    
    ax[0].invert_yaxis()
    ax[0].set_ylabel('MD (M)',fontsize=20)
    ax[0].yaxis.grid(True)
    
    ##Track 1
    ##Gamma Ray
    ax_GR = ax[0].twiny()
    ax_GR.plot(GR,MD, color='black')
    ax_GR.set_xlabel('GR (API)',color='black',fontsize=15)
    ax_GR.tick_params('x',colors='black')  ##change the color of the x-axis tick label
    ax[0].get_xaxis().set_visible(False)
    ax[0].yaxis.grid(True)
    ax_GR.grid(True,alpha=0.5)
    
    ##Track2
    ##All the calculated Vsh
    ax_1 = ax[1].twiny()
    ax_1.plot(VSH_larionov_young,MD, color='green')
    ax_1.set_xlabel('VSH_larionov_young',color='green',fontsize=15)
    ax_1.tick_params('x',colors='green')  ##change the color of the x-axis tick label
    ax_1.set_xlim([0,1])
    ax_1.spines['top'].set_position(('outward',160))

    ax_2 = ax[1].twiny()
    ax_2.plot(VSH_larionov_old,MD, color='red')
    ax_2.set_xlabel('VSH_larionov_old',color='red',fontsize=15)
    ax_2.tick_params('x',colors='red')
    ax_2.set_xlim([0,1])
    ax_2.spines['top'].set_position(('outward',40)) ##move the x-axis up

    ax_3 = ax[1].twiny()
    ax_3.plot(VSH_clavier, color='blue')
    ax_3.set_xlabel('VSH_clavier',color='blue',fontsize=15)
    ax_3.tick_params('x',colors='blue')
    ax_3.set_xlim([0,1])
    ax_3.spines['top'].set_position(('outward',80))
    
    ax_4 = ax[1].twiny()
    ax_4.plot(VSH_steiber,MD, color='orange')
    ax_4.set_xlabel('VSH_steiber',color='orange',fontsize=15)
    ax_4.tick_params('x',colors='orange')
    ax_4.set_xlim([0,1])
    ax_4.spines['top'].set_position(('outward',120))
    
    ax_5 = ax[1].twiny()
    ax_5.plot(VSH_linear,MD, color='purple')
    ax_5.set_xlabel('VSH_linear',color='purple',fontsize=15)
    ax_5.tick_params('x',colors='purple')
    ax_5.set_xlim([0,1])
    ax_5.spines['top'].set_position(('outward',0))
    
    ax[1].get_xaxis().set_visible(False)
    ax[1].yaxis.grid(True)
    ax_1.grid(True,alpha=0.5)
    
    fig.savefig(r'{}\Vsh_Images\{}.png'.format(os.path.split(directory)[0], well), dpi=300)
    plt.close()


##porosity
den_ma, den_fl = 2.65, 1.1
for well in well_BS_CALI:
    data_dict[well]['PHID'] = (data_dict[well]['RHOB'] - den_ma) / (den_fl - den_ma)
    data_dict[well]['PHIND'] = ((data_dict[well]['NPHI']**2 + data_dict[well]['PHID']**2)/2)**0.5
    
###creates a folder to save the new log files
###checks if a folder called Interpreted_Logs already exists to avoid error
if os.path.exists(os.path.join(os.path.split(directory)[0], "Interpreted_Logs")):
    pass
else:
    os.mkdir(os.path.join(os.path.split(directory)[0], "Interpreted_Logs")) 

#plot for each well
for well in well_BS_CALI:
    data_dict[well].to_csv(r'{}\Interpreted_Logs\{}.csv'.format(os.path.split(directory)[0], well))
