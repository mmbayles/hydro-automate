import sys
import fileinput
import textwrap
import re
import shutil

#TODO: Eric wants to fine-tune current conditions
#TODO: according to how Matthew will package data, how input is read needs adjustment
#TODO: function to recalculate lag times

#grab original .basin file from safe folder and copies it into where HMS where pull from it\
#TODO: can shutil.copy2 take on multiple destinations, to consolidate following?
#2yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_2yrStorm")
#5yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_5yrStorm")
#10yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_10yrStorm")
#25yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_25yrStorm")
#50yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_50yrStorm")
#100yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CoonCreek_100yrStorm")
#200yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_200yrStorm")
#500yr
shutil.copy2(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",
             r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_500yrStorm")

#define values to change to
#according to len(re.findall(r"Curve Number: (\d\d.\d\d)",fdata)), list must be 51 characters long
#var = [66.66] * 51 


with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_BasinParams.csv",'r') as f:
    fdata = f.read()
#CREATE DICTIONARY OF SUBBASIN CONSTANT PARAMETERS
CC_params_subbasins = re.findall(r"\n(.*?)\,", fdata)
CC_params_l = re.findall(r"\n.*?,(.*?)\,", fdata)
CC_params_l = [float(l) for l in CC_params_l]

CC_params_Y = re.findall(r"\n.*?,.*?,(\d*.\d*)", fdata)
CC_params_Y = [float(Y) for Y in CC_params_Y]

CC_params = {}
for subbasin in range(len(CC_params_subbasins)): #51 instances
    CC_params[f'{CC_params_subbasins[subbasin]}'] = np.array(([float(f'{CC_params_l[subbasin]}'),float(f'{CC_params_Y[subbasin]}')]))

#CREATE DICTIONARY OF SUBBASIN EXPERIMENTAL CNs
placeholder = [33]*len(CC_params_subbasins) #eventually, this placeholder could be a dictionary of experimental CNs coming from the DST

CC_CNs = {}
for subbasin in range(len(CC_params_subbasins)): #51 instances
    CC_CNs[f'{CC_params_subbasins[subbasin]}'] = placeholder[subbasin]

#CREATE DICTIONARY OF SUBBASINS' CALCULATED LAG
def calcL(subbasin):
    S = (1000/CC_CNs[subbasin]) - 10
    L = ((CC_params[subbasin][0]**0.8)*(S+1)**0.7)/(1900*CC_params[subbasin][1]**0.5)
    return L

CC_Ls = {}
for subbasin in range(len(CC_params_subbasins)): #51 instances
    CC_Ls[f'{CC_params_subbasins[subbasin]}'] = calcL(f'{CC_params_subbasins[subbasin]}')

#order the CN and L lists so that they can be eaten by re.sub
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

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
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_2yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_2yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)
    
#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------        
#5yr
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_5yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_5yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)


#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------        

#10yr
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_10yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_10yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------        

#25yr
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_25yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_25yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------        

#50yr
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_50yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_50yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)


#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------        

#100yr
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CoonCreek_100yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CoonCreek_100yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------        

#200yr
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_200yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_200yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#regenerate ordered lists every time (I know this is SO inefficient)---------------------------------------------
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

ordered_CNs = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])

#-----------------------------------------------------------------------------------------------------------        

#500yr
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_500yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_500yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)