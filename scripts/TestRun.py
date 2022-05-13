import os,sys

# PHYS
#sample = '/eos/atlas/user/j/jbossios/SM/ZHFRun2/DAOD_PHYS_testFiles/mc16_13TeV/DAOD_PHYS.20609937._000047.pool.root.1'
#sample = '/eos/atlas/user/j/jbossios/xAH/DAOD_PHYS_testFile/DAOD_PHYS.27674492._000001.pool.root.1'

# dijets
#sample = '/eos/atlas/atlaslocalgroupdisk/jetetmiss/Jona/DAOD_PHYS_test_samples/R22/MC/MC20a_dijets/mc20_13TeV/DAOD_PHYS.28673892._000138.pool.root.1'

# Zee
#sample = '/eos/atlas/atlaslocalgroupdisk/jetetmiss/Jona/DAOD_PHYS_test_samples/R22/MC/MC20a_Zee_Sh_2211/mc20_13TeV/DAOD_PHYS.28687438._000008.pool.root.1'

# Zmumu
#sample = '/eos/atlas/atlaslocalgroupdisk/jetetmiss/Jona/DAOD_PHYS_test_samples/R22/MC/MC20a_Zmumu_Sh_2211/mc20_13TeV/DAOD_PHYS.28687472._000012.pool.root.1'

# Data18
sample = '/eos/atlas/atlaslocalgroupdisk/jetetmiss/Jona/DAOD_PHYS_test_samples/R22/Data/2018/data18_13TeV/DAOD_PHYS.28592482._000163.pool.root.1'

config = 'config_example.py'

is_mc = False

################################################
## DO NOT MODIFY
################################################

# run xAH_run.py
command  = "python source/xAODAnaHelpers/scripts/xAH_run.py --config source/ATLAS_xAHplusCPalgsExamples/configs/"
command += config
if is_mc:
  command += " --extraOptions='--isMC'"
else:
  command += " --extraOptions='--isData'"
command += " --nevents 2000"
command += " --files "
command += sample
command += " --force direct"
print(command)
os.system(command)
