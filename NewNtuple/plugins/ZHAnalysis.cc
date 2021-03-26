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
#include <cstring>
#include <vector>

#include "TLorentzVector.h"
#include "TVector3.h"
#include "TProfile.h"
#include "TTree.h"
#include "TString.h"

// user include files
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
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

//
// class declaration
//

class ZHAnalysis : public edm::one::EDAnalyzer<edm::one::SharedResources> {

   public:

      explicit ZHAnalysis(const edm::ParameterSet&);
      ~ZHAnalysis();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:

      virtual void beginJob() override;
      bool HLTaccept(const edm::Event&, std::string&);
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      
      edm::EDGetTokenT<pat::MuonCollection> muonToken_;
      //edm::EDGetTokenT<pat::PackedGenParticleCollection> genCollToken;
      edm::EDGetTokenT<reco::VertexCollection> vertexToken_;
      //edm::EDGetTokenT<reco::Vertex> vertexToken_;
      edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
      edm::EDGetTokenT<pat::JetCollection> jetToken_;

      TTree *ZHCollection; //||prevent split
      std::string HLTPath_;
      std::string bTag_;
      TLorentzVector mu1V4, mu2V4, jet1V4, jet2V4;
      std::vector<float> *ZPt, *ZEta, *ZPhi, *ZM;
      std::vector<float> *HiggsPt, *HiggsEta, *HiggsPhi, *HiggsM;
      std::vector<float> *mu1Charge, *mu1Pt, *mu1Eta, *mu1Phi, *mu1M, *mu1Iso, *mu1Global, *mu1Tight;
      std::vector<float> *mu2Charge, *mu2Pt, *mu2Eta, *mu2Phi, *mu2M, *mu2Iso, *mu2Global, *mu2Tight;
      std::vector<float> *jet1Pt, *jet1Eta, *jet1Phi, *jet1M, *jet1ID, *jet1bTag;
      std::vector<float> *jet2Pt, *jet2Eta, *jet2Phi, *jet2M, *jet2ID, *jet2bTag;

      //TH1F* h_GenDiMuonM;
      
  
  
};

