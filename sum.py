import pandas as pd
import matplotlib.pyplot as plt #import libraries
from statsmodels.tsa.seasonal import seasonal_decompose

edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage

edataps=edataps[0:208756] #pumped storage data is a bit longer than demand data
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

begin_day='2012-06-29 00:00:00' #2012-06-29 is the earliest date useable
final_day='2020-10-01 23:30:00' #2020-10-02 is the latest date useable

edataps=edataps[begin_day:final_day] #slice dataset for desired range

daysum=edataps.POWER_ELEXM_PS_MW.resample('D').sum()#resample the dataset to sum over each day
daysum=daysum.to_frame()#convert new series into dataframe

fig,(ax1,ax2,ax3)=plt.subplots(3,1,figsize=(10,20))
sumplot=pd.DataFrame(daysum.POWER_ELEXM_PS_MW,daysum.index)
sumplot=seasonal_decompose(sumplot,model='additive')#seasonal decomposition
sumplot.observed.plot(ax=ax1) #plot observed data
ax1.set(xlabel='Time (daily)',ylabel='Sum of power generated (MW)',title='Sum of energy generated for each separate day from'+' '+ begin_day[:10]+' '+'to'+' '+final_day[:10])
sumplot.trend.plot(ax=ax2) #plot trend of data
ax2.set(xlabel='Time (daily)',ylabel='Trend of daily sum (MW)')
#sumplot.seasonal.plot(ax=ax3)#plot seasonality of data
#ax3.set(xlabel='Time (daily)',ylabel='Seasonality of daily sum (MW)')
sumplot.resid.plot(ax=ax3)#plot residuals of data
ax3.set(xlabel='Time (daily)',ylabel='Residual of daily sum (MW)')
plt.show()






