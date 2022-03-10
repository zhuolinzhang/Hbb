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
	auto dSF = d.Define("mu_id_sf", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int idHistAbsEtaMu1 = idHist->GetXaxis()->FindBin(std::fabs(mu1Eta));
		int idHistPtMu1 = idHist->GetYaxis()->FindBin(mu1Pt);
		int idHistAbsEtaMu2 = idHist->GetXaxis()->FindBin(std::fabs(mu2Eta));
		int idHistPtMu2 = idHist->GetYaxis()->FindBin(mu2Pt);
		float idSFMu1 = 1;
		float idSFMu2 = 1;
		if (!(idHistPtMu1 > idHist->GetNbinsY() || idHistPtMu1 == 0)) idSFMu1 = idHist->GetBinContent(idHistAbsEtaMu1, idHistPtMu1);
		if (!(idHistPtMu2 > idHist->GetNbinsY() || idHistPtMu2 == 0)) idSFMu2 = idHist->GetBinContent(idHistAbsEtaMu2, idHistPtMu2);
		float finalSF = idSFMu1 * idSFMu2;
		return finalSF;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_iso_sf", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int isoHistAbsEtaMu1 = isoHist->GetXaxis()->FindBin(std::fabs(mu1Eta));
		int isoHistPtMu1 = isoHist->GetYaxis()->FindBin(mu1Pt);
		int isoHistAbsEtaMu2 = isoHist->GetXaxis()->FindBin(std::fabs(mu2Eta));
		int isoHistPtMu2 = isoHist->GetYaxis()->FindBin(mu2Pt);
		float isoSFMu1 = 1;
		float isoSFMu2 = 1;
		if (!(isoHistPtMu1 > isoHist->GetNbinsY() || isoHistPtMu1 == 0)) isoSFMu1 = isoHist->GetBinContent(isoHistAbsEtaMu1, isoHistPtMu1);
		if (!(isoHistPtMu2 > isoHist->GetNbinsY() || isoHistPtMu2 == 0)) isoSFMu2 = isoHist->GetBinContent(isoHistAbsEtaMu2, isoHistPtMu2);
		float finalSF = isoSFMu1 * isoSFMu2;
		return finalSF;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_id_sf_err", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int idHistAbsEtaMu1 = idHist->GetXaxis()->FindBin(std::fabs(mu1Eta));
		int idHistPtMu1 = idHist->GetYaxis()->FindBin(mu1Pt);
		int idHistAbsEtaMu2 = idHist->GetXaxis()->FindBin(std::fabs(mu2Eta));
		int idHistPtMu2 = idHist->GetYaxis()->FindBin(mu2Pt);
		float idSFSystErrMu1 = 0;
		float idSFMu1 = 1;
		float idSFSystErrMu2 = 0;
		float idSFMu2 = 1;
		if (!(idHistPtMu1 > idHist->GetNbinsY() || idHistPtMu1 == 0)) 
		{
			idSFSystErrMu1 = idHist->GetBinError(idHistAbsEtaMu1, idHistPtMu1);
			idSFMu1 = idHist->GetBinContent(idHistAbsEtaMu1, idHistPtMu1);
		}
		if (!(idHistPtMu2 > idHist->GetNbinsY() || idHistPtMu2 == 0)) 
		{
			idSFSystErrMu2 = idHist->GetBinError(idHistAbsEtaMu2, idHistPtMu2);
			idSFMu2 = idHist->GetBinContent(idHistAbsEtaMu2, idHistPtMu2);
		}
		float finalSFSystErr = idSFMu1 * idSFMu2 * (idSFSystErrMu1 / idSFMu1 + idSFSystErrMu2 / idSFMu2);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_iso_sf_err", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int isoHistAbsEtaMu1 = isoHist->GetXaxis()->FindBin(std::fabs(mu1Eta));
		int isoHistPtMu1 = isoHist->GetYaxis()->FindBin(mu1Pt);
		int isoHistAbsEtaMu2 = isoHist->GetXaxis()->FindBin(std::fabs(mu2Eta));
		int isoHistPtMu2 = isoHist->GetYaxis()->FindBin(mu2Pt);
		float isoSFSystErrMu1 = 0;
		float isoSFMu1 = 1;
		float isoSFSystErrMu2 = 0;
		float isoSFMu2 = 1;
		if (!(isoHistPtMu1 > isoHist->GetNbinsY() || isoHistPtMu1 == 0)) 
		{
			isoSFSystErrMu1 = isoHist->GetBinError(isoHistAbsEtaMu1, isoHistPtMu1);
			isoSFMu1 = isoHist->GetBinContent(isoHistAbsEtaMu1, isoHistPtMu1);
		}
		if (!(isoHistPtMu2 > isoHist->GetNbinsY() || isoHistPtMu2 == 0)) 
		{
			isoSFSystErrMu2 = isoHist->GetBinError(isoHistAbsEtaMu2, isoHistPtMu2);
			isoSFMu2 = isoHist->GetBinContent(isoHistAbsEtaMu2, isoHistPtMu2);
		}
		float finalSFSystErr = isoSFMu1 * isoSFMu2 * (isoSFSystErrMu1 / isoSFMu1 + isoSFSystErrMu2 / isoSFMu2);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("z_sf", "mu_id_sf * mu_iso_sf").Define("z_sf_err", "TMath::Sqrt(mu_iso_sf * mu_iso_sf * mu_id_sf_err * mu_id_sf_err + mu_id_sf * mu_id_sf * mu_iso_sf_err * mu_iso_sf_err)")
		.Define("z_sf_up", "z_sf + z_sf_err").Define("z_sf_down", "z_sf - z_sf_err");
	dSF.Snapshot("ZHCandidates", outputPath, dSF.GetColumnNames());
}

