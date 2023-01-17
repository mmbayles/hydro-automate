import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import fileinput
import textwrap
import re
import json
from collections import OrderedDict
from datetime import datetime
import reach_station_lookup

#usage: pull together all pertinent data from .dss files (time series, Qmax, calculated WSE) with the support of Qmax~WSE correlations compiled from RAS, and HMS reach~RAS station correlations compiled manually
#SET UP DICTIONARY OF ARRAYS HOLDING QMAX, WSE, SLOPE & INTERCEPT /STATION /STORM

#bring in compiled .csv (UTF-8) file of Peak Flow ~ WSE correlations, exported from RAS summary table and keep only 
#reach, river station, profile, Q Total and W.S. Elev columns;
#.csv should have no extra spaces, keep headings
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\PeakFlow_WSE_Correlations_RiverStations_WFK_090722.csv",'r') as f:
        fdata = f.read()
stations = re.findall(r"\n.*?,(.*?),.*?,.*?,\d*.\d*",fdata) #regex structured this way to toss the culvert
stations = list(OrderedDict.fromkeys(stations)) #to remove duplicates and maintain order
q_max = re.findall(r"\n.*?,.*?,.*?,(\d*.\d*)\,",fdata)
q_max = [float(x) for x in q_max]
wse = re.findall(r"\n.*?,.*?,.*?,.*?,(\d*.\d*)",fdata)
wse = [float(x) for x in wse]

#define slope and intercept functions
def slope(x0,x1,y0,y1):
    return((y1-y0)/(x1-x0)) if x1-x0 else None
def intercept(x0,x1,y0,y1):
    return y0-(((y1-y0)/(x1-x0))*x0) if x1-x0 else None

#compile info for each river station
qmax_wse = {}
i = 0
for station in range(len(stations)):
    qmax_wse[f'{stations[station]}'] = np.array(([q_max[i],wse[i],99,999],
                   [q_max[i+1],wse[i+1],slope(q_max[i],q_max[i+1],wse[i],wse[i+1]),intercept(q_max[i],q_max[i+1],wse[i],wse[i+1])],
                   [q_max[i+2],wse[i+2],slope(q_max[i+1],q_max[i+2],wse[i+1],wse[i+2]),intercept(q_max[i+1],q_max[i+2],wse[i+1],wse[i+2])],
                   [q_max[i+3],wse[i+3],slope(q_max[i+2],q_max[i+3],wse[i+2],wse[i+3]),intercept(q_max[i+2],q_max[i+3],wse[i+2],wse[i+3])],
                   [q_max[i+4],wse[i+4],slope(q_max[i+3],q_max[i+4],wse[i+3],wse[i+4]),intercept(q_max[i+3],q_max[i+4],wse[i+3],wse[i+4])],
                   [q_max[i+5],wse[i+5],slope(q_max[i+4],q_max[i+5],wse[i+4],wse[i+5]),intercept(q_max[i+4],q_max[i+5],wse[i+4],wse[i+5])],
                   [q_max[i+6],wse[i+6],slope(q_max[i+5],q_max[i+6],wse[i+5],wse[i+6]),intercept(q_max[i+5],q_max[i+6],wse[i+5],wse[i+6])],
                  [q_max[i+7],wse[i+7],slope(q_max[i+6],q_max[i+7],wse[i+6],wse[i+7]),intercept(q_max[i+6],q_max[i+7],wse[i+6],wse[i+7])]))
    i = i+8
    
#DEFINE HMS REACHES TO PULL TIME SERIES DATA FROM DSS VUE (pulled from hms_reach from proof. 
#naming is case insensitive. requires some manual adjustments because HMS cuts off names)

# #KEY STATION ~ HMS REACH LOOKUP
# #proofs for development of following lists are in proofs.ipynb
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\HMS_RAS_NetworkCorrelation_WFK_090722.csv",'r') as f:
        fdata = f.read()        
reaches = re.findall(r"\n.*?,.*?,.*?,.*?(.*?)\,",fdata)
key_station = re.findall(r"\n.*?,.*?,.*?,.*?,.*?(.*?)\,",fdata)
key_station = [float(x) for x in key_station]

#KEY STATION ~ HMS REACH LOOKUP
WFK = reach_station_lookup.Watershed('WFK') #usage: WFK.get_reach(station) or WFK.get_station('reach')

