#include "TH2.h"
#include "ROOT/RDataFrame.hxx"
#include "TFile.h"
#include "TMath.h"

#include <math.h>
#include <string>
#include <map>
#include <iostream>

void calculateULSF(TH2F* idHist, TH2F* isoHist, std::string datasetPath, std::string outputPath)
{
	auto d = ROOT::RDataFrame("ZHCandidates", datasetPath);
	auto dSF = d.Define("mu1_sf", [&](float muPt, float muEta){
		int idHistAbsEta = idHist->GetXaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetYaxis()->FindBin(muPt);
		int isoHistAbsEta = isoHist->GetXaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetYaxis()->FindBin(muPt);
		float idSF = 1;
		float isoSF = 1;
		if (!(idHistPt > idHist->GetNbinsY() || idHistPt == 0)) idSF = idHist->GetBinContent(idHistAbsEta, idHistPt);
		if (!(isoHistPt > isoHist->GetNbinsY() || isoHistPt == 0)) isoSF = isoHist->GetBinContent(isoHistAbsEta, isoHistPt);
		float finalSF = idSF * isoSF;
		return finalSF;
		}, {"mu1_pt", "mu1_eta"})
		.Define("mu1_sf_err", [&](float muPt, float muEta){
		int idHistAbsEta = idHist->GetXaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetYaxis()->FindBin(muPt);
		int isoHistAbsEta = isoHist->GetXaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetYaxis()->FindBin(muPt);
		float idSFSystErr = 0;
		float isoSFSystErr = 0;
		float idSF = 1;
		float isoSF = 1;
		if (!(idHistPt > idHist->GetNbinsY() || idHistPt == 0)) 
		{
			idSFSystErr = idHist->GetBinError(idHistAbsEta, idHistPt);
			idSF = idHist->GetBinContent(idHistAbsEta, idHistPt);
		}
		if (!(isoHistPt > isoHist->GetNbinsY() || isoHistPt == 0)) 
		{
			isoSFSystErr = isoHist->GetBinError(isoHistAbsEta, isoHistPt);
			isoSF = isoHist->GetBinContent(isoHistAbsEta, isoHistPt);
		}
		float finalSFSystErr = std::sqrt(isoSF * isoSF * idSFSystErr * idSFSystErr + idSF * idSF * isoSFSystErr * isoSFSystErr);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta"})
		.Define("mu2_sf", [&](float muPt, float muEta){
		int idHistAbsEta = idHist->GetXaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetYaxis()->FindBin(muPt);
		int isoHistAbsEta = isoHist->GetXaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetYaxis()->FindBin(muPt);
		float idSF;
		float isoSF;
		if (idHistPt > idHist->GetNbinsY() || idHistPt == 0) idSF = 1;
		else idSF = idHist->GetBinContent(idHistAbsEta, idHistPt);
		if (isoHistPt > isoHist->GetNbinsY() || isoHistPt == 0) isoSF = 1;
		else isoSF = isoHist->GetBinContent(isoHistAbsEta, isoHistPt);
		float finalSF = idSF * isoSF;
		return finalSF;
		}, {"mu2_pt", "mu2_eta"})
		.Define("mu2_sf_err", [&](float muPt, float muEta){
		int idHistAbsEta = idHist->GetXaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetYaxis()->FindBin(muPt);
		int isoHistAbsEta = isoHist->GetXaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetYaxis()->FindBin(muPt);
		float idSFSystErr = 0;
		float isoSFSystErr = 0;
		float idSF = 1;
		float isoSF = 1;
		if (!(idHistPt > idHist->GetNbinsY() || idHistPt == 0)) 
		{
			idSFSystErr = idHist->GetBinError(idHistAbsEta, idHistPt);
			idSF = idHist->GetBinContent(idHistAbsEta, idHistPt);
		}
		if (!(isoHistPt > isoHist->GetNbinsY() || isoHistPt == 0)) 
		{
			isoSFSystErr = isoHist->GetBinError(isoHistAbsEta, isoHistPt);
			isoSF = isoHist->GetBinContent(isoHistAbsEta, isoHistPt);
		}
		float finalSFSystErr = std::sqrt(isoSF * isoSF * idSFSystErr * idSFSystErr + idSF * idSF * isoSFSystErr * isoSFSystErr);
		return finalSFSystErr;
		}, {"mu2_pt", "mu2_eta"})
		.Define("z_sf", "mu1_sf * mu2_sf").Define("z_sf_err", "TMath::Sqrt(mu2_sf * mu2_sf * mu1_sf_err * mu1_sf_err + mu1_sf * mu1_sf * mu2_sf_err * mu2_sf_err)")
		.Define("z_sf_up", "z_sf + z_sf_err").Define("z_sf_down", "z_sf - z_sf_err");
	dSF.Snapshot("ZHCandidates", outputPath, dSF.GetColumnNames());
}

void calculateReReco1718SF(TH2F* idHist, TH2F* isoHist, std::string datasetPath, std::string outputPath)
{
	auto d = ROOT::RDataFrame("ZHCandidates", datasetPath);
	auto dSF = d.Define("mu1_sf", [&](float muPt, float muEta){
		int idHistAbsEta = idHist->GetYaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetXaxis()->FindBin(muPt);
		int isoHistAbsEta = isoHist->GetYaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetXaxis()->FindBin(muPt);
		float idSF = 1;
		float isoSF = 1;
		if (!(idHistPt > idHist->GetNbinsX() || idHistPt == 0)) idSF = idHist->GetBinContent(idHistPt, idHistAbsEta);
		if (!(isoHistPt > isoHist->GetNbinsX() || isoHistPt == 0)) isoSF = isoHist->GetBinContent(isoHistPt, isoHistAbsEta);
		float finalSF = idSF * isoSF;
		return finalSF;
		}, {"mu1_pt", "mu1_eta"})
		.Define("mu1_sf_err", [&](float muPt, float muEta){
		int idHistAbsEta = idHist->GetYaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetXaxis()->FindBin(muPt);
		int isoHistAbsEta = isoHist->GetYaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetXaxis()->FindBin(muPt);
		float idSF = 1;
		float idSFSystErr = 0;
		float isoSF = 1;
		float isoSFSystErr = 0;
		if (!(idHistPt > idHist->GetNbinsX() || idHistPt == 0)) 
		{
			idSF = idHist->GetBinContent(idHistPt, idHistAbsEta);
			idSFSystErr = idHist->GetBinError(idHistPt, idHistAbsEta);
		}
		if (!(isoHistPt > isoHist->GetNbinsX() || isoHistPt == 0)) 
		{
			isoSF = isoHist->GetBinContent(isoHistPt, isoHistAbsEta);
			isoSFSystErr = isoHist->GetBinError(isoHistPt, isoHistAbsEta);
		}
		float finalSFSystErr = std::sqrt(isoSF * isoSF * idSFSystErr * idSFSystErr + idSF * idSF * isoSFSystErr * isoSFSystErr);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta"})
		.Define("mu2_sf", [&](float muPt, float muEta){
		int idHistAbsEta = idHist->GetYaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetXaxis()->FindBin(muPt);
		int isoHistAbsEta = isoHist->GetYaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetXaxis()->FindBin(muPt);
		float idSF;
		float isoSF;
		if (idHistPt > idHist->GetNbinsX() || idHistPt == 0) idSF = 1;
		else idSF = idHist->GetBinContent(idHistPt, idHistAbsEta);
		if (isoHistPt > isoHist->GetNbinsX() || isoHistPt == 0) isoSF = 1;
		else isoSF = isoHist->GetBinContent(isoHistPt, isoHistAbsEta);
		float finalSF = idSF * isoSF;
		return finalSF;		
		}, {"mu2_pt", "mu2_eta"})
		.Define("mu2_sf_err", [&](float muPt, float muEta){
		int idHistAbsEta = idHist->GetYaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetXaxis()->FindBin(muPt);
		int isoHistAbsEta = isoHist->GetYaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetXaxis()->FindBin(muPt);
		float idSF = 1;
		float idSFSystErr = 0;
		float isoSF = 1;
		float isoSFSystErr = 0;
		if (!(idHistPt > idHist->GetNbinsX() || idHistPt == 0)) 
		{
			idSF = idHist->GetBinContent(idHistPt, idHistAbsEta);
			idSFSystErr = idHist->GetBinError(idHistPt, idHistAbsEta);
		}
		if (!(isoHistPt > isoHist->GetNbinsX() || isoHistPt == 0)) 
		{
			isoSF = isoHist->GetBinContent(isoHistPt, isoHistAbsEta);
			isoSFSystErr = isoHist->GetBinError(isoHistPt, isoHistAbsEta);
		}
		float finalSFSystErr = std::sqrt(isoSF * isoSF * idSFSystErr * idSFSystErr + idSF * idSF * isoSFSystErr * isoSFSystErr);
		return finalSFSystErr;
		}, {"mu2_pt", "mu2_eta"})
		.Define("z_sf", "mu1_sf * mu2_sf").Define("z_sf_err", "TMath::Sqrt(mu2_sf * mu2_sf * mu1_sf_err * mu1_sf_err + mu1_sf * mu1_sf * mu2_sf_err * mu2_sf_err)")
		.Define("z_sf_up", "z_sf + z_sf_err").Define("z_sf_down", "z_sf - z_sf_err");
	dSF.Snapshot("ZHCandidates", outputPath, dSF.GetColumnNames());
}

void calculateReReco16SF(TH2F* idHist, TH2F* isoHist, std::string datasetPath, std::string outputPath)
{
	auto d = ROOT::RDataFrame("ZHCandidates", datasetPath);
	auto dSF = d.Define("mu1_sf", [&](float muPt, float muEta){
		int idHistEta = idHist->GetXaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetYaxis()->FindBin(muPt);
		int isoHistEta = isoHist->GetXaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetYaxis()->FindBin(muPt);
		float idSF = 1;
		float isoSF = 1;
		if (!(idHistPt > idHist->GetNbinsY() || idHistPt == 0)) idSF = idHist->GetBinContent(idHistEta, idHistPt);
		if (!(isoHistPt > isoHist->GetNbinsY() || isoHistPt == 0)) isoSF = isoHist->GetBinContent(isoHistEta, isoHistPt);
		float finalSF = idSF * isoSF;
		return finalSF;
		}, {"mu1_pt", "mu1_eta"})
		.Define("mu1_sf_err", [&](float muPt, float muEta){
		int idHistEta = idHist->GetXaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetYaxis()->FindBin(muPt);
		int isoHistEta = isoHist->GetXaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetYaxis()->FindBin(muPt);
		float idSF = 1;
		float idSFSystErr = 0;
		float isoSF = 1;
		float isoSFSystErr = 0;
		if (!(idHistPt > idHist->GetNbinsY() || idHistPt == 0)) 
		{
			idSF = idHist->GetBinContent(idHistEta, idHistPt);
			idSFSystErr = idHist->GetBinError(idHistEta, idHistPt);
		}
		if (!(isoHistPt > isoHist->GetNbinsY() || isoHistPt == 0))
		{
			isoSF = isoHist->GetBinContent(isoHistEta, isoHistPt);
			isoSFSystErr = isoHist->GetBinError(isoHistEta, isoHistPt);
		}
		float finalSFSystErr = std::sqrt(isoSF * isoSF * idSFSystErr * idSFSystErr + idSF * idSF * isoSFSystErr * isoSFSystErr);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta"})
		.Define("mu2_sf", [&](float muPt, float muEta){
		int idHistEta = idHist->GetXaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetYaxis()->FindBin(muPt);
		int isoHistEta = isoHist->GetXaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetYaxis()->FindBin(muPt);
		float idSF;
		float isoSF;
		if (idHistPt > idHist->GetNbinsY() || idHistPt == 0) idSF = 1;
		else idSF = idHist->GetBinContent(idHistEta, idHistPt);
		if (isoHistPt > isoHist->GetNbinsY() || isoHistPt == 0) isoSF = 1;
		else isoSF = isoHist->GetBinContent(isoHistEta, isoHistPt);
		float finalSF = idSF * isoSF;
		return finalSF;
		}, {"mu2_pt", "mu2_eta"})
		.Define("mu2_sf_err", [&](float muPt, float muEta){
		int idHistEta = idHist->GetXaxis()->FindBin(std::fabs(muEta));
		int idHistPt = idHist->GetYaxis()->FindBin(muPt);
		int isoHistEta = isoHist->GetXaxis()->FindBin(std::fabs(muEta));
		int isoHistPt = isoHist->GetYaxis()->FindBin(muPt);
		float idSF = 1;
		float idSFSystErr = 0;
		float isoSF = 1;
		float isoSFSystErr = 0;
		if (!(idHistPt > idHist->GetNbinsY() || idHistPt == 0)) 
		{
			idSF = idHist->GetBinContent(idHistEta, idHistPt);
			idSFSystErr = idHist->GetBinError(idHistEta, idHistPt);
		}
		if (!(isoHistPt > isoHist->GetNbinsY() || isoHistPt == 0))
		{
			isoSF = isoHist->GetBinContent(isoHistEta, isoHistPt);
			isoSFSystErr = isoHist->GetBinError(isoHistEta, isoHistPt);
		}
		float finalSFSystErr = std::sqrt(isoSF * isoSF * idSFSystErr * idSFSystErr + idSF * idSF * isoSFSystErr * isoSFSystErr);
		return finalSFSystErr;
		}, {"mu2_pt", "mu2_eta"})
		.Define("z_sf", "mu1_sf * mu2_sf").Define("z_sf_err", "TMath::Sqrt(mu2_sf * mu2_sf * mu1_sf_err * mu1_sf_err + mu1_sf * mu1_sf * mu2_sf_err * mu2_sf_err)")
		.Define("z_sf_up", "z_sf + z_sf_err").Define("z_sf_down", "z_sf - z_sf_err");
	dSF.Snapshot("ZHCandidates", outputPath, dSF.GetColumnNames());
}

void readSF(std::string filePath, std::string sfRootFilePath, std::string sfFolder = ".")
{
	ROOT::EnableImplicitMT();
	
	std::string campaignName = filePath.substr(filePath.find_last_of('_') + 1, filePath.find_last_of('.') - filePath.find_last_of('_') - 1);
	std::cout << "Dataset Campaign: " << campaignName << std::endl;
	std::map <std::string, std::string> sfFileMap = {{"2018UL", "Run2018_UL"}, {"2018ReReco", "Run2018_legacy"}, {"2017UL", "Run2017_UL"}, {"2017ReReco", "Run2017_legacy"}, {"2016UL", "Run2016_UL"}, {"2016ReReco", "Run2016_legacy"}, {"2016APVUL", "Run2016_UL_HIPM"}, {"2016APVReReco", "Run2016_legacy_HIPM"}};
	std::map <std::string, std::string> idHistNameReRecoMap = {{"2018ReReco", "NUM_LooseID_DEN_TrackerMuons_pt_abseta"}, {"2017ReReco", "NUM_LooseID_DEN_genTracks_pt_abseta"}, {"2016ReReco", "NUM_LooseID_DEN_genTracks_eta_pt"}, {"2016APVReReco", "NUM_LooseID_DEN_genTracks_eta_pt"}};
	std::map <std::string, std::string> isoHistNameReRecoMap = {{"2018ReReco", "NUM_LooseRelIso_DEN_LooseID_pt_abseta"}, {"2017ReReco", "NUM_LooseRelIso_DEN_LooseID_pt_abseta"}, {"2016ReReco", "NUM_LooseRelIso_DEN_LooseID_eta_pt"}, {"2016APVReReco", "NUM_LooseRelIso_DEN_LooseID_eta_pt"}};
	std::string idSFPath = sfFolder + "/Efficiencies_muon_generalTracks_Z_" + sfFileMap[campaignName] + "_ID.root";
	std::string isoSFPath = sfFolder + "/Efficiencies_muon_generalTracks_Z_" + sfFileMap[campaignName] + "_ISO.root";

	if (campaignName.find("UL") != std::string::npos)
	{
		TFile *idSF = new TFile(idSFPath.c_str(), "READ");
		TH2F *looseIDHist = (TH2F*)idSF->Get("NUM_LooseID_DEN_TrackerMuons_abseta_pt");
		TFile *isoSF = new TFile(isoSFPath.c_str(), "READ");
		TH2F *looseIsoHist = (TH2F*)isoSF->Get("NUM_LooseRelIso_DEN_LooseID_abseta_pt");
		calculateULSF(looseIDHist, looseIsoHist, filePath, sfRootFilePath);
	}
	else if (campaignName.find("ReReco") != std::string::npos)
	{
		if (campaignName.find("2016") != std::string::npos)
		{
			TFile *idSF = new TFile(idSFPath.c_str(), "READ");
			TH2F *looseIDHist = (TH2F*)idSF->Get(idHistNameReRecoMap[campaignName].c_str());
			TFile *isoSF = new TFile(isoSFPath.c_str(), "READ");
			TH2F *looseIsoHist = (TH2F*)isoSF->Get(isoHistNameReRecoMap[campaignName].c_str());
			calculateReReco16SF(looseIDHist, looseIsoHist, filePath, sfRootFilePath);
		}
		else
		{
			TFile *idSF = new TFile(idSFPath.c_str(), "READ");
			TH2F *looseIDHist = (TH2F*)idSF->Get(idHistNameReRecoMap[campaignName].c_str());
			TFile *isoSF = new TFile(isoSFPath.c_str(), "READ");
			TH2F *looseIsoHist = (TH2F*)isoSF->Get(isoHistNameReRecoMap[campaignName].c_str());
			calculateReReco1718SF(looseIDHist, looseIsoHist, filePath, sfRootFilePath);
		}
	}
}