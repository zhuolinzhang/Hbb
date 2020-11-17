// -*- C++ -*-
//
// Package:    Analysis/JetTester
// Class:      JetTester
// 
/**\class JetTester JetTester.cc Analysis/JetTester/plugins/JetTester.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  James Dolen
//         Created:  Thu, 11 Jun 2015 22:52:52 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// DataFormats
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

// TFile
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

// root
#include "TH1.h"
#include "TTree.h"
#include "TLorentzVector.h"

//
// class declaration
//

class JetAnalysis : public edm::EDAnalyzer {
   public:
      explicit JetAnalysis(const edm::ParameterSet&);
      ~JetAnalysis();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::EDGetTokenT<pat::JetCollection> ak4PFCHSminiAODjetToken_;
      


	  TH1D * h_ak4chsminiAOD_pt;
    TH1D * h_ak4chsminiAOD_uncpt;
    TH1D * h_ak4chsminiAOD_ht;
	  
};

//
// constructors and destructor
//
JetAnalysis::JetAnalysis(const edm::ParameterSet& iConfig){

  edm::InputTag JetTag("slimmedJets");
  ak4PFCHSminiAODjetToken_ = consumes<pat::JetCollection>(JetTag);

  edm::Service<TFileService> fs;
  h_ak4chsminiAOD_pt = fs->make<TH1D>("h_ak4chsminiAOD_pt", "h_ak4chsminiAOD_pt", 500, 0, 500); 
  h_ak4chsminiAOD_uncpt = fs->make<TH1D>("h_ak4chsminiAOD_uncpt", "h_ak4chsminiAOD_uncpt", 500, 0, 500);
  h_ak4chsminiAOD_ht = fs->make<TH1D>("h_ak4chsminiAOD_ht", "h_ak4chsminiAOD_ht", 500, 0, 500);
  

}


JetAnalysis::~JetAnalysis()
{
}


//
// member functions
//

// ------------ method called for each event  ------------
void
JetAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;
  using namespace std;
  using namespace reco;
  using namespace pat;
  //bool verbose = false;

  //--------------------------------------------------------------------------------------------
  // AK R=0.4 CHS jets - from miniAOD


  edm::Handle<pat::JetCollection> AK4CHSminiAOD;
  iEvent.getByToken(ak4PFCHSminiAODjetToken_, AK4CHSminiAOD);

  int count_AK4CHSminiAOD = 0;
  double ht = 0;
  for (const pat::Jet &ijet : *AK4CHSminiAOD) {  
    count_AK4CHSminiAOD++;
    if (count_AK4CHSminiAOD>=2) break;

    h_ak4chsminiAOD_pt->Fill(ijet.pt());
    h_ak4chsminiAOD_uncpt->Fill(ijet.pt()*ijet.jecFactor("Uncorrected"));
    ht += ijet.pt();

  }
  h_ak4chsminiAOD_ht->Fill(ht);


  




}


// ------------ method called once each job just before starting event loop  ------------
void 
JetAnalysis::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
JetAnalysis::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
JetAnalysis::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetAnalysis);
