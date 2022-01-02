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
	if len(pathList) > 1:
		folderPath = '/'.join(pathList[:-1])
		if os.path.exists(folderPath): pass
		else: os.mkdir(folderPath)

start = time.time()
checkOutPut(args.o)
d = ROOT.RDataFrame("demo/ZHCollection", args.i)
bTagWPMedium = {"2018UL": 0.4168, "2018ReReco": 0.4184, "2017UL": 0.4506, "2017ReReco": 0.4941, "2016UL": 0.5847, "2016APVUL": 0.6001, "2016ReReco": 0.6321}
bTagWPLoose = {"2018UL": 0.1208, "2018ReReco": 0.1241, "2017UL": 0.1355, "2017ReReco": 0.1522, "2016UL": 0.1918, "2016APVUL": 0.2027, "2016ReReco": 0.2217}
jetID = {"2018UL": "jetNumConst[i] > 1 && jetNEMF[i] < 0.9 && jetMUF[i] < 0.8 && jetNHF[i] < 0.9 && fabs(jetEta[i]) <= 2.6 && jetCEMF[i] < 0.8 && jetCHM[i] > 0 && jetCHF[i] > 0",
		"2018ReReco": "jetNumConst[i] > 1 && jetNEMF[i] < 0.9 && jetMUF[i] < 0.8 && jetNHF[i] < 0.9 && fabs(jetEta[i]) <= 2.6 && jetCEMF[i] < 0.8 && jetCHM[i] > 0 && jetCHF[i] > 0",
		"2017UL": "jetNumConst[i] > 1 && jetNEMF[i] < 0.9 && jetMUF[i] < 0.8 && jetNHF[i] < 0.9 && fabs(jetEta[i]) <= 2.6 && jetCEMF[i] < 0.8 && jetCHM[i] > 0 && jetCHF[i] > 0",
		"2017ReReco": "(jetNumConst[i] > 1 && jetNEMF[i] < 0.9 && jetMUF[i] < 0.8 && jetNHF[i] < 0.9 && fabs(jetEta[i]) <= 2.7) && (fabs(jetEta[i]) > 2.4 || (fabs(jetEta[i]) <= 2.4 && jetCEMF[i] < 0.8 && jetCHM[i] > 0 && jetCHF[i] > 0))",
		"2016UL": "(jetNEMF[i] < 0.99 && jetNHF[i] < 0.9 && fabs(jetEta[i]) <= 2.7) && (fabs(jetEta[i]) > 2.4 || (fabs(jetEta[i]) <= 2.4 && jetCEMF[i] < 0.8 && jetCHM[i] > 0 && jetCHF[i] > 0 && jetNumConst[i] > 1 && jetMUF[i] < 0.8))",
		"2016APVUL": "(jetNEMF[i] < 0.9 && jetNHF[i] < 0.9 && fabs(jetEta[i]) <= 2.7) && (fabs(jetEta[i]) > 2.4 || (fabs(jetEta[i]) <= 2.4 && jetCEMF[i] < 0.8 && jetCHM[i] > 0 && jetCHF[i] > 0 && jetNumConst[i] > 1 && jetMUF[i] < 0.8))",
		"2016ReReco": "(jetNumConst[i] > 1 && jetNEMF[i] < 0.9 && jetMUF[i] < 0.8 && jetNHF[i] < 0.9 && fabs(jetEta[i]) <= 2.7) && (fabs(jetEta[i]) > 2.4 || (fabs(jetEta[i]) <= 2.4 && jetCEMF[i] < 0.9 && jetCHM[i] > 0 && jetCHF[i] > 0))"}

makeJetId = '''
using bool_T = ROOT::RVec<bool>;
using floats = const ROOT::RVec<float>&;
bool_T makeJetId(floats jetEta, floats jetCEMF, floats jetCHM, floats jetCHF, floats jetNumConst, floats jetNEMF, floats jetMUF, floats jetNHF)
{{
	bool_T jetIDVec;
		for (size_t i = 0; i < jetEta.size(); i++)
		{{
			bool jetID = {};
			jetIDVec.push_back(jetID);
		}}
	return jetIDVec;
}}
'''.format(jetID[args.c])

findGoodParticles = '''
using floats = const ROOT::RVec<float>&;
using bools = const ROOT::RVec<bool>&;
using ints = const ROOT::RVec<int>&;

int findGoodMuonIdx(floats mu1Pt, floats mu2Pt, bools mu1Loose, bools mu2Loose, floats mu1Eta, floats mu2Eta, floats mu1Iso, floats mu2Iso, floats ZM)
{{
	int idx = -1;
	for (size_t i = 0; i < mu1Pt.size(); i++)
	{{
		if (mu1Pt[i] > 20 && mu2Pt[i] > 20 && mu1Loose[i] && mu2Loose[i] && fabs(mu1Eta[i]) < 2.4 && fabs(mu2Eta[i]) < 2.4 && mu1Iso[i] < 0.15 && mu2Iso[i] < 0.15 && ZM[i] >= 75 && ZM[i] <= 105)
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
	int maxbTagSum = -1;
	for (size_t i = 0; i < jet1Pt.size(); i++)
	{{
		if (jet1Pt[i] > 20 && jet2Pt[i] > 20 && fabs(jet1Eta[i]) < 2.5 && fabs(jet2Eta[i]) < 2.5 && jet1bTag[i] > {} && jet2bTag[i] > {} && jet1ID[i] && jet2ID[i] && HiggsM[i] >= 50 && HiggsM[i] <= 200)
		{{
			if (jet1bTag[i] > jet2bTag[i])
			{{
				if (!(jet1bTag[i] > {})) continue;
			}}
			else
			{{
				if (!(jet2bTag[i] > {})) continue;
			}}
			if ((jet1bTag[i] + jet2bTag[i]) > maxbTagSum) 
			{{
				maxbTagSum = jet1bTag[i] + jet2bTag[i];
				idx = i;
			}}
		}}
	}}
	return idx;
}}
'''.format(bTagWPLoose[args.c], bTagWPLoose[args.c], bTagWPMedium[args.c], bTagWPMedium[args.c])

