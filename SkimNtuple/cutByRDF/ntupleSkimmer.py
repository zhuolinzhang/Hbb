import ROOT
import argparse
import time
import os

parse = argparse.ArgumentParser()
parse.add_argument('-i', help='The input .root file')
parse.add_argument('-o', help='The output skimmed .root file')
parse.add_argument('-c', help='The campaign of dataset')
args = parse.parse_args()

def checkOutPut(path: str):
	pathList = path.split('/')
	folderPath = '/'.join(pathList[:-1])
	if os.path.exists(folderPath): pass
	else: os.mkdir(folderPath)

start = time.time()
checkOutPut(args.o)
ROOT.ROOT.EnableImplicitMT()
d = ROOT.RDataFrame("demo/ZHCollection", args.i)
jetID = {"2018UL": {"jetEta": 2.6, "jetCEMF": 0.8, "jetCHM": 0, "jetCHF": 0, "jetNumConst": 1, "jetNEMF": 0.9, "jetMUF": 0.8, "jetNHF": 0.9},
		"2018ReReco": {"jetEta": 2.6, "jetCEMF": 0.8, "jetCHM": 0, "jetCHF": 0, "jetNumConst": 1, "jetNEMF": 0.9, "jetMUF": 0.8, "jetNHF": 0.9},
		"2017UL": {"jetEta": 2.6, "jetCEMF": 0.8, "jetCHM": 0, "jetCHF": 0, "jetNumConst": 1, "jetNEMF": 0.9, "jetMUF": 0.8, "jetNHF": 0.9},
		"2017ReReco": {"jetEta": 2.7, "jetCEMF": 0.8, "jetCHM": 0, "jetCHF": 0, "jetNumConst": 1, "jetNEMF": 0.9, "jetMUF": 0.8, "jetNHF": 0.9},
		"2016UL": {"jetEta": 2.4, "jetCEMF": 0.8, "jetCHM": 0, "jetCHF": 0, "jetNumConst": 1, "jetNEMF": 0.9, "jetMUF": 0.8, "jetNHF": 0.9},
		"2016APVUL": {"jetEta": 2.4, "jetCEMF": 0.8, "jetCHM": 0, "jetCHF": 0, "jetNumConst": 1, "jetNEMF": 0.9, "jetMUF": 0.8, "jetNHF": 0.9},
		"2016ReReco": {"jetEta": 2.4, "jetCEMF": 0.9, "jetCHM": 0, "jetCHF": 0, "jetNumConst": 1, "jetNEMF": 0.9, "jetMUF": 0.8, "jetNHF": 0.9}}
bTagWP = {"2018UL": 0.4168, "2018ReReco": 0.4184, "2017UL": 0.4506, "2017ReReco": 0.4941, "2016UL": 0.5847, "2016APVUL": 0.5847, "2016ReReco": 0.6324}

