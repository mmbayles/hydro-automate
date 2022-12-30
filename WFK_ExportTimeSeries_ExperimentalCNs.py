# name=WFK_ExportTimeSeries_ExperimentalCNs
# description=Export time series data after running final version of WFK HMS model
# displayinmenu=true
# displaytouser=true
# displayinselector=true
from hec.script import *
from hec.io import TimeSeriesContainer
from hec.io import PairedDataContainer
from hec.hecmath import TimeSeriesMath
from hec.hecmath import PairedDataMath
from hec.heclib.dss import HecDss, DSSPathname, HecTimeSeries
import java
from hec.heclib.dss import *
import sys

#syntax and guidance to develop this script found in DSS Programmers Guide for Java and HEC-DSSVue Users Manual
#https://www.hec.usace.army.mil/confluence/dssjavaprogrammer/dss-progammers-guide-for-java
#https://www.hec.usace.army.mil/software/hec-dssvue/documentation/User'sManual_2.0/HEC-DSSVue_20_Users_Manual.pdf


reaches = ['HC A - HC B',
 'HC B- HC C',
 'HC C - JUNCTION',
 'HC D - JUNCTION',
 'HC C&D - HC E',
 'WFK 17 - JUNCTION',
 'B A - JUNCTION',
 'B A & WFK 17 - B B',
 'B B - B C',
 'WFK 4 - JUNCTION',
 'WFK 5 - JUNCTION',
 'WFK 12 - KC WFK L',
 'WFK 3 - KC WFK F',
 'KLINKNER - JUNCTION',
 'MLSNA - JUNCTION',
 'JUNCTION - KC WFK A',
 'KC WFK A - KC WFK B',
 'WFK 1 - JUNCTION',
 'KC WFK C - JUNCTION',
 'JUNCTION - KC WFK D',
 'KC WFK D - JUNCTION',
 'KC WFK B - JUNCTION',
 'JUNCTION - KC WFK E',
 'WFK16 - KC WFK E',
 'KC WFK E - JUNCTION',
 'KC WFK F - JUNCTION',
 'JUNCTION - JUNCTION',
 'JUNCTION - KC WFK H',
 'KC WFK H & I - JUNCTION',
 'KC WFK L - JUNCTION',
 'JUNCTION- JUNCTION (KCWFK K)',
 'KC WFK J - JUNCTION',
 'JUNCTION 2- JUNCTION 3',
 'KC WFK M - JUNCTION',
 'JUNCTION - KC WFK K',
 'JUNCTION - SB',
 'SEAS & KC WFK - WFK B',
 'WFK A - JUNCTION',
 'WFK B JUNCTIONS',
 'WFK D - JUNCTION',
 'WFK B - JUNCTION',
 'WFK C - JUNCTION',
 'JUNCTION - WFK E',
 'WFK F - JUNCTION',
 'JUNCTION - WFK G',
 'B C - B D',
 'JUNCTION - JUNCTION - WFK H',
 'WFK I - JUNCTION',
 'JUNCTION - WFK H',
 'WFK H - JUNCTION',
 'HC E  - JUNCTION',
 'JUNCTION - OUTFLOW']


#2yr
file = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/WFK_2yrStorm/MSE4_No_Dams.dss" # specify the DSS file
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 2yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/TimeSeriesData/2yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 


#5yr
file = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/WFK_5yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 5yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/TimeSeriesData/5yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#10yr
file = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/WFK_10yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 10yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/TimeSeriesData/10yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#25yr
file = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/WFK_25yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 25yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/TimeSeriesData/25yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#50yr
file = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/WFK_50yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 50yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/TimeSeriesData/50yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#100yr
file = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/WFK_100yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 100yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/TimeSeriesData/100yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#200yr
file = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/WFK_200yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 200yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/TimeSeriesData/200yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 

#500yr
file = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/WFK_500yrStorm/MSE4_No_Dams.dss" 
dssfile = HecDss.open(file) # open the file
#pull time series data into .txt file for each HMS reach
for reach in range(len(reaches)):
	flow = dssfile.get("//{}/FLOW/*/5Minute/RUN:MSE4 NO DAMS/".format(reaches[reach]))
	theTable = Tabulate.newTable("{} 500yr Storm Flow Time Series".format(reaches[reach])) # create the table
	theTable.addData(flow) # add the data
	theTable.showTable() # show the table (script won't run without this command; would rather tables visibility be muted)
	opts = TableExportOptions()# get new export options
	opts.delimiter = ","# delimit with commas
	fileName = "C:/Users/paige/OneDrive/Documents/HMS_WFK_Final/TimeSeriesData/500yr_{}.txt".format(reaches[reach]) # set the output file name
	theTable.export(fileName, opts)# export to the file
dssfile.close() 
