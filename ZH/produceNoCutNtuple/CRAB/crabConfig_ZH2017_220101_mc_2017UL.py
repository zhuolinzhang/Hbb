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

version = '220101'
# 'MultiCRAB' part
if __name__ == '__main__':
    
    from CRABAPI.RawCommand import crabCommand
    config.General.requestName = 'DYBJetsToLL_M-50_Zpt-100to200_TuneCP5_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYBJetsToLL_M-50_Zpt-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYBJetsToLL_M-50_Zpt-200toInf_TuneCP5_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYBJetsToLL_M-50_Zpt-200toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v3/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

    config.General.requestName = 'ZZ_TuneCP5_13TeV-pythia8_ZH2017_' + version
    config.Data.inputDataset = '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM'
    config.Data.outputDatasetTag = config.General.requestName
    config.JobType.psetName = '../test/ZHAnalysis_cfg.py'
    config.JobType.pyCfgParams=['globalTag=106X_mc2017_realistic_v8', 'isData=0', 'hltPath=HLT_IsoMu20_v*', 'roccorPath=ZH/Tree/data/RoccoR2017UL.txt']
    crabCommand('submit', config = config)

