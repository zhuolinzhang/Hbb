import Tools.CheckCRABResults as CheckResults
import Tools.CopySE2lxslc as CopyFiles
import Tools.haddFiles as Hadd
import argparse
import os
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 description="This script can query and copy the result of CRAB jobs if you specify a .txt file which recorded all submitted datasets.", epilog="If you use -s to specify a .txt file, this script can only find MC samples or DATA once.")
parser.add_argument("-m", "--mode", type=int, help='''1 - Only check results
2 - Check results and copy files 
3 - mode 2 and generate HTCondor scripts
4 - mode 3 and merge files''')
parser.add_argument("--clean", help="Delete all source files", action='store_true')
parser.add_argument("-t", "--task", type=str, help="Input the task name (e.g. ZHTree)")
parser.add_argument("-d", "--date", type=str, help="Input the date (YYMMDD)")
parser.add_argument("-s", "--dataset", type=str, default=None, help="Dataset list")
parser.add_argument("--isData", action="store_true", help="The custom dataset is DATA")
parser.add_argument("-p", "--save", type=str, default="/publicfs/cms/user/zhangzhuolin/CRABResult", help='''The home path of save query result
The default path is /publicfs/cms/user/zhangzhuolin/CRABResult''')
args = parser.parse_args()

# Check VO is activated. But if the VO is invaild, this function doesn't work. I will update to fix this
# bug in the furture.
CheckResults.checkVO()
resultPath = '/publicfs/cms/user/zhangzhuolin/CRABResult'
if args.mode in range(1, 5):
    resultTuple = CheckResults.checkCRABResluts(resultPath, args.task, args.date, args.dataset, args.isData)
    mcList = resultTuple[0]
    dataList = resultTuple[1]
    if args.mode in range(2, 5):
        t3Directory = '/publicfs/cms/user/zhangzhuolin/target_files/{}_{}'.format(args.task, args.date)
        for datasetName in mcList:
            jobName = datasetName + "_" + args.task + "_" + args.date
            CopyFiles.copyFiles(t3Directory, jobName, datasetName, 'mc')
            if args.mode in range (3, 5):
                scriptSavePath = resultPath + '/' + args.task + "_" + args.date + "/" + "mcJobSubmit"
                Hadd.generateScripts(scriptSavePath, os.getcwd() + '/Tools', jobName, mcList.index(datasetName), 'mc')
                if args.mode == 4:
                    Hadd.haddFiles(t3Directory, jobName, datasetName, args.clean)
        for datasetName in dataList:
            jobName = datasetName + "_" + args.task + "_" + args.date
            CopyFiles.copyFiles(t3Directory, jobName, datasetName, 'data')
            if args.mode in range (3, 5):
                scriptSavePath = resultPath + '/' + args.task + "_" + args.date + "/" + "dataJobSubmit"
                Hadd.generateScripts(scriptSavePath, os.getcwd() + '/Tools', jobName, dataList.index(datasetName), 'data')
                if args.mode == 4:
                    Hadd.haddFiles(t3Directory, jobName, datasetName, args.clean)
else: 
    raise SystemError("The mode number is wrong! Please execute the script again!")
