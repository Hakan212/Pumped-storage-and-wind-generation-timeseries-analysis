import pandas as pd
import matplotlib.pyplot as plt #import libraries
from statsmodels.tsa.seasonal import seasonal_decompose

edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage

edataps=edataps[0:208756] #pumped storage data is a bit longer than demand data
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

begin_day='2012-06-29 00:00:00' #2012-06-29 is the earliest date useable
final_day='2020-10-02 23:30:00' #2020-10-02 is the latest date useable

edataps=edataps[begin_day:final_day] #slice dataset for desired range

daymin=edataps.POWER_ELEXM_PS_MW.resample('D').min()#resample the dataset to take min of each
daymin=daymin.to_frame()
daymax=edataps.POWER_ELEXM_PS_MW.resample('D').max()#resample the dataset to take the max of each day
daymax=daymax.to_frame()
daydiff=daymax-daymin #compute difference

fig,(ax1,ax2,ax3)=plt.subplots(3,3,figsize=(30,20))
diffplot=pd.DataFrame(daydiff.POWER_ELEXM_PS_MW,daydiff.index)
maxplot=pd.DataFrame(daymax.POWER_ELEXM_PS_MW,daymax.index)
minplot=pd.DataFrame(daymin.POWER_ELEXM_PS_MW,daymin.index)

diffplot=seasonal_decompose(diffplot,model='additive')#seasonal decomposition
maxplot=seasonal_decompose(maxplot,model='additive')#seasonal decomposition
minplot=seasonal_decompose(minplot,model='additive')#seasonal decomposition
plot=[diffplot,maxplot,minplot]
for i in range(3): #plotting difference maxima and minima
    plot[i].observed.plot(ax=ax1[i])    
    plot[i].trend.plot(ax=ax2[i])
    #plot[i].seasonal.plot(ax=ax3[i]) seasonality not used for this analysis
    plot[i].resid.plot(ax=ax3[i])
    
ax1[0].set(xlabel='Time (daily)',ylabel='Difference in power (MW)',title='Difference in maximum power and minimum power generated from'+' '+ begin_day[:10]+' '+'to'+' '+final_day[:10])
ax2[0].set(xlabel='Time (daily)',ylabel='Trend of difference (MW)')
#ax3[0].set(xlabel='Time (daily)',ylabel='Seasonality of difference (MW)')
ax3[0].set(xlabel='Time (daily)',ylabel='Residual of difference (MW)')

ax1[1].set(xlabel='Time (daily)',ylabel='Maximum power generated each day (MW)',title='Maximum power generated for each day from'+' '+ begin_day[:10]+' '+'to'+' '+final_day[:10])
ax2[1].set(xlabel='Time (daily)',ylabel='Trend of generation (MW)')
#ax3[1].set(xlabel='Time (daily)',ylabel='Seasonality of generation (MW)')
ax3[1].set(xlabel='Time (daily)',ylabel='Residual of generation (MW)')

ax1[2].set(xlabel='Time (daily)',ylabel='Minimum power generated each day (MW)',title='Minimum power generated for each day from'+' '+ begin_day[:10]+' '+'to'+' '+final_day[:10])
ax2[2].set(xlabel='Time (daily)',ylabel='Trend of generation (MW)')
#ax3[2].set(xlabel='Time (daily)',ylabel='Seasonality of generation (MW)')
ax3[2].set(xlabel='Time (daily)',ylabel='Residual of generation (MW)')
plt.show()