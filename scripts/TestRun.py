import os,sys

# PHYS
sample = '/eos/atlas/atlaslocalgroupdisk/jetetmiss/Jona/DAOD_PHYS_test_samples/R22/MC/MC20a_dijets/mc20_13TeV/DAOD_PHYS.28673892._000138.pool.root.1'

config = 'minimal_commonCP_Jona.py'

is_data = False
is_mc = True

################################################
## DO NOT MODIFY
################################################

# run xAH_run.py
command  = "python source/xAODAnaHelpers/scripts/xAH_run.py --config source/ATLAS_xAHplusCPalgsExamples/configs/"
command += config
if is_mc:
  command += " --extraOptions='--isMC'"
elif is_data:
  command += " --extraOptions='--isData'"
command += " --nevents 2000"
command += " --files "
command += sample
command += " --force direct"
print(command)
os.system(command)
