import sys
import fileinput
import textwrap
import re
import shutil
import numpy as np

#TODO: Eric wants to fine-tune current conditions
#TODO: according to how Matthew will package data, how input is read needs adjustment
#TODO: function to recalculate lag times

#grab original .basin file from safe folder and copies it into where HMS where pull from it\
#TODO: can shutil.copy2 take on multiple destinations, to consolidate following?
#2yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_2yrStorm")
#5yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_5yrStorm")
#10yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_10yrStorm")
#25yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_25yrStorm")
#50yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_50yrStorm")
#100yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_100yrStorm")
#200yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_200yrStorm")
#500yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_500yrStorm")

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_BasinParams.csv",'r') as f:
    fdata = f.read()
#CREATE DICTIONARY OF SUBBASIN CONSTANT PARAMETERS
WFK_params_subbasins = re.findall(r"\n(.*?)\,", fdata)

WFK_params_l = re.findall(r"\n.*?,(.*?)\,", fdata)
WFK_params_l = [float(l) for l in WFK_params_l]

WFK_params_Y = re.findall(r"\n.*?,.*?,(\d*.\d*)", fdata)
WFK_params_Y = [float(Y) for Y in WFK_params_Y]

WFK_params = {}
for subbasin in range(len(WFK_params_subbasins)): #42 instances
    WFK_params[f'{WFK_params_subbasins[subbasin]}'] = np.array(([float(f'{WFK_params_l[subbasin]}'),float(f'{WFK_params_Y[subbasin]}')]))


#CREATE DICTIONARY OF SUBBASIN EXPERIMENTAL CNs
placeholder = [33]*len(WFK_params_subbasins)
WFK_CNs = {}
for subbasin in range(len(WFK_params_subbasins)): #42 instances
    WFK_CNs[f'{WFK_params_subbasins[subbasin]}'] = placeholder[subbasin]


#CREATE DICTIONARY OF SUBBASINS' CALCULATED LAG
def calcL(subbasin):
    S = (1000/WFK_CNs[subbasin]) - 10
    L = ((WFK_params[subbasin][0]**0.8)*(S+1)**0.7)/(1900*WFK_params[subbasin][1]**0.5)
    return L

WFK_Ls = {}
for subbasin in range(len(WFK_params_subbasins)): #51 instances
    WFK_Ls[f'{WFK_params_subbasins[subbasin]}'] = calcL(f'{WFK_params_subbasins[subbasin]}')

#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------        
#define replacement functions
def replace_CN(m):
    if not ordered_CNs: 
        raise Exception("length of replacements does not match length of Curve Number instances in file")

    return f"Curve Number: {ordered_CNs.pop(0)}"

def replace_L(m):
    if not ordered_Ls: 
        raise Exception("length of replacements does not match length of Lag instances in file")

    return f"Lag: {ordered_Ls.pop(0)}"

#TODO: inefficient. opens each file in each storm directory one by one. regenerates var each time so that replacement
#has correct values to chew on
# #replace text in file
#2yr
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_2yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d\d?.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_2yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
    f.write(fdata)
    
#5yr
#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------    
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_5yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d\d?.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_5yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
    f.write(fdata)

#10yr
#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------     
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_10yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d\d?.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_10yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
    f.write(fdata)
    
#25yr
#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------     
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_25yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d\d?.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_25yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
    f.write(fdata)
    
#50yr
#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------     
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_50yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d\d?.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_50yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
    f.write(fdata)
    
#100yr
#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------     
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_100yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d\d?.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_100yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
    f.write(fdata)
    
#200yr
#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------     
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_200yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d\d?.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_200yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
    f.write(fdata)
    
#500yr
#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(WFK_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(WFK_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------    
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_500yrStorm\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d\d?.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_500yrStorm\West_Fork_Kickapoo___No_Dams.basin",'w') as f:
    f.write(fdata)
    