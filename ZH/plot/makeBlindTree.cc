#include <vector>
#include <iostream>
#include <string>
#include <map>
#include <algorithm>
#include <time.h>
#include "ROOT/RDataFrame.hxx"
#include "TTree.h"
#include "TFile.h"
#include "TString.h"
#include "TSystemDirectory.h"
#include "TList.h"
#include "TIterator.h"
#include "TSystem.h"

// List all .root files in a folder. Then we can read them one by one in other functions.
std::vector<TString> listFiles(TString dirName, TString dirPath, bool outputListFlag = false, TString newDirPath = "")
{
    // We use TString in this function to change these variables easily. But in
    // some constructor, we must use const char *.
    const char *ext = ".root";
    std::vector<TString> fileStringList;
    TSystemDirectory dir(dirName.Data(), dirPath.Data());
    TList *fileList = dir.GetListOfFiles();
    if (fileList)
    {
        TSystemFile *file;
        TString fileName;
        TIter next(fileList);
        while ((file = (TSystemFile *)next()))
        {
            fileName = file->GetName();
            if (!file->IsDirectory() && fileName.EndsWith(ext))
            {
                if (outputListFlag)
                    fileStringList.push_back(newDirPath + "/" + fileName);
                else
                    fileStringList.push_back(dirPath + "/" + fileName);
                //std::cout << fileName.Data() << std::endl;
            }
        }
    }
    return fileStringList;
}

TString returnPathOrFileName(TString fileName, std::string flag)
{
    std::string fileNameString = std::string(fileName.Data());
    std::string nameString;
    if (flag == "path") nameString = fileNameString.substr(0, fileNameString.find_last_of("/"));
    else 
    {
        // file name beginning with /
        if(flag == "file") nameString = fileNameString.substr(fileNameString.find_last_of("/"), fileNameString.length());
        else std::cout << "You input wrong option!" << std::endl;
    }
    return TString(nameString);
}

// Check the path exist. If the path doesn't exist, mkdir it.
void checkPath(TString pathName)
{
    if (gSystem->AccessPathName(pathName.Data()))
    {
        gSystem->mkdir(pathName.Data());
        std::cout << "The folder " << pathName.Data() << " is created!" << std::endl;
    }
    else
        std::cout << "The folder " << pathName.Data() << " exist!" << std::endl;
}

int makeBlindTree(TString inputPath)
{
    clock_t tStart = clock();
    ROOT::IsImplicitMTEnabled();
    //TString inputPath = "./ZHTree";
    TString outputSideband = "./sideband";
    TString outputSR = "./sr";
    checkPath(outputSideband);
    checkPath(outputSR);
    TString treeName = "ZHCandidates";
    std::vector<TString> inputFileList = listFiles(inputPath, inputPath);
    for (auto fileName : inputFileList)
    {
        auto d = ROOT::RDataFrame(treeName.Data(), fileName.View());
        std::cout << "Blind " << fileName << std::endl;
        auto branchNames = d.GetColumnNames();
        auto d_sideband = d.Filter("HiggsM < 90 || HiggsM > 150");
        TString datasetName = returnPathOrFileName(fileName, "file");
        d_sideband.Snapshot(treeName.View(), (outputSideband + datasetName).View(), branchNames);
        if (!fileName.Contains("DoubleMuon"))
        {
            auto d_sr = d.Filter("HiggsM >= 90 && HiggsM <= 150");
            d_sr.Snapshot(treeName.View(), (outputSR + datasetName).View(), branchNames);
        }
    }
    printf("Time taken: %.2fs\n", (double)(clock() - tStart) / CLOCKS_PER_SEC);
    return 0;
}
