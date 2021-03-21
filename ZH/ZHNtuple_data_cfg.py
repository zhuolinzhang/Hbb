import FWCore.ParameterSet.Config as cms

process = cms.Process("ZHNtuple")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False),
SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.source = cms.Source("PoolSource", fileNames =
        cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/data/Run2018A/DoubleMuon/MINIAOD/17Sep2018-v2/00000/02F59D88-91F7-D14D-8FD4-6530DBC467FC.root'))

process.demo = cms.EDAnalyzer("ZHNtuple",
                                       muon = cms.InputTag("slimmedMuons"),
                                       vertex = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                       triggerResults = cms.InputTag("TriggerResults", "", "HLT"),
                                       HLTPath = cms.string("HLT_IsoMu20_v*"),
                                       jet = cms.InputTag("slimmedJets"),
                                       #GenPartTag  = cms.InputTag("prunedGenParticles"),
                                       UseRochCorr = cms.untracked.bool(False),
                                       RndmSeed    = cms.untracked.uint32(2345)
)

process.TFileService = cms.Service("TFileService",
          fileName = cms.string('ntuple_ZH_data.root')
)

process.p = cms.Path(process.demo)
