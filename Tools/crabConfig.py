from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'diboson_bkg_ZZ_TuneCP5'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ZpeakData_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.publication = False
config.Data.outputDatasetTag = 'diboson_bkg_ZZ_TuneCP5'
config.Data.splitting = 'Automatic'
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

config.Site.storageSite = 'T2_CN_Beijing'