#PULL EXPERIMENTAL DATA FROM DSS VUE; SWAP HMS REACH FOR RAS STATION IDENTIFIER
#2 year data
dict_of_stations_2yr = {}
dict_of_stations_max_2yr = {}
for reach in range(len(reaches)):
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\TimeSeriesData\2yr_{}.txt".format(reaches[reach]),'r') as f: 
        fdata = f.read() 
    day = re.findall(r"\d{2}\s\w{3}\s\d{4}",fdata)
    time = re.findall(r"\d\d:\d\d",fdata)
    cfs = re.findall(r"\d\d:\d\d,(\d*)",fdata)
    cfs = [float(x) for x in cfs]
    cfs_max = max(cfs)
    dict_of_stations_2yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = {'day range':'01/01/2021-01/04/2021', 'time step':'5min', 'cfs':cfs}
    dict_of_stations_max_2yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = cfs_max

#5 year data
dict_of_stations_5yr = {}
dict_of_stations_max_5yr = {}
for reach in range(len(reaches)):
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\TimeSeriesData\5yr_{}.txt".format(reaches[reach]),'r') as f: 
        fdata = f.read() 
    day = re.findall(r"\d{2}\s\w{3}\s\d{4}",fdata)
    time = re.findall(r"\d\d:\d\d",fdata)
    cfs = re.findall(r"\d\d:\d\d,(\d*)",fdata)
    cfs = [float(x) for x in cfs]
    cfs_max = max(cfs)
    dict_of_stations_5yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = {'day range':'01/01/2021-01/04/2021', 'time step':'5min', 'cfs':cfs}
    dict_of_stations_max_5yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = cfs_max

#10 year data
dict_of_stations_10yr = {}
dict_of_stations_max_10yr = {}
for reach in range(len(reaches)):
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\TimeSeriesData\10yr_{}.txt".format(reaches[reach]),'r') as f: 
        fdata = f.read() 
    day = re.findall(r"\d{2}\s\w{3}\s\d{4}",fdata)
    time = re.findall(r"\d\d:\d\d",fdata)
    cfs = re.findall(r"\d\d:\d\d,(\d*)",fdata)
    cfs = [float(x) for x in cfs]
    cfs_max = max(cfs)
    dict_of_stations_10yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = {'day range':'01/01/2021-01/04/2021', 'time step':'5min', 'cfs':cfs}
    dict_of_stations_max_10yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = cfs_max
    
#25 year data
dict_of_stations_25yr = {}
dict_of_stations_max_25yr = {}
for reach in range(len(reaches)):
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\TimeSeriesData\25yr_{}.txt".format(reaches[reach]),'r') as f: 
        fdata = f.read() 
    day = re.findall(r"\d{2}\s\w{3}\s\d{4}",fdata)
    time = re.findall(r"\d\d:\d\d",fdata)
    cfs = re.findall(r"\d\d:\d\d,(\d*)",fdata)
    cfs = [float(x) for x in cfs]
    cfs_max = max(cfs)
    dict_of_stations_25yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = {'day range':'01/01/2021-01/04/2021', 'time step':'5min', 'cfs':cfs}
    dict_of_stations_max_25yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = cfs_max
    
#50 year data
dict_of_stations_50yr = {}
dict_of_stations_max_50yr = {}
for reach in range(len(reaches)):
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\TimeSeriesData\50yr_{}.txt".format(reaches[reach]),'r') as f: 
        fdata = f.read() 
    day = re.findall(r"\d{2}\s\w{3}\s\d{4}",fdata)
    time = re.findall(r"\d\d:\d\d",fdata)
    cfs = re.findall(r"\d\d:\d\d,(\d*)",fdata)
    cfs = [float(x) for x in cfs]
    cfs_max = max(cfs)
    dict_of_stations_50yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = {'day range':'01/01/2021-01/04/2021', 'time step':'5min', 'cfs':cfs}
    dict_of_stations_max_50yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = cfs_max

#100 year data
dict_of_stations_100yr = {}
dict_of_stations_max_100yr = {}
for reach in range(len(reaches)):
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\TimeSeriesData\100yr_{}.txt".format(reaches[reach]),'r') as f: 
        fdata = f.read() 
    day = re.findall(r"\d{2}\s\w{3}\s\d{4}",fdata)
    time = re.findall(r"\d\d:\d\d",fdata)
    cfs = re.findall(r"\d\d:\d\d,(\d*)",fdata)
    cfs = [float(x) for x in cfs]
    cfs_max = max(cfs)
    dict_of_stations_100yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = {'day range':'01/01/2021-01/04/2021', 'time step':'5min', 'cfs':cfs}
    dict_of_stations_max_100yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = cfs_max
    
