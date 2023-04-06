import subprocess
import os
import time
import CC_cn_adjustments as cn_adjust

# utility: trigger full workflow, one-off
project_dir = os.path.join(os.getcwd(), "HMS_CC_FINAL")
hms_exe = ""
print("hms model directory", project_dir)

# STEP1: adjust CN and lag values in HMS .basin file
# list_files = subprocess.run("python CC_cn_adjustments.py", cwd=r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final")
list_files = cn_adjust.prepare_model_runs(project_dir)
# # time.sleep(2)
# print("The exit code to run STEP1 was %d" % list_files.returncode)

# if list_files.returncode == 0:
#     # STEP2: run all storm scenarios
#     # must cd to installation folder of HEC
#     t = r"C:\Program Files\HEC\HEC-HMS\4.6"
#     os.chdir(t)
#     list_files = subprocess.run(
#         [r"hec-hms.cmd", "-s", r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final\CC_HMSRun.script"],
#         executable=r"C:\Program Files\HEC\HEC-HMS\4.6\hec-hms.cmd")
#     print("The exit code to run STEP2 was %d" % list_files.returncode)
#
#     time.sleep(2)
#     if list_files.returncode == 0:
#         # STEP3: extract each HMS reach time series data from output .dss file, compile to .json file
#         list_files = subprocess.run("python CC_dss_output.py", cwd=r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final")
#         print("The exit code to run STEP3 was %d" % list_files.returncode)
#
#         time.sleep(2)
#         if list_files.returncode == 0:
#             # STEP4: compile time series, peak Q, peak WSE data to JSON file
#             list_files = subprocess.run("python CC_CompiledDataToJSON.py",
#                                         cwd=r"C:\Users\paige\OneDrive\Documents\HMS_CC_Final")
#             print("The exit code to run STEP4 was %d" % list_files.returncode)
