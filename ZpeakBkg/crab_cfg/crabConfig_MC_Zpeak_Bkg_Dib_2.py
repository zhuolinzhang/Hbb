from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'diboson_bkg_ZZTo2L2Q'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ZpeakBkg_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.publication = True
config.Data.outputDatasetTag = 'diboson_bkg_ZZTo2L2Q'
config.Data.splitting = 'Automatic'

config.Site.storageSite = 'T2_CN_Beijing'