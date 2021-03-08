import pandas as pd
import matplotlib.pyplot as plt #import libraries
from statsmodels.tsa.seasonal import seasonal_decompose

edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage data

edataps=edataps[0:208756] #pumped storage data is a bit longer than demand data so slice
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

begin_day='2012-06-29 00:00:00' #2012-06-29 is the earliest date useable 
final_day='2020-10-02 00:00:00' #2020-10-02 is the latest date useable

edataps=edataps[begin_day:final_day] #slice dataset for desired range
daycsum=edataps.groupby(edataps.index.date)['POWER_ELEXM_PS_MW'].cumsum()
daycsum=daycsum.to_frame()#convert new series into dataframe

fig,(ax1,ax2,ax3)=plt.subplots(3,1,figsize=(10,20))#start plotting data
csumplot=pd.DataFrame(daycsum.POWER_ELEXM_PS_MW,daycsum.index)#create dataframe for plotting

csumplot=seasonal_decompose(csumplot,model='additive',period=48)#Seasonal decomposition with an additive model
csumplot.observed.plot(ax=ax1) #plot observed data
ax1.set(xlabel='Time (half-hours)',ylabel='Cumulative power generated (MW)',title='Daily resetting cumulative power generated from'+' '+ begin_day[:10]+' '+'to'+' '+final_day[:10])
csumplot.trend.plot(ax=ax2)#plot trend of data
ax2.set(xlabel='Time (half-hours)',ylabel='Trend of daily accumulation (MW)')
#csumplot.seasonal.plot(ax=ax3)#plot seasonality of data
#ax3.set(xlabel='Time (half-hours)',ylabel='Seasonality of daily accumulation (MW)')
csumplot.resid.plot(ax=ax3)#plot residuals of data
ax3.set(xlabel='Time (half-hours)',ylabel='Residual of daily accumulation (MW)')
plt.show()