ROOT.gInterpreter.Declare("""
using floats = const ROOT::RVec<float>&;
using bool_T = ROOT::RVec<bool>;
using bools = const ROOT::RVec<bool>&;
using ints = const ROOT::RVec<int>&;

bool_T makeJetId(floats jetEta, floats jetCEMF, floats jetCHM, floats jetCHF, floats jetNumConst, floats jetNEMF, floats jetMUF, floats jetNHF)
{{
	bool_T jetIDVec;
		for (size_t i = 0; i < jetEta.size(); i++)
		{{
			jetIDVec.push_back(jetEta[i] <= {} && jetCEMF[i] < {} && jetCHM[i] > {} && jetCHF[i] > {} && jetNumConst[i] > {} && jetNEMF[i] < {} && jetMUF[i] < {} && jetNHF[i] < {});
		}}
	return jetIDVec;
}}

int findGoodMuonIdx(floats mu1Pt, floats mu2Pt, bools mu1Tight, bools mu2Tight, floats mu1Eta, floats mu2Eta, floats mu1Iso, floats mu2Iso, floats ZM)
{{
	int idx = -1;
		for (size_t i = 0; i < mu1Pt.size(); i++)
		{{
			if (mu1Pt[i] > 25 && mu2Pt[i] > 15 && mu1Tight[i] && mu2Tight[i] && fabs(mu1Eta[i]) < 2.4 && fabs(mu2Eta[i]) < 2.4 && mu1Iso[i] < 0.4 && mu2Iso[i] < 0.4 && ZM[i] >= 75 && ZM[i] <= 105)
			{{
				idx = i;
				break;
			}}
		}}
	return idx;
}}

int findGoodJetIdx(floats jet1Pt, floats jet2Pt, floats jet1Eta, floats jet2Eta, floats jet1bTag, floats jet2bTag, bools jet1ID, bools jet2ID, floats HiggsM)
{{
	int idx = -1;
		for (size_t i = 0; i < jet1Pt.size(); i++)
		{{
			if (jet1Pt[i] > 20 && jet2Pt[i] > 20 && fabs(jet1Eta[i]) < 2.5 && fabs(jet2Eta[i]) < 2.5 && jet1bTag[i] > {} && jet2bTag[i] > {} && jet1ID[i] && jet2ID[i] && HiggsM[i] >= 50 && HiggsM[i] <= 200)
			{{
				idx = i;
				break;
			}}
		}}
	return idx;
}}

""".format(jetID[args.c]["jetEta"], jetID[args.c]["jetCEMF"], jetID[args.c]["jetCHM"], jetID[args.c]["jetCHF"], jetID[args.c]["jetNumConst"], jetID[args.c]["jetNEMF"], jetID[args.c]["jetMUF"], jetID[args.c]["jetNHF"], bTagWP[args.c], bTagWP[args.c]))
dInitCount = d.Count()
dFull = d.Define("jet1ID", "makeJetId(jet1Eta, jet1CEMF, jet1CHM, jet1CHF, jet1NumConst, jet1NEMF, jet1MUF, jet1NHF)").Define("jet2ID", "makeJetId(jet2Eta, jet2CEMF, jet2CHM, jet2CHF, jet2NumConst, jet2NEMF, jet2MUF, jet2NHF)")
dCut = dFull.Define("goodMuonId", "findGoodMuonIdx(mu1Pt, mu2Pt, mu1Tight, mu2Tight, mu1Eta, mu2Eta, mu1Iso, mu2Iso, ZM)").Define("goodJetId", "findGoodJetIdx(jet1Pt, jet2Pt, jet1Eta, jet2Eta, jet1bTag, jet2bTag, jet1ID, jet2ID, HiggsM)")
dFinal = dCut.Filter("goodMuonId != -1").Filter("goodJetId != -1").Define("z_pt", "ZPt[goodMuonId]").Define("z_eta", "ZEta[goodMuonId]").Define("z_phi", "ZPhi[goodMuonId]").Define("z_mass", "ZM[goodMuonId]").Define("higgs_pt", "HiggsPt[goodJetId]").Define("higgs_eta", "HiggsEta[goodJetId]").Define("higgs_phi", "HiggsPhi[goodJetId]").Define("higgs_mass", "HiggsM[goodJetId]")
'''
dFinal = dCut.Filter("goodMuonIdx != -1").Filter("goodJetIdx != -1")\
                .Define("mu1_pt", "mu1Pt[goodMuonIdx]").Define("mu1_eta", "mu1Eta[goodMuonIdx]").Define("mu1_phi", "mu1Phi[goodMuonIdx]").Define("mu1_mass", "mu1M[goodMuonIdx]")\
                .Define("mu2_pt", "mu2Pt[goodMuonIdx]").Define("mu2_eta", "mu2Eta[goodMuonIdx]").Define("mu2_phi", "mu2Phi[goodMuonIdx]").Define("mu2_mass", "mu2M[goodMuonIdx]")\
                .Define("jet1_pt", "jet1Pt[goodJetIdx]").Define("jet1_eta", "jet1Eta[goodJetIdx]").Define("jet1_phi", "jet1Phi[goodJetIdx]").Define("jet1_mass", "jet1M[goodJetIdx]").Define("jet1_bTag", "jet1bTag[goodJetIdx]").Define("jet1_id", "jet1Id[goodJetIdx]")\
                .Define("jet2_pt", "jet2Pt[goodJetIdx]").Define("jet2_eta", "jet2Eta[goodJetIdx]").Define("jet2_phi", "jet2Phi[goodJetIdx]").Define("jet2_mass", "jet2M[goodJetIdx]").Define("jet2_bTag", "jet2bTag[goodJetIdx]").Define("jet2_id", "jet2Id[goodJetIdx]")\
                .Define("z_pt", "ZPt[goodMuonIdx]").Define("z_eta", "ZEta[goodMuonIdx]").Define("z_phi", "ZPhi[goodMuonIdx]").Define("z_mass", "ZM[goodMuonIdx]")\
                .Define("higgs_pt", "HiggsPt[goodJetIdx]").Define("higgs_eta", "HiggsEta[goodJetIdx]").Define("higgs_phi", "HiggsPhi[goodJetIdx]").Define("higgs_mass", "HiggsM[goodJetIdx]")
'''
dFinalCount = dFinal.Count()
print(args.i.split('/')[-1].rstrip(".root"))
print("The Nevents before cut: {}".format(dInitCount.GetValue()))
print("The Nevents after cut: {}".format(dFinalCount.GetValue()))
branchList = ROOT.vector('string')(("z_pt", "z_eta", "z_phi", "z_mass", "higgs_pt", "higgs_eta", "higgs_phi", "higgs_mass"))
# branchList = ROOT.vector('string')(("mu1_pt", "mu1_eta", "mu1_phi", "mu1_mass", "mu2_pt", "mu2_eta", "mu2_phi", "mu2_mass", "jet1_pt", "jet1_eta", "jet1_phi", "jet1_mass", "jet1_bTag", "jet1_id", "jet2_pt", "jet2_eta", "jet2_phi", "jet2_mass", "jet2_bTag", "jet2_id", "z_pt", "z_eta", "z_phi", "z_mass", "higgs_pt", "higgs_eta", "higgs_phi", "higgs_mass"))
dFinal.Snapshot("ZHCandidates", args.o, branchList) 
end = time.time()
print("Spend time: {} s".format(end - start))