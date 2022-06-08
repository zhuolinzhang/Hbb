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
#include "Math/GenVector/LorentzVector.h"
#include "Math/Vector4D.h"
#include "TRandom.h"
#include "TRandom3.h"

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
#include "ZH/Tree/interface/RoccoR.cc"

//
// class declaration
//

class ZHTree : public edm::one::EDAnalyzer<edm::one::SharedResources> {

   public:

      explicit ZHTree(const edm::ParameterSet&);
      ~ZHTree();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:

      virtual void beginJob() override;
      bool HLTaccept(const edm::Event&, std::string&);
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      
      edm::EDGetTokenT<pat::MuonCollection> muonToken_;
      //edm::EDGetTokenT<pat::PackedGenParticleCollection> genCollToken_;
      edm::EDGetTokenT<reco::GenParticleCollection> genCollToken_;
      edm::EDGetTokenT<reco::VertexCollection> vertexToken_;
      //edm::EDGetTokenT<reco::Vertex> vertexToken_;
      edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
      edm::EDGetTokenT<pat::JetCollection> jetToken_;

      TTree *ZHCollection;
      std::string HLTPath_;
      std::string bTag_;
      std::string roccorPath;
      bool isData_;
      ROOT::Math::PtEtaPhiMVector mu1V4, mu2V4, jet1V4, jet2V4;
      ROOT::Math::PxPyPzEVector mu1PxPyPzEV4, mu2PxPyPzEV4;
      std::vector<int> *mu1Charge, *mu2Charge;
      std::vector<float> *ZPt, *ZEta, *ZPhi, *ZM;
      std::vector<float> *HiggsPt, *HiggsEta, *HiggsPhi, *HiggsM;
      std::vector<float> *mu1Pt, *mu1Eta, *mu1Phi, *mu1M, *mu1Iso;
      std::vector<float> *mu2Pt, *mu2Eta, *mu2Phi, *mu2M, *mu2Iso;
      //std::vector<float> *mu1GenPt, *mu1GenEta, *mu1GenPhi, *mu1GenM;
      //std::vector<float> *mu2GenPt, *mu2GenEta, *mu2GenPhi, *mu2GenM, *mu2GenIso;
      std::vector<float> *jet1Pt, *jet1Eta, *jet1Phi, *jet1M, *jet1bTag, *jet1NHF, *jet1NEMF, *jet1MUF, *jet1CEMF, *jet1NumConst, *jet1CHM, *jet1NumNeutralParticles, *jet1CHF;
      std::vector<float> *jet2Pt, *jet2Eta, *jet2Phi, *jet2M, *jet2bTag, *jet2NHF, *jet2NEMF, *jet2MUF, *jet2CEMF, *jet2NumConst, *jet2CHM, *jet2NumNeutralParticles, *jet2CHF;
      std::vector<bool> *mu1Global, *mu1Loose, *mu1Tight, *mu2Global, *mu2Loose, *mu2Tight;

      RoccoR rc;

      //TH1F* h_GenDiMuonM;
};

