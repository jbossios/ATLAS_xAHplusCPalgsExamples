#include <xAHplusCPalgsExample/TTreeMaker.h>
#include <xAODEventInfo/EventInfo.h>

#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>
#include "xAODCore/ShallowCopy.h"
#include "xAODBase/IParticleHelpers.h"
#include "xAODCore/AuxContainerBase.h"

using std::cout;  using std::endl;
using std::string; using std::vector;

#include "TH1F.h"

#include <xAODAnaHelpers/HelperFunctions.h>
#include <xAODAnaHelpers/HelperClasses.h>

#include <xAHplusCPalgsExample/HelpTreeBaseExtended.h>

// this is needed to distribute the algorithm to the workers
ClassImp(TTreeMaker)

TTreeMaker :: TTreeMaker (const std::string& name,ISvcLocator *pSvcLocator) : EL::AnaAlgorithm (name, pSvcLocator)
{
 // Here you put any code for the base initialization of variables,
 // e.g. initialize all pointers to 0.  This is also where you
 // declare all properties for your algorithm.  Note that things like
 // resetting statistics variables or booking histograms should
 // rather go into the initialize() function.
 
 declareProperty("m_name", m_name = "TTreeMaker");
 declareProperty("m_outputStream", m_outputStream = "TTree");
 declareProperty("m_muonContainerName", m_muonContainerName = "");
 declareProperty("m_muonDetailStr", m_muonDetailStr = "");
 declareProperty("m_jetContainerName", m_jetContainerName = "");
 declareProperty("m_jetDetailStr", m_jetDetailStr = "");
 
}

StatusCode TTreeMaker :: initialize ()
{
  // Here you do everything that needs to be done at the very
  // beginning on each worker node, e.g. create histograms and output
  // trees.  This method gets called before any input files are
  // connected.
  
 ANA_MSG_INFO ("in initialize");
 
 m_event = wk()->xaodEvent();
 m_store = wk()->xaodStore();
 
 m_debug=false;
 
 if(m_debug) Info("initialize()", "after add store");
 
 m_systematicsList.addHandle(m_muonHandle);
 m_systematicsList.addHandle(m_jetHandle);
 ANA_CHECK (m_systematicsList.initialize());
 
 if(m_debug) Info("initialize()", "left");
 
 return StatusCode::SUCCESS;
}



StatusCode TTreeMaker :: execute ()
{
 // Here you do everything that needs to be done on every single
 // events, e.g. read input variables, apply cuts, and fill
 // histograms and trees.  This is where most of your actual analysis
 // code will go.
 
 // retrieve the eventInfo object from the event store
 const xAOD::EventInfo *eventInfo = nullptr;
 ANA_CHECK (evtStore()->retrieve (eventInfo, "EventInfo"));
 
 // print out run and event number from retrieved object
 ANA_MSG_INFO ("in execute, runNumber = " << eventInfo->runNumber() << ", eventNumber = " << eventInfo->eventNumber());
 
 
 for (const auto& sys : m_systematicsList.systematicsVector())
 {
  
  std::string sysname;
  ANA_CHECK(m_systematicsList.service().makeSystematicsName(sysname, "%SYS%",sys))
  
  if( m_helpTree.find( sysname ) == m_helpTree.end() )
  {
   AddTree( sysname );
  }
  
  const xAOD::EventInfo* eventInfo(0);
  ANA_CHECK( HelperFunctions::retrieve(eventInfo, "EventInfo", m_event, m_store));
  
  const xAOD::VertexContainer* vertices(0);
  ANA_CHECK( HelperFunctions::retrieve(vertices, "PrimaryVertices", m_event, m_store));
  
  const xAOD::Vertex *pv = 0;
  pv = vertices->at( HelperFunctions::getPrimaryVertexLocation( vertices ) );
  
  m_helpTree[sysname]->FillEvent( eventInfo );
  
  if(!m_muonContainerName.empty())
  {
    if(m_debug) cout << " Filling muons " << endl;
    string muonContainerName=m_muonContainerName;
    const xAOD::MuonContainer* muons(nullptr);
    ANA_CHECK (m_muonHandle.retrieve (muons, sys));
    m_helpTree[sysname]->FillMuons(muons, HelperFunctions::getPrimaryVertex( vertices ) );
  }
  if(!m_jetContainerName.empty())
  {
    if(m_debug) cout << " Filling jets " << endl;
    string jetContainerName = m_jetContainerName;
    const xAOD::JetContainer* jets(nullptr);
    ANA_CHECK (m_jetHandle.retrieve (jets, sys));
    m_helpTree[sysname]->FillJets(jets, HelperFunctions::getPrimaryVertexLocation( vertices ), "jet");
  }
  m_helpTree[sysname]->Fill();
  
 } //for sys list
  
 return StatusCode::SUCCESS;
}


StatusCode TTreeMaker :: finalize ()
{
  // This method is the mirror image of initialize(), meaning it gets
  // called after the last event has been processed on the worker node
  // and allows you to finish up any objects you created in
  // initialize() before they are written to disk.  This is actually
  // fairly rare, since this happens separately for each worker node.
  // Most of the time you want to do your post-processing on the
  // submission node after all your histogram outputs have been
  // merged.
  
  
  if (!m_helpTree.empty())
  {
    for( auto tree : m_helpTree)
    {
      if (tree.second) delete tree.second;
    }
  }
  
  TFile* treeFile = wk()->getOutputFile( m_name.c_str() );
  
  return StatusCode::SUCCESS;
}


StatusCode TTreeMaker::AddTree(string syst = "")
{
  
  Info("AddTree()", "%s", m_name.c_str() );
  
  string treeName = "MiniTree_";
  if (!syst.empty()) treeName += syst;
  TTree * outTree = new TTree(treeName.c_str(), treeName.c_str());
  if( !outTree )
  {
    Error("AddTree()","Failed to instantiate output tree!");
    return StatusCode::FAILURE;
  }

  // get the file we created already
  TFile* treeFile = wk()->getOutputFile( m_name.c_str() );
  outTree->SetDirectory( treeFile );
  
  m_helpTree[syst] = new HelpTreeBaseExtended( m_event, outTree, treeFile );

  m_helpTree[syst]->AddEvent(m_evtDetailStr);

  if(!m_muonContainerName.empty())
    m_helpTree[syst]->AddMuons(m_muonDetailStr);

  if(!m_jetContainerName.empty())
    m_helpTree[syst]->AddJets(m_jetDetailStr);

  // SetAutoFlush to reduce memory use
  outTree->SetAutoFlush(-500000);

  return StatusCode::SUCCESS;
}
