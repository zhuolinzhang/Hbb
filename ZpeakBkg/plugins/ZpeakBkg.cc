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

#include <TLorentzVector.h>
#include <TVector3.h>
#include <TProfile.h>
#include <TTree.h>


// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

//
// class declaration
//

class ZpeakBkg : public edm::one::EDAnalyzer<edm::one::SharedResources> {

   public:

      explicit ZpeakBkg(const edm::ParameterSet&);
      ~ZpeakBkg();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:

      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      
      edm::EDGetTokenT<pat::MuonCollection> muonCollToken;
      //edm::EDGetTokenT<pat::PackedGenParticleCollection> genCollToken;
      edm::EDGetTokenT<std::vector<reco::Vertex>> vertexToken;
      //edm::EDGetTokenT<reco::Vertex> vertexToken;
  
      TH1F* h_RecDiMuonM_Nocut;
      TH1F* h_RecDiMuonM_pt;
      TH1F* h_RecDiMuonM_eta;
      TH1F* h_RecDiMuonM_iso;
      TH1F* h_RecDiMuonM_dxy;
      TH1F* h_RecDiMuonM;
      TH1F* h_RecDiMuonM_Global;
      //TH1F* h_GenDiMuonM;
  
};

//
// constructors and destructor
//
ZpeakBkg::ZpeakBkg(const edm::ParameterSet& iConfig) {

  edm::InputTag theMuonLabel("slimmedMuons");
  //edm::InputTag theGenMuonLabel("packedGenParticles");
  edm::InputTag VertexTag ("offlineSlimmedPrimaryVertices");
  
  muonCollToken = consumes<pat::MuonCollection>(theMuonLabel);
  //genCollToken = consumes<pat::PackedGenParticleCollection>(theGenMuonLabel);
  vertexToken = consumes<std::vector<reco::Vertex>>(VertexTag);

  edm::Service<TFileService> fs;
  
  h_RecDiMuonM_Nocut = fs->make<TH1F>("h_RecDiMuonM_Nocut",";m_{#mu^{+}#mu^{-}};",60,75,105);
  h_RecDiMuonM_pt = fs->make<TH1F>("h_RecDiMuonM_pt",";m_{#mu^{+}#mu^{-}};",60,75,105);
  h_RecDiMuonM_eta = fs->make<TH1F>("h_RecDiMuonM_eta",";m_{#mu^{+}#mu^{-}};",60,75,105);
  h_RecDiMuonM_iso = fs->make<TH1F>("h_RecDiMuonM_iso",";m_{#mu^{+}#mu^{-}};",60,75,105);
  h_RecDiMuonM_dxy = fs->make<TH1F>("h_RecDiMuonM_dxy",";m_{#mu^{+}#mu^{-}};",60,75,105);
  h_RecDiMuonM = fs->make<TH1F>("h_RecDiMuonM",";m_{#mu^{+}#mu^{-}};",60,75,105);
  h_RecDiMuonM_Global = fs->make<TH1F>("h_RecDiMuonM_Global",";m_{#mu^{+}#mu^{-}};",400,0,200);
  
  //h_GenDiMuonM = fs->make<TH1F>("h_GenDiMuonM",";m_{#mu^{+}#mu^{-}};",80,70,110);
 
}


