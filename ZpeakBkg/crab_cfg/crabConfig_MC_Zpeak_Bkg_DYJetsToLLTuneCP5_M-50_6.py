from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'DYJetsToLLTuneCP5_M-50_6'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ZpeakBkg_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.publication = True
config.Data.outputDatasetTag = 'DYJetsToLLTuneCP5_M-50_6'
config.Data.splitting = 'Automatic'

config.Site.storageSite = 'T2_CN_Beijing'