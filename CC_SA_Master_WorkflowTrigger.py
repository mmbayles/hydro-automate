import subprocess
import os
import time

#Master Loop
#CC
for basin in range(len(subbasins_no_dams)):
    CC_CNs = CC.get_SA_CN(f'{subbasins_no_dams[basin]}') #this updated definition of CC_CNs will be applied to the object by the same name in step 1
    JSON_name_ext = f'{subbasins_no_dams[basin]}' #this updated definition of JSON_name_ext will be applied to the object by the same name in step 4
    
    
    #Core workflow- inner loop
    #STEP1: adjust CN and lag values in HMS .basin file
    list_files = subprocess.run("python CC_sa_cn_adjustments.py",cwd=r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final")
    print("The exit code to run STEP1 was %d" %list_files.returncode)

    time.sleep(2)
    
    #STEP2: run all storm scenarios
    #must cd to installation folder of HEC
    t = r"C:\Program Files\HEC\HEC-HMS\4.6"
    os.chdir(t)
    list_files = subprocess.run([r"hec-hms.cmd", "-s", r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_HMSRun.script"],executable=r"C:\Program Files\HEC\HEC-HMS\4.6\hec-hms.cmd")
    print("The exit code to run STEP2 was %d" %list_files.returncode)

    time.sleep(2)

    #STEP3: extract each HMS reach time series data from output .dss file, save to .txt files
    t = r"C:\Program Files\HEC\HEC-DSSVue"
    os.chdir(t)
    list_files = subprocess.run([r"HEC-DSSVue.exe", r"C:\Users\paige\AppData\Roaming\HEC\HEC-DSSVue\scripts\CC_ExportTimeSeries_ExperimentalCNs.py"],executable=r"C:\Program Files\HEC\HEC-DSSVue\HEC-DSSVue.exe")
    print("The exit code to run STEP3 was %d" %list_files.returncode)

    time.sleep(2)

    #STEP4: compile time series, peak Q, peak WSE data to JSON file
    list_files = subprocess.run("python CC_sa_CompiledDataToJSON.py",cwd=r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final")
    print("The exit code to run STEP4 was %d" %list_files.returncode)