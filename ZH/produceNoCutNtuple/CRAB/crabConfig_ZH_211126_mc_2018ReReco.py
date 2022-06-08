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

version = '211221'
# 'MultiCRAB' part
if __name__ == '__main__':
    
    from CRABAPI.RawCommand import crabCommand
    config.General.requestName = 'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_ZH2018_' + version
    config.Data.inputDataset = '/ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_ZH2018_' + version
    config.Data.inputDataset = '/ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_ZH2018_' + version
    config.Data.inputDataset = '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-4to50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-4to50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-4to50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-4to50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-4to50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_BGenFilter_Zpt-100to200_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_BGenFilter_Zpt-100to200_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_BGenFilter_Zpt-200toInf_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/DYJetsToLL_BGenFilter_Zpt-200toInf_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=102X_upgrade2018_realistic_v15', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018.txt']
    crabCommand('submit', config = config)

