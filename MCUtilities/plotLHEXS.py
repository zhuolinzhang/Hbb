import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='The input root file path')
parser.add_argument('-events', type=int, help='The number of events')
parser.add_argument('-xs', type=float, help='The cross section of the sample')
parser.add_argument('-libpath', default='libExRootAnalysis.so', help='The path of libExRootAnalysis.so')
args = parser.parse_args()

# extract the output name of MG5
mg5Name = args.i.split('/')[-1]
folderPathList = args.i.split('/')[:-1]
folderPath = '/'.join(folderPathList)
outputPath = folderPath + '/' + "mg5XS_" + mg5Name

totalXS = args.xs * 1000
lumi = args.events / totalXS

ROOT.gROOT.SetBatch()

ROOT.gSystem.Load(args.libpath)
df = ROOT.RDataFrame("LHEF", args.i)

ROOT.gInterpreter.Declare("""
using doubles = ROOT::RVec<double>&;
using ints = ROOT::RVec<int>&;
double findHiggsMass(ints pid, doubles particleMass)
{
	for (size_t i = 0; i < pid.size(); i++) if (pid[i] == 25) return particleMass[i];
}
double findHiggsPt(ints pid, doubles particlePt)
{
	for (size_t i = 0; i < pid.size(); i++) if (pid[i] == 25) return particlePt[i];
}
""")
dHiggs = df.Define("HiggsM", "findHiggsMass(Particle.PID, Particle.M)").Define("HiggsPt", "findHiggsPt(Particle.PID, Particle.PT)")

hHiggsM = dHiggs.Histo1D(ROOT.RDF.TH1DModel("hHiggsM", "HiggsMass", 75, 50, 200), "HiggsM")
hHiggsPt = dHiggs.Histo1D(ROOT.RDF.TH1DModel("hHiggsPt", "HiggsPt", 50, 0, 500), "HiggsPt")
hHiggsM.GetXaxis().SetTitle("m_{Higgs} [GeV]")
hHiggsM.GetYaxis().SetTitle("Nevents / 2 GeV")
hHiggsPt.GetXaxis().SetTitle("p_{T}^{Higgs} [GeV]")
hHiggsPt.GetYaxis().SetTitle("Nevents / 10 GeV")
hHiggsPtXS = hHiggsPt.Clone()
hHiggsPtXS.SetName("hHiggsPtXS")
hHiggsPtXS.SetTitle("HiggsPtXS")
hHiggsPtXS.GetYaxis().SetTitle("d#sigma / dp_{T} [fb/GeV]")
for i in range(1, hHiggsPtXS.GetNbinsX() + 1):
	oldBinError = hHiggsPtXS.GetBinError(i)
	hHiggsPtXS.SetBinContent(i, (hHiggsPtXS.GetBinContent(i) / (lumi * hHiggsPtXS.GetBinWidth(i))))
	hHiggsPtXS.SetBinError(i, oldBinError / (lumi * hHiggsPtXS.GetBinWidth(i)))

fOut = ROOT.TFile(outputPath, "recreate")
hHiggsM.Write()
hHiggsPt.Write()
hHiggsPtXS.Write()
fOut.Close()
print("Total XS: {} fb".format(hHiggsPtXS.Integral("width")))