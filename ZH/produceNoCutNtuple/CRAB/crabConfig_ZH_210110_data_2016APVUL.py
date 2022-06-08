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

version = '210110'
# 'MultiCRAB' part
if __name__ == '__main__':
    
    from CRABAPI.RawCommand import crabCommand
    config.General.requestName = 'DoubleMuon2016B_ZH2016APV_' + version
    config.Data.inputDataset = '/DoubleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v1/MINIAOD'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_dataRun2_v35', 'isData=1', 'hltPath=HLT_Mu17_v*', 'roccorPath=ZH/Tree/data/RoccoR2016aUL.txt']
    config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
    crabCommand('submit', config = config)

    config.General.requestName = 'DoubleMuon2016C_ZH2016APV_' + version
    config.Data.inputDataset = '/DoubleMuon/Run2016C-HIPM_UL2016_MiniAODv2-v1/MINIAOD'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_dataRun2_v35', 'isData=1', 'hltPath=HLT_Mu17_v*', 'roccorPath=ZH/Tree/data/RoccoR2016aUL.txt']
    config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
    crabCommand('submit', config = config)

    config.General.requestName = 'DoubleMuon2016D_ZH2016APV_' + version
    config.Data.inputDataset = '/DoubleMuon/Run2016D-HIPM_UL2016_MiniAODv2-v1/MINIAOD'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_dataRun2_v35', 'isData=1', 'hltPath=HLT_Mu17_v*', 'roccorPath=ZH/Tree/data/RoccoR2016aUL.txt']
    config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
    crabCommand('submit', config = config)

    config.General.requestName = 'DoubleMuon2016E_ZH2016APV_' + version
    config.Data.inputDataset = '/DoubleMuon/Run2016E-HIPM_UL2016_MiniAODv2-v1/MINIAOD'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_dataRun2_v35', 'isData=1', 'hltPath=HLT_Mu17_v*', 'roccorPath=ZH/Tree/data/RoccoR2016aUL.txt']
    config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
    crabCommand('submit', config = config)

    config.General.requestName = 'DoubleMuon2016F_ZH2016APV_' + version
    config.Data.inputDataset = '/DoubleMuon/Run2016F-HIPM_UL2016_MiniAODv2-v1/MINIAOD'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_dataRun2_v35', 'isData=1', 'hltPath=HLT_Mu17_v*', 'roccorPath=ZH/Tree/data/RoccoR2016aUL.txt']
    config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'
    crabCommand('submit', config = config)

