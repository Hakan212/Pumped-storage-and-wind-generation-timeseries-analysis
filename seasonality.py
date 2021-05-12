import pandas as pd
import matplotlib.pyplot as plt #import libraries
from statsmodels.tsa.seasonal import seasonal_decompose

edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage
edata=pd.read_csv('espeni.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')
edataps=edataps[0:208756] #pumped storage data is a bit longer than demand data
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

beginday1='2019-02-11 00:00:00' #set slice dates for the dataset, over a period of 6 years
finalday1='2019-02-18 00:00:00' 
beginday2='2016-02-08 00:00:00'
finalday2='2016-02-15 00:00:00'
beginday3='2013-02-04 00:00:00'
finalday3='2013-02-11 00:00:00'

windgen=edata.POWER_ELEXM_WIND_MW+edata.POWER_NGEM_EMBEDDED_WIND_GENERATION_MW #combine embedded and non-embedded generation

edataps1=edataps[beginday1:finalday1] #slice dataset for pumped storage across all years
edataps2=edataps[beginday2:finalday2]
edataps3=edataps[beginday3:finalday3]
edataps=[edataps1,edataps2,edataps3] #combine into array

edata1=windgen[beginday1:finalday1]#slide dataset for wind generation across all years
edata2=windgen[beginday2:finalday2]
edata3=windgen[beginday3:finalday3]
edata=[edata1,edata2,edata3] #combine into array

fig,(ax1,ax2,ax3,ax4,ax5,ax6)=plt.subplots(6,1,figsize=(10,20))#start plotting

edataps2.index=edataps1.index #plot all weeks in same index
edataps3.index=edataps1.index
edata2.index=edata1.index
edata3.index=edata1.index

splot=[0,0,0]#pre-define values
wplot=[0,0,0]

for i in range(3):
    splot[i]=pd.DataFrame(edataps[i].POWER_ELEXM_PS_MW,edataps[i].index)#form dataframes
    wplot[i]=pd.DataFrame(edata[i],edata[i].index)
    splot[i]=seasonal_decompose(splot[i],model='additive',period=48)#perform seasonal decomposition
    wplot[i]=seasonal_decompose(wplot[i],model='additive',period=48)

splot[0].observed.plot(ax=ax1,alpha=0.5,label='2019 PS generation (a)',ylim=(-4000,3000))#plot observed pumped storage data across all years in 1st figure
splot[1].observed.plot(ax=ax1,alpha=0.5,label='2016 PS generation')
splot[2].observed.plot(ax=ax1,alpha=0.5,label='2013 PS generation')
ax1.axhline(y=0,color='r',linestyle='-') #draw horizontal line
ax1.set(xlabel='',ylabel='Power generated (MW)') #set axis labels

x=['2019-02-11 00:00:00','2019-02-12 00:00:00','2019-02-13 00:00:00','2019-02-14 00:00:00','2019-02-15 00:00:00','2019-02-16 00:00:00','2019-02-17 00:00:00','2019-02-18 00:00:00'] #write x-axis labels
xt=['Mon','Tue','Wed','Thurs','Fri','Sat','Sun'] #change x axis

splot[0].seasonal.plot(ax=ax2,alpha=0.5,label='2019 PS seasonality (b)',ylim=(-4000,3000))#plot seasonality of pumped storage data across all years in 2nd figure
splot[1].seasonal.plot(ax=ax2,alpha=0.5,label='2016 PS seasonality')
splot[2].seasonal.plot(ax=ax2,alpha=0.5,label='2013 PS seasonality')
ax2.set(xlabel='',ylabel='Seasonality (MW)') #set axis labels
ax2.axhline(y=0,color='r',linestyle='-') #draw horizontal line

wplot[0].observed.plot(ax=ax3,label='2019 Wind generation (a)') #plot observed data of wind generation across all years in 3rd figure 
wplot[1].observed.plot(ax=ax3,label='2016 Wind generation')
wplot[2].observed.plot(ax=ax3,label='2013 Wind generation')
ax3.set(xlabel='',ylabel='Power Generated (MW)') #set axis labels

wplot[0].seasonal.plot(ax=ax4,alpha=0.5,label='2019 Wind seasonality (b)',ylim=(-600,400)) #plot seasonality of wind generation across all years in 3 different figures
wplot[1].seasonal.plot(ax=ax5,alpha=0.5,label='2016 Wind seasonality (c)',color='orange',ylim=(-600,400))
wplot[2].seasonal.plot(ax=ax6,alpha=0.5,label='2013 Wind seasonality (d)',color='green',ylim=(-600,400))

ax4.set(xlabel='',ylabel='Seasonality (MW)') #set axis labels
ax5.set(xlabel='',ylabel='Seasonality (MW)')
ax6.set(xlabel='',ylabel='Seasonality (MW)')

ax=[ax1,ax2,ax3,ax4,ax5,ax6]
for i in range (6):
    ax[i].legend() #set legends for all figures
    ax[i].set_xticks(x) #replace x ticks for all figures
    ax[i].set_xticklabels(xt)
