import pandas as pd
import matplotlib.pyplot as plt #import libraries
from statsmodels.tsa.seasonal import seasonal_decompose

edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage

edataps=edataps[0:208756] #pumped storage data is a bit longer than demand data
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

begin_day='2017-02-13 00:00:00' #2012-06-29 is the earliest date useable
final_day='2017-02-20 00:00:00' #2020-10-02 is the latest date useable

edataps=edataps[begin_day:final_day] #slice dataset for desired range

fig,(ax1,ax2,ax3,ax4)=plt.subplots(4,1,figsize=(10,20))#start plotting
csumplot=pd.DataFrame(edataps.POWER_ELEXM_PS_MW,edataps.index)

csumplot=seasonal_decompose(csumplot,model='additive',period=48)#seasonal decomposition
csumplot.observed.plot(ax=ax1)#plot observed data
ax1.set(xlabel='',ylabel='Power generated (MW)',title='Power generated from'+' '+ begin_day[:10]+' '+'to'+' '+final_day[:10])
csumplot.trend.plot(ax=ax2)#plot trend of data
ax2.set(xlabel='',ylabel='Trend of generation (MW)')
csumplot.seasonal.plot(ax=ax3)#plot seasonality of data
ax3.set(xlabel='',ylabel='Seasonality of generation (MW)')
csumplot.resid.plot(ax=ax4)#plot residuals of data
ax4.set(xlabel='',ylabel='Residual of daily generation (MW)')
plt.show()






