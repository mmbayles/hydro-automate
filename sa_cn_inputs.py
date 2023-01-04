import re

#usage: Sensitivity Analysis will need to loop throuh each subbasin, adjusting one CN value at a time. 
#This tool will accept a watershed (CC or WFK) and subbasin value, and return the appropriate dictionary of subbasin:CN values 
#to be applied to Step 1 (CN and Lag adjustments)
#CC = sa_cn_inputs.SA_CN_Inputs('CC') or WFK = sa_cn_inputs.SA_CN_Inputs('WFK')
#CC.get_SA_CN('subbasin') or WFK.get_SA_CN('subbasin')

#define function to be used to write sets of CN value inputs
#list of list flattening code inspired by https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists

def adjust_cn(index,reduction):
    replaced_cn = reduction*cn_no_dams[index]
    if index == 0:
        adjusted_cn = [[replaced_cn], cn_no_dams[1:]] #place solo replaced value into its own list, so list of lists may be flattened
        adjusted_cn = [item for sublist in adjusted_cn for item in sublist] #utilizes .append(), an inefficient operation
        return adjusted_cn
    elif index == len(cn_no_dams):
        adjusted_cn = [cn_no_dams[0:(len(cn_no_dams))],[replaced_cn]]
        adjusted_cn = [item for sublist in adjusted_cn for item in sublist]
        return adjusted_cn
    elif 0<index and index<len(cn_no_dams):
        adjusted_cn = [cn_no_dams[0:index],[replaced_cn],cn_no_dams[(index+1):]]
        adjusted_cn = [item for sublist in adjusted_cn for item in sublist]
        return adjusted_cn


#CC------------------------------------------------------------------------------------------------------------------------
#grab CNs from No Dams basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\Original_BasinFile\Coon_Creek___No_Dams.basin",'r') as f:
    fdata = f.read()

CC_subbasins_no_dams = re.findall(r"Subbasin: (.*)",fdata)
cn_no_dams = re.findall(r"Curve Number: (\d\d.\d\d*)",fdata) #list of strings
cn_no_dams = [float(x) for x in cn_no_dams]

#build skeleton of basin:CN dictionary to be completed in function below
CC_SA_CN_dict = {}

#build experimental parameters & results dictionary

#build skeleton of CC_experimental dictionary
years = [5,10,25,50,100,200,500]
CC_anyl_stations = ['30304.08', '16878.2']
CC_experimental = {'5yr':{'30304.08':{}, '16878.2':{}}, 
             '10yr':{'30304.08':{}, '16878.2':{}},
             '25yr':{'30304.08':{}, '16878.2':{}},
             '50yr':{'30304.08':{}, '16878.2':{}},
             '100yr':{'30304.08':{}, '16878.2':{}},
             '200yr':{'30304.08':{}, '16878.2':{}},
             '500yr':{'30304.08':{}, '16878.2':{}}}

