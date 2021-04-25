import Tools.CheckCRABResults as CheckResults
import Tools.CopySE2lxslc as CopyFiles
import Tools.haddFiles as Hadd
import argparse
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--mode", type=int, help='''1 - Only check results
2 - Check results and copy files 
3 - Check results, copy files and merge files''')
parser.add_argument("-o", type=str, help="Input skim to delete all source files")
args = parser.parse_args()

CheckResults.checkVO()
taskName = input("Please input the task name: ") # my CRAB job name style: dataset primary name_taskname_date e.g. ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8_AddTrigger_210112
taskFullDate = input("Please input the date (YYMMDD): ")
resultPath = '/publicfs/cms/user/zhangzhuolin/CRABResult'
if args.mode in range(1, 4):
    resultTuple = CheckResults.checkCRABResluts(resultPath, taskName, taskFullDate)
    mcList = resultTuple[0]
    dataList = resultTuple[1]
    if args.mode in range(2, 4):
        t3Directory = '/publicfs/cms/user/zhangzhuolin/target_files/{}_{}'.format(taskName, taskFullDate)
        for datasetName in mcList:
            jobName = datasetName + "_" + taskName + "_" + taskFullDate
            CopyFiles.copyFiles(t3Directory, jobName, datasetName, taskFullDate, 'mc')
            if args.mode == 3:
                Hadd.haddFiles(t3Directory, jobName, datasetName, args.o)
        for datasetName in dataList:
            jobName = datasetName + "_" + taskName + "_" + taskFullDate
            CopyFiles.copyFiles(t3Directory, jobName, datasetName, taskFullDate, 'data')
            if args.mode == 3:
                Hadd.haddFiles(t3Directory, jobName, datasetName, args.o)
else: print("Error: The mode number is wrong!")