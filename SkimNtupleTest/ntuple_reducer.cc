#include <vector>
#include <fstream>
#include "ROOT/RDataFrame.hxx"
#include "TTree.h"
#include "TFile.h"
#include "TString.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TSystemDirectory.h"
#include "TList.h"
#include "TIterator.h"

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

void makeFlatTree(TString oldDirName, TString oldDirPath, TString newDirPath, const char *oldTreeName, const char *newTreeName)
{
    using namespace std;
    vector<TString> originFileList = listFiles(oldDirName, oldDirPath);
    for (auto originFile = originFileList.cbegin(); originFile != originFileList.cend(); originFile++)
    {
        TFile *fOrigin = new TFile(originFile->Data(), "READ");
        cout << "Make " << originFile->Data() << " to flat TTree." << endl;
        TString originFileNameCopy = originFile->Copy();
        TTreeReader myReader(oldTreeName, fOrigin);
        TTreeReaderValue<vector<float>> mu1Charge = {myReader, "mu1Charge"};
        TTreeReaderValue<vector<float>> mu1Pt = {myReader, "mu1Pt"};
        TTreeReaderValue<vector<float>> mu1Eta = {myReader, "mu1Eta"};
        TTreeReaderValue<vector<float>> mu1Phi = {myReader, "mu1Phi"};
        TTreeReaderValue<vector<float>> mu1M = {myReader, "mu1M"};
        TTreeReaderValue<vector<float>> mu1Iso = {myReader, "mu1Iso"};
        TTreeReaderValue<vector<bool>> mu1Global = {myReader, "mu1Global"};
        TTreeReaderValue<vector<bool>> mu1Tight = {myReader, "mu1Tight"};
        TTreeReaderValue<vector<float>> mu2Charge = {myReader, "mu2Charge"};
        TTreeReaderValue<vector<float>> mu2Pt = {myReader, "mu2Pt"};
        TTreeReaderValue<vector<float>> mu2Eta = {myReader, "mu2Eta"};
        TTreeReaderValue<vector<float>> mu2Phi = {myReader, "mu2Phi"};
        TTreeReaderValue<vector<float>> mu2M = {myReader, "mu2M"};
        TTreeReaderValue<vector<float>> mu2Iso = {myReader, "mu2Iso"};
        TTreeReaderValue<vector<bool>> mu2Global = {myReader, "mu2Global"};
        TTreeReaderValue<vector<bool>> mu2Tight = {myReader, "mu2Tight"};
        TTreeReaderValue<vector<float>> ZPt = {myReader, "ZPt"};
        TTreeReaderValue<vector<float>> ZEta = {myReader, "ZEta"};
        TTreeReaderValue<vector<float>> ZPhi = {myReader, "ZPhi"};
        TTreeReaderValue<vector<float>> ZM = {myReader, "ZM"};
        TTreeReaderValue<vector<float>> jet1Pt = {myReader, "jet1Pt"};
        TTreeReaderValue<vector<float>> jet1Eta = {myReader, "jet1Eta"};
        TTreeReaderValue<vector<float>> jet1Phi = {myReader, "jet1Phi"};
        TTreeReaderValue<vector<float>> jet1M = {myReader, "jet1M"};
        TTreeReaderValue<vector<bool>> jet1ID = {myReader, "jet1ID"};
        TTreeReaderValue<vector<float>> jet1bTag = {myReader, "jet1bTag"};
        TTreeReaderValue<vector<float>> jet2Pt = {myReader, "jet2Pt"};
        TTreeReaderValue<vector<float>> jet2Eta = {myReader, "jet2Eta"};
        TTreeReaderValue<vector<float>> jet2Phi = {myReader, "jet2Phi"};
        TTreeReaderValue<vector<float>> jet2M = {myReader, "jet2M"};
        TTreeReaderValue<vector<bool>> jet2ID = {myReader, "jet2ID"};
        TTreeReaderValue<vector<float>> jet2bTag = {myReader, "jet2bTag"};
        TTreeReaderValue<vector<float>> HiggsPt = {myReader, "HiggsPt"};
        TTreeReaderValue<vector<float>> HiggsEta = {myReader, "HiggsEta"};
        TTreeReaderValue<vector<float>> HiggsPhi = {myReader, "HiggsPhi"};
        TTreeReaderValue<vector<float>> HiggsM = {myReader, "HiggsM"};

        float mu1Charge_, mu1Pt_, mu1Eta_, mu1Phi_, mu1M_, mu1Iso_, mu2Charge_, mu2Pt_, mu2Eta_, mu2Phi_, mu2M_, mu2Iso_;
        float jet1Pt_, jet1Eta_, jet1Phi_, jet1M_, jet1bTag_, jet2Pt_, jet2Eta_, jet2Phi_, jet2M_, jet2bTag_;
        float ZPt_, ZPhi_, ZEta_, ZM_, HiggsPt_, HiggsEta_, HiggsPhi_, HiggsM_;
        bool mu1Global_, mu1Tight_, mu2Global_, mu2Tight_, jet1ID_, jet2ID_;

        vector<TTreeReaderValue<vector<float>>> floatVectors = {mu1Charge, mu1Pt, mu1Eta, mu1Phi, mu1M, mu1Iso, mu2Charge, mu2Pt, mu2Eta, mu2Phi, mu2M, mu2Iso,
                                                                jet1Pt, jet1Eta, jet1Phi, jet1M, jet1bTag, jet2Pt, jet2Eta, jet2Phi, jet2M, jet2bTag,
                                                                ZPt, ZEta, ZPhi, ZM, HiggsPt, HiggsEta, HiggsPhi, HiggsM};
        vector<TTreeReaderValue<vector<bool>>> boolVectors = {mu1Global, mu1Tight, mu2Global, mu2Tight, jet1ID, jet2ID};
        vector<float> floatNumbers = {mu1Charge_, mu1Pt_, mu1Eta_, mu1Phi_, mu1M_, mu1Iso_, mu2Charge_, mu2Pt_, mu2Eta_, mu2Phi_, mu2M_, mu2Iso_,
                                      jet1Pt_, jet1Eta_, jet1Phi_, jet1M_, jet1bTag_, jet2Pt_, jet2Eta_, jet2Phi_, jet2M_, jet2bTag_,
                                      ZPt_, ZEta_, ZPhi_, ZM_, HiggsPt_, HiggsEta_, HiggsPhi_, HiggsM_};
        vector<bool> boolNumbers = {mu1Global_, mu1Tight_, mu2Global_, mu2Tight_, jet1ID_, jet2ID_};
        TFile fFlat = TFile((newDirPath + originFileNameCopy.Remove(0, oldDirPath.Length())).Data(), "RECREATE");
        TTree *flatZHTree = new TTree(newTreeName, newTreeName);

        const int muNumFloat = 6;
        const int jetNumFloat = 5;
        flatZHTree->SetAutoSave(0);
        flatZHTree->Branch("mu1Charge", &mu1Charge_);
        flatZHTree->Branch("mu1Pt", &mu1Pt_);
        flatZHTree->Branch("mu1Eta", &mu1Eta_);
        flatZHTree->Branch("mu1Phi", &mu1Phi_);
        flatZHTree->Branch("mu1M", &mu1M_);
        flatZHTree->Branch("mu1Iso", &mu1Iso_);
        flatZHTree->Branch("mu1Global", &mu1Global_, "mu1Global/O");
        flatZHTree->Branch("mu1Tight", &mu1Tight_, "mu1Tight/O");

        flatZHTree->Branch("mu2Charge", &mu2Charge_);
        flatZHTree->Branch("mu2Pt", &mu2Pt_);
        flatZHTree->Branch("mu2Eta", &mu2Eta_);
        flatZHTree->Branch("mu2Phi", &mu2Phi_);
        flatZHTree->Branch("mu2M", &mu2M_);
        flatZHTree->Branch("mu2Iso", &mu2Iso_);
        flatZHTree->Branch("mu2Global", &mu2Global_, "mu2Global/O");
        flatZHTree->Branch("mu2Tight", &mu2Tight_, "mu2Tight/O");

        flatZHTree->Branch("ZPt", &ZPt_);
        flatZHTree->Branch("ZEta", &ZEta_);
        flatZHTree->Branch("ZPhi", &ZPhi_);
        flatZHTree->Branch("ZM", &ZM_);

        flatZHTree->Branch("jet1Pt", &jet1Pt_);
        flatZHTree->Branch("jet1Eta", &jet1Eta_);
        flatZHTree->Branch("jet1Phi", &jet1Phi_);
        flatZHTree->Branch("jet1M", &jet1M_);
        flatZHTree->Branch("jet1bTag", &jet1bTag_);
        flatZHTree->Branch("jet1ID", &jet1ID_, "jet1ID/O");

        flatZHTree->Branch("jet2Pt", &jet2Pt_);
        flatZHTree->Branch("jet2Eta", &jet2Eta_);
        flatZHTree->Branch("jet2Phi", &jet2Phi_);
        flatZHTree->Branch("jet2M", &jet2M_);
        flatZHTree->Branch("jet2bTag", &jet2bTag_);
        flatZHTree->Branch("jet2ID", &jet2ID_, "jet2ID/O");

        flatZHTree->Branch("HiggsPt", &HiggsPt_);
        flatZHTree->Branch("HiggsEta", &HiggsEta_);
        flatZHTree->Branch("HiggsPhi", &HiggsPhi_);
        flatZHTree->Branch("HiggsM", &HiggsM_);

        while (myReader.Next())
        {
            for (size_t i = 0; i < floatNumbers.size(); i++)
                floatNumbers[i] = floatVectors[i]->at(0);
            for (size_t i = 0; i < boolNumbers.size(); i++)
                boolNumbers[i] = boolVectors[i]->at(0);
            mu1Charge_ = floatNumbers[0];
            mu1Pt_ = floatNumbers[1];
            mu1Eta_ = floatNumbers[2];
            mu1Phi_ = floatNumbers[3];
            mu1M_ = floatNumbers[4];
            mu1Iso_ = floatNumbers[5];

            mu2Charge_ = floatNumbers[0 + muNumFloat];
            mu2Pt_ = floatNumbers[1 + muNumFloat];
            mu2Eta_ = floatNumbers[2 + muNumFloat];
            mu2Phi_ = floatNumbers[3 + muNumFloat];
            mu2M_ = floatNumbers[4 + muNumFloat];
            mu2Iso_ = floatNumbers[5 + muNumFloat];

            jet1Pt_ = floatNumbers[0 + 2 * muNumFloat];
            jet1Eta_ = floatNumbers[1 + 2 * muNumFloat];
            jet1Phi_ = floatNumbers[2 + 2 * muNumFloat];
            jet1M_ = floatNumbers[3 + 2 * muNumFloat];
            jet1bTag_ = floatNumbers[4 + 2 * muNumFloat];

            jet2Pt_ = floatNumbers[0 + 2 * muNumFloat + jetNumFloat];
            jet2Eta_ = floatNumbers[1 + 2 * muNumFloat + jetNumFloat];
            jet2Phi_ = floatNumbers[2 + 2 * muNumFloat + jetNumFloat];
            jet2M_ = floatNumbers[3 + 2 * muNumFloat + jetNumFloat];
            jet2bTag_ = floatNumbers[4 + 2 * muNumFloat + jetNumFloat];

            ZPt_ = floatNumbers[0 + 2 * muNumFloat + 2 * jetNumFloat];
            ZEta_ = floatNumbers[1 + 2 * muNumFloat + 2 * jetNumFloat];
            ZPhi_ = floatNumbers[2 + 2 * muNumFloat + 2 * jetNumFloat];
            ZM_ = floatNumbers[3 + 2 * muNumFloat + 2 * jetNumFloat];

            HiggsPt_ = floatNumbers[4 + 2 * muNumFloat + 2 * jetNumFloat];
            HiggsEta_ = floatNumbers[5 + 2 * muNumFloat + 2 * jetNumFloat];
            HiggsPhi_ = floatNumbers[6 + 2 * muNumFloat + 2 * jetNumFloat];
            HiggsM_ = floatNumbers[7 + 2 * muNumFloat + 2 * jetNumFloat];

            mu1Global_ = boolNumbers[0];
            mu1Tight_ = boolNumbers[1];
            mu2Global_ = boolNumbers[2];
            mu2Tight_ = boolNumbers[3];
            jet1ID_ = boolNumbers[4];
            jet2ID_ = boolNumbers[5];

            flatZHTree->Fill();
        }
        flatZHTree->Write();
        fFlat.Close();
        fOrigin->Close();
    }
}

