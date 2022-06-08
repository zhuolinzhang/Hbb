from CRABClient.UserUtilities import config

config = config()

config.General.workArea = 'crab_project'
config.JobType.pluginName = 'Analysis'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publication = False
config.Site.storageSite = 'T2_CN_Beijing'
config.JobType.allowUndistributedCMSSW = True

version = '220311'
# 'MultiCRAB' part
if __name__ == '__main__':
    
    from CRABAPI.RawCommand import crabCommand
    config.General.requestName = 'DYJetsToLL_BGenFilter_Zpt-100to200_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ZH2016_' + version
    config.Data.inputDataset = '/DYJetsToLL_BGenFilter_Zpt-100to200_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=80X_mcRun2_asymptotic_2016_TrancheIV_v8', 'isData=0', 'hltPath=HLT_Mu17_Mu8_v*', 'roccorPath=ZH/Tree/data/RoccoR2016.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_BGenFilter_Zpt-200toInf_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ZH2016_' + version
    config.Data.inputDataset = '/DYJetsToLL_BGenFilter_Zpt-200toInf_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=80X_mcRun2_asymptotic_2016_TrancheIV_v8', 'isData=0', 'hltPath=HLT_Mu17_Mu8_v*', 'roccorPath=ZH/Tree/data/RoccoR2016.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8_ZH2016_' + version
    config.Data.inputDataset = '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=80X_mcRun2_asymptotic_2016_TrancheIV_v8', 'isData=0', 'hltPath=HLT_Mu17_Mu8_v*', 'roccorPath=ZH/Tree/data/RoccoR2016.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_ZH2016_' + version
    config.Data.inputDataset = '/ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=80X_mcRun2_asymptotic_2016_TrancheIV_v8', 'isData=0', 'hltPath=HLT_Mu17_Mu8_v*', 'roccorPath=ZH/Tree/data/RoccoR2016.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_ZH2016_' + version
    config.Data.inputDataset = '/ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/RunIISummer16MiniAODv3-PUMoriond17_94X_mcRun2_asymptotic_v3-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=80X_mcRun2_asymptotic_2016_TrancheIV_v8', 'isData=0', 'hltPath=HLT_Mu17_Mu8_v*', 'roccorPath=ZH/Tree/data/RoccoR2016.txt']
    crabCommand('submit', config = config)

