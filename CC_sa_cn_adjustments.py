import sys
import fileinput
import textwrap
import re
import shutil
import numpy as np
import cn_inputs

#script functionality: using original No Dams .basin file, swap FloodScape-user defined CNs within .basin file, recalculate Lag accordingly

#TODO: current CN values may be fine-tuned according to SmartScape data, current CN conditions are, as of now, pulled from NRCS contractor's .basin files 
#TODO: according to how data will be packaged from FloodScape, how input is read needs adjustment


# grab original .basin file from safe folder and copy to where HMS will pull from it. these copied .basin files stored in their respective filepaths will edited below

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


#basin parameters built into basin models are saved to a BasinParams.csv file, adapted from data provided by NRCS contractors
#these values are needed to recalculate lag (L) according to the watershed lag method (part 630.1502a Hydrology National Engineering Handbook)
#L = ((l**0.8)(S+1)**0.7)/(1900*Y**0.5) where S = (1000/CN) - 10

with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_BasinParams.csv",'r') as f:
    fdata = f.read()
#create dictionary of subbasin constant parameters
CC_params_subbasins = re.findall(r"\n(.*?)\,", fdata)

CC_params_l = re.findall(r"\n.*?,(.*?)\,", fdata)
CC_params_l = [float(l) for l in CC_params_l]

CC_params_Y = re.findall(r"\n.*?,.*?,(\d*.\d*)", fdata)
CC_params_Y = [float(Y) for Y in CC_params_Y]

CC_params = {}
for subbasin in range(len(CC_params_subbasins)): #51 instances
    CC_params[f'{CC_params_subbasins[subbasin]}'] = np.array(([float(f'{CC_params_l[subbasin]}'),float(f'{CC_params_Y[subbasin]}')]))

#how input is read may need adjustment, see TODO section------------------------------------------------------------------------------
#bring in dictionary of subbasin experimental CNs
# CC_CNs_input = cn_inputs.CN_Inputs('CC') #bring in module
# CC_CNs_input.reset() #ensure values are reset, otherwise past replacements perpetuate
# #CC_CNs_input.replaceCN('Lower Coon Creek I', 66.66) #if we wanted to change any CN values
# CC_CNs = CC_CNs_input.get_basin_CN_input() #this is a subbasin:CN dictionary

#Bring in current dictionary of subbasin:CN values based on which iteration master loop is on
from CC_SA_Master_WorkflowTrigger import CC_CNs
#-------------------------------------------------------------------------------------------------------------------------------------

#define function to calculate lag (as referenced in part 630.1502a Hydrology National Engineering Handbook; see above)
def calcL(subbasin):
    S = (1000/CC_CNs[subbasin]) - 10
    L = ((CC_params[subbasin][0]**0.8)*(S+1)**0.7)/(1900*CC_params[subbasin][1]**0.5)
    return L

#create dictionary of subbasins' calculated lag
CC_Ls = {}
for subbasin in range(len(CC_params_subbasins)): #51 instances
    CC_Ls[f'{CC_params_subbasins[subbasin]}'] = calcL(f'{CC_params_subbasins[subbasin]}')


#order the CN and L lists so that they can be eaten by re.sub; create template from which to regenerate ordered lists for each storm, as list.pop() consumes list
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
ordered_subbasins = re.findall(r"Subbasin: (.*)", fdata)
ordered_Ls_template = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_Ls_template.append(CC_Ls[f'{ordered_subbasins[ordered_subbasin]}'])

    
ordered_CNs_template = []
for ordered_subbasin in range(len(ordered_subbasins)):
    ordered_CNs_template.append(CC_CNs[f'{ordered_subbasins[ordered_subbasin]}'])
    


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


#2yr-----------------------------------------------------------------------------------------------------------
ordered_Ls = ordered_Ls_template.copy()
ordered_CNs = ordered_CNs_template.copy()
#replace values in .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_2yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)
#write to the .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_2yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#-----------------------------------------------------------------------------------------------------------        
#5yr
ordered_Ls = ordered_Ls_template.copy()
ordered_CNs = ordered_CNs_template.copy()
#replace values in .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_5yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)
#write to the .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_5yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#-----------------------------------------------------------------------------------------------------------        
#10yr
ordered_Ls = ordered_Ls_template.copy()
ordered_CNs = ordered_CNs_template.copy()
#replace values in .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_10yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)
#write to the .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_10yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#-----------------------------------------------------------------------------------------------------------        
#25yr
ordered_Ls = ordered_Ls_template.copy()
ordered_CNs = ordered_CNs_template.copy()
#replace values in .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_25yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)
#write to the .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_25yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#-----------------------------------------------------------------------------------------------------------        
#50yr
ordered_Ls = ordered_Ls_template.copy()
ordered_CNs = ordered_CNs_template.copy()
#replace values in .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_50yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)
#write to the .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_50yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)
    
#-----------------------------------------------------------------------------------------------------------        
#100yr
ordered_Ls = ordered_Ls_template.copy()
ordered_CNs = ordered_CNs_template.copy()
#replace values in .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CoonCreek_100yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)
#write to the .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CoonCreek_100yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)

#-----------------------------------------------------------------------------------------------------------        
#200yr
ordered_Ls = ordered_Ls_template.copy()
ordered_CNs = ordered_CNs_template.copy()
#replace values in .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_200yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
#for loop; create a lookup between .basin file subbasin and above dictionaries
#OR, reorder and pop from end with each function... this seems way easier, less robust
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)
#write to .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_200yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)


#-----------------------------------------------------------------------------------------------------------        
#500yr
ordered_Ls = ordered_Ls_template.copy()
ordered_CNs = ordered_CNs_template.copy()
#replace values in .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_500yrStorm\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()
fdata = re.sub(r"Curve Number: (\d\d.\d\d*)", replace_CN, fdata)
fdata = re.sub(r"Lag: (\d\d.\d\d*)", replace_L, fdata)
#write to .basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_500yrStorm\Coon_Creek___No_Dams.basin",'w') as f:
    f.write(fdata)
    
    