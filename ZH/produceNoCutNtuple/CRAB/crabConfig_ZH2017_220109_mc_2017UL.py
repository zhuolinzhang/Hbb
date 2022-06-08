from CRABClient.UserUtilities import config

config = config()

config.General.workArea = 'crab_project'
config.JobType.pluginName = 'Analysis'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 8
config.Data.publication = False
config.Site.storageSite = 'T2_CN_Beijing'
config.JobType.allowUndistributedCMSSW = True

version = '220109'
# 'MultiCRAB' part
if __name__ == '__main__':
    
    from CRABAPI.RawCommand import crabCommand

    config.General.requestName = 'QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v3/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)