#200 year data
dict_of_stations_200yr = {}
dict_of_stations_max_200yr = {}
for reach in range(len(reaches)):
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\TimeSeriesData\200yr_{}.txt".format(reaches[reach]),'r') as f: 
        fdata = f.read() 
    day = re.findall(r"\d{2}\s\w{3}\s\d{4}",fdata)
    time = re.findall(r"\d\d:\d\d",fdata)
    cfs = re.findall(r"\d\d:\d\d,(\d*)",fdata)
    cfs = [float(x) for x in cfs]
    cfs_max = max(cfs)
    dict_of_stations_200yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = {'day range':'01/01/2021-01/04/2021', 'time step':'5min', 'cfs':cfs}
    dict_of_stations_max_200yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = cfs_max
    
#500 year data
dict_of_stations_500yr = {}
dict_of_stations_max_500yr = {}
for reach in range(len(reaches)):
    with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\TimeSeriesData\500yr_{}.txt".format(reaches[reach]),'r') as f: 
        fdata = f.read() 
    day = re.findall(r"\d{2}\s\w{3}\s\d{4}",fdata)
    time = re.findall(r"\d\d:\d\d",fdata)
    cfs = re.findall(r"\d\d:\d\d,(\d*)",fdata)
    cfs = [float(x) for x in cfs]
    cfs_max = max(cfs)
    dict_of_stations_500yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = {'day range':'01/01/2021-01/04/2021', 'time step':'5min', 'cfs':cfs}
    dict_of_stations_max_500yr[f"{WFK.get_station(f'{reaches[reach]}')}"] = cfs_max

    
#WSE CALCULATION
#create some useful elements to make looping easier
storms = ['2yr', '5yr', '10yr','25yr', '50yr', '100yr', '200yr', '500yr']
dict_of_stations_max_names = {0:dict_of_stations_max_2yr, 1:dict_of_stations_max_5yr,2:dict_of_stations_max_10yr,
                             3:dict_of_stations_max_25yr,4:dict_of_stations_max_50yr,5:dict_of_stations_max_100yr,
                             6:dict_of_stations_max_200yr,7:dict_of_stations_max_500yr}

