#include <vector>
#include <fstream>
#include <string>
#include <map>
#include <algorithm>
#include "ROOT/RDataFrame.hxx"
#include "TTree.h"
#include "TFile.h"
#include "TString.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
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

// return the path name of folder in the path or return the file name with a slash in the path 
TString returnPathOrFileName(TString fileName, std::string flag)
{
    std::string fileNameString = std::string(fileName.Data());
    std::string nameString;
    if (flag == "path") nameString = fileNameString.substr(0, fileNameString.find_last_of("/"));
    else 
    {
        // file name with /
        if(flag == "file") nameString = fileNameString.substr(fileNameString.find_last_of("/"), fileNameString.length());
        else std::cout << "You input wrong option!" << std::endl;
    }
    return TString(nameString);
}

// Calculate the cutflow in a .root file.
void cutFlowCalc(TString fileName, std::vector<int> cutFlowCollection)
{
    using namespace std;
    size_t nEvents = cutFlowCollection.size();
    size_t nPassMuPt = nEvents - count(cutFlowCollection.begin(), cutFlowCollection.end(), 0);
    size_t nPassMuTight = nPassMuPt - count(cutFlowCollection.begin(), cutFlowCollection.end(), 1);
    size_t nPassMuEta = nPassMuTight - count(cutFlowCollection.begin(), cutFlowCollection.end(), 2);
    size_t nPassMuIso = nPassMuEta - count(cutFlowCollection.begin(), cutFlowCollection.end(), 3);
    size_t nPassZM = nPassMuIso - count(cutFlowCollection.begin(), cutFlowCollection.end(), 4);
    size_t nPassJetPt = nPassZM - count(cutFlowCollection.begin(), cutFlowCollection.end(), 5);
    size_t nPassbTag = nPassJetPt - count(cutFlowCollection.begin(), cutFlowCollection.end(), 6);
    size_t nPassJetID = nPassbTag - count(cutFlowCollection.begin(), cutFlowCollection.end(), 7);
    size_t nPassHiggsM = nPassJetID - count(cutFlowCollection.begin(), cutFlowCollection.end(), 8);
    ofstream cutFlowOut(fileName.Data());
    cutFlowOut << "Name\tPass\tAll\tEff.(%)\tCumulative Eff.(%)" << endl;
    cutFlowOut << "Muon Pt" << "\t" << nPassMuPt << "\t" << nEvents << "\t" << (float) nPassMuPt / nEvents * 100 << "\t" << (float) nPassMuPt / nEvents * 100 << endl;
    cutFlowOut << "Tight Muon" << "\t" << nPassMuTight << "\t" << nPassMuPt << "\t" << (float) nPassMuTight / nPassMuPt * 100 << "\t" << (float) nPassMuTight / nEvents * 100 << endl;
    cutFlowOut << "Muon Eta" << "\t" << nPassMuEta << "\t" << nPassMuTight << "\t" << (float) nPassMuEta / nPassMuTight * 100 << "\t" << (float) nPassMuEta / nEvents * 100 << endl;
    cutFlowOut << "Muon Iso" << "\t" << nPassMuIso << "\t" << nPassMuEta << "\t" << (float) nPassMuIso / nPassMuEta * 100 << "\t" << (float) nPassMuIso / nEvents * 100 << endl;
    cutFlowOut << "Z Mass" << "\t" << nPassZM << "\t" << nPassMuIso << "\t" << (float) nPassZM / nPassMuIso * 100 << "\t" << (float) nPassZM / nEvents * 100 << endl;
    cutFlowOut << "Jet Pt" << "\t" << nPassJetPt << "\t" << nPassZM << "\t" << (float) nPassJetPt / nPassZM * 100 << "\t" << (float) nPassJetPt / nEvents * 100 << endl;
    cutFlowOut << "deepCSV" << "\t" << nPassbTag << "\t" << nPassJetPt << "\t" << (float) nPassbTag / nPassJetPt * 100 << "\t" << (float) nPassbTag / nEvents * 100 << endl;
    cutFlowOut << "Jet ID" << "\t" << nPassJetID << "\t" << nPassbTag << "\t" << (float) nPassJetID / nPassbTag * 100 << "\t" << (float) nPassJetID / nEvents * 100 << endl;
    cutFlowOut << "Higgs Mass" << "\t" << nPassHiggsM << "\t" << nPassJetID << "\t" << (float) nPassHiggsM / nPassJetID * 100 << "\t" << (float) nPassHiggsM / nEvents * 100;
    cutFlowOut.close();
}