ZpeakBkg::~ZpeakBkg() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void ZpeakBkg::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  using namespace edm;
  using namespace std;
  using namespace reco;
  using namespace pat;
   
  edm::Handle<vector<pat::Muon>> muons;
  iEvent.getByToken(muonCollToken, muons);

  /* 
  edm::Handle <pat::PackedGenParticleCollection> genColl;
  iEvent.getByToken(genCollToken, genColl);
  */

  edm::Handle<vector<reco::Vertex>> vertices;
  iEvent.getByToken(vertexToken, vertices);
  if(!vertices.isValid()) {
    throw cms::Exception("Vertex collection not valid!"); 
  } 



   // Let's check that we have at least one good vertex! 
  
  std::vector<reco::Vertex>::const_iterator firstGoodVertex = vertices->end();

   for (std::vector<reco::Vertex>::const_iterator it=vertices->begin(); it!=firstGoodVertex; ++it) {
    if (!it->isFake() && it->ndof()>4 && it->position().Rho()<2. && std::abs(it->position().Z())<24.) {
      if(firstGoodVertex == vertices->end()) firstGoodVertex = it;
      break;
    }
  }
  // Require a good vertex
  if(firstGoodVertex == vertices->end()) return;

  /////////////////////////////////////////////////
  // Dimuon pairs /////////////////////////////////
  /////////////////////////////////////////////////
    
  //put your code here
  // no cut
  for (auto mup = muons->cbegin(); mup != muons->cend(); ++mup) {
      if ( not (mup->charge() > 0 ) ) continue;
      if ( not (mup->isGlobalMuon()) ) continue;
      // Some constrains were mentioned in AN-18-073 added by Zhuolin 2020-10-11
      // find mu-
           for (auto mum = muons->cbegin(); mum != muons->cend(); ++mum) {
                if ( not (mum->charge() < 0 ) ) continue;
                if ( not (mum->isGlobalMuon()) ) continue;
                
                double diMuonRecMass = ((mup->p4() + mum->p4()).M());

                h_RecDiMuonM_Global->Fill(diMuonRecMass);

                if ( diMuonRecMass < 75 || diMuonRecMass > 105) continue; // only look around the Z peak
                h_RecDiMuonM_Nocut->Fill(diMuonRecMass);

           }
  }
  

  // add pt constraints

  for (auto mup = muons->cbegin(); mup != muons->cend(); ++mup) {
      if ( not (mup->charge() > 0 ) ) continue;
      if ( not (mup->isGlobalMuon()) ) continue;
      // find mu-
           for (auto mum = muons->cbegin(); mum != muons->cend(); ++mum) {
                if ( not (mum->charge() < 0 ) ) continue;
                if ( not (mum->isGlobalMuon()) ) continue;

                // pt constraints - Zhuolin 2020-10-12
                if ( mup->pt() > mum->pt() ){
                  if ( mup->pt() <= 25.0 ) continue;
                  if ( mum->pt() <= 15.0 ) continue;
                }
                else
                {
                  if ( mup->pt() <= 15.0 ) continue;
                  if ( mum->pt() <= 25.0 ) continue;
                }
                
                double diMuonRecMass = ((mup->p4() + mum->p4()).M());
                if ( diMuonRecMass < 75 || diMuonRecMass > 105) continue; // only look around the Z peak
                h_RecDiMuonM_pt->Fill(diMuonRecMass);

           }
  }


  // add eta constraint

  for (auto mup = muons->cbegin(); mup != muons->cend(); ++mup) {
      if ( not (mup->charge() > 0 ) ) continue;
      if ( not (mup->isGlobalMuon()) ) continue;
      if ( fabs(mup->eta()) >= 2.4 ) continue;

      // find mu-
           for (auto mum = muons->cbegin(); mum != muons->cend(); ++mum) {
                if ( not (mum->charge() < 0 ) ) continue;
                if ( not (mum->isGlobalMuon()) ) continue;
                if ( fabs(mum->eta()) >= 2.4 ) continue;

                // pt constraints - Zhuolin 2020-10-12
                if ( mup->pt() > mum->pt() ){
                  if ( mup->pt() <= 25.0 ) continue;
                  if ( mum->pt() <= 15.0 ) continue;
                }
                else
                {
                  if ( mup->pt() <= 15.0 ) continue;
                  if ( mum->pt() <= 25.0 ) continue;
                }
                
                double diMuonRecMass = ((mup->p4() + mum->p4()).M());
                if ( diMuonRecMass < 75 || diMuonRecMass > 105) continue; // only look around the Z peak
                h_RecDiMuonM_eta->Fill(diMuonRecMass);

           }
  }


  // add isolation constraint

  for (auto mup = muons->cbegin(); mup != muons->cend(); ++mup) {
      if ( not (mup->charge() > 0 ) ) continue;
      if ( not (mup->isGlobalMuon()) ) continue;
      //if ( not (mup->pt() > 20.0 ) ) continue;
      if ( fabs(mup->eta()) >= 2.4 ) continue;
      // Some constraints were mentioned in AN-18-073 added by Zhuolin 2020-10-11
      if ((mup->pfIsolationR04().sumChargedHadronPt + std::max(0., mup->pfIsolationR04().sumNeutralHadronEt + mup->pfIsolationR04().sumPhotonEt - 0.5*mup->pfIsolationR04().sumPUPt))/mup->pt() >= 0.4) continue; // PF isolation

      // find mu-
           for (auto mum = muons->cbegin(); mum != muons->cend(); ++mum) {
                if ( not (mum->charge() < 0 ) ) continue;
                if ( not (mum->isGlobalMuon()) ) continue;
                //if ( not (mum->pt() > 20.0 ) ) continue;
                if ( fabs(mum->eta()) >= 2.4 ) continue;
                // Some constraints were mentioned in AN-18-073 added by Zhuolin 2020-10-11
                if ((mum->pfIsolationR04().sumChargedHadronPt + std::max(0., mum->pfIsolationR04().sumNeutralHadronEt + mum->pfIsolationR04().sumPhotonEt - 0.5*mum->pfIsolationR04().sumPUPt))/mum->pt() >= 0.4) continue;

                // pt constraints - Zhuolin 2020-10-12
                if ( mup->pt() > mum->pt() ){
                  if ( mup->pt() <= 25.0 ) continue;
                  if ( mum->pt() <= 15.0 ) continue;
                }
                else
                {
                  if ( mup->pt() <= 15.0 ) continue;
                  if ( mum->pt() <= 25.0 ) continue;
                }
                
                double diMuonRecMass = ((mup->p4() + mum->p4()).M());
                if ( diMuonRecMass < 75 || diMuonRecMass > 105) continue; // only look around the Z peak
                h_RecDiMuonM_iso->Fill(diMuonRecMass);

           }
  }

  // add dxy constraint

  for (auto mup = muons->cbegin(); mup != muons->cend(); ++mup) {
      if ( not (mup->charge() > 0 ) ) continue;
      if ( not (mup->isGlobalMuon()) ) continue;
      //if ( not (mup->pt() > 20.0 ) ) continue;
      if ( fabs(mup->eta()) >= 2.4 ) continue;
      // Some constraints were mentioned in AN-18-073 added by Zhuolin 2020-10-11
      if ((mup->pfIsolationR04().sumChargedHadronPt + std::max(0., mup->pfIsolationR04().sumNeutralHadronEt + mup->pfIsolationR04().sumPhotonEt - 0.5*mup->pfIsolationR04().sumPUPt))/mup->pt() >= 0.4) continue; // PF isolation
      if ( not (fabs(mup->muonBestTrack()->dxy(firstGoodVertex->position())) < 0.5 ) ) continue; 

      // find mu-
           for (auto mum = muons->cbegin(); mum != muons->cend(); ++mum) {
                if ( not (mum->charge() < 0 ) ) continue;
                if ( not (mum->isGlobalMuon()) ) continue;
                //if ( not (mum->pt() > 20.0 ) ) continue;
                if ( fabs(mum->eta()) >= 2.4 ) continue;
                // Some constraints were mentioned in AN-18-073 added by Zhuolin 2020-10-11
                if ((mum->pfIsolationR04().sumChargedHadronPt + std::max(0., mum->pfIsolationR04().sumNeutralHadronEt + mum->pfIsolationR04().sumPhotonEt - 0.5*mum->pfIsolationR04().sumPUPt))/mum->pt() >= 0.4) continue;
                if ( not (fabs(mum->muonBestTrack()->dxy(firstGoodVertex->position())) < 0.5 ) ) continue; 

                // pt constraints - Zhuolin 2020-10-12
                if ( mup->pt() > mum->pt() ){
                  if ( mup->pt() <= 25.0 ) continue;
                  if ( mum->pt() <= 15.0 ) continue;
                }
                else
                {
                  if ( mup->pt() <= 15.0 ) continue;
                  if ( mum->pt() <= 25.0 ) continue;
                }
                
                double diMuonRecMass = ((mup->p4() + mum->p4()).M());
                if ( diMuonRecMass < 75 || diMuonRecMass > 105) continue; // only look around the Z peak
                h_RecDiMuonM_dxy->Fill(diMuonRecMass);

           }
  }

  // add dz constraint (full constraints)

  for (auto mup = muons->cbegin(); mup != muons->cend(); ++mup) {
      if ( not (mup->charge() > 0 ) ) continue;
      if ( not (mup->isGlobalMuon()) ) continue;
      //if ( not (mup->pt() > 20.0 ) ) continue;
      if ( fabs(mup->eta()) >= 2.4 ) continue;
      // Some constraints were mentioned in AN-18-073 added by Zhuolin 2020-10-11
      if ((mup->pfIsolationR04().sumChargedHadronPt + std::max(0., mup->pfIsolationR04().sumNeutralHadronEt + mup->pfIsolationR04().sumPhotonEt - 0.5*mup->pfIsolationR04().sumPUPt))/mup->pt() >= 0.4) continue; // PF isolation
      if ( not (fabs(mup->muonBestTrack()->dxy(firstGoodVertex->position())) < 0.5 ) ) continue; 
      if ( not (fabs(mup->muonBestTrack()->dz(firstGoodVertex->position())) < 1. ) ) continue;

      // find mu-
           for (auto mum = muons->cbegin(); mum != muons->cend(); ++mum) {
                if ( not (mum->charge() < 0 ) ) continue;
                if ( not (mum->isGlobalMuon()) ) continue;
                //if ( not (mum->pt() > 20.0 ) ) continue;
                if ( fabs(mum->eta()) >= 2.4 ) continue;
                // Some constraints were mentioned in AN-18-073 added by Zhuolin 2020-10-11
                if ((mum->pfIsolationR04().sumChargedHadronPt + std::max(0., mum->pfIsolationR04().sumNeutralHadronEt + mum->pfIsolationR04().sumPhotonEt - 0.5*mum->pfIsolationR04().sumPUPt))/mum->pt() >= 0.4) continue;
                if ( not (fabs(mum->muonBestTrack()->dxy(firstGoodVertex->position())) < 0.5 ) ) continue; 
                if ( not (fabs(mum->muonBestTrack()->dz(firstGoodVertex->position())) < 1. ) ) continue;

                // pt constraints - Zhuolin 2020-10-12
                if ( mup->pt() > mum->pt() ){
                  if ( mup->pt() <= 25.0 ) continue;
                  if ( mum->pt() <= 15.0 ) continue;
                }
                else
                {
                  if ( mup->pt() <= 15.0 ) continue;
                  if ( mum->pt() <= 25.0 ) continue;
                }
                
                double diMuonRecMass = ((mup->p4() + mum->p4()).M());
                if ( diMuonRecMass < 75 || diMuonRecMass > 105) continue; // only look around the Z peak
                h_RecDiMuonM->Fill(diMuonRecMass);

           }
  }
}


// ------------ method called once each job just before starting event loop  ------------
void ZpeakBkg::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void ZpeakBkg::endJob() {
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void ZpeakBkg::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  // The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

}

//define this as a plug-in
DEFINE_FWK_MODULE(ZpeakBkg);