calc_wse = {'2yr':{}, '5yr':{}, '10yr':{}, '25yr':{}, '50yr':{},'100yr':{}, '200yr':{}, '500yr':{}}
for storm in range(len(dict_of_stations_max_names)): #8 instances
    for station in range(len(key_station)): #42 instances
        #under 2yr Qmax
        if dict_of_stations_max_names[storm][f'{key_station[station]}'] <= qmax_wse[f'{key_station[station]}'][0,0]:
            statement = 'Warning: Max flow is under model parameters'
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = 99
        #between 2yr & 5yr Qmax
        if qmax_wse[f'{key_station[station]}'][0,0] < dict_of_stations_max_names[storm][f'{key_station[station]}'] <= qmax_wse[f'{key_station[station]}'][1,0]:
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][1,2] * dict_of_stations_max_names[storm][f'{key_station[station]}'] + qmax_wse[f'{key_station[station]}'][1,3] # y=mx+b
        #between 5yr & 10yr Qmax
        if qmax_wse[f'{key_station[station]}'][1,0] < dict_of_stations_max_names[storm][f'{key_station[station]}'] <= qmax_wse[f'{key_station[station]}'][2,0]:
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][2,2] * dict_of_stations_max_names[storm][f'{key_station[station]}'] + qmax_wse[f'{key_station[station]}'][2,3] # y=mx+b
        #between 10yr and 25yr Qmax
        if qmax_wse[f'{key_station[station]}'][2,0] < dict_of_stations_max_names[storm][f'{key_station[station]}'] <= qmax_wse[f'{key_station[station]}'][3,0]:
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][3,2] * dict_of_stations_max_names[storm][f'{key_station[station]}'] + qmax_wse[f'{key_station[station]}'][3,3] # y=mx+b
        #between 25yr and 50yr Qmax
        if qmax_wse[f'{key_station[station]}'][3,0] < dict_of_stations_max_names[storm][f'{key_station[station]}'] <= qmax_wse[f'{key_station[station]}'][4,0]:
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][4,2] * dict_of_stations_max_names[storm][f'{key_station[station]}'] + qmax_wse[f'{key_station[station]}'][4,3] # y=mx+b
        #between 50yr and 100yr Qmax
        if qmax_wse[f'{key_station[station]}'][4,0] < dict_of_stations_max_names[storm][f'{key_station[station]}'] <= qmax_wse[f'{key_station[station]}'][5,0]:
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][5,2] * dict_of_stations_max_names[storm][f'{key_station[station]}'] + qmax_wse[f'{key_station[station]}'][5,3] # y=mx+b
        #between 100yr and 200yr Qmax
        if qmax_wse[f'{key_station[station]}'][5,0] < dict_of_stations_max_names[storm][f'{key_station[station]}'] <= qmax_wse[f'{key_station[station]}'][6,0]:
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][6,2] * dict_of_stations_max_names[storm][f'{key_station[station]}'] + qmax_wse[f'{key_station[station]}'][6,3] # y=mx+b
        #between 200yr and 500yr Qmax
        if qmax_wse[f'{key_station[station]}'][6,0] < dict_of_stations_max_names[storm][f'{key_station[station]}'] <= qmax_wse[f'{key_station[station]}'][7,0]:
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][7,2] * dict_of_stations_max_names[storm][f'{key_station[station]}'] + qmax_wse[f'{key_station[station]}'][7,3] # y=mx+b
        #above 500yr Qmax
        if dict_of_stations_max_names[storm][f'{key_station[station]}'] > qmax_wse[f'{key_station[station]}'][7,0]:
            statement = 'Warning: Max flow is above model parameters; 200yr to 500yr rating curve applied to flow'
            calc_wse[f'{storms[storm]}'][f'{key_station[station]}'] = qmax_wse[f'{key_station[station]}'][7,2] * dict_of_stations_max_names[storm][f'{key_station[station]}'] + qmax_wse[f'{key_station[station]}'][7,3] # y=mx+b
            
            