void cutFlowCalc(TString fileName, TString pathName, ROOT::RDF::RResultPtr<ROOT::RDF::RCutFlowReport> dCutFlow)
{
    dCutFlow->Print();
    TString cutFlowFileName = fileName.Copy();
    cutFlowFileName.Remove(cutFlowFileName.Length() - 5, cutFlowFileName.Length());
    std::ofstream cutFlowOut((pathName + cutFlowFileName + ".txt").Data());
    cutFlowOut << "Name\tAll\tPass\tEfficiency\tCumulative Eff" << std::endl;
    std::vector<ULong64_t> cutFlowAllVec;
    for (auto cutInfo : dCutFlow)
    {
        cutFlowAllVec.push_back(cutInfo.GetAll());
        cutFlowOut << cutInfo.GetName() << "\t" << cutInfo.GetAll() << "\t" << cutInfo.GetPass() << "\t"
                   << cutInfo.GetEff() << " %"
                   << "\t" << (float)cutInfo.GetPass() / (float)cutFlowAllVec[0] * 100 << " %" << std::endl;
    }
    cutFlowOut.close();
}

int ntuple_reducer()
{
    ROOT::IsImplicitMTEnabled();
    auto oldTreeName = "demo/ZHCollection"; // need to modify!!!!!!
    auto newTreeName = "ZHCandidates";

    TString oldDirName = "Samples"; // need to modify when you skim TTree
    TString oldPathName = "./Samples";
    TString flatPathName = "./FlatTrees";
    TString skimPathName = "./Skim";
    TString muonCutFlowPathName = "./MuonCutFlow";
    makeFlatTree(oldDirName, oldPathName, flatPathName, oldTreeName, newTreeName);
    std::vector<TString> flatList = listFiles(oldDirName, oldPathName, 1, flatPathName);
    for (auto fileName : flatList)
    {
        ROOT::RDataFrame d(newTreeName, fileName.View());
        std::cout << "Skim " << fileName << std::endl;
        auto branchNames = d.GetColumnNames();
        auto dCutMuon = d.Filter("mu1Pt > 25 && mu2Pt > 15", "Muon pt").Filter("mu1Tight == 1 && mu2Tight == 1", "Tight muon").Filter("mu1Eta < 2.4 && mu2Eta < 2.4", "Muon eta").Filter("mu1Iso < 0.4 && mu2Iso < 0.4", "Muon iso.").Filter("ZM > 75 && ZM < 105", "Z mass");
        /*
        auto dCutJet = d_cut_muon.Filter("jet1Pt > 20 && jet2Pt > 20", "Jet pt").Filter("jet1bTag > 0.4184 && jet2bTag > 0.4814", "deepCSV 2018 medium")
        .Filter("jet1ID == 1 && jet2ID == 1", "Jet ID")
        .Filter("HiggsM >= 90 && HiggsM <= 150", "Higgs mass");
        */
        fileName.Remove(0, flatPathName.Length());
        auto dMuonCutFlow = dCutMuon.Report();
        cutFlowCalc(fileName, muonCutFlowPathName, dMuonCutFlow);
        dCutMuon.Snapshot(TString(newTreeName).View(), (skimPathName + fileName).View(), branchNames);
    }
    return 0;
}