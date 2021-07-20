import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str, default="/publicfs/cms/user/zhangzhuolin/CRABResult", help="The default path of CRAB result")
parser.add_argument("-t", "--task", type=str, help="The task name of CRAB job. e.g. ZHTree")
parser.add_argument("-d", "--date", type=str, help="The task date of CRAB job. e.g. 210412")
args = parser.parse_args()

def readLocalList(listFilePath):
    fileList = []
    with open(listFilePath, 'r') as f:
        fileListOrigin = f.readlines()
        for i in fileListOrigin:
            fileList.append(i.rstrip())
    return fileList

def generateScripts(scriptSavePath, skimTTreeSavePath, originTTreePath, macroPath, scriptNum):
    if os.path.exists(scriptSavePath): pass
    else: os.mkdir(scriptSavePath)
    fileName = 'SkimJobSubmit_' + str(scriptNum) + '.sh'
    with open(scriptSavePath + '/' + fileName, 'w') as f:
        f.write('export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch/\n')
        f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
        f.write('root -b -q \'{}("{}", "{}")\''.format(macroPath, originTTreePath, skimTTreeSavePath))
    os.chmod(scriptSavePath +"/" + fileName, 0o755)
    print("Script {} is generated!".format(fileName))

t3OriginPath = '/publicfs/cms/user/zhangzhuolin/target_files'
t3SkimPath = '/publicfs/cms/user/zhangzhuolin/TTreeReducer'
macroPath = t3SkimPath + '/ntupleReducerUL.cc'
taskFilePath = t3OriginPath + '/' + args.task + "_" + args.date
skimFilePath = t3SkimPath + '/' + args.task + "_" + args.date
checkResultPath = args.path + "/" + args.task + "_" + args.date
mcListPath = checkResultPath + "/" + "MCList.txt"
dataListPath = checkResultPath + "/" + "DataList.txt"

mcList = readLocalList(mcListPath)
dataList = readLocalList(dataListPath)

mcScriptSavePath = checkResultPath + "/" + "MCReduceScripts"
dataScriptSavePath = checkResultPath + "/" + "DataReduceScripts"

for i in mcList:
    print("Generate the script of {}.".format(i))
    mcSourcePath = taskFilePath + '/' + i + '.root'
    generateScripts(mcScriptSavePath, skimFilePath, mcSourcePath, macroPath, mcList.index(i))

for i in dataList:
    print("Generate the script of {}.".format(i))
    dataSourcePath = taskFilePath + '/' + i + '.root'
    generateScripts(dataScriptSavePath, skimFilePath, dataSourcePath, macroPath, dataList.index(i))