for year in years:
    CC_experimental[f'{year}yr']['30304.08'] = {CC_subbasins_no_dams[0]:{},CC_subbasins_no_dams[1]:{},CC_subbasins_no_dams[2]:{},CC_subbasins_no_dams[3]:{},CC_subbasins_no_dams[4]:{},CC_subbasins_no_dams[5]:{},CC_subbasins_no_dams[6]:{},CC_subbasins_no_dams[7]:{},CC_subbasins_no_dams[8]:{},CC_subbasins_no_dams[9]:{},CC_subbasins_no_dams[10]:{},CC_subbasins_no_dams[11]:{},CC_subbasins_no_dams[12]:{},CC_subbasins_no_dams[13]:{},CC_subbasins_no_dams[14]:{},CC_subbasins_no_dams[15]:{},CC_subbasins_no_dams[16]:{},CC_subbasins_no_dams[17]:{},CC_subbasins_no_dams[18]:{},CC_subbasins_no_dams[19]:{},CC_subbasins_no_dams[20]:{},CC_subbasins_no_dams[21]:{},CC_subbasins_no_dams[22]:{},CC_subbasins_no_dams[23]:{},CC_subbasins_no_dams[24]:{},CC_subbasins_no_dams[25]:{},CC_subbasins_no_dams[26]:{},CC_subbasins_no_dams[27]:{},CC_subbasins_no_dams[28]:{},CC_subbasins_no_dams[29]:{},CC_subbasins_no_dams[30]:{},CC_subbasins_no_dams[31]:{},CC_subbasins_no_dams[32]:{},CC_subbasins_no_dams[33]:{},CC_subbasins_no_dams[34]:{},CC_subbasins_no_dams[35]:{},CC_subbasins_no_dams[36]:{},CC_subbasins_no_dams[37]:{},CC_subbasins_no_dams[38]:{},CC_subbasins_no_dams[39]:{},CC_subbasins_no_dams[40]:{},CC_subbasins_no_dams[41]:{},CC_subbasins_no_dams[42]:{},CC_subbasins_no_dams[43]:{},CC_subbasins_no_dams[44]:{},CC_subbasins_no_dams[45]:{},CC_subbasins_no_dams[46]:{},CC_subbasins_no_dams[47]:{},CC_subbasins_no_dams[48]:{},CC_subbasins_no_dams[49]:{},CC_subbasins_no_dams[50]:{}}
    CC_experimental[f'{year}yr']['16878.2'] = {CC_subbasins_no_dams[0]:{},CC_subbasins_no_dams[1]:{},CC_subbasins_no_dams[2]:{},CC_subbasins_no_dams[3]:{},CC_subbasins_no_dams[4]:{},CC_subbasins_no_dams[5]:{},CC_subbasins_no_dams[6]:{},CC_subbasins_no_dams[7]:{},CC_subbasins_no_dams[8]:{},CC_subbasins_no_dams[9]:{},CC_subbasins_no_dams[10]:{},CC_subbasins_no_dams[11]:{},CC_subbasins_no_dams[12]:{},CC_subbasins_no_dams[13]:{},CC_subbasins_no_dams[14]:{},CC_subbasins_no_dams[15]:{},CC_subbasins_no_dams[16]:{},CC_subbasins_no_dams[17]:{},CC_subbasins_no_dams[18]:{},CC_subbasins_no_dams[19]:{},CC_subbasins_no_dams[20]:{},CC_subbasins_no_dams[21]:{},CC_subbasins_no_dams[22]:{},CC_subbasins_no_dams[23]:{},CC_subbasins_no_dams[24]:{},CC_subbasins_no_dams[25]:{},CC_subbasins_no_dams[26]:{},CC_subbasins_no_dams[27]:{},CC_subbasins_no_dams[28]:{},CC_subbasins_no_dams[29]:{},CC_subbasins_no_dams[30]:{},CC_subbasins_no_dams[31]:{},CC_subbasins_no_dams[32]:{},CC_subbasins_no_dams[33]:{},CC_subbasins_no_dams[34]:{},CC_subbasins_no_dams[35]:{},CC_subbasins_no_dams[36]:{},CC_subbasins_no_dams[37]:{},CC_subbasins_no_dams[38]:{},CC_subbasins_no_dams[39]:{},CC_subbasins_no_dams[40]:{},CC_subbasins_no_dams[41]:{},CC_subbasins_no_dams[42]:{},CC_subbasins_no_dams[43]:{},CC_subbasins_no_dams[44]:{},CC_subbasins_no_dams[45]:{},CC_subbasins_no_dams[46]:{},CC_subbasins_no_dams[47]:{},CC_subbasins_no_dams[48]:{},CC_subbasins_no_dams[49]:{},CC_subbasins_no_dams[50]:{}}



