#!/usr/bin/python
import os, sys
from time import strftime

test = False

timestamp = strftime("_%d%m%y")
if not test:
  if not os.path.exists("gridOutput"):
    os.system("mkdir gridOutput")
  if not os.path.exists("gridOutput/gridJobs"):
    os.system("mkdir gridOutput/gridJobs")

config_name = "source/ATLAS_xAHplusCPalgsExamples/configs/config_example.py"
extraTag = "" # Extra output tag for all files

# Replicate to a given DDM endpoint
destSE = ""

# Exclude site
excludeSite = ""

# PLEASE NOTE: all the samples will be sent using the config defined above
# Each data-taking period and MC16 campaign have dedicated configs
samples = { # should match to the keys of dataSamples.py or mcSamples.py
#    "MC20a_Zee_Sherpa_2211_PHYS_p5057",
#    "MC20a_Zmumu_Sherpa_2211_PHYS_p5057",
    "MC20a_Dijets_Pythia8_PHYS_p5057",
    "Data18_PHYS_p5057",
}

excludeAllExcept_DSIDs = [ # example 364104 will run over DSID=364104 only
  '364700',
  '364701',
]

excludeAllExcept_periods = [ # example: periodD will run over periodD only
]

##################################################################################
# DO NOT MODIFY
##################################################################################

#### Driver option ####
runType = 'grid' # CERN grid

## Set this only for group production submissions ##
production_name = ""

from mcSamples import *
from dataSamples import *

def getDataPeriod(sampleName):
  return sampleName[13:20]

def getMCDSID(sampleName):
  if 'valid' not in sampleName:
    return sampleName[11:17]
  else:
    return sampleName[7:13]

# Create a dictionary with all the requested samples
SamplesDict = dict()
for key in samples: # Loop over provided keys
  if "Data" in key:
    if key in dataSamples:
      for sample in dataSamples[key]: # add each dataset name to the dict
        dataPeriod = getDataPeriod(sample)
        if len(excludeAllExcept_periods) != 0:
          if dataPeriod not in excludeAllExcept_periods: continue # skip data period
        SamplesDict[key+"_"+dataPeriod] = sample
    else: print("ERROR: key "+key+" not found in dataSamples.py")
  else: # MC
    if key in mcSamples:
      for sample in mcSamples[key]: # add each dataset name to the dict
        dsid = getMCDSID(sample)
        if len(excludeAllExcept_DSIDs) != 0:
          if dsid not in excludeAllExcept_DSIDs: continue # skip DSID
        SamplesDict[key+"_"+dsid] = sample
    else: print("ERROR: key "+key+" not found in mcSamples.py")

for sampleName, sample in SamplesDict.items():

  output_tag = sampleName + extraTag + timestamp
  submit_dir = "gridOutput/gridJobs/submitDir_"+output_tag

  ## Configure submission driver ##
  driverCommand = ''
  if runType == 'grid':
    #driverCommand  = 'prun --optSubmitFlags="--forceStaged"'
    driverCommand  = 'prun --optSubmitFlags="--noEmail" '
    if destSE != "": driverCommand += ' --optGridDestSE='+destSE
    if excludeSite != "": driverCommand += ' --optSubmitFlags="--excludedSite='+excludeSite+'"'
    #driverCommand += ' --optGridMemory=4096' # Temporary
    if 'Systematics' in config_name: driverCommand += ' --optGridNFilesPerJob=1' # run one file per job when running with systematics
    driverCommand += ' --optGridOutputSampleName='
    #driverCommand = 'prun --optGridMaxNFilesPerJob=2 --optSubmitFlags="--forceStaged" --optGridOutputSampleName='
    #driverCommand = 'prun --optSubmitFlags="--skipScout --excludedSite=ANALY_CERN_SHORT,ANALY_BNL_SHORT" --optGridOutputSampleName='
    if len(production_name) > 0:
      #driverCommand = ' prun --optSubmitFlags="--memory=5120 --official --skipScout" --optGridOutputSampleName='
      driverCommand = ' prun --optSubmitFlags="--official --forceStaged" --optGridOutputSampleName='
      #driverCommand = ' prun --optGridMaxNFilesPerJob=2 --optSubmitFlags="--official --forceStaged" --optGridOutputSampleName='
      #driverCommand = ' prun --optSubmitFlags="--official" --optGridOutputSampleName='
      driverCommand += 'group.'+production_name
    else:
      driverCommand += 'user.%nickname%'
    driverCommand += '.%in:name[2]%.'+output_tag
  elif runType == 'local':
    driverCommand = ' direct'

  command = './source/xAODAnaHelpers/scripts/xAH_run.py'
  if runType == 'grid':
    command += ' --inputRucio '

  if 'sampleLists' in sample:
    command += ' --inputList'
  command += ' --files '+sample
  command += ' --config '+config_name
  if 'MC' in sampleName:
    command += " --extraOptions='--isMC'"
  else:
    command += " --extraOptions='--isData'"
  command += ' --force --submitDir '+submit_dir
  command += ' '+driverCommand

  print(command)
  if not test: os.system(command)
