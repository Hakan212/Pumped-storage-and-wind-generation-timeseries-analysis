import pandas as pd
import matplotlib.pyplot as plt #import libraries

edata=pd.read_csv('espeni.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read overall generation
edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage generation

pstorage=edataps.POWER_ELEXM_PS_MW[0:208756]#slice as pumped storage data is longer
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

begin_day='2012-06-29 00:00:00' #2012-06-29 is the earliest date useable 
final_day='2020-10-02 00:00:00' #2020-10-02 is the latest date useable
edata=edata[begin_day:final_day] #slice datasets
edataps=edataps[begin_day:final_day]
fig,axes=plt.subplots(nrows=4,ncols=1,figsize=(7,15))#plot
axes[0].plot_date(edata.index,edata.POWER_ESPENI_MW,'b-',label='Overall electrical demand (a)',linewidth=0.5)#plot 'Elexon sum plus embedded and net imports'
axes[0].set(ylim=(0,60000))
axes[1].plot_date(edata.index,edata.POWER_ELEXM_WIND_MW,'y-',label='Wind generation (b)',linewidth=0.5)#plot wind gen

axes[2].plot_date(edata.index,edata.POWER_NGEM_EMBEDDED_WIND_GENERATION_MW,'g-',label='Embedded wind (c)',linewidth=0.5)#plot embedded wind

axes[3].plot_date(edataps.index,edataps.POWER_ELEXM_PS_MW,'c-',label='Pumped storage generation (d)',linewidth=0.5)#plot pumped storage
axes[3].set(ylim=(-4000,4000))
for i in range(4):#labels for graph
    axes[i].legend(fontsize=14)
    axes[i].set_xlabel('Time (half-hours)')
    axes[i].set_ylabel('Energy (MW)')
plt.show()