ROOT.gInterpreter.Declare(makeJetId)
ROOT.gInterpreter.Declare(findGoodParticles)

dInitCount = d.Count()
dFull = d.Define("jet1ID", "makeJetId(jet1Eta, jet1CEMF, jet1CHM, jet1CHF, jet1NumConst, jet1NEMF, jet1MUF, jet1NHF)").Define("jet2ID", "makeJetId(jet2Eta, jet2CEMF, jet2CHM, jet2CHF, jet2NumConst, jet2NEMF, jet2MUF, jet2NHF)")
dCut = dFull.Define("goodMuonId", "findGoodMuonIdx(mu1Pt, mu2Pt, mu1Loose, mu2Loose, mu1Eta, mu2Eta, mu1Iso, mu2Iso, ZM)").Define("goodJetId", "findGoodJetIdx(jet1Pt, jet2Pt, jet1Eta, jet2Eta, jet1bTag, jet2bTag, jet1ID, jet2ID, HiggsM)")
dFinal = dCut.Filter("goodMuonId != -1").Filter("goodJetId != -1").Define("z_pt", "ZPt[goodMuonId]").Define("z_eta", "ZEta[goodMuonId]").Define("z_phi", "ZPhi[goodMuonId]").Define("z_mass", "ZM[goodMuonId]").Define("higgs_pt", "HiggsPt[goodJetId]").Define("higgs_eta", "HiggsEta[goodJetId]").Define("higgs_phi", "HiggsPhi[goodJetId]").Define("higgs_mass", "HiggsM[goodJetId]")
dFinal = dCut.Filter("goodMuonId != -1").Filter("goodJetId != -1")\
                .Define("mu1_charge", "mu1Charge[goodMuonId]").Define("mu1_pt", "mu1Pt[goodMuonId]").Define("mu1_eta", "mu1Eta[goodMuonId]").Define("mu1_phi", "mu1Phi[goodMuonId]").Define("mu1_mass", "mu1M[goodMuonId]")\
                .Define("mu2_charge", "mu2Charge[goodMuonId]").Define("mu2_pt", "mu2Pt[goodMuonId]").Define("mu2_eta", "mu2Eta[goodMuonId]").Define("mu2_phi", "mu2Phi[goodMuonId]").Define("mu2_mass", "mu2M[goodMuonId]")\
                .Define("jet1_pt", "jet1Pt[goodJetId]").Define("jet1_eta", "jet1Eta[goodJetId]").Define("jet1_phi", "jet1Phi[goodJetId]").Define("jet1_mass", "jet1M[goodJetId]").Define("jet1_bTag", "jet1bTag[goodJetId]")\
                .Define("jet2_pt", "jet2Pt[goodJetId]").Define("jet2_eta", "jet2Eta[goodJetId]").Define("jet2_phi", "jet2Phi[goodJetId]").Define("jet2_mass", "jet2M[goodJetId]").Define("jet2_bTag", "jet2bTag[goodJetId]")\
                .Define("z_pt", "ZPt[goodMuonId]").Define("z_eta", "ZEta[goodMuonId]").Define("z_phi", "ZPhi[goodMuonId]").Define("z_mass", "ZM[goodMuonId]")\
                .Define("higgs_pt", "HiggsPt[goodJetId]").Define("higgs_eta", "HiggsEta[goodJetId]").Define("higgs_phi", "HiggsPhi[goodJetId]").Define("higgs_mass", "HiggsM[goodJetId]")
dFinalCount = dFinal.Count()
print(args.i.split('/')[-1].rstrip(".root"))
print("The Nevents before cut: {}".format(dInitCount.GetValue()))
print("The Nevents after cut: {}".format(dFinalCount.GetValue()))
#branchList = ROOT.vector('string')(("z_pt", "z_eta", "z_phi", "z_mass", "higgs_pt", "higgs_eta", "higgs_phi", "higgs_mass"))
branchList = ROOT.vector('string')(("mu1_charge", "mu1_pt", "mu1_eta", "mu1_phi", "mu1_mass", "mu2_charge", "mu2_pt", "mu2_eta", "mu2_phi", "mu2_mass", "jet1_pt", "jet1_eta", "jet1_phi", "jet1_mass", "jet1_bTag", "jet2_pt", "jet2_eta", "jet2_phi", "jet2_mass", "jet2_bTag", "z_pt", "z_eta", "z_phi", "z_mass", "higgs_pt", "higgs_eta", "higgs_phi", "higgs_mass"))
if dFinal.Count().GetValue() > 0:
	dFinal.Snapshot("ZHCandidates", args.o, branchList) 
end = time.time()
print("Spend time: {} s".format(end - start))
