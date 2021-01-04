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
#include "TString.h"
#include "TNtuple.h"


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
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"
//
// class declaration
//

class TrackerDis : public edm::one::EDAnalyzer<edm::one::SharedResources> {

   public:

      explicit TrackerDis(const edm::ParameterSet&);
      ~TrackerDis();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

   private:

      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      
      edm::EDGetTokenT<pat::MuonCollection> muon_label;
      //edm::EDGetTokenT<pat::PackedGenParticleCollection> genCollToken;
      edm::EDGetTokenT<reco::VertexCollection> vertex_label;
      //edm::EDGetTokenT<reco::Vertex> vertex_label;
      edm::EDGetTokenT<edm::TriggerResults> trigger_label;
  
      TNtuple *mupDetector;
      TNtuple *mumDetector;
      TNtuple *mupTriggerDetector;
      TNtuple *mumTriggerDetector;
      TNtuple *mupCutDetector;
      TNtuple *mumCutDetector;
      TNtuple *mupCutTriggerDetector;
      TNtuple *mumCutTriggerDetector;
  
};

//
// constructors and destructor
//
TrackerDis::TrackerDis(const edm::ParameterSet& iConfig) {

  using namespace std;
  
  muon_label = (consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muon")));
  //genCollToken = consumes<pat::PackedGenParticleCollection>(theGenMuonLabel);
  vertex_label = (consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexTag")));
  trigger_label = (consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerResults")));

  edm::Service<TFileService> fs;
  mupDetector = fs->make<TNtuple>("mupDetector", "Muon Plus Detector Parameters", "m:pt:eta:phi:nMuonHits:nMatchedStations:nPixelHits:nTrackerLayerHits");
  mumDetector = fs->make<TNtuple>("mumDetector", "Muon Minus Detector Parameters", "m:pt:eta:phi:nMuonHits:nMatchedStations:nPixelHits:nTrackerLayerHits");
  mupTriggerDetector = fs->make<TNtuple>("mupTriggerDetector", "Muon Plus Detector Parameters After HLT", "m:pt:eta:phi:nMuonHits:nMatchedStations:nPixelHits:nTrackerLayerHits");
  mumTriggerDetector = fs->make<TNtuple>("mumTriggerDetector", "Muon Minus Detector Parameters After HLT", "m:pt:eta:phi:nMuonHits:nMatchedStations:nPixelHits:nTrackerLayerHits");
  mupCutDetector = fs->make<TNtuple>("mupCutDetector", "Muon Plus Detector Parameters With Cuts", "m:pt:eta:phi:nMuonHits:nMatchedStations:nPixelHits:nTrackerLayerHits");
  mumCutDetector = fs->make<TNtuple>("mumCutDetector", "Muon Minus Detector Parameters With Cuts", "m:pt:eta:phi:nMuonHits:nMatchedStations:nPixelHits:nTrackerLayerHits");
  mupCutTriggerDetector = fs->make<TNtuple>("mupCutTriggerDetector", "Muon Plus Detector Parameters After HLT With Cuts", "m:pt:eta:phi:nMuonHits:nMatchedStations:nPixelHits:nTrackerLayerHits");
  mumCutTriggerDetector = fs->make<TNtuple>("mumCutTriggerDetector", "Muon Minus Detector Parameters After HLT With Cuts", "m:pt:eta:phi:nMuonHits:nMatchedStations:nPixelHits:nTrackerLayerHits"); 
  //h_GenDiMuonM = fs->make<TH1F>("h_GenDiMuonM",";m_{#mu^{+}#mu^{-}};",80,70,110);
 
}


TrackerDis::~TrackerDis() {
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void TrackerDis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {

  using namespace edm;
  using namespace std;
  using namespace reco;
  using namespace pat;
   
  edm::Handle<vector<pat::Muon>> muons;
  iEvent.getByToken(muon_label, muons);

  /* 
  edm::Handle <pat::PackedGenParticleCollection> genColl;
  iEvent.getByToken(genCollToken, genColl);
  */

  edm::Handle<vector<reco::Vertex>> vertices;
  iEvent.getByToken(vertex_label, vertices);
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
  // Tight Muon
  // find mu+
  
  for (auto mup = muons->cbegin(); mup != muons->cend(); ++mup) {
      const char *hltName = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*";
      double mupRecPt = ((mup->p4()).pt());
      double mupRecEta = ((mup->p4()).eta());
      double mupRecPhi = ((mup->p4()).phi());
      double mupRecM = ((mup->p4()).M());

      // Use tight muon ID, pT and eta cut were mentioned in AN2018/073 - Zhuolin 2020-12-22
      if ( not (mup->charge() > 0 ) ) continue;
      if ( not (fabs(mup->eta()) < 2.4) ) continue;

      if ( not (mup->isGlobalMuon()) ) continue;
      if ( not (mup->isPFMuon()) ) continue;
      if ( not (mup->globalTrack()->normalizedChi2() < 10.) ) continue;
      if ( not (fabs(mup->muonBestTrack()->dxy(firstGoodVertex->position())) < 0.2 ) ) continue; // dxy < 0.2 
      if ( not (fabs(mup->muonBestTrack()->dz(firstGoodVertex->position())) < 0.5 ) ) continue; // dz < 0.5
      // PF Isolation very loose
      if ( not ((mup->pfIsolationR04().sumChargedHadronPt + std::max(0., mup->pfIsolationR04().sumNeutralHadronEt + mup->pfIsolationR04().sumPhotonEt - 0.5*mup->pfIsolationR04().sumPUPt))/mup->pt() < 0.4) ) continue; 
      float mupMuonHits = mup->globalTrack()->hitPattern().numberOfValidMuonHits();
      float mupMuonStations = mup->numberOfMatchedStations();
      float mupPixelHits = mup->innerTrack()->hitPattern().numberOfValidPixelHits();
      float mupTrackerLayers = mup->innerTrack()->hitPattern().trackerLayersWithMeasurement();
      // find mu-
           for (auto mum = muons->cbegin(); mum != muons->cend(); ++mum) {
                double mumRecPt = ((mum->p4()).pt());
                double mumRecEta = ((mum->p4()).eta());
                double mumRecPhi = ((mum->p4()).phi());
                double mumRecM = ((mum->p4()).M());

                if ( not (mum->charge() < 0 ) ) continue;
                if ( not (fabs(mum->eta()) < 2.4) ) continue;
                
                if ( not (mum->isPFMuon()) ) continue;
                if ( not (mum->isGlobalMuon()) ) continue;
                if ( not (mum->globalTrack()->normalizedChi2() < 10.) ) continue; // chi-square of the global-muon track fit < 10
                if ( not (fabs(mum->muonBestTrack()->dxy(firstGoodVertex->position())) < 0.2 ) ) continue; // dxy < 0.2 
                if ( not (fabs(mum->muonBestTrack()->dz(firstGoodVertex->position())) < 0.5 ) ) continue; // dz < 0.5
                // PF Isolation very loose
                if ( not ((mum->pfIsolationR04().sumChargedHadronPt + std::max(0., mum->pfIsolationR04().sumNeutralHadronEt + mum->pfIsolationR04().sumPhotonEt - 0.5*mum->pfIsolationR04().sumPUPt))/mum->pt() < 0.4) ) continue; 
                // pt constrains - Zhuolin 2020-10-12
                if ( mup->pt() > mum->pt() ){
                  if ( mup->pt() <= 25.0 ) continue;
                  if ( mum->pt() <= 15.0 ) continue;
                }
                else
                {
                  if ( mup->pt() <= 15.0 ) continue;
                  if ( mum->pt() <= 25.0 ) continue;
                }
                float mumMuonHits = mum->globalTrack()->hitPattern().numberOfValidMuonHits();
                float mumMuonStations = mum->numberOfMatchedStations();
                float mumPixelHits = mum->innerTrack()->hitPattern().numberOfValidPixelHits();
                float mumTrackerLayers = mum->innerTrack()->hitPattern().trackerLayersWithMeasurement();
                double diMuonRecMass = ((mup->p4() + mum->p4()).M());
                if ( diMuonRecMass < 75 || diMuonRecMass > 105) continue; // only look around the Z peak
                // Trigger match
                const pat::Muon *muon1 = &(*mup);
                const pat::Muon *muon2 = &(*mum);

                if ( muon1->triggerObjectMatchByPath(hltName) != nullptr && muon2->triggerObjectMatchByPath(hltName) != nullptr){
                    mupCutTriggerDetector->Fill(mupRecM, mupRecPt, mupRecEta, mupRecPhi, mupMuonHits, mupMuonStations, mupPixelHits, mupTrackerLayers);
                    mumCutTriggerDetector->Fill(mumRecM, mumRecPt, mumRecEta, mumRecPhi, mumMuonHits, mumMuonStations, mumPixelHits, mumTrackerLayers);
           }
                mupCutDetector->Fill(mupRecM, mupRecPt, mupRecEta, mupRecPhi, mupMuonHits, mupMuonStations, mupPixelHits, mupTrackerLayers);
                mumCutDetector->Fill(mumRecM, mumRecPt, mumRecEta, mumRecPhi, mumMuonHits, mumMuonStations, mumPixelHits, mumTrackerLayers);
           }
  }
  
    // Loose Muon
    // find mu+

    for (auto mup = muons->cbegin(); mup != muons->cend(); ++mup) {
        const char *hltName = "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*";
        double mupRecPt = ((mup->p4()).pt());
        double mupRecEta = ((mup->p4()).eta());
        double mupRecPhi = ((mup->p4()).phi());
        double mupRecM = ((mup->p4()).M());
        if ( not (mup->charge() > 0 ) ) continue;
        // Loose Muon ID
        if ( not (mup->isGlobalMuon()) ) continue;
        if ( not (mup->isPFMuon()) ) continue;
        float mupMuonHits = mup->globalTrack()->hitPattern().numberOfValidMuonHits();
        float mupMuonStations = mup->numberOfMatchedStations();
        float mupPixelHits = mup->innerTrack()->hitPattern().numberOfValidPixelHits();
        float mupTrackerLayers = mup->innerTrack()->hitPattern().trackerLayersWithMeasurement();

        // find mu-
             for (auto mum = muons->cbegin(); mum != muons->cend(); ++mum) {
                  double mumRecPt = ((mum->p4()).pt());
                  double mumRecEta = ((mum->p4()).eta());
                  double mumRecPhi = ((mum->p4()).phi());
                  double mumRecM = ((mum->p4()).M()); 
                  if ( not (mum->charge() < 0 ) ) continue;
                  // Loose muon ID
                  if ( not (mum->isPFMuon()) ) continue;
                  if ( not (mum->isGlobalMuon()) ) continue;
                  float mumMuonHits = mum->globalTrack()->hitPattern().numberOfValidMuonHits();
                  float mumMuonStations = mum->numberOfMatchedStations();
                  float mumPixelHits = mum->innerTrack()->hitPattern().numberOfValidPixelHits();
                  float mumTrackerLayers = mum->innerTrack()->hitPattern().trackerLayersWithMeasurement();
                  
                  double diMuonRecMass = ((mup->p4() + mum->p4()).M());
                  if ( diMuonRecMass < 75 || diMuonRecMass > 105) continue; // only look around the Z peak
                  
                  // Trigger match
                  const pat::Muon *muon1 = &(*mup);
                  const pat::Muon *muon2 = &(*mum);
                  if ( muon1->triggerObjectMatchByPath(hltName) != nullptr && muon2->triggerObjectMatchByPath(hltName) != nullptr) 
                  {
                      mupTriggerDetector->Fill(mupRecM, mupRecPt, mupRecEta, mupRecPhi, mupMuonHits, mupMuonStations, mupPixelHits, mupTrackerLayers);
                      mumTriggerDetector->Fill(mumRecM, mumRecPt, mumRecEta, mumRecPhi, mumMuonHits, mumMuonStations, mumPixelHits, mumTrackerLayers);
                  }
                  mupDetector->Fill(mupRecM, mupRecPt, mupRecEta, mupRecPhi, mupMuonHits, mupMuonStations, mupPixelHits, mupTrackerLayers);
                  mumDetector->Fill(mumRecM, mumRecPt, mumRecEta, mumRecPhi, mumMuonHits, mumMuonStations, mumPixelHits, mumTrackerLayers);

             }
    
    }
    
                /*
                int idxmup_Gen = -1;
                int idxmum_Gen = -1;

                // Gen matching
                for (auto genParticle = genColl->cbegin(); genParticle != genColl->cend(); ++genParticle) {
                    const pat::PackedGenParticle& mcMuon = (*genParticle);
                    if ( not (abs(mcMuon.pdgId()) == 13 ) ) continue; // make sure it is a muon
                    if ( fabs(mcMuon.eta()) > 2.4 ) continue;
                    if ( fabs(mcMuon.eta()) > 2.4 ) continue;
                    if ( not (mcMuon.pt() > 1.5 ) ) continue;
                    if ( deltaR(mcMuon, *(mup->innerTrack())) < 0.1 && mcMuon.charge() > 0 ) idxmup_Gen = std::distance(genColl->cbegin(), genParticle);
                    if ( deltaR(mcMuon, *(mum->innerTrack())) < 0.1 && mcMuon.charge() < 0 ) idxmum_Gen = std::distance(genColl->cbegin(), genParticle);
                }
                if ( idxmup_Gen > -1 && idxmum_Gen > -1) {
                    double diMuonRecMassGen = (genColl->at(idxmup_Gen).p4() + genColl->at(idxmum_Gen).p4()).M();
                    h_GenDiMuonM->Fill(diMuonRecMassGen);
                }
                */
           
  
}


// ------------ method called once each job just before starting event loop  ------------
void TrackerDis::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void TrackerDis::endJob() {
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void TrackerDis::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {

  // The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);

}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackerDis);
