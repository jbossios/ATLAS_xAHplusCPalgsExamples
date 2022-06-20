#ifndef xAHplusCPalgsExample_TTreeMaker_H
#define xAHplusCPalgsExample_TTreeMaker_H

#include <EventLoop/StatusCode.h>

#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"
#include "TTree.h"
#include "TH1D.h"

#include "xAODParticleEvent/Particle.h"
#include <xAODMuon/MuonContainer.h>
#include <xAODEgamma/ElectronContainer.h>
#include <xAODJet/JetContainer.h>

// external tools include(s):
#include "AsgTools/AnaToolHandle.h"

#include <SystematicsHandles/SysReadHandle.h>
#include <SystematicsHandles/SysListHandle.h>

#include <AnaAlgorithm/AnaAlgorithm.h>

#include <xAHplusCPalgsExample/HelpTreeBaseExtended.h>

class HelpTreeBaseExtended;

class TTreeMaker : public EL::AnaAlgorithm
{
 
 private: 
 
 std::string m_name;
 std::string m_outputStream;

 public:
 
 // this is a standard algorithm constructor
 TTreeMaker (const std::string& name, ISvcLocator* pSvcLocator);
 ~TTreeMaker() {};
 
 CP::SysListHandle m_systematicsList {this};
 CP::SysReadHandle<xAOD::MuonContainer> m_muonHandle {this, "muons", "outMuons_%SYS%", "the muon collection to run on"};
 CP::SysReadHandle<xAOD::ElectronContainer> m_elHandle {this, "electrons", "outElectrons_%SYS%", "the electron collection to run on"};
 CP::SysReadHandle<xAOD::JetContainer> m_jetHandle {this, "jets", "outJets_%SYS%", "the jet collection to run on"};
 
 bool m_debug;

 std::string m_trigDetailStr;
 std::string m_evtDetailStr;
 std::string m_jetContainerName;
 std::string m_jetDetailStr;
 std::string m_muonContainerName;
 std::string m_muonDetailStr;
 std::string m_tauContainerName;
 std::string m_tauDetailStr;
 std::string m_elContainerName;
 std::string m_elDetailStr;
 std::string m_photonContainerName;
 std::string m_photonDetailStr;
 std::string m_metContainerName;
 std::string m_metDetailStr;
 std::string m_resolvedJetsName;
 std::string m_resolvedJetDetailStr;
 
 // these are the functions inherited from AnaAlgorithm
 StatusCode setupJob (EL::Job& job);
 virtual StatusCode initialize () override;
 virtual StatusCode execute () override;
 virtual StatusCode finalize () override;  
 
 virtual StatusCode AddTree (std::string);      //!
 
 /** The TEvent object */
 xAOD::TEvent* m_event = nullptr; //!
 /** The TStore object */
 xAOD::TStore* m_store = nullptr; //!

 private:
 
 std::map< std::string, HelpTreeBaseExtended* > m_helpTree; //!
 
 // this is needed to distribute the algorithm to the workers
 ClassDef(TTreeMaker, 1);                                 //!
 
};

#endif
