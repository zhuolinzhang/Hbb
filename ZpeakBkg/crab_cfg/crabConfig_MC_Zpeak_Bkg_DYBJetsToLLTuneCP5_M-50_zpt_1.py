from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'DYBJetsToLLTuneCP5_M-50_zpt_1'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ZpeakBkg_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/DYBJetsToLL_M-50_Zpt-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.publication = True
config.Data.outputDatasetTag = 'DYBJetsToLLTuneCP5_M-50_zpt_1'
config.Data.splitting = 'Automatic'

config.Site.storageSite = 'T2_CN_Beijing'