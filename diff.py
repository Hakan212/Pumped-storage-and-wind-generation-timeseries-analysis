import pandas as pd
import matplotlib.pyplot as plt #import libraries
from statsmodels.tsa.seasonal import seasonal_decompose

edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage
edata=pd.read_csv('espeni.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')
edataps=edataps[0:208756] #pumped storage data is a bit longer than demand data
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

begin_day='2012-06-29 00:00:00' #2012-06-29 is the earliest date useable
final_day='2020-10-02 23:30:00' #2020-10-02 is the latest date useable

edataps=edataps[begin_day:final_day] #slice dataset for desired range
edata=edata[begin_day:final_day]
windgen=edata.POWER_ELEXM_WIND_MW+edata.POWER_NGEM_EMBEDDED_WIND_GENERATION_MW
daymin=edataps.POWER_ELEXM_PS_MW.resample('D').min()#resample the dataset to take min of pumped storage
daymin=daymin.to_frame()
daymax=edataps.POWER_ELEXM_PS_MW.resample('D').max()#resample the dataset to take the max of pumped storage
daymax=daymax.to_frame()

maxwind=windgen.resample('D').max() #resample the dataset to take the max of wind generation
maxwind=maxwind.to_frame()
minwind=windgen.resample('D').min() #resample the dataset to take the min of wind generation
minwind=minwind.to_frame()
fig,(ax1,ax2,ax3,ax4,ax5)=plt.subplots(5,2,figsize=(13,18))

maxplot=pd.DataFrame(daymax.POWER_ELEXM_PS_MW,daymax.index)
minplot=pd.DataFrame(daymin.POWER_ELEXM_PS_MW,daymin.index)

maxplot=seasonal_decompose(maxplot,model='additive',period=7*4*12)#seasonal decomposition
minplot=seasonal_decompose(minplot,model='additive',period=7*4*12)
maxwind=seasonal_decompose(maxwind,model='additive',period=7*4*12)
minwind=seasonal_decompose(minwind,model='additive',period=7*4*12)

diffwind=maxwind.trend-minwind.trend #plot difference in trends
diffplot=maxplot.trend-minplot.trend
maxplot.observed.plot(ax=ax1[0],label='Maximum pumped storage generation (a)') #plot seasonal decompositions with labels
maxplot.trend.plot(ax=ax2[0],label='Trend of maximum pumped storage (b)')
maxplot.seasonal.plot(ax=ax3[0],label='Seasonality of maximum pumped storage (c)',ylim=(-600,400))
maxplot.resid.plot(ax=ax5[0],label='Residuals of maximum pumped storage (e)')

minplot.observed.plot(ax=ax1[0],label='Minimum pumped storage generation')
minplot.trend.plot(ax=ax2[0],label='Trend of minimum pumped storage')
minplot.seasonal.plot(ax=ax4[0],color='orange',label='Seasonality of minimum pumped storage (d)',ylim=(-600,400))
minplot.resid.plot(ax=ax5[0],alpha=0.5,label='Residuals of minimum pumped storage')

maxwind.observed.plot(ax=ax1[1],label='Maximum wind generation (a)')
maxwind.trend.plot(ax=ax2[1],label='Trend of maximum wind generation (b)',ylim=(0,13000))
maxwind.seasonal.plot(ax=ax3[1],label='Seasonality of maximum wind generation (c)',ylim=(-3000,3000))
maxwind.resid.plot(ax=ax5[1],label='Residuals of maximum wind generation (e)')

minwind.observed.plot(ax=ax1[1],label='Minimum wind generation',alpha=0.5)
minwind.trend.plot(ax=ax2[1],label='Trend of minimum wind generation')
minwind.seasonal.plot(ax=ax4[1],color='orange',label='Seasonality of minimum wind generation (d)',ylim=(-3000,3000))
minwind.resid.plot(ax=ax5[1],label='Residuals of minimum wind generation',alpha=0.5)
diffwind.plot(ax=ax2[1],label='Trend of difference in wind generation',alpha=0.8)
diffplot.plot(ax=ax2[0],label='Trend of difference in pumped storage',alpha=0.5)
for i in range(2):
    ax1[i].legend()
    ax2[i].legend() 
    ax3[i].legend()
    ax4[i].legend()
    ax5[i].legend()

ax1[0].set(xlabel='Time (daily)',ylabel='Pumped storage power generated (MW)')
ax2[0].set(xlabel='Time (daily)',ylabel='Trend of generation (MW)')
ax3[0].set(xlabel='Time (daily)',ylabel='Seasonality of generation (MW)')
ax4[0].set(xlabel='Time (daily)',ylabel='Seasonality of generation (MW)')
ax5[0].set(xlabel='Time (daily)',ylabel='Residual of generation (MW)')

ax1[1].set(xlabel='Time (daily)',ylabel='Wind power generated (MW)')
ax2[1].set(xlabel='Time (daily)',ylabel='Trend of generation (MW)')
ax3[1].set(xlabel='Time (daily)',ylabel='Seasonality of generation (MW)')
ax4[1].set(xlabel='Time (daily)',ylabel='Seasonality of generation (MW)')
ax5[1].set(xlabel='Time (daily)',ylabel='Residual of generation (MW)')
plt.show()
