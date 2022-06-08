import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("ZHTree")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))

options = VarParsing.VarParsing('analysis')

options.register ('globalTag',
                  '106X_upgrade2018_realistic_v15_L1v1', # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "Global Tag For Analysis")

options.register ('isData',
                  0, # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "The input dataset is MC or Data. MC=0, Data=1")

options.register ('hltPath',
                  'HLT_IsoMu20_v*', # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "The HLT path in analysis")

options.register ('roccorPath',
                  'ZH/Tree/data/RoccoR2018UL.txt', # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,          # string, int, or float
                  "The RoccoR file path in analysis")

options.parseArguments()

if options.isData == 0: isDataBool = False
elif options.isData == 1: isDataBool = True

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, options.globalTag, '')

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False),
SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.source = cms.Source("PoolSource", fileNames =
        cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/data/Run2018A/DoubleMuon/MINIAOD/12Nov2019_UL2018-v2/100000/020353D5-EB7E-3A42-928B-64ABB6449999.root'))

process.demo = cms.EDAnalyzer("ZHTree",
                                       muonTag = cms.InputTag("slimmedMuons"),
                                       vertexTag = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                       triggerTag = cms.InputTag("TriggerResults", "", "HLT"),
                                       HLTPath = cms.string(options.hltPath),
                                       jetTag = cms.InputTag("slimmedJets"),
                                       bTag = cms.string("pfDeepCSVJetTags"),
                                       genPartTag  = cms.InputTag("prunedGenParticles"),
                                       isData = cms.bool(isDataBool),
                                       roccorFile = cms.FileInPath(options.roccorPath),
                                       #UseRochCorr = cms.untracked.bool(False),
                                       RndmSeed    = cms.untracked.uint32(2345)
)

process.TFileService = cms.Service("TFileService",
          fileName = cms.string('ZHTree.root')
)

process.p = cms.Path(process.demo)
