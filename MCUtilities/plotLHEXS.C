#include "TFile.h"
#include "TSystem.h"
#include "TTreeReader.h"
#include "TTreeReaderArray.h"
#include "TH1.h"
#include "TCanvas.h"

#include <iostream>

void plotLHEXS(std::string inPath, double totalXs, std::string libPath="libExRootAnalysis.so")
{
	using namespace std;
	const char *libPathChar = libPath.c_str();
	gSystem->Load(libPathChar);
	std::string mg5Name = inPath.substr(inPath.find_last_of('/') + 1, inPath.find_last_of('.'));
	std::string folderPath = inPath.substr(0, inPath.find_last_of('/'));
	std::string outPath = folderPath + '/' + "mg5XS_" + mg5Name;
	const char *fInPath = inPath.c_str();
	const char *fOutPath = outPath.c_str();
	TFile *f = TFile::Open(fInPath);
	totalXs = totalXs * 1000;
	double nEvents = 10000;
	double lumi = nEvents / totalXs;
    double edge[22] = {0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 350, 400, 500};
	TH1D *mgHiggsM = new TH1D("mgHiggsM", "mgHiggsM", 75, 50, 200);
	TH1D *mgHiggsPt = new TH1D("mgHiggsPt", "mgHiggsPt", 21, edge);
	TTreeReader myReader("LHEF", f);
	TTreeReaderArray<double> particlePt = {myReader, "Particle.PT"};
	TTreeReaderArray<double> particleEta = {myReader, "Particle.Eta"};
	TTreeReaderArray<double> particlePhi = {myReader, "Particle.Phi"};
	TTreeReaderArray<double> particleM = {myReader, "Particle.M"};
	TTreeReaderArray<int> particlePID = {myReader, "Particle.PID"};
	while (myReader.Next())
	{
		int higgsIndex;
		for (size_t i = 0; i < particlePID.GetSize(); i++)
		{
			if (particlePID.At(i) == 25) higgsIndex = i;
		}
		mgHiggsM->Fill(particleM.At(higgsIndex));
		mgHiggsPt->Fill(particlePt.At(higgsIndex));
	}
	TCanvas *c = new TCanvas();
	TFile *fOut = new TFile(fOutPath, "recreate");
	mgHiggsM->GetXaxis()->SetTitle("m_{Higgs} [GeV]");
	mgHiggsM->GetYaxis()->SetTitle("Nevents / 2 GeV");
	mgHiggsM->Draw();
	mgHiggsM->Write();
	c->SaveAs("./mg5_higgs_M.pdf");
	mgHiggsPt->GetXaxis()->SetTitle("p_{T}^{Higgs} [GeV]");
	mgHiggsPt->GetYaxis()->SetTitle("Nevents");
	mgHiggsPt->Draw();
	mgHiggsPt->Write();
	c->SaveAs("./mg5_higgs_Pt.pdf");
	TH1D *higgsXSPt = (TH1D*) mgHiggsPt->Clone();
	higgsXSPt->SetName("mg5HiggsXSPt");
	higgsXSPt->SetTitle("mg5HiggsXSPt");
	for (int i = 1; i < higgsXSPt->GetNbinsX() + 1; i++)
	{
		double oldBinError = higgsXSPt->GetBinError(i);
		higgsXSPt->SetBinContent(i, (higgsXSPt->GetBinContent(i) / (lumi * higgsXSPt->GetBinWidth(i))));
		higgsXSPt->SetBinError(i, oldBinError / (lumi * higgsXSPt->GetBinWidth(i)));
	}
	higgsXSPt->GetYaxis()->SetTitle("d#sigma / dp_{T} [fb/GeV]");
	higgsXSPt->Draw();
	std::cout << "Total XS: " << higgsXSPt->Integral("width") << " fb" << std::endl;
	c->SaveAs("./higgs_XSPt.pdf");
    higgsXSPt->Write();
	fOut->Close();
}