// Count the cutflow of every entry in the TTree. If an entry passed one condition, the counter plus. 
std::vector<int> cutFlowCount(std::vector<std::map<std::string, float>> muonCollection, std::vector<std::map<std::string, float>> jetCollection)
{
    std::vector<int> entryCutScore;
    // Because there are m muon pairs * n jet pairs possibilities for the each entry, we nest the jet loop into the muon loop. 
    for (auto muPair : muonCollection)
        {
            int cutScore = 0;
            if (muPair["mu1Pt"] > 25 && muPair["mu2Pt"] > 15) 
            {
                cutScore++;
                if (muPair["mu1Tight"] == 1 && muPair["mu2Tight"] == 1)
                {
                    cutScore++;
                    if (muPair["mu1Eta"] < 2.4 && muPair["mu2Eta"] < 2.4)
                    {
                        cutScore++;
                        if (muPair["mu1Iso"] < 0.4 && muPair["mu2Iso"] < 0.4)
                        {
                            cutScore++;
                            if (muPair["ZM"] >= 75 && muPair["ZM"] <= 105) cutScore++;
                        }
                    }
                }
            }
            if (cutScore < 5) entryCutScore.push_back(cutScore);
            else if (cutScore == 5)
            {
                for (auto jetPair : jetCollection)
                {
                    if (jetPair["jet1Pt"] > 20 && jetPair["jet2Pt"] > 20) 
                    {
                        cutScore++;
                        if (jetPair["jet1bTag"] > 0.4184 && jetPair["jet2bTag"] > 0.4184)
                        {
                            cutScore++;
                            if (jetPair["jet1ID"] == 1 && jetPair["jet2ID"] == 1)
                            {
                                cutScore++;
                                if (jetPair["HiggsM"] >= 50 && jetPair["HiggsM"] <= 200) cutScore++;
                            }
                        }
                    }
                    entryCutScore.push_back(cutScore);
                    cutScore = 5;
                }
            }
        }
    std::sort(entryCutScore.begin(), entryCutScore.end());
    return entryCutScore;
}

// Check the path is exist. If the path didn't exist, then create the path. 
// Notice: If the parent path of the input path didn't exist, the function is error.
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