#COMPILE ALL INFO TO JSON
#set up dictionary to be populated
CompiledRiverStationData = {'2yr':{'5075.74':{},
 '4688.81':{},
 '21459.97':{},
 '18520.11':{},
 '9044.28':{},
 '4683.66':{},
 '1299.05':{},
 '6131.81':{},
 '2722.88':{},
 '2945.19':{},
 '5429.81':{},
 '1689.83':{},
 '12749.08':{},
 '5350.41':{},
 '10798.11':{},
 '6346.46':{},
 '2417.83':{},
 '6721.04':{},
 '1933.21':{},
 '6000.33':{},
 '3277.91':{},
 '4687.52':{},
 '3751.15':{},
 '5128.21':{},
 '4660.94':{},
 '2048.78':{},
 '11827.62':{},
 '1446.65':{},
 '5600.6':{},
 '15905.06':{},
 '1052.29':{},
 '3338.29':{},
 '5313.02':{},
 '5325.85':{},
 '3737.3':{},
 '13383.6':{},
 '2334.44':{},
 '1020.65':{},
 '29422.32':{},
 '23916.11':{},
 '15699.21':{},
 '3134.44':{},
 '2179.29':{},
 '23321.9':{},
 '16392.48':{},
 '20307.34':{},
 '11361.86':{},
 '1690.2':{},
 '2432.4':{},
 '10964.2':{},
 '9033.32':{},
 '4276.96':{}},'5yr':{'5075.74':{},
 '4688.81':{},
 '21459.97':{},
 '18520.11':{},
 '9044.28':{},
 '4683.66':{},
 '1299.05':{},
 '6131.81':{},
 '2722.88':{},
 '2945.19':{},
 '5429.81':{},
 '1689.83':{},
 '12749.08':{},
 '5350.41':{},
 '10798.11':{},
 '6346.46':{},
 '2417.83':{},
 '6721.04':{},
 '1933.21':{},
 '6000.33':{},
 '3277.91':{},
 '4687.52':{},
 '3751.15':{},
 '5128.21':{},
 '4660.94':{},
 '2048.78':{},
 '11827.62':{},
 '1446.65':{},
 '5600.6':{},
 '15905.06':{},
 '1052.29':{},
 '3338.29':{},
 '5313.02':{},
 '5325.85':{},
 '3737.3':{},
 '13383.6':{},
 '2334.44':{},
 '1020.65':{},
 '29422.32':{},
 '23916.11':{},
 '15699.21':{},
 '3134.44':{},
 '2179.29':{},
 '23321.9':{},
 '16392.48':{},
 '20307.34':{},
 '11361.86':{},
 '1690.2':{},
 '2432.4':{},
 '10964.2':{},
 '9033.32':{},
 '4276.96':{}},'10yr':{'5075.74':{},
 '4688.81':{},
 '21459.97':{},
 '18520.11':{},
 '9044.28':{},
 '4683.66':{},
 '1299.05':{},
 '6131.81':{},
 '2722.88':{},
 '2945.19':{},
 '5429.81':{},
 '1689.83':{},
 '12749.08':{},
 '5350.41':{},
 '10798.11':{},
 '6346.46':{},
 '2417.83':{},
 '6721.04':{},
 '1933.21':{},
 '6000.33':{},
 '3277.91':{},
 '4687.52':{},
 '3751.15':{},
 '5128.21':{},
 '4660.94':{},
 '2048.78':{},
 '11827.62':{},
 '1446.65':{},
 '5600.6':{},
 '15905.06':{},
 '1052.29':{},
 '3338.29':{},
 '5313.02':{},
 '5325.85':{},
 '3737.3':{},
 '13383.6':{},
 '2334.44':{},
 '1020.65':{},
 '29422.32':{},
 '23916.11':{},
 '15699.21':{},
 '3134.44':{},
 '2179.29':{},
 '23321.9':{},
 '16392.48':{},
 '20307.34':{},
 '11361.86':{},
 '1690.2':{},
 '2432.4':{},
 '10964.2':{},
 '9033.32':{},
 '4276.96':{}},'25yr':{'5075.74':{},
 '4688.81':{},
 '21459.97':{},
 '18520.11':{},
 '9044.28':{},
 '4683.66':{},
 '1299.05':{},
 '6131.81':{},
 '2722.88':{},
 '2945.19':{},
 '5429.81':{},
 '1689.83':{},
 '12749.08':{},
 '5350.41':{},
 '10798.11':{},
 '6346.46':{},
 '2417.83':{},
 '6721.04':{},
 '1933.21':{},
 '6000.33':{},
 '3277.91':{},
 '4687.52':{},
 '3751.15':{},
 '5128.21':{},
 '4660.94':{},
 '2048.78':{},
 '11827.62':{},
 '1446.65':{},
 '5600.6':{},
 '15905.06':{},
 '1052.29':{},
 '3338.29':{},
 '5313.02':{},
 '5325.85':{},
 '3737.3':{},
 '13383.6':{},
 '2334.44':{},
 '1020.65':{},
 '29422.32':{},
 '23916.11':{},
 '15699.21':{},
 '3134.44':{},
 '2179.29':{},
 '23321.9':{},
 '16392.48':{},
 '20307.34':{},
 '11361.86':{},
 '1690.2':{},
 '2432.4':{},
 '10964.2':{},
 '9033.32':{},
 '4276.96':{}},'50yr':{'5075.74':{},
 '4688.81':{},
 '21459.97':{},
 '18520.11':{},
 '9044.28':{},
 '4683.66':{},
 '1299.05':{},
 '6131.81':{},
 '2722.88':{},
 '2945.19':{},
 '5429.81':{},
 '1689.83':{},
 '12749.08':{},
 '5350.41':{},
 '10798.11':{},
 '6346.46':{},
 '2417.83':{},
 '6721.04':{},
 '1933.21':{},
 '6000.33':{},
 '3277.91':{},
 '4687.52':{},
 '3751.15':{},
 '5128.21':{},
 '4660.94':{},
 '2048.78':{},
 '11827.62':{},
 '1446.65':{},
 '5600.6':{},
 '15905.06':{},
 '1052.29':{},
 '3338.29':{},
 '5313.02':{},
 '5325.85':{},
 '3737.3':{},
 '13383.6':{},
 '2334.44':{},
 '1020.65':{},
 '29422.32':{},
 '23916.11':{},
 '15699.21':{},
 '3134.44':{},
 '2179.29':{},
 '23321.9':{},
 '16392.48':{},
 '20307.34':{},
 '11361.86':{},
 '1690.2':{},
 '2432.4':{},
 '10964.2':{},
 '9033.32':{},
 '4276.96':{}},'100yr':{'5075.74':{},
 '4688.81':{},
 '21459.97':{},
 '18520.11':{},
 '9044.28':{},
 '4683.66':{},
 '1299.05':{},
 '6131.81':{},
 '2722.88':{},
 '2945.19':{},
 '5429.81':{},
 '1689.83':{},
 '12749.08':{},
 '5350.41':{},
 '10798.11':{},
 '6346.46':{},
 '2417.83':{},
 '6721.04':{},
 '1933.21':{},
 '6000.33':{},
 '3277.91':{},
 '4687.52':{},
 '3751.15':{},
 '5128.21':{},
 '4660.94':{},
 '2048.78':{},
 '11827.62':{},
 '1446.65':{},
 '5600.6':{},
 '15905.06':{},
 '1052.29':{},
 '3338.29':{},
 '5313.02':{},
 '5325.85':{},
 '3737.3':{},
 '13383.6':{},
 '2334.44':{},
 '1020.65':{},
 '29422.32':{},
 '23916.11':{},
 '15699.21':{},
 '3134.44':{},
 '2179.29':{},
 '23321.9':{},
 '16392.48':{},
 '20307.34':{},
 '11361.86':{},
 '1690.2':{},
 '2432.4':{},
 '10964.2':{},
 '9033.32':{},
 '4276.96':{}},'200yr':{'5075.74':{},
 '4688.81':{},
 '21459.97':{},
 '18520.11':{},
 '9044.28':{},
 '4683.66':{},
 '1299.05':{},
 '6131.81':{},
 '2722.88':{},
 '2945.19':{},
 '5429.81':{},
 '1689.83':{},
 '12749.08':{},
 '5350.41':{},
 '10798.11':{},
 '6346.46':{},
 '2417.83':{},
 '6721.04':{},
 '1933.21':{},
 '6000.33':{},
 '3277.91':{},
 '4687.52':{},
 '3751.15':{},
 '5128.21':{},
 '4660.94':{},
 '2048.78':{},
 '11827.62':{},
 '1446.65':{},
 '5600.6':{},
 '15905.06':{},
 '1052.29':{},
 '3338.29':{},
 '5313.02':{},
 '5325.85':{},
 '3737.3':{},
 '13383.6':{},
 '2334.44':{},
 '1020.65':{},
 '29422.32':{},
 '23916.11':{},
 '15699.21':{},
 '3134.44':{},
 '2179.29':{},
 '23321.9':{},
 '16392.48':{},
 '20307.34':{},
 '11361.86':{},
 '1690.2':{},
 '2432.4':{},
 '10964.2':{},
 '9033.32':{},
 '4276.96':{}},'500yr':{'5075.74':{},
 '4688.81':{},
 '21459.97':{},
 '18520.11':{},
 '9044.28':{},
 '4683.66':{},
 '1299.05':{},
 '6131.81':{},
 '2722.88':{},
 '2945.19':{},
 '5429.81':{},
 '1689.83':{},
 '12749.08':{},
 '5350.41':{},
 '10798.11':{},
 '6346.46':{},
 '2417.83':{},
 '6721.04':{},
 '1933.21':{},
 '6000.33':{},
 '3277.91':{},
 '4687.52':{},
 '3751.15':{},
 '5128.21':{},
 '4660.94':{},
 '2048.78':{},
 '11827.62':{},
 '1446.65':{},
 '5600.6':{},
 '15905.06':{},
 '1052.29':{},
 '3338.29':{},
 '5313.02':{},
 '5325.85':{},
 '3737.3':{},
 '13383.6':{},
 '2334.44':{},
 '1020.65':{},
 '29422.32':{},
 '23916.11':{},
 '15699.21':{},
 '3134.44':{},
 '2179.29':{},
 '23321.9':{},
 '16392.48':{},
 '20307.34':{},
 '11361.86':{},
 '1690.2':{},
 '2432.4':{},
 '10964.2':{},
 '9033.32':{},
 '4276.96':{}}}

