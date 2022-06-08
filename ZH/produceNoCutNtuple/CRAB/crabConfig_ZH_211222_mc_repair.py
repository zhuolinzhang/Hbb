from CRABClient.UserUtilities import config

config = config()

config.General.workArea = 'crab_project'
config.JobType.pluginName = 'Analysis'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publication = False
config.Site.storageSite = 'T2_CN_Beijing'
config.JobType.allowUndistributedCMSSW = True

version = '211224'
# 'MultiCRAB' part
if __name__ == '__main__':
    
    from CRABAPI.RawCommand import crabCommand
    '''
    config.General.requestName = 'DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_upgrade2018_realistic_v15_L1v1', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_upgrade2018_realistic_v15_L1v1', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_upgrade2018_realistic_v15_L1v1', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018UL.txt']
    crabCommand('submit', config = config)

    '''
    config.General.requestName = 'QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v3/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_upgrade2018_realistic_v15_L1v1', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v3/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_upgrade2018_realistic_v15_L1v1', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAOD-106X_upgrade2018_realistic_v11_L1v1-v3/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_upgrade2018_realistic_v15_L1v1', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018UL.txt']
    crabCommand('submit', config = config)
