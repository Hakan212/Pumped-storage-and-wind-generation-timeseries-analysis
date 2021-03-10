# Adapted from Jin Hyun Cheong,2019, https://towardsdatascience.com/four-ways-to-quantify-synchrony-between-time-series-data-b99136c4a9c9

def crosscorr(datax, datay, lag=0, wrap=False):
    """ Lag-N cross correlation. 
    Shifted data filled with NaNs 
    
    Parameters
    ----------
    lag : int, default 0
    datax, datay : pandas.Series objects of equal length
    Returns
    ----------
    crosscorr : float
    """
    if wrap: #cross correlation function with wrap functionality, which takes edge values into account
        shiftedy = datay.shift(lag) 
        shiftedy.iloc[:lag] = datay.iloc[-lag:].values
        return datax.corr(shiftedy) 
    else: 
        return datax.corr(datay.shift(lag)) #do normal cross-correlation if no wrap needed
import pandas as pd #import libraries
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

edata=pd.read_csv('espeni.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage
edataps=pd.read_csv('ps_data.csv',parse_dates=True,infer_datetime_format=True,index_col='ELEXM_utc')#read pumped storage
edataps=edataps[0:208756]#slice dataset as pumped storage is slightly longer
edata.index=edata.index.tz_convert(None)#convert into useable timezone
edataps=edataps.resample('0.5H').interpolate() #interpolate over missing values in pstorage data

begin_day='2012-06-29 00:00:00' #2012-06-29 is the earliest date useable 
final_day='2020-10-02 00:00:00' #2020-10-02 is the latest date useable
edata=edata[begin_day:final_day] #slice datasets
edataps=edataps[begin_day:final_day]
da=edataps.POWER_ELEXM_PS_MW
db=edata.POWER_ELEXM_WIND_MW+edata.POWER_NGEM_EMBEDDED_WIND_GENERATION_MW #add wind gen and embedded together

seconds = 5 #time lag parameters
fps = 30 #time lag parameters
no_splits=80 #specify number of windows for WTLCC
samples_per_split = int(da.shape[0]/no_splits) #specifiying the size of the window
rss=[] #pre-defining variables
for t in range(0, no_splits): #perform WTLCC
    d1 = da.iloc[(t)*samples_per_split:(t+1)*samples_per_split] #takes a specified window
    d2 = db.iloc[(t)*samples_per_split:(t+1)*samples_per_split]
    rs = [crosscorr(d1,d2, lag) for lag in range(-int(seconds*fps),int(seconds*fps+1))] #Calculates pearson correlation in each window
    rss.append(rs) #appends to total data until loop ends
rss = pd.DataFrame(rss)

rs = [crosscorr(da,db, lag) for lag in range(-int(seconds*fps),int(seconds*fps+1))]#sets up regular TLCC
offset = np.ceil(len(rs)/2)-np.argmax(rs) #calculates overall offset

fig,(ax1,ax2)=plt.subplots(2,1,figsize=(14,14))#plotting
ax1.plot(rs)#plotting TLCC correlations
ax1.axvline(np.ceil(len(rs)/2),color='k',linestyle='--',label='Center')#plotting centre 0 offset line
ax1.axvline(np.argmax(rs),color='blue',linestyle='--',label='Peak synchrony')#plotting peak correlation offset line
ax1.set(title='Time lagged cross correlation'+' '+f'Offset = {offset} frames\nPumped storage generation leads <> Wind generation leads',xlim=[0,seconds*fps+1], xlabel='Offset',ylabel='Pearson r')
ax1.set_xticks([0, 50, 100, 151, 201, 251, 301])
ax1.set_xticklabels([-150, -100, -50, 0, 50, 100, 150]);
ax1.legend()

sns.heatmap(rss,cmap='RdBu_r',ax=ax2,vmin=-0.2,vmax=0.15) #plotting WTLCC heatmap
ax2.axvline(np.ceil(len(rs)/2),color='k',linestyle='--',label='Center')
ax2.axvline(np.argmax(rs),color='blue',linestyle='--',label='Peak synchrony')#plotting peak correlation offset line
ax2.set(title='Windowed time lagged cross correlation\nPumped storage generation leads <> Wind generation leads',xlim=[0,seconds*fps+1], xlabel='Offset',ylabel='Window epochs')
ax2.set_xticks([0, 50, 100, 151, 201, 251, 301])
ax2.set_xticklabels([-150, -100, -50, 0, 50, 100, 150]);
ax2.legend()
plt.show()