//
// constructors and destructor
//
ZHTree::ZHTree(const edm::ParameterSet& iConfig) {

  muonToken_ = (consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muonTag")));
  genCollToken_ = consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genPartTag"));
  vertexToken_ = (consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexTag")));
  triggerToken_ = (consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerTag")));
  jetToken_ = (consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("jetTag")));
  HLTPath_ = iConfig.getParameter<std::string>("HLTPath");
  bTag_ = iConfig.getParameter<std::string>("bTag");
  isData_ = iConfig.getParameter<bool>("isData");
  
  edm::Service<TFileService> fs;
  ZHCollection = fs->make<TTree>("ZHCollection", "ZHCollection");
  
  mu1Charge = 0; mu1Pt = 0; mu1Eta = 0; mu1Phi = 0; mu1M = 0; mu1Iso = 0; mu1Global = 0; mu1Tight = 0; mu1Loose = 0;
  mu2Charge = 0; mu2Pt = 0; mu2Eta = 0; mu2Phi = 0; mu2M = 0; mu2Iso = 0; mu2Global = 0; mu2Tight = 0; mu2Loose = 0;
  jet1Pt = 0; jet1Eta = 0; jet1Phi = 0; jet1M = 0; jet1bTag = 0; jet1NHF = 0; jet1NEMF = 0; jet1MUF = 0; jet1CEMF = 0; jet1NumConst = 0; jet1CHM = 0; jet1NumNeutralParticles = 0; jet1CHF = 0;
  jet2Pt = 0; jet2Eta = 0; jet2Phi = 0; jet2M = 0; jet2bTag = 0; jet2NHF = 0; jet2NEMF = 0; jet2MUF = 0; jet2CEMF = 0; jet2NumConst = 0; jet2CHM = 0; jet2NumNeutralParticles = 0; jet2CHF = 0;
  ZPt = 0; ZEta = 0; ZPhi = 0; ZM = 0;
  HiggsPt = 0; HiggsEta = 0; HiggsPhi = 0; HiggsM = 0;
  //h_GenDiMuonM = fs->make<TH1F>("h_GenDiMuonM",";m_{#mu^{+}#mu^{-}};",80,70,110);

  rc.init((iConfig.getParameter<edm::FileInPath>("roccorFile")).fullPath());
}


ZHTree::~ZHTree() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// Check event pass HLT
bool ZHTree::HLTaccept(const edm::Event& iEvent, std::string& HLTPaths) {
  edm::Handle<edm::TriggerResults> triggerColleciton;
  iEvent.getByToken(triggerToken_, triggerColleciton);
  const edm::TriggerResults triggerObj = * (triggerColleciton.product()); 
  const edm::TriggerNames& triggerNames = iEvent.triggerNames(triggerObj);
  std::string HLTPathsClear = HLTPaths;
  if (HLTPaths.rfind("*") == (HLTPaths.length() - 1)) HLTPathsClear.pop_back();
  TString HLTPathsCompare = TString(HLTPathsClear);
  bool passTrig = false;
  for (size_t i = 0; i < triggerObj.size(); i++)
  {
    TString trigName = triggerNames.triggerName(i);
    bool find = false;
    if (trigName.Contains(HLTPathsCompare)) {
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
void ZHTree::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  using namespace std;
  using namespace pat;

  edm::Handle<vector<pat::Muon>> muonHandle;
  iEvent.getByToken(muonToken_, muonHandle);

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
  //const char *hltName = HLTPath_.c_str();
  bool eventTriggerPass = 0;
  bool muonSelectionFlag = 0;
  bool jetSelectionFlag = 0;
  if (HLTaccept(iEvent, HLTPath_)) eventTriggerPass = 1;
  // find mu+
  if (isData_)
  {
    for (auto mu1 = muonHandle->cbegin(); mu1 != muonHandle->cend(); ++mu1) 
    {
      if (!eventTriggerPass) continue;
      if (muonHandle->size() < 2) continue;
      if (mu1->innerTrack().isNull()) continue;
      // find mu-
      for (auto mu2 = muonHandle->cbegin(); mu2 != muonHandle->cend(); ++mu2) 
      {
        if (!(mu2 > mu1)) continue;
        if (!(mu1->charge() * mu2->charge() < 0)) continue;
        if (mu2->innerTrack().isNull()) continue;
        //if (mu1->triggerObjectMatchByPath(hltName) == nullptr || mu2->triggerObjectMatchByPath(hltName) == nullptr) continue; // it can't be used in 2016 MC

        double dataSFMu1 = rc.kScaleDT(mu1->charge(), mu1->pt(), mu1->eta(), mu1->phi(), 0, 0);
        double dataSFMu2 = rc.kScaleDT(mu2->charge(), mu2->pt(), mu2->eta(), mu2->phi(), 0, 0);
        mu1V4.SetCoordinates(mu1->pt(), mu1->eta(), mu1->phi(), mu1->mass());
        mu2V4.SetCoordinates(mu2->pt(), mu2->eta(), mu2->phi(), mu2->mass());
        mu1PxPyPzEV4.SetCoordinates(mu1V4.Px() * dataSFMu1, mu1V4.Py() * dataSFMu1, mu1V4.Pz() * dataSFMu1, mu1V4.E() * dataSFMu1);
        mu2PxPyPzEV4.SetCoordinates(mu2V4.Px() * dataSFMu2, mu2V4.Py() * dataSFMu2, mu2V4.Pz() * dataSFMu2, mu2V4.E() * dataSFMu2);

        mu1Charge->push_back(mu1->charge()); mu1Pt->push_back(mu1PxPyPzEV4.Pt()); mu1Eta->push_back(mu1PxPyPzEV4.Eta()); mu1Phi->push_back(mu1PxPyPzEV4.Phi()); mu1M->push_back(mu1PxPyPzEV4.M());
        mu1Iso->push_back((mu1->pfIsolationR04().sumChargedHadronPt + std::max(0., mu1->pfIsolationR04().sumNeutralHadronEt + mu1->pfIsolationR04().sumPhotonEt - 0.5 * mu1->pfIsolationR04().sumPUPt)) / mu1->pt());
        mu1Global->push_back(mu1->isGlobalMuon()); mu1Tight->push_back(mu1->isTightMuon(*firstGoodVertex)); mu1Loose->push_back(mu1->isLooseMuon());
        //if (!mu1->innerTrack().isNull()) mu1TrackerLayer->push_back(mu1->innerTrack()->hitPattern().trackerLayersWithMeasurement());
        mu2Charge->push_back(mu2->charge()); mu2Pt->push_back(mu2PxPyPzEV4.Pt()); mu2Eta->push_back(mu2PxPyPzEV4.Eta()); mu2Phi->push_back(mu2PxPyPzEV4.Phi()); mu2M->push_back(mu2PxPyPzEV4.M());
        mu2Iso->push_back((mu2->pfIsolationR04().sumChargedHadronPt + std::max(0., mu2->pfIsolationR04().sumNeutralHadronEt + mu2->pfIsolationR04().sumPhotonEt - 0.5 * mu2->pfIsolationR04().sumPUPt)) / mu2->pt());
        mu2Global->push_back(mu2->isGlobalMuon()); mu2Tight->push_back(mu2->isTightMuon(*firstGoodVertex)); mu2Loose->push_back(mu2->isLooseMuon());
        //if (!mu2->innerTrack().isNull()) mu2TrackerLayer->push_back(mu2->innerTrack()->hitPattern().trackerLayersWithMeasurement());

        ROOT::Math::PxPyPzEVector ZPxPyPzEV4 = mu1PxPyPzEV4 + mu2PxPyPzEV4;
        ZPt->push_back(ZPxPyPzEV4.Pt()); ZEta->push_back(ZPxPyPzEV4.Eta()); ZPhi->push_back(ZPxPyPzEV4.Phi()); ZM->push_back(ZPxPyPzEV4.M());
        muonSelectionFlag = 1;
      }
    }
  }
  else
  {
    edm::Handle<vector<reco::GenParticle>> genCollHandle;
    iEvent.getByToken(genCollToken_, genCollHandle);
    for (auto mu1 = muonHandle->cbegin(); mu1 != muonHandle->cend(); ++mu1) 
    {
      if (!eventTriggerPass) continue;
      if (muonHandle->size() < 2) continue;
      if (mu1->innerTrack().isNull()) continue;
      // find mu-
      for (auto mu2 = muonHandle->cbegin(); mu2 != muonHandle->cend(); ++mu2) 
      {
        if (!(mu2 > mu1)) continue;
        if (!(mu1->charge() * mu2->charge() < 0)) continue;
        if (mu2->innerTrack().isNull()) continue;
        //if (mu1->triggerObjectMatchByPath(hltName) == nullptr || mu2->triggerObjectMatchByPath(hltName) == nullptr) continue; // it can't be used in 2016 MC

        int idxMu1Gen = -1;
        int idxMu2Gen = -1;
        float bestdrMu1 = 9999.;
        float bestdrMu2 = 9999.;

        // Gen matching
        for (auto genParticle = genCollHandle->cbegin(); genParticle != genCollHandle->cend(); ++genParticle)
        {
          if (!(fabs(genParticle->pdgId()) == 13 && genParticle->status() == 1))
            continue; // make sure it is a muon
          if (fabs(genParticle->eta()) > 2.4)
            continue;
          if (!(genParticle->pt() > 1.5))
            continue;
          if (deltaR(*genParticle, *mu1) < 0.1 && deltaR(*genParticle, *mu1) < bestdrMu1 && genParticle->charge() * mu1->charge() == 1)
          {
            idxMu1Gen = std::distance(genCollHandle->cbegin(), genParticle);
            bestdrMu1 = deltaR(*genParticle, *mu1);
          }
          if (deltaR(*genParticle, *mu2) < 0.1 && deltaR(*genParticle, *mu2) < bestdrMu2 && genParticle->charge() * mu2->charge() == 1)
          {
            idxMu2Gen = std::distance(genCollHandle->cbegin(), genParticle);
            bestdrMu2 = deltaR(*genParticle, *mu2);
          }
        }
        
        double mcSFMu1 = 1;
        double mcSFMu2 = 1;
        if (idxMu1Gen != -1)
          mcSFMu1 = rc.kSpreadMC(mu1->charge(), mu1->pt(), mu1->eta(), mu1->phi(), genCollHandle->at(idxMu1Gen).pt(), 0, 0);
        else
          mcSFMu1 = rc.kSmearMC(mu1->charge(), mu1->pt(), mu1->eta(), mu1->phi(), mu1->innerTrack()->hitPattern().trackerLayersWithMeasurement(), gRandom->Rndm(), 0, 0);
        if (idxMu2Gen != -1)
          mcSFMu2 = rc.kSpreadMC(mu2->charge(), mu2->pt(), mu2->eta(), mu2->phi(), genCollHandle->at(idxMu2Gen).pt(), 0, 0);
        else
          mcSFMu2 = rc.kSmearMC(mu2->charge(), mu2->pt(), mu2->eta(), mu2->phi(), mu2->innerTrack()->hitPattern().trackerLayersWithMeasurement(), gRandom->Rndm(), 0, 0);
        mu1V4.SetCoordinates(mu1->pt(), mu1->eta(), mu1->phi(), mu1->mass());
        mu2V4.SetCoordinates(mu2->pt(), mu2->eta(), mu2->phi(), mu2->mass());
        mu1PxPyPzEV4.SetCoordinates(mu1V4.Px() * mcSFMu1, mu1V4.Py() * mcSFMu1, mu1V4.Pz() * mcSFMu1, mu1V4.E() * mcSFMu1);
        mu2PxPyPzEV4.SetCoordinates(mu2V4.Px() * mcSFMu2, mu2V4.Py() * mcSFMu2, mu2V4.Pz() * mcSFMu2, mu2V4.E() * mcSFMu2);

        mu1Charge->push_back(mu1->charge()); mu1Pt->push_back(mu1PxPyPzEV4.Pt()); mu1Eta->push_back(mu1PxPyPzEV4.Eta()); mu1Phi->push_back(mu1PxPyPzEV4.Phi()); mu1M->push_back(mu1PxPyPzEV4.M());
        mu1Iso->push_back((mu1->pfIsolationR04().sumChargedHadronPt + std::max(0., mu1->pfIsolationR04().sumNeutralHadronEt + mu1->pfIsolationR04().sumPhotonEt - 0.5 * mu1->pfIsolationR04().sumPUPt)) / mu1->pt());
        mu1Global->push_back(mu1->isGlobalMuon()); mu1Tight->push_back(mu1->isTightMuon(*firstGoodVertex)); mu1Loose->push_back(mu1->isLooseMuon());
        //if (!mu1->innerTrack().isNull()) mu1TrackerLayer->push_back(mu1->innerTrack()->hitPattern().trackerLayersWithMeasurement());
        mu2Charge->push_back(mu2->charge()); mu2Pt->push_back(mu2PxPyPzEV4.Pt()); mu2Eta->push_back(mu2PxPyPzEV4.Eta()); mu2Phi->push_back(mu2PxPyPzEV4.Phi()); mu2M->push_back(mu2PxPyPzEV4.M());
        mu2Iso->push_back((mu2->pfIsolationR04().sumChargedHadronPt + std::max(0., mu2->pfIsolationR04().sumNeutralHadronEt + mu2->pfIsolationR04().sumPhotonEt - 0.5 * mu2->pfIsolationR04().sumPUPt)) / mu2->pt());
        mu2Global->push_back(mu2->isGlobalMuon()); mu2Tight->push_back(mu2->isTightMuon(*firstGoodVertex)); mu2Loose->push_back(mu2->isLooseMuon());
        //if (!mu2->innerTrack().isNull()) mu2TrackerLayer->push_back(mu2->innerTrack()->hitPattern().trackerLayersWithMeasurement());

        ROOT::Math::PxPyPzEVector ZPxPyPzEV4 = mu1PxPyPzEV4 + mu2PxPyPzEV4;
        ZPt->push_back(ZPxPyPzEV4.Pt()); ZEta->push_back(ZPxPyPzEV4.Eta()); ZPhi->push_back(ZPxPyPzEV4.Phi()); ZM->push_back(ZPxPyPzEV4.M());
        muonSelectionFlag = 1;
      }
    }
  }
  
  // find b jet in MC samples
  for (auto jet1 = jetHandle->cbegin(); jet1 != jetHandle->cend(); ++jet1) {
    if (jetHandle->size() < 2) continue;
    if (!muonSelectionFlag) continue;
    if (!eventTriggerPass) continue;
    float jet1bTagScore = jet1->bDiscriminator(bTag_ + ":probb") + jet1->bDiscriminator(bTag_ + ":probbb");

    for (auto jet2 = jetHandle->cbegin(); jet2 != jetHandle->cend(); ++jet2){
      if (!(jet2 > jet1)) continue; // avoid double counting
      float jet2bTagScore = jet2->bDiscriminator(bTag_ + ":probb") + jet2->bDiscriminator(bTag_ + ":probbb");
      jet1Pt->push_back(jet1->pt()); jet1Eta->push_back(jet1->eta()); jet1Phi->push_back(jet1->phi()); jet1M->push_back(jet1->mass());
      jet1bTag->push_back(jet1bTagScore); 
      jet1NHF->push_back(jet1->neutralHadronEnergyFraction()); 
      jet1NEMF->push_back(jet1->neutralEmEnergyFraction()); 
      jet1CHF->push_back(jet1->chargedHadronEnergyFraction());
      jet1MUF->push_back(jet1->muonEnergyFraction());
      jet1CEMF->push_back(jet1->chargedEmEnergyFraction());
      jet1NumConst->push_back(jet1->chargedMultiplicity() + jet1->neutralMultiplicity());
      jet1CHM->push_back(jet1->chargedMultiplicity());
      jet1NumNeutralParticles->push_back(jet1->neutralMultiplicity());
      jet2Pt->push_back(jet2->pt()); jet2Eta->push_back(jet2->eta()); jet2Phi->push_back(jet2->phi()); jet2M->push_back(jet2->mass());
      jet2bTag->push_back(jet2bTagScore);
      jet2NHF->push_back(jet2->neutralHadronEnergyFraction());
      jet2NEMF->push_back(jet2->neutralEmEnergyFraction()); 
      jet2CHF->push_back(jet2->chargedHadronEnergyFraction());
      jet2MUF->push_back(jet2->muonEnergyFraction());
      jet2CEMF->push_back(jet2->chargedEmEnergyFraction());
      jet2NumConst->push_back(jet2->chargedMultiplicity() + jet2->neutralMultiplicity());
      jet2CHM->push_back(jet2->chargedMultiplicity());
      jet2NumNeutralParticles->push_back(jet2->neutralMultiplicity());

      jet1V4.SetCoordinates(jet1->pt(), jet1->eta(), jet1->phi(), jet1->mass());
      jet2V4.SetCoordinates(jet2->pt(), jet2->eta(), jet2->phi(), jet2->mass());
      ROOT::Math::PtEtaPhiMVector HiggsV4 = jet1V4 + jet2V4;
      HiggsPt->push_back(HiggsV4.Pt()); HiggsEta->push_back(HiggsV4.Eta()); HiggsPhi->push_back(HiggsV4.Phi()); HiggsM->push_back(HiggsV4.M());
      jetSelectionFlag = 1;
    }
  }
  //mu1Charge->size() >= 1 && jetHandle->size() >= 2 && 
  if (muonSelectionFlag && jetSelectionFlag && eventTriggerPass) ZHCollection->Fill();
  mu1Charge->clear(); mu1Pt->clear(); mu1Eta->clear(); mu1Phi->clear(); mu1M->clear(); mu1Iso->clear(); mu1Global->clear(); mu1Tight->clear(); mu1Loose->clear();//mu1TrackerLayer->clear();
  mu2Charge->clear(); mu2Pt->clear(); mu2Eta->clear(); mu2Phi->clear(); mu2M->clear(); mu2Iso->clear(); mu2Global->clear(); mu2Tight->clear(); mu2Loose->clear();//mu2TrackerLayer->clear();
  jet1Pt->clear(); jet1Eta->clear(); jet1Phi->clear(); jet1M->clear(); jet1bTag->clear(); 
  jet2Pt->clear(); jet2Eta->clear(); jet2Phi->clear(); jet2M->clear(); jet2bTag->clear();
  jet1NHF->clear();
  jet1NEMF->clear();
  jet1CHF->clear();
  jet1MUF->clear();
  jet1CEMF->clear();
  jet1NumConst->clear();
  jet1CHM->clear();
  jet1NumNeutralParticles->clear();
  jet2NHF->clear();
  jet2NEMF->clear();
  jet2CHF->clear();
  jet2MUF->clear();
  jet2CEMF->clear();
  jet2NumConst->clear();
  jet2CHM->clear();
  jet2NumNeutralParticles->clear();
  ZPt->clear(); ZEta->clear(); ZPhi->clear(); ZM->clear();
  HiggsPt->clear(); HiggsEta->clear(); HiggsPhi->clear(); HiggsM->clear();
  
}


// ------------ method called once each job just before starting event loop  ------------
void ZHTree::beginJob() {
  ZHCollection->SetAutoSave(0);
  // muon branchs
  ZHCollection->Branch("mu1Charge", &mu1Charge);
  ZHCollection->Branch("mu1Pt", &mu1Pt);
  ZHCollection->Branch("mu1Eta", &mu1Eta);
  ZHCollection->Branch("mu1Phi", &mu1Phi);
  ZHCollection->Branch("mu1M", &mu1M);
  ZHCollection->Branch("mu1Iso", &mu1Iso);
  ZHCollection->Branch("mu1Global", &mu1Global);
  ZHCollection->Branch("mu1Loose", &mu1Loose);
  ZHCollection->Branch("mu1Tight", &mu1Tight);
  //ZHCollection->Branch("mu1TrackerLayer", &mu1TrackerLayer);

  ZHCollection->Branch("mu2Charge", &mu2Charge);
  ZHCollection->Branch("mu2Pt", &mu2Pt);
  ZHCollection->Branch("mu2Eta", &mu2Eta);
  ZHCollection->Branch("mu2Phi", &mu2Phi);
  ZHCollection->Branch("mu2M", &mu2M);
  ZHCollection->Branch("mu2Iso", &mu2Iso);
  ZHCollection->Branch("mu2Global", &mu2Global);
  ZHCollection->Branch("mu2Loose", &mu2Loose);
  ZHCollection->Branch("mu2Tight", &mu2Tight);
  //ZHCollection->Branch("mu2TrackerLayer", &mu2TrackerLayer);

  ZHCollection->Branch("ZPt", &ZPt);
  ZHCollection->Branch("ZEta", &ZEta);
  ZHCollection->Branch("ZPhi", &ZPhi);
  ZHCollection->Branch("ZM", &ZM);

  ZHCollection->Branch("jet1Pt", &jet1Pt);
  ZHCollection->Branch("jet1Eta", &jet1Eta);
  ZHCollection->Branch("jet1Phi", &jet1Phi);
  ZHCollection->Branch("jet1M", &jet1M);
  ZHCollection->Branch("jet1bTag", &jet1bTag);
  ZHCollection->Branch("jet1NHF", &jet1NHF);
  ZHCollection->Branch("jet1NEMF", &jet1NEMF);
  ZHCollection->Branch("jet1CHF", &jet1CHF);
  ZHCollection->Branch("jet1MUF", &jet1MUF);
  ZHCollection->Branch("jet1CEMF", &jet1CEMF);
  ZHCollection->Branch("jet1NumConst", &jet1NumConst);
  ZHCollection->Branch("jet1CHM", &jet1CHM);
  ZHCollection->Branch("jet1NumNeutralParticles", &jet1NumNeutralParticles);

  ZHCollection->Branch("jet2Pt", &jet2Pt);
  ZHCollection->Branch("jet2Eta", &jet2Eta);
  ZHCollection->Branch("jet2Phi", &jet2Phi);
  ZHCollection->Branch("jet2M", &jet2M);
  ZHCollection->Branch("jet2bTag", &jet2bTag);
  ZHCollection->Branch("jet2NHF", &jet2NHF);
  ZHCollection->Branch("jet2NEMF", &jet2NEMF);
  ZHCollection->Branch("jet2CHF", &jet2CHF);
  ZHCollection->Branch("jet2MUF", &jet2MUF);
  ZHCollection->Branch("jet2CEMF", &jet2CEMF);
  ZHCollection->Branch("jet2NumConst", &jet2NumConst);
  ZHCollection->Branch("jet2CHM", &jet2CHM);
  ZHCollection->Branch("jet2NumNeutralParticles", &jet2NumNeutralParticles);

  ZHCollection->Branch("HiggsPt", &HiggsPt);
  ZHCollection->Branch("HiggsEta", &HiggsEta);
  ZHCollection->Branch("HiggsPhi", &HiggsPhi);
  ZHCollection->Branch("HiggsM", &HiggsM);
}

// ------------ method called once each job just after ending the event loop  ------------
void ZHTree::endJob() {

}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void ZHTree::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  // The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

}

//define this as a plug-in
DEFINE_FWK_MODULE(ZHTree);
