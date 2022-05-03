from AnaAlgorithm.AnaAlgSequence import AnaAlgSequence
from AnaAlgorithm.DualUseConfig import createAlgorithm
from AnaAlgorithm.DualUseConfig import createService
import ROOT

def makeSequence (analysis_dict):
    data_type = analysis_dict['DataType']

    alg_seq = AnaAlgSequence()
    
    # DO NOT UNCOMMENT
    #  Set up the systematics loader/handler algorithm:
    #sysLoader = createAlgorithm( 'CP::SysListLoaderAlg', 'SysLoaderAlg' )
    #sysLoader.sigmaRecommended = 1
    #alg_seq += sysLoader
    
    sysService = createService( 'CP::SystematicsSvc', 'SystematicsSvc', sequence = alg_seq )
    sysService.sigmaRecommended = 1
   
    # DO NOT UNCOMMENT
    # Set up the systematics loader/handler algorithm:
    #sysLoader = CfgMgr.CP__SystematicsSvc( 'SystematicsSvc' )
    #sysLoader.sigmaRecommended = 1
    #sysLoader.systematicsList= ['']
    #ServiceMgr += sysLoader
    
    ##  Include, and then set up the pileup analysis sequence:
    #from AsgAnalysisAlgorithms.PileupAnalysisSequence import makePileupAnalysisSequence
    #pileupSequence = makePileupAnalysisSequence( dataType )
    #pileupSequence.configure( inputName = 'EventInfo', outputName = 'EventInfo_%SYS%' )
    
    ##  Add the pileup sequence to the job:
    #alg_seq += pileupSequence
    
    #from MuonAnalysisAlgorithms.MuonAnalysisSequence import makeMuonAnalysisSequence
    #muonSequenceLoose = makeMuonAnalysisSequence( dataType, deepCopyOutput = True, shallowViewOutput = False,
#                                                   workingPoint = 'Loose.NonIso', postfix = 'loose' )
    #muonSequenceLoose.configure( inputName = 'Muons', outputName = 'AnalysisMuons_%SYS%' )
    #alg_seq += muonSequenceLoose
    
    #from EgammaAnalysisAlgorithms.ElectronAnalysisSequence import  makeElectronAnalysisSequence
    #electronSequence = makeElectronAnalysisSequence( dataType, 'LooseLHElectron.NonIso', shallowViewOutput = False, deepCopyOutput = True )
    #electronSequence.configure( inputName = 'Electrons', outputName = 'AnalysisElectrons_%SYS%' )
    ##print( electronSequence ) # For debugging
    #alg_seq += electronSequence
    
    #from TauAnalysisAlgorithms.TauAnalysisSequence import makeTauAnalysisSequence
    #tauSequence = makeTauAnalysisSequence( dataType, 'Baseline', shallowViewOutput = False, deepCopyOutput = True )
    #tauSequence.configure( inputName = 'TauJets', outputName = 'AnalysisTauJets_%SYS%' )
    ##print( tauSequence ) # For debugging                                                                               
    #alg_seq += tauSequence

    if 'AddJets' in analysis_dict:
      jet_container = analysis_dict['AddJets']['JetContainer']
      other_options = {}
      if 'Options' in analysis_dict['AddJets']:
        other_options = analysis_dict['AddJets']['Options']
      from JetAnalysisAlgorithms.JetAnalysisSequence import makeJetAnalysisSequence
      jet_sequence = makeJetAnalysisSequence( data_type, jet_container, deepCopyOutput = False, shallowViewOutput = True, **other_options)
      jet_sequence.configure( inputName = jet_container, outputName = 'outJets_%SYS%' )
      #print( jet_sequence ) # For debugging
      alg_seq += jet_sequence
    
    return alg_seq
