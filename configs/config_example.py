#import ROOT
from xAODAnaHelpers import Config as xAH_config

import sys
import os

import argparse
import shlex

c = xAH_config()

# Read arguments
parser = argparse.ArgumentParser()
parser.add_argument('--isMC', dest='is_mc', action="store_true", default=False)
parser.add_argument('--isData', dest='is_data', action="store_true", default=False)
extra_args = parser.parse_args(shlex.split(args.extra_options))

# Protections
if not extra_args.is_mc and not extra_args.is_data:
  print('ERROR: isMC and isData were not set (choose one) exiting')
  sys.exit(1)
if extra_args.is_mc and extra_args.is_data:
  print('ERROR: isMC and isData were set (choose one) exiting')
  sys.exit(1)

grls = [
    'GoodRunsLists/data15_13TeV/20170619/data15_13TeV.periodAllYear_DetStatus-v89-pro21-02_Unknown_PHYS_StandardGRL_All_Good_25ns.xml',
    'GoodRunsLists/data16_13TeV/20180129/data16_13TeV.periodAllYear_DetStatus-v89-pro21-01_DQDefects-00-02-04_PHYS_StandardGRL_All_Good_25ns.xml',
    'GoodRunsLists/data17_13TeV/20180619/data17_13TeV.periodAllYear_DetStatus-v99-pro22-01_Unknown_PHYS_StandardGRL_All_Good_25ns_Triggerno17e33prim.xml',
    'GoodRunsLists/data18_13TeV/20190318/data18_13TeV.periodAllYear_DetStatus-v102-pro22-04_Unknown_PHYS_StandardGRL_All_Good_25ns_Triggerno17e33prim.xml',
]

lumis = dict()
lumis["MC16a"] = [
    str("GoodRunsLists/data15_13TeV/20170619/PHYS_StandardGRL_All_Good_25ns_276262-284484_OflLumi-13TeV-008.root"),
    str("GoodRunsLists/data16_13TeV/20180129/PHYS_StandardGRL_All_Good_25ns_297730-311481_OflLumi-13TeV-009.root"),
]
lumis["MC16d"] = [str("GoodRunsLists/data17_13TeV/20180619/physics_25ns_Triggerno17e33prim.lumicalc.OflLumi-13TeV-010.root")]
lumis["MC16e"] = [str("GoodRunsLists/data18_13TeV/20190318/ilumicalc_histograms_None_348885-364292_OflLumi-13TeV-010.root")]

#######################
# Schedule algorithms
#######################

check_duplicates_flag = 'm_checkDuplicatesData' if extra_args.is_data else 'm_checkDuplicatesMC'

# BasicEventSelection
# missing: m_applyIsBadBatmanFlag
c.algorithm("BasicEventSelection", {
    "m_name"                      : "basicEventSel",
    "m_derivationName"            : "",
    "m_applyGRLCut"               : True if extra_args.is_data else False,
    "m_doPUreweighting"           : True if extra_args.is_mc else False,  # Temporary
    "m_PRWFileNames"              : "xAODAnaHelpers/PRW_MC20a_all.root",  # NOTE: harcoded!
    "m_lumiCalcFileNames"         : ",".join(lumis["MC16a"]),  # NOTE: harcoded!
    #"m_autoconfigPRW"             : True,
    "m_GRLxml"                    : ",".join(grls),
    "m_PVNTrack"                  : 2,
    "m_applyPrimaryVertexCut"     : True,
    "m_applyEventCleaningCut"     : True,
    "m_applyJetCleaningEventFlag" : True,
    "m_applyCoreFlagsCut"         : False,
    "m_applyTriggerCut"           : True,
    "m_triggerSelection"          : "HLT_j360 | HLT_mu20_iloose_L1MU15 | HLT_mu26_ivarmedium | HLT_e24_lhmedium_L1EM20VH | HLT_e26_lhtight_nod0_ivarloose",
    "m_useMetaData"               : True,
    check_duplicates_flag         : True,
} )

my_analysis_dict = {
    'DataType': 'data' if extra_args.is_data else 'mc',
    'AddJets': {
        'JetContainer': 'AntiKt4EMPFlowJets',
	'Options': {'runJvtUpdate': True},  # use default value for any other variable not specified
        },
    'AddMuons': { 'WorkingPoint': 'Medium.NonIso'},
    'AddElectrons': { 'WorkingPoint': 'Tight.NonIso'},
}

from xAHplusCPalgsExample.MakeSequence import makeSequence
c.algorithm(makeSequence(my_analysis_dict))

# TTreeMaker
c.algorithm("TTreeMaker", {
    "m_name"                 : "TTreeMaker",
    "m_outputStream"         : "TTreeMaker", # why does it have to be named TTreeMaker?
    "m_muonContainerName"    : "outMuons",
    "m_muonDetailStr"        : "noMultiplicity kinematic",
    "m_elContainerName"      : "outElectrons",
    "m_elDetailStr"          : "noMultiplicity kinematic",
    "m_jetContainerName"     : "outJets",
    "m_jetDetailStr"         : "kinematic jvt_selection",
    "m_evtDetailStr"         : "pileup pileupsys",
} )
