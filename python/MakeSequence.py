from AnaAlgorithm.AnaAlgSequence import AnaAlgSequence
from AnaAlgorithm.DualUseConfig import createAlgorithm
from AnaAlgorithm.DualUseConfig import createService
import ROOT
import sys

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

def makeSequence (analysis_dict):
    try:
        data_type = analysis_dict['DataType']
    except KeyError:
        print('ERROR: DataType is not present in analysis_dict')
        sys.exit(1)

    alg_seq = AnaAlgSequence()
    
    sysService = createService( 'CP::SystematicsSvc', 'SystematicsSvc', sequence = alg_seq )
    sysService.sigmaRecommended = 1
   
    ##  Include, and then set up the pileup analysis sequence:
    #from AsgAnalysisAlgorithms.PileupAnalysisSequence import makePileupAnalysisSequence
    #pileup_sequence = makePileupAnalysisSequence( data_type, autoConfig = True )
    ##pileup_sequence = makePileupAnalysisSequence( data_type, userPileupConfigs=grls, userLumicalcFiles=lumis["MC16a"])  # NOTE: hardcoded
    #pileup_sequence.configure( inputName = 'EventInfo', outputName = 'EventInfo_%SYS%' )
    #alg_seq += pileup_sequence
    
    if 'AddMuons' in analysis_dict:
        try:
            muon_wp = analysis_dict['AddMuons']['WorkingPoint']
        except KeyError:
            print('ERROR: WorkingPoint is not present in analysis_dict["AddMuons"]')
            sys.exit(1)
        from MuonAnalysisAlgorithms.MuonAnalysisSequence import makeMuonAnalysisSequence
        muon_sequence = makeMuonAnalysisSequence( data_type, deepCopyOutput = False, shallowViewOutput = True,
                                                       workingPoint = muon_wp)
        muon_sequence.configure( inputName = 'Muons', outputName = 'outMuons_%SYS%' )
        #print( muon_sequence ) # For debugging
        alg_seq += muon_sequence

    if 'AddElectrons' in analysis_dict:
        try:
            el_wp = analysis_dict['AddElectrons']['WorkingPoint']
        except KeyError:
            print('ERROR: WorkingPoint is not present in analysis_dict["AddElectrons"]')
            sys.exit(1)
        from EgammaAnalysisAlgorithms.ElectronAnalysisSequence import  makeElectronAnalysisSequence
        el_wps = el_wp.split('.')
        id_wp = el_wps[0]
        iso_wp = el_wps[1]
        final_el_wp = '{}LHElectron.{}'.format(id_wp, iso_wp)
        electron_sequence = makeElectronAnalysisSequence( data_type, final_el_wp, shallowViewOutput = True, deepCopyOutput = False )
        electron_sequence.configure( inputName = 'Electrons', outputName = 'outElectrons_%SYS%' )
        #print( electron_sequence ) # For debugging
        alg_seq += electron_sequence
    
    #from TauAnalysisAlgorithms.TauAnalysisSequence import makeTauAnalysisSequence
    #tauSequence = makeTauAnalysisSequence( dataType, 'Baseline', shallowViewOutput = False, deepCopyOutput = True )
    #tauSequence.configure( inputName = 'TauJets', outputName = 'AnalysisTauJets_%SYS%' )
    ##print( tauSequence ) # For debugging                                                                               
    #alg_seq += tauSequence

    if 'AddJets' in analysis_dict:
        try:
            jet_container = analysis_dict['AddJets']['JetContainer']
        except KeyError:
            print('ERROR: JetContainer is not present in analysis_dict["AddJets"]')
            sys.exit(1)
        other_options = {}
        if 'Options' in analysis_dict['AddJets']:
            other_options = analysis_dict['AddJets']['Options']
        from JetAnalysisAlgorithms.JetAnalysisSequence import makeJetAnalysisSequence
        jet_sequence = makeJetAnalysisSequence( data_type, jet_container, deepCopyOutput = False, shallowViewOutput = True, **other_options)
        jet_sequence.configure( inputName = jet_container, outputName = 'outJets_%SYS%' )
        #print( jet_sequence ) # For debugging
        alg_seq += jet_sequence
    
    return alg_seq
