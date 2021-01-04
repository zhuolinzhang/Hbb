from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_DetectorAnalysis_201226'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'TrackerDis_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'FileBased'
#config.Data.unitsPerJob = 10
config.Data.publication = False
config.Data.outputDatasetTag = 'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_DetectorAnalysis_201226'
config.Data.splitting = 'Automatic'

config.Site.storageSite = 'T2_CN_Beijing'
