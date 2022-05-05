/*******************************************************************
 *
 * Algorithm to select events passing reco or truth ZHF selections
 *
 * Jona Bossio (jbossioscern.ch)
 *
 ******************************************************************/

// EL includes:
#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <SelectionHelpers/ISelectionAccessor.h>
#include <AsgTesting/UnitTest.h>

// EDM includes:
#include "xAODCore/ShallowCopy.h"
#include "AthContainers/ConstDataVector.h"
#include "AthContainers/DataVector.h"
#include "xAODJet/JetContainer.h"

// package include:
#include "xAHplusCPalgsExample/HelpTreeBaseExtended.h"

// xAODAnaHelpers includes
#include "xAODAnaHelpers/HelperClasses.h"
#include <xAODAnaHelpers/HelperFunctions.h>

using namespace std;
using namespace xAH;

// this is needed to distribute the algorithm to the workers
ClassImp(HelpTreeBaseExtended)

HelpTreeBaseExtended :: HelpTreeBaseExtended(xAOD::TEvent *event, TTree* tree, TFile* file, const float units, bool debug, xAOD::TStore* store) :
  HelpTreeBase(event, tree, file, units, debug, store)
{
  Info("HelpTreeBaseExtended", "Creating output TTree  %s", tree->GetName());
}

HelpTreeBaseExtended :: ~HelpTreeBaseExtended()
{
}

// Jets
void HelpTreeBaseExtended::AddJetsUser(const std::string& detailStr, const std::string& jetName)
{
  // jvt_selection
  if(detailStr.find("jvt_selection") != std::string::npos){
    m_addJVTdec = true;
    std::string branchName = jetName + "_jvt_selection";
    m_tree->Branch(branchName.c_str(), &m_jet_jvt_dec);
  }
}

void HelpTreeBaseExtended::FillJetsUser( const xAOD::Jet* jet, const std::string& jetName) {
  (void)jetName;
  // jvt_selection
  if(m_addJVTdec) {
    std::unique_ptr<CP::ISelectionAccessor> acc;
    ASSERT_SUCCESS (CP::makeSelectionAccessor ("jvt_selection,as_bits", acc));
    unsigned int jvtDec = int(acc->getBool (*jet));
    m_jet_jvt_dec.push_back(jvtDec);
  }
}

void HelpTreeBaseExtended::ClearJetsUser(const std::string& jetName) {
  (void)jetName;
  if(m_addJVTdec){
    m_jet_jvt_dec.clear();
  }
}