//
// constructors and destructor
//
ZHAnalysis::ZHAnalysis(const edm::ParameterSet& iConfig) {

  muonToken_ = (consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muonTag")));
  //genCollToken = consumes<pat::PackedGenParticleCollection>(theGenMuonLabel);
  vertexToken_ = (consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexTag")));
  triggerToken_ = (consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerTag")));
  jetToken_ = (consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("jetTag")));
  HLTPath_ = iConfig.getParameter<std::string>("HLTPath");
  bTag_ = iConfig.getParameter<std::string>("bTag");

  edm::Service<TFileService> fs;
  ZHCollection = fs->make<TTree>("ZHCollection", "ZHCollection");
  mu1Charge = 0; mu1Pt = 0; mu1Eta = 0; mu1Phi = 0; mu1M = 0; mu1Iso = 0; mu1Global = 0; mu1Tight = 0;
  mu2Charge = 0; mu2Pt = 0; mu2Eta = 0; mu2Phi = 0; mu2M = 0; mu2Iso = 0; mu2Global = 0; mu2Tight = 0;
  jet1Pt = 0; jet1Eta = 0; jet1Phi = 0; jet1M = 0; jet1ID = 0; jet1bTag = 0; 
  jet2Pt = 0; jet2Eta = 0; jet2Phi = 0; jet2M = 0; jet2ID = 0; jet2bTag = 0;
  ZPt = 0; ZEta = 0; ZPhi = 0; ZM = 0;
  HiggsPt = 0; HiggsEta = 0; HiggsPhi = 0; HiggsM = 0;
  //h_GenDiMuonM = fs->make<TH1F>("h_GenDiMuonM",";m_{#mu^{+}#mu^{-}};",80,70,110);
 
}


ZHAnalysis::~ZHAnalysis() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// Check event pass HLT
bool ZHAnalysis::HLTaccept(const edm::Event& iEvent, std::string& HLTPaths) {
  edm::Handle<edm::TriggerResults> triggerColleciton;
  iEvent.getByToken(triggerToken_, triggerColleciton);
  const edm::TriggerResults triggerObj = * (triggerColleciton.product()); 
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(triggerObj);
  std::string HLTPaths_clear = HLTPaths;
  if (HLTPaths.rfind("*") == (HLTPaths.length() - 1)) HLTPaths_clear.pop_back();
  TString HLTPaths_compare = TString(HLTPaths_clear);
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
void ZHAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  using namespace std;
  using namespace pat;
  
  edm::Handle<vector<pat::Muon>> muonHandle;
  iEvent.getByToken(muonToken_, muonHandle);

  /* 
  edm::Handle <pat::PackedGenParticleCollection> genColl;
  iEvent.getByToken(genCollToken, genColl);
  */

  edm::Handle<vector<reco::Vertex>> vertexHandle;
  iEvent.getByToken(vertexToken_, vertexHandle);

  edm::Handle<vector<pat::Jet>> jetHandle;
  iEvent.getByToken(jetToken_, jetHandle);

  if(!vertexHandle.isValid()) {
    throw cms::Exception("Vertex collection not valid!"); 
  } 

   // Let's check that we have at least one good vertex! 
  
  std::vector<reco::Vertex>::const_iterator firstGoodVertex = vertexHandle->end();

   for (std::vector<reco::Vertex>::const_iterator it=vertexHandle->begin(); it!=firstGoodVertex; ++it) {
    if (!it->isFake() && it->ndof()>4 && it->position().Rho()<2. && std::abs(it->position().Z())<24.) {
      if(firstGoodVertex == vertexHandle->end()) firstGoodVertex = it;
      break;
    }
  }
  // Require a good vertex
  if(firstGoodVertex == vertexHandle->end()) return;

  /////////////////////////////////////////////////
  // Dimuon pairs /////////////////////////////////
  /////////////////////////////////////////////////
    
  //put your code here
  const char *hltName = HLTPath_.c_str();
  bool eventTriggerPass = 0;
  bool muonSelectionFlag = 1;
  if (HLTaccept(iEvent, HLTPath_)) eventTriggerPass = 1;
  // find mu+
  for (auto mu1 = muonHandle->cbegin(); mu1 != muonHandle->cend(); ++mu1) {
      if (muonHandle->size() < 2) {
        muonSelectionFlag = 0;
        continue;
      }
      if (!eventTriggerPass) continue;
      // find mu-
      for (auto mu2 = muonHandle->cbegin(); mu2 != muonHandle->cend(); ++mu2) {
        if (!(mu2 > mu1)) continue;
        if (!(mu1->charge() * mu2->charge() < 0)) continue;
        if (mu1->triggerObjectMatchByPath(hltName) == nullptr || mu2->triggerObjectMatchByPath(hltName) == nullptr) continue;
        mu1Charge->push_back(mu1->charge()); mu1Pt->push_back(mu1->pt()); mu1Eta->push_back(mu1->eta()); mu1Phi->push_back(mu1->phi()); mu1M->push_back(mu1->mass());
        mu1Iso->push_back(((mu1->pfIsolationR04().sumChargedHadronPt + std::max(0., mu1->pfIsolationR04().sumNeutralHadronEt + mu1->pfIsolationR04().sumPhotonEt - 0.5 * mu1->pfIsolationR04().sumPUPt)) / mu1->pt() < 0.4));
        mu1Global->push_back(mu1->isGlobalMuon()); mu1Tight->push_back(mu1->isTightMuon(*firstGoodVertex));
        mu2Charge->push_back(mu2->charge()); mu2Pt->push_back(mu2->pt()); mu2Eta->push_back(mu2->eta()); mu2Phi->push_back(mu2->phi()); mu2M->push_back(mu2->mass());
        mu2Iso->push_back(((mu2->pfIsolationR04().sumChargedHadronPt + std::max(0., mu2->pfIsolationR04().sumNeutralHadronEt + mu2->pfIsolationR04().sumPhotonEt - 0.5 * mu2->pfIsolationR04().sumPUPt)) / mu2->pt() < 0.4));
        mu2Global->push_back(mu2->isGlobalMuon()); mu2Tight->push_back(mu2->isTightMuon(*firstGoodVertex));

        mu1V4.SetPtEtaPhiM(mu1->pt(), mu1->eta(), mu1->phi(), mu1->mass());
        mu2V4.SetPtEtaPhiM(mu2->pt(), mu2->eta(), mu2->phi(), mu2->mass());
        TLorentzVector ZV4 = mu1V4 + mu2V4;
        
        ZPt->push_back(ZV4.Pt()); ZEta->push_back(ZV4.Eta()); ZPhi->push_back(ZV4.Phi()); ZM->push_back(ZV4.M());
      }
  }

  // find b jet in MC samples
  for (auto jet1 = jetHandle->cbegin(); jet1 != jetHandle->cend(); ++jet1) {
    if (jetHandle->size() < 2) continue;
    if (!muonSelectionFlag) continue;
    float NHF  = jet1->neutralHadronEnergyFraction();
    float NEMF = jet1->neutralEmEnergyFraction();
    float CHF  = jet1->chargedHadronEnergyFraction();
    float MUF  = jet1->muonEnergyFraction();
    float CEMF = jet1->chargedEmEnergyFraction();
    float NumConst = jet1->chargedMultiplicity() + jet1->neutralMultiplicity();
    float CHM = jet1->chargedMultiplicity();
    bool jet1ID2018 = fabs(jet1->eta())<=2.6 && CEMF<0.8 && CHM>0 && CHF>0 && NumConst>1 && NEMF<0.9 && MUF <0.8 && NHF < 0.9;
    float jet1bTagScore = jet1->bDiscriminator(bTag_ + ":probb") + jet1->bDiscriminator(bTag_ + ":probbb");

    for (auto jet2 = jetHandle->cbegin(); jet2 != jetHandle->cend(); ++jet2){
      if (!(jet2 > jet1)) continue; // avoid double counting
      float NHF  = jet2->neutralHadronEnergyFraction();
      float NEMF = jet2->neutralEmEnergyFraction();
      float CHF  = jet2->chargedHadronEnergyFraction();
      float MUF  = jet2->muonEnergyFraction();
      float CEMF = jet2->chargedEmEnergyFraction();
      float NumConst = jet2->chargedMultiplicity() + jet2->neutralMultiplicity();
      float CHM = jet2->chargedMultiplicity();
      bool jet2ID2018 = fabs(jet2->eta())<=2.6 && CEMF<0.8 && CHM>0 && CHF>0 && NumConst>1 && NEMF<0.9 && MUF <0.8 && NHF < 0.9;
      float jet2bTagScore = jet2->bDiscriminator(bTag_ + ":probb") + jet2->bDiscriminator(bTag_ + ":probbb");
      jet1Pt->push_back(jet1->pt()); jet1Eta->push_back(jet1->eta()); jet1Phi->push_back(jet1->phi()); jet1M->push_back(jet1->mass());
      jet1ID->push_back(jet1ID2018); jet1bTag->push_back(jet1bTagScore);    
      jet2Pt->push_back(jet2->pt()); jet2Eta->push_back(jet2->eta()); jet2Phi->push_back(jet2->phi()); jet2M->push_back(jet2->mass());
      jet2ID->push_back(jet2ID2018); jet2bTag->push_back(jet2bTagScore);    

      jet1V4.SetPtEtaPhiM(jet1->pt(), jet1->eta(), jet1->phi(), jet1->mass());
      jet2V4.SetPtEtaPhiM(jet2->pt(), jet2->eta(), jet2->phi(), jet2->mass());
      TLorentzVector HiggsV4 = jet1V4 + jet2V4;
      HiggsPt->push_back(HiggsV4.Pt()); HiggsEta->push_back(HiggsV4.Eta()); HiggsPhi->push_back(HiggsV4.Phi()); HiggsM->push_back(HiggsV4.M());

    }
  }

  ZHCollection->Fill();
  
  mu1Charge->clear(); mu1Pt->clear(); mu1Eta->clear(); mu1Phi->clear(); mu1M->clear(); mu1Iso->clear(); mu1Global->clear(); mu1Tight->clear();
  mu2Charge->clear(); mu2Pt->clear(); mu2Eta->clear(); mu2Phi->clear(); mu2M->clear(); mu2Iso->clear(); mu2Global->clear(); mu2Tight->clear();
  jet1Pt->clear(); jet1Eta->clear(); jet1Phi->clear(); jet1M->clear(); jet1ID->clear(); jet1bTag->clear(); 
  jet2Pt->clear(); jet2Eta->clear(); jet2Phi->clear(); jet2M->clear(); jet2ID->clear(); jet2bTag->clear();
  ZPt->clear(); ZEta->clear(); ZPhi->clear(); ZM->clear();
  HiggsPt->clear(); HiggsEta->clear(); HiggsPhi->clear(); HiggsM->clear();         
  

                /*
                int idxmu1_Gen = -1;
                int idxmu2_Gen = -1;

                // Gen matching
                for (auto genParticle = genColl->cbegin(); genParticle != genColl->cend(); ++genParticle) {
                    const pat::PackedGenParticle& mcMuon = (*genParticle);
                    if ( not (abs(mcMuon.pdgId()) == 13 ) ) continue; // make sure it is a muon
                    if ( fabs(mcMuon.eta()) > 2.4 ) continue;
                    if ( fabs(mcMuon.eta()) > 2.4 ) continue;
                    if ( not (mcMuon.pt() > 1.5 ) ) continue;
                    if ( deltaR(mcMuon, *(mu1->innerTrack())) < 0.1 && mcMuon.charge() > 0 ) idxmu1_Gen = std::distance(genColl->cbegin(), genParticle);
                    if ( deltaR(mcMuon, *(mu2->innerTrack())) < 0.1 && mcMuon.charge() < 0 ) idxmu2_Gen = std::distance(genColl->cbegin(), genParticle);
                }
                if ( idxmu1_Gen > -1 && idxmu2_Gen > -1) {
                    double diMuonRecMassGen = (genColl->at(idxmu1_Gen).p4() + genColl->at(idxmu2_Gen).p4()).M();
                    h_GenDiMuonM->Fill(diMuonRecMassGen);
                }
                */
           
  
}


// ------------ method called once each job just before starting event loop  ------------
void ZHAnalysis::beginJob() {
  // muon branchs
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

  ZHCollection->Branch("HiggsPt", &HiggsPt);
  ZHCollection->Branch("HiggsEta", &HiggsEta);
  ZHCollection->Branch("HiggsPhi", &HiggsPhi);
  ZHCollection->Branch("HiggsM", &HiggsM);

  ZHCollection->Branch("jet1Pt", &jet1Pt);
  ZHCollection->Branch("jet1Eta", &jet1Eta);
  ZHCollection->Branch("jet1Phi", &jet1Phi);
  ZHCollection->Branch("jet1M", &jet1M);
  ZHCollection->Branch("jet1ID", &jet1ID);
  ZHCollection->Branch("jet1bTag", &jet1bTag);

  ZHCollection->Branch("jet2Pt", &jet2Pt);
  ZHCollection->Branch("jet2Eta", &jet2Eta);
  ZHCollection->Branch("jet2Phi", &jet2Phi);
  ZHCollection->Branch("jet2M", &jet2M);
  ZHCollection->Branch("jet2ID", &jet2ID);
  ZHCollection->Branch("jet2bTag", &jet2bTag);
}

// ------------ method called once each job just after ending the event loop  ------------
void ZHAnalysis::endJob() {
  ZHCollection->GetDirectory()->cd();
  ZHCollection->Write();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void ZHAnalysis::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  // The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

}

//define this as a plug-in
DEFINE_FWK_MODULE(ZHAnalysis);
