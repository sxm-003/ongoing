import numpy as np
import pandas as pd
from scipy.stats import lognorm, chi2
import matplotlib.pyplot as plt

#generating 7 day time series data 
timestamp = pd.date_range(start = '2025-05-28', end = '2025-06-01', freq='1min')

def synthesis(peak=8,shift_peak=14):
    """cpu usage synthesis based on combination lognormal distrubution simulating the overall usage distribution with peak usage at "peak" and chi-sqared distribution simulating the other peak(after break) with peak at shift_peak """

    hours = timestamp.hour + timestamp.minute / 60

    #lognormal load
    s = 0.5    
    mu = np.log(peak) + s**2
    scale = np.exp(mu)
    lognorm_load = 175 * lognorm.pdf(hours + 0.01, s=s, scale=scale)
    
    #chi-sqared load
    df = 3.5
    chi_load = 100 * chi2.pdf(hours - shift_peak, df=df) #shift_peak adjusts the peak to the value of shift_peak

    #noise
    noise = np.random.normal(0, 5, len(timestamp))

    #abnormal random spikes
    spikes = (np.random.rand(len(timestamp)) < 0.004) * np.random.randint(30, 70, len(timestamp))

    #weekly modulation
    weekly_modulation = 1 + 0.7 * ((timestamp.dayofweek < 5).astype(int))
    
    #cpu usage data synthesis
    base = 30 #base usage of cpu in percentage
    cpu_usage = base + (lognorm_load + chi_load)*weekly_modulation + noise + spikes
    cpu_usage = np.clip(cpu_usage, 0, 100)  # clip to valid range

    data_frame = pd.DataFrame({
    'timestamp': timestamp,
    'cpu_usage': cpu_usage
    })
    plt.figure(figsize=(12,8))
    plt.plot(timestamp[:], cpu_usage[:])

    return data_frame.to_csv("synthetic_data.csv")

synthesis()