void cutTree(TString oldFileName, TString newDirPath, const char *oldTreeName, const char *newTreeName)
{
    using namespace std;
    TFile *fOrigin = new TFile(oldFileName.Data(), "READ");
    cout << "Cut " << oldFileName.Data() << endl;
    TTreeReader myCutReader(oldTreeName, fOrigin);
    TTreeReaderValue<vector<int>> mu1Charge = {myCutReader, "mu1Charge"};
    TTreeReaderValue<vector<float>> mu1Pt = {myCutReader, "mu1Pt"};
    TTreeReaderValue<vector<float>> mu1Eta = {myCutReader, "mu1Eta"};
    TTreeReaderValue<vector<float>> mu1Phi = {myCutReader, "mu1Phi"};
    TTreeReaderValue<vector<float>> mu1M = {myCutReader, "mu1M"};
    TTreeReaderValue<vector<float>> mu1Iso = {myCutReader, "mu1Iso"};
    TTreeReaderValue<vector<bool>> mu1Global = {myCutReader, "mu1Global"};
    TTreeReaderValue<vector<bool>> mu1Tight = {myCutReader, "mu1Tight"};
    TTreeReaderValue<vector<int>> mu2Charge = {myCutReader, "mu2Charge"};
    TTreeReaderValue<vector<float>> mu2Pt = {myCutReader, "mu2Pt"};
    TTreeReaderValue<vector<float>> mu2Eta = {myCutReader, "mu2Eta"};
    TTreeReaderValue<vector<float>> mu2Phi = {myCutReader, "mu2Phi"};
    TTreeReaderValue<vector<float>> mu2M = {myCutReader, "mu2M"};
    TTreeReaderValue<vector<float>> mu2Iso = {myCutReader, "mu2Iso"};
    TTreeReaderValue<vector<bool>> mu2Global = {myCutReader, "mu2Global"};
    TTreeReaderValue<vector<bool>> mu2Tight = {myCutReader, "mu2Tight"};
    TTreeReaderValue<vector<float>> ZPt = {myCutReader, "ZPt"};
    TTreeReaderValue<vector<float>> ZEta = {myCutReader, "ZEta"};
    TTreeReaderValue<vector<float>> ZPhi = {myCutReader, "ZPhi"};
    TTreeReaderValue<vector<float>> ZM = {myCutReader, "ZM"};
    TTreeReaderValue<vector<float>> jet1Pt = {myCutReader, "jet1Pt"};
    TTreeReaderValue<vector<float>> jet1Eta = {myCutReader, "jet1Eta"};
    TTreeReaderValue<vector<float>> jet1Phi = {myCutReader, "jet1Phi"};
    TTreeReaderValue<vector<float>> jet1M = {myCutReader, "jet1M"};
    TTreeReaderValue<vector<bool>> jet1ID = {myCutReader, "jet1ID"};
    TTreeReaderValue<vector<float>> jet1bTag = {myCutReader, "jet1bTag"};
    TTreeReaderValue<vector<float>> jet2Pt = {myCutReader, "jet2Pt"};
    TTreeReaderValue<vector<float>> jet2Eta = {myCutReader, "jet2Eta"};
    TTreeReaderValue<vector<float>> jet2Phi = {myCutReader, "jet2Phi"};
    TTreeReaderValue<vector<float>> jet2M = {myCutReader, "jet2M"};
    TTreeReaderValue<vector<bool>> jet2ID = {myCutReader, "jet2ID"};
    TTreeReaderValue<vector<float>> jet2bTag = {myCutReader, "jet2bTag"};
    TTreeReaderValue<vector<float>> HiggsPt = {myCutReader, "HiggsPt"};
    TTreeReaderValue<vector<float>> HiggsEta = {myCutReader, "HiggsEta"};
    TTreeReaderValue<vector<float>> HiggsPhi = {myCutReader, "HiggsPhi"};
    TTreeReaderValue<vector<float>> HiggsM = {myCutReader, "HiggsM"};
    
    TString rootFileName = returnPathOrFileName(oldFileName, "file");
    TFile *fCut = new TFile((newDirPath + rootFileName).Data(), "RECREATE");
    TTree *cutZHTree = new TTree(newTreeName, newTreeName);
    TString cutFlowFileName = newDirPath + "/CutFlow/" + rootFileName.Remove(rootFileName.First('.'), rootFileName.Length() - rootFileName.First('.')) + ".txt";

    int mu1Charge_, mu2Charge_;
    float mu1Pt_, mu1Eta_, mu1Phi_, mu1M_, mu1Iso_, mu2Pt_, mu2Eta_, mu2Phi_, mu2M_, mu2Iso_;
    float jet1Pt_, jet1Eta_, jet1Phi_, jet1M_, jet1bTag_, jet2Pt_, jet2Eta_, jet2Phi_, jet2M_, jet2bTag_;
    float ZPt_, ZPhi_, ZEta_, ZM_, HiggsPt_, HiggsEta_, HiggsPhi_, HiggsM_;
    bool mu1Global_, mu1Tight_, mu2Global_, mu2Tight_, jet1ID_, jet2ID_;
    cutZHTree->SetAutoSave(0);
    cutZHTree->Branch("mu1Charge", &mu1Charge_, "mu1Charge/I");
    cutZHTree->Branch("mu1Pt", &mu1Pt_);
    cutZHTree->Branch("mu1Eta", &mu1Eta_);
    cutZHTree->Branch("mu1Phi", &mu1Phi_);
    cutZHTree->Branch("mu1M", &mu1M_);
    cutZHTree->Branch("mu1Iso", &mu1Iso_);
    cutZHTree->Branch("mu1Global", &mu1Global_, "mu1Global/O");
    cutZHTree->Branch("mu1Tight", &mu1Tight_, "mu1Tight/O");

    cutZHTree->Branch("mu2Charge", &mu2Charge_, "mu2Charge/I");
    cutZHTree->Branch("mu2Pt", &mu2Pt_);
    cutZHTree->Branch("mu2Eta", &mu2Eta_);
    cutZHTree->Branch("mu2Phi", &mu2Phi_);
    cutZHTree->Branch("mu2M", &mu2M_);
    cutZHTree->Branch("mu2Iso", &mu2Iso_);
    cutZHTree->Branch("mu2Global", &mu2Global_, "mu2Global/O");
    cutZHTree->Branch("mu2Tight", &mu2Tight_, "mu2Tight/O");

    cutZHTree->Branch("ZPt", &ZPt_);
    cutZHTree->Branch("ZEta", &ZEta_);
    cutZHTree->Branch("ZPhi", &ZPhi_);
    cutZHTree->Branch("ZM", &ZM_);

    cutZHTree->Branch("jet1Pt", &jet1Pt_);
    cutZHTree->Branch("jet1Eta", &jet1Eta_);
    cutZHTree->Branch("jet1Phi", &jet1Phi_);
    cutZHTree->Branch("jet1M", &jet1M_);
    cutZHTree->Branch("jet1bTag", &jet1bTag_);
    cutZHTree->Branch("jet1ID", &jet1ID_, "jet1ID/O");

    cutZHTree->Branch("jet2Pt", &jet2Pt_);
    cutZHTree->Branch("jet2Eta", &jet2Eta_);
    cutZHTree->Branch("jet2Phi", &jet2Phi_);
    cutZHTree->Branch("jet2M", &jet2M_);
    cutZHTree->Branch("jet2bTag", &jet2bTag_);
    cutZHTree->Branch("jet2ID", &jet2ID_, "jet2ID/O");

    cutZHTree->Branch("HiggsPt", &HiggsPt_);
    cutZHTree->Branch("HiggsEta", &HiggsEta_);
    cutZHTree->Branch("HiggsPhi", &HiggsPhi_);
    cutZHTree->Branch("HiggsM", &HiggsM_);

    vector<int> cutFlowCollection;

    while (myCutReader.Next())
    {
        map<string, float> eachMuPair, eachJetPair;
        vector<map<string, float>> oldMuPair, cutMuPair;
        vector<map<string, float>> oldJetPair, cutJetPair;
        vector<int> entryCutScore;
        for (size_t i = 0; i < mu1Pt->size(); i++)
        {
            eachMuPair["mu1Charge"] = mu1Charge->at(i);
            eachMuPair["mu1Pt"] = mu1Pt->at(i);
            eachMuPair["mu1Eta"] = mu1Eta->at(i);
            eachMuPair["mu1Phi"] = mu1Phi->at(i);
            eachMuPair["mu1M"] = mu1M->at(i);
            eachMuPair["mu1Tight"] = mu1Tight->at(i);
            eachMuPair["mu1Global"] = mu1Global->at(i);
            eachMuPair["mu1Charge"] = mu1Charge->at(i);
            eachMuPair["mu2Pt"] = mu2Pt->at(i);
            eachMuPair["mu2Eta"] = mu2Eta->at(i);
            eachMuPair["mu2Phi"] = mu2Phi->at(i);
            eachMuPair["mu2M"] = mu2M->at(i);
            eachMuPair["mu2Tight"] = mu2Tight->at(i);
            eachMuPair["mu2Global"] = mu2Global->at(i);
            eachMuPair["ZPt"] = ZPt->at(i);
            eachMuPair["ZEta"] = ZEta->at(i);
            eachMuPair["ZPhi"] = ZPhi->at(i);
            eachMuPair["ZM"] = ZM->at(i);
            oldMuPair.push_back(eachMuPair);
        }
        for (size_t i = 0; i < jet1Pt->size(); i++)
        {
            eachJetPair["jet1Pt"] = jet1Pt->at(i);
            eachJetPair["jet1Eta"] = jet1Eta->at(i);
            eachJetPair["jet1Phi"] = jet1Phi->at(i);
            eachJetPair["jet1M"] = jet1M->at(i);
            eachJetPair["jet1bTag"] = jet1bTag->at(i);
            eachJetPair["jet1ID"] = jet1ID->at(i);
            eachJetPair["jet2Pt"] = jet2Pt->at(i);
            eachJetPair["jet2Eta"] = jet2Eta->at(i);
            eachJetPair["jet2Phi"] = jet2Phi->at(i);
            eachJetPair["jet2M"] = jet2M->at(i);
            eachJetPair["jet2bTag"] = jet2bTag->at(i);
            eachJetPair["jet2ID"] = jet2ID->at(i);
            eachJetPair["HiggsPt"] = HiggsPt->at(i);
            eachJetPair["HiggsEta"] = HiggsEta->at(i);
            eachJetPair["HiggsPhi"] = HiggsPhi->at(i);
            eachJetPair["HiggsM"] = HiggsM->at(i);
            oldJetPair.push_back(eachJetPair);
        }
        for (auto muPair : oldMuPair)
        {
            if (!(muPair["mu1Pt"] > 25 && muPair["mu2Pt"] > 15)) continue;
            if (!(muPair["mu1Tight"] == 1 && muPair["mu2Tight"] == 1)) continue;
            if (!(muPair["mu1Eta"] < 2.4 && muPair["mu2Eta"] < 2.4)) continue;
            if (!(muPair["mu1Iso"] < 0.4 && muPair["mu2Iso"] < 0.4)) continue;
            if (!(muPair["ZM"] >= 75 && muPair["ZM"] <= 105)) continue;
            cutMuPair.push_back(muPair);
        }
        for (auto jetPair : oldJetPair)
        {
            if (!(jetPair["jet1Pt"] > 20 && jetPair["jet2Pt"] > 20)) continue;
            if (!(jetPair["jet1bTag"] > 0.4184 && jetPair["jet2bTag"] > 0.4184)) continue;
            if (!(jetPair["jet1ID"] == 1 && jetPair["jet2ID"] == 1)) continue;
            if (!(jetPair["HiggsM"] >= 50 && jetPair["HiggsM"] <= 200)) continue;
            cutJetPair.push_back(jetPair);
        }
        if (cutMuPair.size() > 0 && cutJetPair.size() > 0)
        {
            mu1Charge_ = (int)cutMuPair[0]["mu1Charge"];
            mu2Charge_ = (int)cutMuPair[0]["mu2Charge"];

            mu1Pt_ = cutMuPair[0]["mu1Pt"];
            mu1Eta_ = cutMuPair[0]["mu1Eta"];
            mu1Phi_ = cutMuPair[0]["mu1Phi"];
            mu1M_ = cutMuPair[0]["mu1M"];
            mu1Iso_ = cutMuPair[0]["mu1Iso"];

            mu2Pt_ = cutMuPair[0]["mu2Pt"];
            mu2Eta_ = cutMuPair[0]["mu2Eta"];
            mu2Phi_ = cutMuPair[0]["mu2Phi"];
            mu2M_ = cutMuPair[0]["mu2M"];
            mu2Iso_ = cutMuPair[0]["mu1Iso"];

            jet1Pt_ = cutJetPair[0]["jet1Pt"];
            jet1Eta_ = cutJetPair[0]["jet1Eta"];
            jet1Phi_ = cutJetPair[0]["jet1Phi"];
            jet1M_ = cutJetPair[0]["jet1M"];
            jet1bTag_ = cutJetPair[0]["jet1bTag"];

            jet2Pt_ = cutJetPair[0]["jet2Pt"];
            jet2Eta_ = cutJetPair[0]["jet2Eta"];
            jet2Phi_ = cutJetPair[0]["jet2Phi"];
            jet2M_ = cutJetPair[0]["jet2M"];
            jet2bTag_ = cutJetPair[0]["jet1bTag"];

            ZPt_ = cutMuPair[0]["ZPt"];
            ZEta_ = cutMuPair[0]["ZEta"];
            ZPhi_ = cutMuPair[0]["ZPhi"];
            ZM_ = cutMuPair[0]["ZM"];

            HiggsPt_ = cutJetPair[0]["HiggsPt"];
            HiggsEta_ = cutJetPair[0]["HiggsEta"];
            HiggsPhi_ = cutJetPair[0]["HiggsPhi"];
            HiggsM_ = cutJetPair[0]["HiggsM"];

            mu1Global_ = (bool)cutMuPair[0]["mu1Global"];
            mu1Tight_ = (bool)cutMuPair[0]["mu1Tight"];
            mu2Global_ = (bool)cutMuPair[0]["mu2Global"];
            mu2Tight_ = (bool)cutMuPair[0]["mu2Tight"];
            jet1ID_ = (bool)cutJetPair[0]["jet1ID"];
            jet2ID_ = (bool)cutJetPair[0]["jet2ID"];
            cutZHTree->Fill();
        }

        entryCutScore = cutFlowCount(oldMuPair, oldJetPair); // count cutflow of each event
        cutFlowCollection.push_back(entryCutScore.back()); // push the result to the set of cutflow
        oldMuPair.clear();
        oldJetPair.clear();
        cutMuPair.clear();
        cutJetPair.clear();
        eachMuPair.clear();
        eachJetPair.clear();
    }
    cout << "Calculate the cut flow of " << oldFileName << endl;
    cutFlowCalc(cutFlowFileName, cutFlowCollection);
    cutZHTree->Write();
    fCut->Close();
    fOrigin->Close();
}


// main function
int ntupleReducer(TString fileName, TString savePath)
{
    //ROOT::IsImplicitMTEnabled(); // open multi-process (For HTCondor, comment it!)
    auto oldTreeName = "demo/ZHCollection"; // keep same with the name of TTree in the source
    auto newTreeName = "ZHCandidates";

    // create the workspace
    TString oldDirName = "Samples";
    TString oldPathName = returnPathOrFileName(fileName, "path");
    TString flatPathName = savePath + "/FlatTrees";
    TString cutFlowPathName = savePath + "/CutFlow";
    checkPath(savePath);
    checkPath(cutFlowPathName);
    TString flatFileName = flatPathName + returnPathOrFileName(fileName, "file");
    cutTree(fileName, savePath, oldTreeName, newTreeName);
    return 0;
}