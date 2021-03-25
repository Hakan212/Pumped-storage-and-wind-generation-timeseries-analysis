import pandas as pd
import matplotlib.pyplot as plt #import libraries
from statsmodels.tsa.seasonal import seasonal_decompose

edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage
edata=pd.read_csv('espeni.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')
edataps=edataps[0:208756] #pumped storage data is a bit longer than demand data
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

beginday1='2019-02-11 00:00:00' 
finalday1='2019-02-18 00:00:00' 
beginday2='2016-02-08 00:00:00'
finalday2='2016-02-15 00:00:00'
beginday3='2013-02-04 00:00:00'
finalday3='2013-02-11 00:00:00'

windgen=edata.POWER_ELEXM_WIND_MW+edata.POWER_NGEM_EMBEDDED_WIND_GENERATION_MW
edataps1=edataps[beginday1:finalday1] #slice dataset for desired range
edataps2=edataps[beginday2:finalday2]
edataps3=edataps[beginday3:finalday3]
edata1=windgen[beginday1:finalday1]
edata2=windgen[beginday2:finalday2]
edata3=windgen[beginday3:finalday3]
fig,(ax1,ax2,ax3,ax4,ax5,ax6)=plt.subplots(6,1,figsize=(10,20))#start plotting

edataps2.index=edataps1.index
edataps3.index=edataps1.index
edata2.index=edata1.index
edata3.index=edata1.index

splot1=pd.DataFrame(edataps1.POWER_ELEXM_PS_MW,edataps1.index)
splot2=pd.DataFrame(edataps2.POWER_ELEXM_PS_MW,edataps1.index)
splot3=pd.DataFrame(edataps3.POWER_ELEXM_PS_MW,edataps1.index)

wplot1=pd.DataFrame(edata1,edata1.index)
wplot2=pd.DataFrame(edata2,edata1.index)
wplot3=pd.DataFrame(edata3,edata1.index)

splot1=seasonal_decompose(splot1,model='additive',period=48)#seasonal decomposition for pumped storage
splot2=seasonal_decompose(splot2,model='additive',period=48)
splot3=seasonal_decompose(splot3,model='additive',period=48)

wplot1=seasonal_decompose(wplot1,model='additive',period=48)#seasonal decomposition for wind
wplot2=seasonal_decompose(wplot2,model='additive',period=48)
wplot3=seasonal_decompose(wplot3,model='additive',period=48)

splot1.observed.plot(ax=ax1,alpha=0.5,label='2019 PS generation (a)',ylim=(-4000,3000))#plot observed data
splot2.observed.plot(ax=ax1,alpha=0.5,label='2016 PS generation')
splot3.observed.plot(ax=ax1,alpha=0.5,label='2013 PS generation')
ax1.axhline(y=0,color='r',linestyle='-')
ax1.set(xlabel='',ylabel='Power generated (MW)')

x=['2019-02-11 00:00:00','2019-02-12 00:00:00','2019-02-13 00:00:00','2019-02-14 00:00:00','2019-02-15 00:00:00','2019-02-16 00:00:00','2019-02-17 00:00:00','2019-02-18 00:00:00']
xt=['Mon','Tue','Wed','Thurs','Fri','Sat','Sun']#change x axis
ax1.set_xticks(x)
ax1.set_xticklabels(xt);

splot1.seasonal.plot(ax=ax2,alpha=0.5,label='2019 PS seasonality (b)',ylim=(-4000,3000))#plot seasonality of data
splot2.seasonal.plot(ax=ax2,alpha=0.5,label='2016 PS seasonality')
splot3.seasonal.plot(ax=ax2,alpha=0.5,label='2013 PS seasonality')
ax2.set(xlabel='',ylabel='Seasonality (MW)')
ax2.set_xticks(x)
ax2.set_xticklabels(xt);
ax2.legend(loc='lower left')
ax2.axhline(y=0,color='r',linestyle='-')

wplot1.observed.plot(ax=ax3,label='2019 Wind generation (a)')#plot observed data
wplot2.observed.plot(ax=ax3,label='2016 Wind generation')
wplot3.observed.plot(ax=ax3,label='2013 Wind generation')
ax3.set(xlabel='',ylabel='Power Generated (MW)')

ax3.set_xticks(x)
ax3.set_xticklabels(xt)
wplot1.seasonal.plot(ax=ax4,alpha=0.5,label='2019 Wind seasonality (b)',ylim=(-600,400))
wplot2.seasonal.plot(ax=ax5,alpha=0.5,label='2016 Wind seasonality (c)',color='orange',ylim=(-600,400))
wplot3.seasonal.plot(ax=ax6,alpha=0.5,label='2013 Wind seasonality (d)',color='green',ylim=(-600,400))

ax4.set(xlabel='',ylabel='Seasonality (MW)')
ax5.set(xlabel='',ylabel='Seasonality (MW)')
ax6.set(xlabel='',ylabel='Seasonality (MW)')
ax1.legend(loc='lower left')
ax2.legend()
ax3.legend(loc='lower left')
ax4.legend()
ax5.legend()
ax6.legend()

ax4.set_xticks(x)
ax4.set_xticklabels(xt)
ax5.set_xticks(x)
ax5.set_xticklabels(xt)
ax6.set_xticks(x)
ax6.set_xticklabels(xt)



