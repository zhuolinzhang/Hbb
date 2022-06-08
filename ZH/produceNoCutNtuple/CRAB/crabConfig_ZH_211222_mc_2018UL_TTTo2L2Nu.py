from CRABClient.UserUtilities import config

config = config()

config.General.workArea = 'crab_project'
config.JobType.pluginName = 'Analysis'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 7
config.Data.publication = False
config.Site.storageSite = 'T2_CN_Beijing'
config.JobType.allowUndistributedCMSSW = True

version = '220111'
# 'MultiCRAB' part
if __name__ == '__main__':
    
    from CRABAPI.RawCommand import crabCommand
    config.General.requestName = 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ZH2018_' + version
    config.Data.inputDataset = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_upgrade2018_realistic_v15_L1v1', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2018UL.txt']
    crabCommand('submit', config = config)
