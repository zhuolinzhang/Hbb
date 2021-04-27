import Tools.CheckCRABResults as CheckResults
import Tools.CopySE2lxslc as CopyFiles
import Tools.haddFiles as Hadd
import argparse
import os
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--mode", type=int, help='''1 - Only check results
2 - Check results and copy files 
3 - mode 2 and generate HTCondor scripts
4 - mode 3 and merge files''')
parser.add_argument("-o", type=str, help="Input skim to delete all source files")
args = parser.parse_args()

# Check VO is activated. But if the VO is invaild, this function doesn't work. I will update to fix this
# bug in the furture.
CheckResults.checkVO()
taskName = input("Please input the task name(e.g. ZHTree): ") # my CRAB job name style: dataset primary name_taskname_date e.g. ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_AddTrigger_210112
taskFullDate = input("Please input the date (YYMMDD): ")
resultPath = '/publicfs/cms/user/zhangzhuolin/CRABResult'
if args.mode in range(1, 5):
    resultTuple = CheckResults.checkCRABResluts(resultPath, taskName, taskFullDate)
    mcList = resultTuple[0]
    dataList = resultTuple[1]
    if args.mode in range(2, 5):
        t3Directory = '/publicfs/cms/user/zhangzhuolin/target_files/{}_{}'.format(taskName, taskFullDate)
        for datasetName in mcList:
            jobName = datasetName + "_" + taskName + "_" + taskFullDate
            CopyFiles.copyFiles(t3Directory, jobName, datasetName, taskFullDate, 'mc')
            if args.mode in range (3, 5):
                scriptSavePath = resultPath + '/' + taskName + "_" + taskFullDate + "/" + "mcJobSubmit"
                Hadd.generateScripts(scriptSavePath, os.getcwd() + '/Tools', jobName, mcList.index(datasetName), 'mc')
                if args.mode == 4:
                    Hadd.haddFiles(t3Directory, jobName, datasetName, args.o)
        for datasetName in dataList:
            jobName = datasetName + "_" + taskName + "_" + taskFullDate
            CopyFiles.copyFiles(t3Directory, jobName, datasetName, taskFullDate, 'data')
            if args.mode in range (3, 5):
                scriptSavePath = resultPath + '/' + taskName + "_" + taskFullDate + "/" + "dataJobSubmit"
                Hadd.generateScripts(scriptSavePath, os.getcwd() + '/Tools', jobName, dataList.index(datasetName), 'data')
                if args.mode == 4:
                    Hadd.haddFiles(t3Directory, jobName, datasetName, args.o)
else: print("Error: The mode number is wrong! Please execute the script again!")