#for storm in range(len(dict_of_stations_max_names)): #8 instances
for station in range(len(key_station)): #42 instances
    CompiledRiverStationData['2yr'][f'{key_station[station]}']['time series'] = dict_of_stations_2yr[f'{key_station[station]}']
    CompiledRiverStationData['2yr'][f'{key_station[station]}']['Qmax'] = dict_of_stations_max_2yr[f'{key_station[station]}']
    CompiledRiverStationData['2yr'][f'{key_station[station]}']['WSE'] = calc_wse['2yr'][f'{key_station[station]}']
for station in range(len(key_station)): #51 instances
    CompiledRiverStationData['5yr'][f'{key_station[station]}']['time series'] = dict_of_stations_5yr[f'{key_station[station]}']
    CompiledRiverStationData['5yr'][f'{key_station[station]}']['Qmax'] = dict_of_stations_max_5yr[f'{key_station[station]}']
    CompiledRiverStationData['5yr'][f'{key_station[station]}']['WSE'] = calc_wse['5yr'][f'{key_station[station]}']
for station in range(len(key_station)): #51 instances
    CompiledRiverStationData['10yr'][f'{key_station[station]}']['time series'] = dict_of_stations_10yr[f'{key_station[station]}']
    CompiledRiverStationData['10yr'][f'{key_station[station]}']['Qmax'] = dict_of_stations_max_10yr[f'{key_station[station]}']
    CompiledRiverStationData['10yr'][f'{key_station[station]}']['WSE'] = calc_wse['10yr'][f'{key_station[station]}']