void calculateReReco1718SF(TH2F* idHist, TH2F* isoHist, std::string datasetPath, std::string outputPath)
{
	auto d = ROOT::RDataFrame("ZHCandidates", datasetPath);
	auto dSF = d.Define("mu_id_sf", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int idHistAbsEtaMu1 = idHist->GetYaxis()->FindBin(std::fabs(mu1Eta));
		int idHistPtMu1 = idHist->GetXaxis()->FindBin(mu1Pt);
		int idHistAbsEtaMu2 = idHist->GetYaxis()->FindBin(std::fabs(mu2Eta));
		int idHistPtMu2 = idHist->GetXaxis()->FindBin(mu2Pt);
		float idSFMu1 = 1;
		float idSFMu2 = 1;
		if (!(idHistPtMu1 > idHist->GetNbinsX() || idHistPtMu1 == 0)) idSFMu1 = idHist->GetBinContent(idHistPtMu1, idHistAbsEtaMu1);
		if (!(idHistPtMu2 > idHist->GetNbinsX() || idHistPtMu2 == 0)) idSFMu2 = idHist->GetBinContent(idHistPtMu2, idHistAbsEtaMu2);
		float finalSF = idSFMu1 * idSFMu2;
		return finalSF;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_id_sf_err", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int idHistAbsEtaMu1 = idHist->GetYaxis()->FindBin(std::fabs(mu1Eta));
		int idHistPtMu1 = idHist->GetXaxis()->FindBin(mu1Pt);
		int idHistAbsEtaMu2 = idHist->GetYaxis()->FindBin(std::fabs(mu2Eta));
		int idHistPtMu2 = idHist->GetXaxis()->FindBin(mu2Pt);
		float idSFMu1 = 1;
		float idSFSystErrMu1 = 0;
		float idSFMu2 = 1;
		float idSFSystErrMu2 = 0;
		if (!(idHistPtMu1 > idHist->GetNbinsX() || idHistPtMu1 == 0)) 
		{
			idSFMu1 = idHist->GetBinContent(idHistPtMu1, idHistAbsEtaMu1);
			idSFSystErrMu1 = idHist->GetBinError(idHistPtMu1, idHistAbsEtaMu1);
		}
		if (!(idHistPtMu2 > idHist->GetNbinsX() || idHistPtMu2 == 0)) 
		{
			idSFMu2 = idHist->GetBinContent(idHistPtMu2, idHistAbsEtaMu2);
			idSFSystErrMu2 = idHist->GetBinError(idHistPtMu2, idHistAbsEtaMu2);
		}
		float finalSFSystErr = idSFMu1 * idSFMu2 * (idSFSystErrMu1 / idSFMu1 + idSFSystErrMu2 / idSFMu2);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_iso_sf", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int isoHistAbsEtaMu1 = isoHist->GetYaxis()->FindBin(std::fabs(mu1Eta));
		int isoHistPtMu1 = isoHist->GetXaxis()->FindBin(mu1Pt);
		int isoHistAbsEtaMu2 = isoHist->GetYaxis()->FindBin(std::fabs(mu2Eta));
		int isoHistPtMu2 = isoHist->GetXaxis()->FindBin(mu2Pt);
		float isoSFMu1 = 1;
		float isoSFMu2 = 1;
		if (!(isoHistPtMu1 > isoHist->GetNbinsX() || isoHistPtMu1 == 0)) isoSFMu1 = isoHist->GetBinContent(isoHistPtMu1, isoHistAbsEtaMu1);
		if (!(isoHistPtMu2 > isoHist->GetNbinsX() || isoHistPtMu2 == 0)) isoSFMu2 = isoHist->GetBinContent(isoHistPtMu2, isoHistAbsEtaMu2);
		float finalSF = isoSFMu1 * isoSFMu2;
		return finalSF;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_iso_sf_err", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int isoHistAbsEtaMu1 = isoHist->GetYaxis()->FindBin(std::fabs(mu1Eta));
		int isoHistPtMu1 = isoHist->GetXaxis()->FindBin(mu1Pt);
		int isoHistAbsEtaMu2 = isoHist->GetYaxis()->FindBin(std::fabs(mu2Eta));
		int isoHistPtMu2 = isoHist->GetXaxis()->FindBin(mu2Pt);
		float isoSFMu1 = 1;
		float isoSFSystErrMu1 = 0;
		float isoSFMu2 = 1;
		float isoSFSystErrMu2 = 0;
		if (!(isoHistPtMu1 > isoHist->GetNbinsX() || isoHistPtMu1 == 0)) 
		{
			isoSFMu1 = isoHist->GetBinContent(isoHistPtMu1, isoHistAbsEtaMu1);
			isoSFSystErrMu1 = isoHist->GetBinError(isoHistPtMu1, isoHistAbsEtaMu1);
		}
		if (!(isoHistPtMu2 > isoHist->GetNbinsX() || isoHistPtMu2 == 0)) 
		{
			isoSFMu2 = isoHist->GetBinContent(isoHistPtMu2, isoHistAbsEtaMu2);
			isoSFSystErrMu2 = isoHist->GetBinError(isoHistPtMu2, isoHistAbsEtaMu2);
		}
		float finalSFSystErr = isoSFMu1 * isoSFMu2 * (isoSFSystErrMu1 / isoSFMu1 + isoSFSystErrMu2 / isoSFMu2);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("z_sf", "mu_id_sf * mu_iso_sf").Define("z_sf_err", "TMath::Sqrt(mu_iso_sf * mu_iso_sf * mu_id_sf_err * mu_id_sf_err + mu_id_sf * mu_id_sf * mu_iso_sf_err * mu_iso_sf_err)")
		.Define("z_sf_up", "z_sf + z_sf_err").Define("z_sf_down", "z_sf - z_sf_err");
	dSF.Snapshot("ZHCandidates", outputPath, dSF.GetColumnNames());
}

void calculateReReco16SF(TH2F* idHist, TH2F* isoHist, std::string datasetPath, std::string outputPath)
{
	auto d = ROOT::RDataFrame("ZHCandidates", datasetPath);
	auto dSF = d.Define("mu_id_sf", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int idHistEtaMu1 = idHist->GetXaxis()->FindBin(std::fabs(mu1Eta));
		int idHistPtMu1 = idHist->GetYaxis()->FindBin(mu1Pt);
		int idHistEtaMu2 = idHist->GetXaxis()->FindBin(std::fabs(mu2Eta));
		int idHistPtMu2 = idHist->GetYaxis()->FindBin(mu2Pt);
		float idSFMu1 = 1;
		float idSFMu2 = 1;
		if (!(idHistPtMu1 > idHist->GetNbinsY() || idHistPtMu1 == 0)) idSFMu1 = idHist->GetBinContent(idHistEtaMu1, idHistPtMu1);
		if (!(idHistPtMu2 > idHist->GetNbinsY() || idHistPtMu2 == 0)) idSFMu2 = idHist->GetBinContent(idHistEtaMu2, idHistPtMu2);
		float finalSF = idSFMu1 * idSFMu2;
		return finalSF;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_id_sf_err", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int idHistEtaMu1 = idHist->GetXaxis()->FindBin(std::fabs(mu1Eta));
		int idHistPtMu1 = idHist->GetYaxis()->FindBin(mu1Pt);
		int idHistEtaMu2 = idHist->GetXaxis()->FindBin(std::fabs(mu2Eta));
		int idHistPtMu2 = idHist->GetYaxis()->FindBin(mu2Pt);
		float idSFMu1 = 1;
		float idSFSystErrMu1 = 0;
		float idSFMu2 = 1;
		float idSFSystErrMu2 = 0;
		if (!(idHistPtMu1 > idHist->GetNbinsY() || idHistPtMu1 == 0)) 
		{
			idSFMu1 = idHist->GetBinContent(idHistEtaMu1, idHistPtMu1);
			idSFSystErrMu1 = idHist->GetBinError(idHistEtaMu1, idHistPtMu1);
		}
		if (!(idHistPtMu2 > idHist->GetNbinsY() || idHistPtMu2 == 0)) 
		{
			idSFMu2 = idHist->GetBinContent(idHistEtaMu2, idHistPtMu2);
			idSFSystErrMu2 = idHist->GetBinError(idHistEtaMu2, idHistPtMu2);
		}
		float finalSFSystErr = idSFMu1 * idSFMu2 * (idSFSystErrMu1 / idSFMu1 + idSFSystErrMu2 / idSFMu2);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_iso_sf", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int isoHistEtaMu1 = isoHist->GetXaxis()->FindBin(std::fabs(mu1Eta));
		int isoHistPtMu1 = isoHist->GetYaxis()->FindBin(mu1Pt);
		int isoHistEtaMu2 = isoHist->GetXaxis()->FindBin(std::fabs(mu2Eta));
		int isoHistPtMu2 = isoHist->GetYaxis()->FindBin(mu2Pt);
		float isoSFMu1 = 1;
		float isoSFMu2 = 1;
		if (!(isoHistPtMu1 > isoHist->GetNbinsY() || isoHistPtMu1 == 0)) isoSFMu1 = isoHist->GetBinContent(isoHistEtaMu1, isoHistPtMu1);
		if (!(isoHistPtMu2 > isoHist->GetNbinsY() || isoHistPtMu2 == 0)) isoSFMu2 = isoHist->GetBinContent(isoHistEtaMu2, isoHistPtMu2);
		float finalSF = isoSFMu1 * isoSFMu2;
		return finalSF;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("mu_iso_sf_err", [&](float mu1Pt, float mu1Eta, float mu2Pt, float mu2Eta){
		int isoHistEtaMu1 = isoHist->GetXaxis()->FindBin(std::fabs(mu1Eta));
		int isoHistPtMu1 = isoHist->GetYaxis()->FindBin(mu1Pt);
		int isoHistEtaMu2 = isoHist->GetXaxis()->FindBin(std::fabs(mu2Eta));
		int isoHistPtMu2 = isoHist->GetYaxis()->FindBin(mu2Pt);
		float isoSFMu1 = 1;
		float isoSFSystErrMu1 = 0;
		float isoSFMu2 = 1;
		float isoSFSystErrMu2 = 0;
		if (!(isoHistPtMu1 > isoHist->GetNbinsY() || isoHistPtMu1 == 0)) 
		{
			isoSFMu1 = isoHist->GetBinContent(isoHistEtaMu1, isoHistPtMu1);
			isoSFSystErrMu1 = isoHist->GetBinError(isoHistEtaMu1, isoHistPtMu1);
		}
		if (!(isoHistPtMu2 > isoHist->GetNbinsY() || isoHistPtMu2 == 0)) 
		{
			isoSFMu2 = isoHist->GetBinContent(isoHistEtaMu2, isoHistPtMu2);
			isoSFSystErrMu2 = isoHist->GetBinError(isoHistEtaMu2, isoHistPtMu2);
		}
		float finalSFSystErr = isoSFMu1 * isoSFMu2 * (isoSFSystErrMu1 / isoSFMu1 + isoSFSystErrMu2 / isoSFMu2);
		return finalSFSystErr;
		}, {"mu1_pt", "mu1_eta", "mu2_pt", "mu2_eta"})
		.Define("z_sf", "mu_id_sf * mu_iso_sf").Define("z_sf_err", "TMath::Sqrt(mu_iso_sf * mu_iso_sf * mu_id_sf_err * mu_id_sf_err + mu_id_sf * mu_id_sf * mu_iso_sf_err * mu_iso_sf_err)")
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