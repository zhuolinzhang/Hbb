import FWCore.ParameterSet.Config as cms

process = cms.Process("ZpeakSigTrigger")

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
        cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/data/Run2018B/DoubleMuon/MINIAOD/17Sep2018-v1/00000/054806F3-BB73-8B41-BD57-203C5E8940D2.root'))

process.demo = cms.EDAnalyzer("ZpeakSigTrigger",
                                       muon = cms.InputTag("slimmedMuons"),
                                       vertexTag = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                       triggerResults = cms.InputTag("TriggerResults", "", "HLT"),
                                       #GenPartTag  = cms.InputTag("prunedGenParticles"),
                                       UseRochCorr = cms.untracked.bool(False),
                                       RndmSeed    = cms.untracked.uint32(2345)
)

process.TFileService = cms.Service("TFileService",
          fileName = cms.string('zpeak_data_trigger.root')
)

process.p = cms.Path(process.demo)