for station in range(len(key_station)): #51 instances
    CompiledRiverStationData['25yr'][f'{key_station[station]}']['time series'] = dict_of_stations_25yr[f'{key_station[station]}']
    CompiledRiverStationData['25yr'][f'{key_station[station]}']['Qmax'] = dict_of_stations_max_25yr[f'{key_station[station]}']
    CompiledRiverStationData['25yr'][f'{key_station[station]}']['WSE'] = calc_wse['25yr'][f'{key_station[station]}']
for station in range(len(key_station)): #51 instances
    CompiledRiverStationData['50yr'][f'{key_station[station]}']['time series'] = dict_of_stations_50yr[f'{key_station[station]}']
    CompiledRiverStationData['50yr'][f'{key_station[station]}']['Qmax'] = dict_of_stations_max_50yr[f'{key_station[station]}']
    CompiledRiverStationData['50yr'][f'{key_station[station]}']['WSE'] = calc_wse['50yr'][f'{key_station[station]}']
for station in range(len(key_station)): #51 instances
    CompiledRiverStationData['100yr'][f'{key_station[station]}']['time series'] = dict_of_stations_100yr[f'{key_station[station]}']
    CompiledRiverStationData['100yr'][f'{key_station[station]}']['Qmax'] = dict_of_stations_max_100yr[f'{key_station[station]}']
    CompiledRiverStationData['100yr'][f'{key_station[station]}']['WSE'] = calc_wse['100yr'][f'{key_station[station]}']
for station in range(len(key_station)): #51 instances
    CompiledRiverStationData['200yr'][f'{key_station[station]}']['time series'] = dict_of_stations_200yr[f'{key_station[station]}']
    CompiledRiverStationData['200yr'][f'{key_station[station]}']['Qmax'] = dict_of_stations_max_200yr[f'{key_station[station]}']
    CompiledRiverStationData['200yr'][f'{key_station[station]}']['WSE'] = calc_wse['200yr'][f'{key_station[station]}']
for station in range(len(key_station)): #51 instances
    CompiledRiverStationData['500yr'][f'{key_station[station]}']['time series'] = dict_of_stations_500yr[f'{key_station[station]}']
    CompiledRiverStationData['500yr'][f'{key_station[station]}']['Qmax'] = dict_of_stations_max_500yr[f'{key_station[station]}']
    CompiledRiverStationData['500yr'][f'{key_station[station]}']['WSE'] = calc_wse['500yr'][f'{key_station[station]}']

# Serializing json
json_object = json.dumps(CompiledRiverStationData, indent=4)
date = datetime.today()
date = date.strftime("%d%m%Y_%H%M%S")

# Writing to sample.json
from WFK_SA_Master_WorkflowTrigger import JSON_name_ext
with open(r'C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\{}_CompiledRiverStationData_{}.json'.format(JSON_name_ext,date), "w") as outfile:
    outfile.write(json_object)