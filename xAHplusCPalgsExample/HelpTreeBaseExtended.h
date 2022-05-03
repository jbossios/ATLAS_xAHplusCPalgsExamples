/** @file HelpTreeBaseExtended.h
 *  @brief Extension of xAH's HelpTreeBase
 *  @author Jona Bossio (jbossios@cern.ch)
 */

#ifndef xAHplusCPalgsExample_HelpTreeBaseExtended_H
#define xAHplusCPalgsExample_HelpTreeBaseExtended_H

// EDM include(s):
#include "xAODJet/JetContainer.h"

// algorithm wrapper
#include "xAODAnaHelpers/HelpTreeBase.h"

// Infrastructure include(s):
#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"

// ROOT include(s):
#include "TH1D.h"
#include "TFile.h"
#include "TLorentzVector.h"

#include <sstream>

#include "AsgTools/AnaToolHandle.h"

// NOTE:
// Variables that don't get filled at submission time should be
// protected from being send from the submission node to the worker
// node (done by the //!)

class HelpTreeBaseExtended : public HelpTreeBase
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.

  private:

    unsigned int m_addJVTdec = 0;
    std::vector<unsigned int> m_jet_jvt_dec;

  public:

    // Constructor
    HelpTreeBaseExtended(xAOD::TEvent *event, TTree* tree, TFile* file, const float units = 1e3, bool debug = false, xAOD::TStore* store = nullptr );
    // Destructor
    ~HelpTreeBaseExtended();

    void AddJetsUser(const std::string& detailStr = "", const std::string& jetName = "jet");

    void FillJetsUser(const xAOD::Jet* jet, const std::string& jetName = "jet");

    void ClearJetsUser(const std::string& jetName = "jet");

    /** @brief Used to distribute the algorithm to the workers*/
    ClassDef(HelpTreeBaseExtended, 1);
};

#endif
