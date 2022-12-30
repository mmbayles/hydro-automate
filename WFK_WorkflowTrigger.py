import subprocess
import os
import time

#STEP1
#list_files = subprocess.run("python WFK_cn_adjustments.py",cwd=r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final")
#print("The exit code to run STEP1 was %d" %list_files.returncode)

#let computer catch up before continuing
time.sleep(2)

#STEP2
#must cd to installation folder of HEC
t = r"C:\Program Files\HEC\HEC-HMS\4.6"
os.chdir(t)
list_files = subprocess.run([r"hec-hms.cmd", "-s", r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final\WFK_HMSRun.script"],executable=r"C:\Program Files\HEC\HEC-HMS\4.6\hec-hms.cmd")
print("The exit code to run STEP2 was %d" %list_files.returncode)

time.sleep(2)

#STEP3
t = r"C:\Program Files\HEC\HEC-DSSVue"
os.chdir(t)
list_files = subprocess.run([r"HEC-DSSVue.exe", r"C:\Users\paige\AppData\Roaming\HEC\HEC-DSSVue\scripts\WFK_ExportTimeSeries_ExperimentalCNs.py"],executable=r"C:\Program Files\HEC\HEC-DSSVue\HEC-DSSVue.exe")
print("The exit code to run STEP3 was %d" %list_files.returncode)

time.sleep(2)

#STEP4
list_files = subprocess.run("python WFK_CompiledDataToJSON.py",cwd=r"C:\Users\paige\OneDrive\Documents\HMS_WFK_Final")
print("The exit code to run STEP4 was %d" %list_files.returncode)