#populate CC_experimental CN values, utilizing adjust_cn function
for station in range(len(CC_anyl_stations)): #2 instances
    for basin in range(len(CC_subbasins_no_dams)): #51 instances
        CC_experimental['5yr'][f'{CC_anyl_stations[station]}'][f'{CC_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9) #CC_subbasins_no_dams maps to cn_no_dams
        CC_experimental['10yr'][f'{CC_anyl_stations[station]}'][f'{CC_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        CC_experimental['25yr'][f'{CC_anyl_stations[station]}'][f'{CC_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        CC_experimental['50yr'][f'{CC_anyl_stations[station]}'][f'{CC_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        CC_experimental['100yr'][f'{CC_anyl_stations[station]}'][f'{CC_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        CC_experimental['200yr'][f'{CC_anyl_stations[station]}'][f'{CC_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        CC_experimental['500yr'][f'{CC_anyl_stations[station]}'][f'{CC_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)

#WFK----------------------------------------------------------------------------------------------------------------------------
#grab CNs from No Dams basin file
with open(r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\Original_BasinFile\West_Fork_Kickapoo___No_Dams.basin",'r') as f:
    fdata = f.read()

WFK_subbasins_no_dams = re.findall(r"Subbasin: (.*)",fdata)
cn_no_dams = re.findall(r"Curve Number: (\d\d.\d\d*)",fdata) #list of strings
cn_no_dams = [float(x) for x in cn_no_dams]

#build skeleton of basin:CN dictionary to be completed in function below
WFK_SA_CN_dict = {}
        
#build experimental parameters & results dictionary

#build skeleton of WFK_experimental dictionary
years = [5,10,25,50,100,200,500]
WFK_anyl_stations = ['3134.44', '4276.96']
WFK_experimental = {'5yr':{'3134.44':{}, '4276.96':{}}, 
             '10yr':{'3134.44':{}, '4276.96':{}},
             '25yr':{'3134.44':{}, '4276.96':{}},
             '50yr':{'3134.44':{}, '4276.96':{}},
             '100yr':{'3134.44':{}, '4276.96':{}},
             '200yr':{'3134.44':{}, '4276.96':{}},
             '500yr':{'3134.44':{}, '4276.96':{}}}

for year in years:
    WFK_experimental[f'{year}yr']['3134.44'] = {WFK_subbasins_no_dams[0]:{},WFK_subbasins_no_dams[1]:{},WFK_subbasins_no_dams[2]:{},WFK_subbasins_no_dams[3]:{},WFK_subbasins_no_dams[4]:{},WFK_subbasins_no_dams[5]:{},WFK_subbasins_no_dams[6]:{},WFK_subbasins_no_dams[7]:{},WFK_subbasins_no_dams[8]:{},WFK_subbasins_no_dams[9]:{},WFK_subbasins_no_dams[10]:{},WFK_subbasins_no_dams[11]:{},WFK_subbasins_no_dams[12]:{},WFK_subbasins_no_dams[13]:{},WFK_subbasins_no_dams[14]:{},WFK_subbasins_no_dams[15]:{},WFK_subbasins_no_dams[16]:{},WFK_subbasins_no_dams[17]:{},WFK_subbasins_no_dams[18]:{},WFK_subbasins_no_dams[19]:{},WFK_subbasins_no_dams[20]:{},WFK_subbasins_no_dams[21]:{},WFK_subbasins_no_dams[22]:{},WFK_subbasins_no_dams[23]:{},WFK_subbasins_no_dams[24]:{},WFK_subbasins_no_dams[25]:{},WFK_subbasins_no_dams[26]:{},WFK_subbasins_no_dams[27]:{},WFK_subbasins_no_dams[28]:{},WFK_subbasins_no_dams[29]:{},WFK_subbasins_no_dams[30]:{},WFK_subbasins_no_dams[31]:{},WFK_subbasins_no_dams[32]:{},WFK_subbasins_no_dams[33]:{},WFK_subbasins_no_dams[34]:{},WFK_subbasins_no_dams[35]:{},WFK_subbasins_no_dams[36]:{},WFK_subbasins_no_dams[37]:{},WFK_subbasins_no_dams[38]:{},WFK_subbasins_no_dams[39]:{},WFK_subbasins_no_dams[40]:{},WFK_subbasins_no_dams[41]:{}}
    WFK_experimental[f'{year}yr']['4276.96'] = {WFK_subbasins_no_dams[0]:{},WFK_subbasins_no_dams[1]:{},WFK_subbasins_no_dams[2]:{},WFK_subbasins_no_dams[3]:{},WFK_subbasins_no_dams[4]:{},WFK_subbasins_no_dams[5]:{},WFK_subbasins_no_dams[6]:{},WFK_subbasins_no_dams[7]:{},WFK_subbasins_no_dams[8]:{},WFK_subbasins_no_dams[9]:{},WFK_subbasins_no_dams[10]:{},WFK_subbasins_no_dams[11]:{},WFK_subbasins_no_dams[12]:{},WFK_subbasins_no_dams[13]:{},WFK_subbasins_no_dams[14]:{},WFK_subbasins_no_dams[15]:{},WFK_subbasins_no_dams[16]:{},WFK_subbasins_no_dams[17]:{},WFK_subbasins_no_dams[18]:{},WFK_subbasins_no_dams[19]:{},WFK_subbasins_no_dams[20]:{},WFK_subbasins_no_dams[21]:{},WFK_subbasins_no_dams[22]:{},WFK_subbasins_no_dams[23]:{},WFK_subbasins_no_dams[24]:{},WFK_subbasins_no_dams[25]:{},WFK_subbasins_no_dams[26]:{},WFK_subbasins_no_dams[27]:{},WFK_subbasins_no_dams[28]:{},WFK_subbasins_no_dams[29]:{},WFK_subbasins_no_dams[30]:{},WFK_subbasins_no_dams[31]:{},WFK_subbasins_no_dams[32]:{},WFK_subbasins_no_dams[33]:{},WFK_subbasins_no_dams[34]:{},WFK_subbasins_no_dams[35]:{},WFK_subbasins_no_dams[36]:{},WFK_subbasins_no_dams[37]:{},WFK_subbasins_no_dams[38]:{},WFK_subbasins_no_dams[39]:{},WFK_subbasins_no_dams[40]:{},WFK_subbasins_no_dams[41]:{}}


#populate WFK_experimental CN values, utilizing adjust_cn function
for station in range(len(WFK_anyl_stations)): #2 instances
    for basin in range(len(WFK_subbasins_no_dams)): #42 instances
        WFK_experimental['5yr'][f'{WFK_anyl_stations[station]}'][f'{WFK_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9) #WFK_subbasins_no_dams maps to cn_no_dams
        WFK_experimental['10yr'][f'{WFK_anyl_stations[station]}'][f'{WFK_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        WFK_experimental['25yr'][f'{WFK_anyl_stations[station]}'][f'{WFK_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        WFK_experimental['50yr'][f'{WFK_anyl_stations[station]}'][f'{WFK_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        WFK_experimental['100yr'][f'{WFK_anyl_stations[station]}'][f'{WFK_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        WFK_experimental['200yr'][f'{WFK_anyl_stations[station]}'][f'{WFK_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)
        WFK_experimental['500yr'][f'{WFK_anyl_stations[station]}'][f'{WFK_subbasins_no_dams[basin]}']['cn'] = adjust_cn(basin,0.9)        

#-------------------------------------------------------------------------------------------------------------------------------
#retrieve set of CN values based on which iteration outer loop (reduction of CN to specific subbasin) is being executed
class SA_CN_Inputs:
    def __init__(self, watershed):
        self.watershed = watershed
    def get_SA_CN(self,subbasin):
        if self.watershed == 'CC':
            CC_SA_CN = CC_experimental['5yr']['30304.08'][subbasin]['cn'] #set of CN values is the same across stations and storms, thus arbitrary values for each may be used in this tool
            for basin in range(len(CC_subbasins_no_dams)):
                CC_SA_CN_dict[f'{CC_subbasins_no_dams[basin]}'] = CC_SA_CN[basin]
            return CC_SA_CN_dict
        if self.watershed == 'WFK':
            WFK_SA_CN = WFK_experimental['5yr']['3134.44'][subbasin]['cn']
            for basin in range(len(WFK_subbasins_no_dams)):
                WFK_SA_CN_dict[f'{WFK_subbasins_no_dams[basin]}'] = WFK_SA_CN[basin]
            return WFK_SA_CN_dict