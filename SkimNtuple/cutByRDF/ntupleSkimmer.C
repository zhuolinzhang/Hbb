#include <vector>
#include <fstream>
#include <string>
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"

using floats = const ROOT::RVec<float>&;
using bools = const ROOT::RVec<bool>&;
using ints = const ROOT::RVec<int>&;

int ntupleSkimmer(std::string oldFilePath, std::string newFilePath)
{
	ROOT::EnableImplicitMT();
	auto d = ROOT::RDataFrame("demo/ZHCollection", oldFilePath); // demo/ZHCollection
	auto dInit = d.Count();
	auto dFull = d.Define("jet1ID", [](floats jet1Eta, floats jet1CEMF, floats jet1CHM, floats jet1CHF, floats jet1NumConst, floats jet1NEMF, floats jet1MUF, floats jet1NHF)
		{
			ROOT::RVec<bool> jetIDVec;
			for (size_t i = 0; i < jet1Eta.size(); i++)
			{
				jetIDVec.push_back(jet1Eta[i] <= 2.6 && jet1CEMF[i] < 0.8 && jet1CHM[i] > 0 && jet1CHF[i] > 0 && jet1NumConst[i] > 1 && jet1NEMF[i] < 0.9 && jet1MUF[i] < 0.8 && jet1NHF[i] < 0.9);
			}
			return jetIDVec;
		}, {"jet1Eta", "jet1CEMF", "jet1CHM", "jet1CHF", "jet1NumConst", "jet1NEMF", "jet1MUF", "jet1NHF"})
		.Define("jet2ID", [](floats jet2Eta, floats jet2CEMF, floats jet2CHM, floats jet2CHF, floats jet2NumConst, floats jet2NEMF, floats jet2MUF, floats jet2NHF)
		{
			ROOT::RVec<bool> jetIDVec;
			for (size_t i = 0; i < jet2Eta.size(); i++)
			{
				jetIDVec.push_back(jet2Eta[i] <= 2.6 && jet2CEMF[i] < 0.8 && jet2CHM[i] > 0 && jet2CHF[i] > 0 && jet2NumConst[i] > 1 && jet2NEMF[i] < 0.9 && jet2MUF[i] < 0.8 && jet2NHF[i] < 0.9);
			}
			return jetIDVec;
		}, {"jet2Eta", "jet2CEMF", "jet2CHM", "jet2CHF", "jet2NumConst", "jet2NEMF", "jet2MUF", "jet2NHF"});
	auto dMuonCut = dFull.Define("goodMuonId", [](floats mu1Pt, floats mu2Pt, bools mu1Tight, bools mu2Tight, floats mu1Eta, floats mu2Eta, floats mu1Iso, floats mu2Iso, floats ZM){
		int idx = -1;
		for (size_t i = 0; i < mu1Pt.size(); i++)
		{
			if (mu1Pt[i] > 25 && mu2Pt[i] > 15 && mu1Tight[i] && mu2Tight[i] && fabs(mu1Eta[i]) < 2.4 && fabs(mu2Eta[i]) < 2.4 && mu1Iso[i] < 0.4 && mu2Iso[i] < 0.4 && ZM[i] >= 75 && ZM[i] <= 105)
			{
				idx = i;
				break;
			}
		}
		return idx;
	}, {"mu1Pt", "mu2Pt", "mu1Tight", "mu2Tight", "mu1Eta", "mu2Eta", "mu1Iso", "mu2Iso", "ZM"}).Filter("goodMuonId != -1");
	auto dJetCut = dMuonCut.Define("goodJetId", [](floats jet1Pt, floats jet2Pt, floats jet1Eta, floats jet2Eta, floats jet1bTag, floats jet2bTag, bools jet1ID, bools jet2ID, floats HiggsM)
	{
		int idx = -1;
		for (size_t i = 0; i < jet1Pt.size(); i++)
		{
			if (jet1Pt[i] > 20 && jet2Pt[i] > 20 && fabs(jet1Eta[i]) < 2.5 && fabs(jet2Eta[i]) < 2.5 && jet1bTag[i] > 0.4168 && jet2bTag[i] > 0.4168 && jet1ID[i] && jet2ID[i] && HiggsM[i] >= 50 && HiggsM[i] <= 200)
			{
				idx = i;
				break;
			}
		}
		return idx;
	}, {"jet1Pt", "jet2Pt", "jet1Eta", "jet2Eta", "jet1bTag", "jet2bTag", "jet1ID", "jet2ID", "HiggsM"}).Filter("goodJetId != -1");

	auto dFinal = dJetCut.Define("z_pt", "ZPt[goodMuonId]").Define("z_eta", "ZEta[goodMuonId]").Define("z_phi", "ZPhi[goodMuonId]").Define("z_mass", "ZM[goodMuonId]").Define("higgs_pt", "HiggsPt[goodJetId]").Define("higgs_eta", "HiggsEta[goodJetId]").Define("higgs_phi", "HiggsPhi[goodJetId]").Define("higgs_mass", "HiggsM[goodJetId]");
	auto dCount = dJetCut.Count();
	std::cout << *dInit << std::endl << *dCount << std::endl;
	dFinal.Snapshot("ZHCandidates", newFilePath, {"z_pt", "z_eta", "z_phi", "z_mass", "higgs_pt", "higgs_eta", "higgs_phi", "higgs_mass"}); // ZHCandidates {"z_pt", "z_eta", "z_phi", "z_m", "higgs_pt", "higgs_eta", "higgs_phi", "higgs_m"}
	return 0;
}