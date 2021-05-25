// -*- C++ -*-
//
// Package:    CMSDASExercises/MuonExercise2
// Class:      MuonExercise2
// 
/**\class MuonExercise3 MuonExercise2.cc CMSDASExercises/MuonExercise3/plugins/MuonExercise2.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Norbert Neumeister
//         Created:  Thu, 10 Dec 2016 21:10:01 GMT
//
//

// system include files
#include <memory>
#include <iomanip>
#include <string>
#include <vector>
#include <algorithm>
#include <fstream>
// ROOT include files
#include "TLorentzVector.h"
#include <TVector3.h>
#include <TProfile.h>
#include <TTree.h>
#include "TString.h"
// CMSSW include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

//
// class declaration
//

class ZHNtuple : public edm::one::EDAnalyzer<edm::one::SharedResources> {

   public:

      explicit ZHNtuple(const edm::ParameterSet&);
      ~ZHNtuple();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:

      virtual void beginJob() override;
      bool HLTaccept(const edm::Event&, std::string&);
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      
      edm::EDGetTokenT<pat::MuonCollection> muonToken_;
      edm::EDGetTokenT<reco::VertexCollection> vertexToken_;
      edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
      edm::EDGetTokenT<pat::JetCollection> jetToken_;
      
      TTree *ZHCollection;
      
      std::vector<int> mu1Charge, mu2Charge;
      std::vector<float> mu1M, mu1Pt, mu1Eta, mu1Phi, mu1Iso;
      std::vector<float> mu2M, mu2Pt, mu2Eta, mu2Phi, mu2Iso;
      
      std::vector<float> jet1M, jet1Pt, jet1Eta, jet1Phi, jet1bTag;
      std::vector<float> jet2M, jet2Pt, jet2Eta, jet2Phi, jet2bTag;
      
      std::vector<float> ZM, ZPt, ZEta, ZPhi;
      std::vector<float> HiggsM, HiggsPt, HiggsEta, HiggsPhi;

      std::vector<bool> mu1Global, mu2Global, mu1Tight, mu2Tight, jet1ID, jet2ID;
      std::vector<int> cutFlowCollect, eventCutFlow, eventMuCutFlow;
      int nMu1, nMu2, nJet1, nJet2;
      std::string HLTPath_;
      std::string bTag_;
};

//
// constructors and destructor
//
ZHNtuple::ZHNtuple(const edm::ParameterSet& iConfig) {

  muonToken_ = (consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muon")));
  vertexToken_ = (consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertex")));
  triggerToken_ = (consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerResults")));
  jetToken_ = (consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("jet")));
  HLTPath_ = iConfig.getParameter<std::string>("HLTPath");
  bTag_ = iConfig.getParameter<std::string>("bTag");

  nMu1 = 0; nMu2 = 0; nJet1 = 0; nJet2 = 0;

  edm::Service<TFileService> fs;
  ZHCollection = fs->make<TTree>("ZHCollection", "ZHCollection");
  ZHCollection->SetAutoSave(0);
  ZHCollection->Branch("mu1Charge", &mu1Charge);
  ZHCollection->Branch("mu1Pt", &mu1Pt);
  ZHCollection->Branch("mu1Eta", &mu1Eta);
  ZHCollection->Branch("mu1Phi", &mu1Phi);
  ZHCollection->Branch("mu1M", &mu1M);
  ZHCollection->Branch("mu1Iso", &mu1Iso);
  ZHCollection->Branch("mu1Global", &mu1Global);
  ZHCollection->Branch("mu1Tight", &mu1Tight);

  ZHCollection->Branch("mu2Charge", &mu2Charge);
  ZHCollection->Branch("mu2Pt", &mu2Pt);
  ZHCollection->Branch("mu2Eta", &mu2Eta);
  ZHCollection->Branch("mu2Phi", &mu2Phi);
  ZHCollection->Branch("mu2M", &mu2M);
  ZHCollection->Branch("mu2Iso", &mu2Iso);
  ZHCollection->Branch("mu2Global", &mu2Global);
  ZHCollection->Branch("mu2Tight", &mu2Tight);

  ZHCollection->Branch("ZPt", &ZPt);
  ZHCollection->Branch("ZEta", &ZEta);
  ZHCollection->Branch("ZPhi", &ZPhi);
  ZHCollection->Branch("ZM", &ZM);

  ZHCollection->Branch("jet1Pt", &jet1Pt);
  ZHCollection->Branch("jet1Eta", &jet1Eta);
  ZHCollection->Branch("jet1Phi", &jet1Phi);
  ZHCollection->Branch("jet1M", &jet1M);
  ZHCollection->Branch("jet1bTag", &jet1bTag);
  ZHCollection->Branch("jet1ID", &jet1ID);

  ZHCollection->Branch("jet2Pt", &jet2Pt);
  ZHCollection->Branch("jet2Eta", &jet2Eta);
  ZHCollection->Branch("jet2Phi", &jet2Phi);
  ZHCollection->Branch("jet2M", &jet2M);
  ZHCollection->Branch("jet2bTag", &jet2bTag);
  ZHCollection->Branch("jet2ID", &jet2ID);
  

  ZHCollection->Branch("HiggsPt", &HiggsPt);
  ZHCollection->Branch("HiggsEta", &HiggsEta);
  ZHCollection->Branch("HiggsPhi", &HiggsPhi);
  ZHCollection->Branch("HiggsM", &HiggsM);
}


ZHNtuple::~ZHNtuple() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// Check event pass HLT
bool ZHNtuple::HLTaccept(const edm::Event& iEvent, std::string& HLTPaths) {
  edm::Handle<edm::TriggerResults> triggerHandle;
  iEvent.getByToken(triggerToken_, triggerHandle);
  const edm::TriggerResults triggerObj = * (triggerHandle.product()); 
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(triggerObj);
  std::string HLTPaths_clear = HLTPaths;
  if (HLTPaths.rfind("*") == (HLTPaths.length() - 1)) HLTPaths_clear.pop_back();
  TString HLTPaths_compare = TString(HLTPaths_clear);
  //bool passTrig=triggerresults->accept(triggerNames.triggerIndex(pathName));
  bool passTrig = false;
  for (size_t i = 0; i < triggerObj.size(); i++)
  {
    TString trigName = triggerNames.triggerName(i);
    bool find = false;
    if (trigName.Contains(HLTPaths_compare)) {
      find = true;
      int accept = triggerObj.accept(i);
      if ((accept == 1) && find) {
        passTrig = true;
      }
    }
  }
  return passTrig;
}

// ------------ method called for each event  ------------
void ZHNtuple::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  using namespace std;
  using namespace pat;
  
  edm::Handle<vector<pat::Muon>> muonsHandle;
  iEvent.getByToken(muonToken_, muonsHandle);

  edm::Handle<vector<reco::Vertex>> verticesHandle;
  iEvent.getByToken(vertexToken_, verticesHandle);

  edm::Handle<vector<pat::Jet>> jetsHandle;
  iEvent.getByToken(jetToken_, jetsHandle);

  if(!verticesHandle.isValid()) {
    throw cms::Exception("Vertex collection not valid!"); 
  } 

   // Let's check that we have at least one good vertex! 
  
  std::vector<reco::Vertex>::const_iterator firstGoodVertex = verticesHandle->end();

   for (std::vector<reco::Vertex>::const_iterator it=verticesHandle->begin(); it!=firstGoodVertex; ++it) {
    if (!it->isFake() && it->ndof()>4 && it->position().Rho()<2. && std::abs(it->position().Z())<24.) {
      if(firstGoodVertex == verticesHandle->end()) firstGoodVertex = it;
      break;
    }
  }
  // Require a good vertex
  if(firstGoodVertex == verticesHandle->end()) return;
  
  const char *hltName = HLTPath_.c_str();
  TLorentzVector mu1Vector, mu2Vector;
  TLorentzVector jet1Vector, jet2Vector;
  TLorentzVector ZVector, HiggsVector;
  bool eventPassFlag = HLTaccept(iEvent, HLTPath_);
  if (muonsHandle->size() >=2 && jetsHandle->size() >= 2 && HLTaccept(iEvent, HLTPath_)) {
    /////////////////////////////////////////////////
    // Dimuon pairs /////////////////////////////////
    /////////////////////////////////////////////////
    
    for (auto mu1 = muonsHandle->cbegin(); mu1 != muonsHandle->cend(); ++mu1) {
      // Use tight muon ID, pT and eta cut were mentioned in AN2018/073 - Zhuolin 2020-12-22
      if (!(mu1->pt() > 25)) continue;
      if (!(fabs(mu1->eta()) < 2.4)) continue;
      if (!mu1->isTightMuon(*firstGoodVertex)) continue; // Tight muon ID
      // PF Isolation very loose
      if (!((mu1->pfIsolationR04().sumChargedHadronPt + std::max(0., mu1->pfIsolationR04().sumNeutralHadronEt + mu1->pfIsolationR04().sumPhotonEt - 0.5 * mu1->pfIsolationR04().sumPUPt)) / mu1->pt() < 0.4)) continue;
      nMu1++;
      // find mu2
      for (auto mu2 = muonsHandle->cbegin(); mu2 != muonsHandle->cend(); ++mu2) {
        if (!(mu2 > mu1)) continue; // avoid double counting
        if (!(mu2->pt() > 15)) continue;
        if (!(mu1->charge() * mu2->charge() < 0)) continue; // muon in dimuon pair should have different charge
        if (!(fabs(mu2->eta()) < 2.4)) continue;
        if (!mu2->isTightMuon(*firstGoodVertex)) continue; // Tight muon ID
        // PF Isolation very loose
        if (!((mu2->pfIsolationR04().sumChargedHadronPt + std::max(0., mu2->pfIsolationR04().sumNeutralHadronEt + mu2->pfIsolationR04().sumPhotonEt - 0.5 * mu2->pfIsolationR04().sumPUPt)) / mu2->pt() < 0.4)) continue; 
        if (((mu1->p4() + mu2->p4()).M()) < 75 || ((mu1->p4() + mu2->p4()).M()) > 105) continue; // only look around the Z peak
        if (mu1->triggerObjectMatchByPath(hltName) == nullptr || mu2->triggerObjectMatchByPath(hltName) == nullptr) continue; // trigger match
        nMu2++;
        
        mu1Charge.push_back(mu1->charge());
        mu1Pt.push_back(mu1->pt());
        mu1Eta.push_back(mu1->eta());
        mu1Phi.push_back(mu1->phi());
        mu1M.push_back((mu1->p4()).M());
        mu1Iso.push_back((mu1->pfIsolationR04().sumChargedHadronPt + std::max(0., mu1->pfIsolationR04().sumNeutralHadronEt + mu1->pfIsolationR04().sumPhotonEt - 0.5 * mu1->pfIsolationR04().sumPUPt)) / mu1->pt());
        mu1Global.push_back(mu1->isGlobalMuon());
        mu1Tight.push_back(mu1->isTightMuon(*firstGoodVertex));
        mu2Charge.push_back(mu2->charge());
        mu2Pt.push_back(mu2->pt());
        mu2Eta.push_back(mu2->eta());
        mu2Phi.push_back(mu2->phi());
        mu2M.push_back((mu2->p4()).M());
        mu2Iso.push_back((mu2->pfIsolationR04().sumChargedHadronPt + std::max(0., mu2->pfIsolationR04().sumNeutralHadronEt + mu2->pfIsolationR04().sumPhotonEt - 0.5 * mu2->pfIsolationR04().sumPUPt)) / mu2->pt());
        mu2Global.push_back(mu2->isGlobalMuon());
        mu2Tight.push_back(mu2->isTightMuon(*firstGoodVertex));
      }
    }
    
    if (nMu1 >= 1 && nMu2 >= 1) {
      size_t nmu1Pt = mu1Pt.size();
      size_t nmu2Pt = mu2Pt.size();
      // reconstruct Z boson only from leading muons
      for (size_t i = 1; i < nmu1Pt; i++) {
        mu1Charge.pop_back();
        mu1Pt.pop_back();
        mu1Eta.pop_back();
        mu1Phi.pop_back();
        mu1M.pop_back();
        mu1Iso.pop_back();
      }
      for (size_t i = 1; i < nmu2Pt; i++) {
        mu2Charge.pop_back();
        mu2Pt.pop_back();
        mu2Eta.pop_back();
        mu2Phi.pop_back();
        mu2M.pop_back();
        mu2Iso.pop_back();
      }
      
      // reconstruct Z boson
      mu1Vector.SetPtEtaPhiM(mu1Pt[0], mu1Eta[0], mu1Phi[0], mu1M[0]);
      mu2Vector.SetPtEtaPhiM(mu2Pt[0], mu2Eta[0], mu2Phi[0], mu2M[0]);
      ZVector = mu1Vector + mu2Vector;
      ZPt.push_back(ZVector.Pt());
      ZEta.push_back(ZVector.Eta());
      ZPhi.push_back(ZVector.Phi());
      ZM.push_back(ZVector.M());
    }
    
  
    /////////////////////////////////////////////////
    // Dijet pairs /////////////////////////////////
    /////////////////////////////////////////////////
    
    for (auto jet1 = jetsHandle->cbegin(); jet1 != jetsHandle->cend(); ++jet1) {
      //if (!(jet1->pt() > 20)) continue;
      //if (!((jet1->bDiscriminator(bTag_ + ":probb") + jet1->bDiscriminator(bTag_ + ":probbb")) > 0.4184)) continue; // deepCSV
      float NHF  = jet1->neutralHadronEnergyFraction();
      float NEMF = jet1->neutralEmEnergyFraction();
      float CHF  = jet1->chargedHadronEnergyFraction();
      float MUF  = jet1->muonEnergyFraction();
      float CEMF = jet1->chargedEmEnergyFraction();
      float NumConst = jet1->chargedMultiplicity() + jet1->neutralMultiplicity();
      float CHM = jet1->chargedMultiplicity();
      //if (!(fabs(jet1->eta())<=2.6 && CEMF<0.8 && CHM>0 && CHF>0 && NumConst>1 && NEMF<0.9 && MUF <0.8 && NHF < 0.9)) continue;
      nJet1++;
      for (auto jet2 = jetsHandle->cbegin(); jet2 != jetsHandle->cend(); ++jet2){
        if (!(jet2 > jet1)) continue; // avoid double counting
        //if (!(jet2->pt() > 20)) continue;
        //if (!((jet2->bDiscriminator(bTag_ + ":probb") + jet2->bDiscriminator(bTag_ + ":probbb")) > 0.4184)) continue; // deepCSV
        float NHF  = jet2->neutralHadronEnergyFraction();
        float NEMF = jet2->neutralEmEnergyFraction();
        float CHF  = jet2->chargedHadronEnergyFraction();
        float MUF  = jet2->muonEnergyFraction();
        float CEMF = jet2->chargedEmEnergyFraction();
        float NumConst = jet2->chargedMultiplicity() + jet2->neutralMultiplicity();
        float CHM = jet2->chargedMultiplicity();
        //if (!(fabs(jet2->eta())<=2.6 && CEMF<0.8 && CHM>0 && CHF>0 && NumConst>1 && NEMF<0.9 && MUF <0.8 && NHF < 0.9)) continue;
        //if ((jet1->p4() + jet2->p4()).M() < 50 || (jet1->p4() + jet2->p4()).M() > 200) continue; // only look around the Higgs mass window
        nJet2++;
        
        jet1Pt.push_back(jet1->pt());
        jet1Eta.push_back(jet1->eta());
        jet1Phi.push_back(jet1->phi());
        jet1M.push_back((jet1->p4()).M());
        jet1bTag.push_back(jet1->bDiscriminator(bTag_ + ":probb") + jet1->bDiscriminator(bTag_ + ":probbb"));
        jet1ID.push_back((fabs(jet1->eta())<=2.6 && CEMF<0.8 && CHM>0 && CHF>0 && NumConst>1 && NEMF<0.9 && MUF <0.8 && NHF < 0.9));
        jet2Pt.push_back(jet2->pt());
        jet2Eta.push_back(jet2->eta());
        jet2Phi.push_back(jet2->phi());
        jet2M.push_back((jet2->p4()).M());
        jet2bTag.push_back(jet2->bDiscriminator(bTag_ + ":probb") + jet2->bDiscriminator(bTag_ + ":probbb"));
        jet2ID.push_back((fabs(jet2->eta())<=2.6 && CEMF<0.8 && CHM>0 && CHF>0 && NumConst>1 && NEMF<0.9 && MUF <0.8 && NHF < 0.9));
      }
    }
    
    if (nJet1 >= 1 && nJet2 >= 1) {
      size_t njet1Pt = jet1Pt.size();
      size_t njet2Pt = jet2Pt.size();
      // reconstruct Higgs boson only from leading jets
      for (size_t i = 1; i < njet1Pt; i++) {
        jet1Pt.pop_back();
        jet1Eta.pop_back();
        jet1Phi.pop_back();
        jet1M.pop_back();
        jet1bTag.pop_back();
        jet1ID.pop_back();
      }
      for (size_t i = 1; i < njet2Pt; i++) {
        jet2Pt.pop_back();
        jet2Eta.pop_back();
        jet2Phi.pop_back();
        jet2M.pop_back();
        jet2bTag.pop_back();
        jet2ID.pop_back();
      }
      
      // reconstruct Higgs boson
      jet1Vector.SetPtEtaPhiM(jet1Pt[0], jet1Eta[0], jet1Phi[0], jet1M[0]);
      jet2Vector.SetPtEtaPhiM(jet2Pt[0], jet2Eta[0], jet2Phi[0], jet2M[0]);
      HiggsVector = jet1Vector + jet2Vector;
      HiggsPt.push_back(HiggsVector.Pt());
      HiggsEta.push_back(HiggsVector.Eta());
      HiggsPhi.push_back(HiggsVector.Phi());
      HiggsM.push_back(HiggsVector.M());
      
    }
  
  if (nMu1 >=1 && nMu2 >= 1 && nJet1 >= 1 && nJet2 >= 1 && eventPassFlag) ZHCollection->Fill();
  
  mu1Charge.clear(); mu1Pt.clear(); mu1Eta.clear(); mu1Phi.clear(); mu1M.clear(); mu1Iso.clear(); mu1Global.clear(); mu1Tight.clear();
  mu2Charge.clear(); mu2Pt.clear(); mu2Eta.clear(); mu2Phi.clear(); mu2M.clear(); mu2Iso.clear(); mu2Global.clear(); mu2Tight.clear();
  
  jet1Pt.clear(); jet1Eta.clear(); jet1Phi.clear(); jet1M.clear(); jet1bTag.clear(); jet1ID.clear();
  jet2Pt.clear(); jet2Eta.clear(); jet2Phi.clear(); jet2M.clear(); jet2bTag.clear(); jet2ID.clear();
  
  ZPt.clear(); ZEta.clear(); ZPhi.clear(); ZM.clear();
  HiggsPt.clear(); HiggsEta.clear(); HiggsPhi.clear(); HiggsM.clear();


  nMu1 = 0; nMu2 = 0; nJet1 = 0; nJet2 = 0;
  
  }
  
}



// ------------ method called once each job just before starting event loop  ------------
void ZHNtuple::beginJob() {


}

// ------------ method called once each job just after ending the event loop  ------------
void ZHNtuple::endJob() {
  
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------

void ZHNtuple::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  // The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

}


//define this as a plug-in
DEFINE_FWK_MODULE(ZHNtuple);
