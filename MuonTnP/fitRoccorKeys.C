#include <string>
#include <vector>
#include <iostream>
#include "RooFit.h"
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooKeysPdf.h"
#include "RooGaussian.h"
#include "RooFFTConvPdf.h"
#include "RooPlot.h"
#include "RooHist.h"
#include "TColor.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TLatex.h"
#include "TAxis.h"
 
void fitRooKeys()
{
	std::vector<std::string> yearList = {"2018", "2017", "2016", "2016APV"};
	std::vector<std::string> dataSetTypeList = {"noRoccor", "roccor"};
	std::vector<std::string> fitResult = {};

	for (auto year : yearList)
	{
		for (auto dataSetType : dataSetTypeList)
		{
			std::cout << "Start fitting " << year << " " << dataSetType << std::endl;
			std::string fitMassName = "z_mass_no_roccor";
			std::string roccorStatus = "Before";
			if (dataSetType == "roccor")
			{
				fitMassName = "z_mass_roccor";
				roccorStatus = "After";
			}
			std::string fileName = "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/DYTreeNoBCut" + year + "Skim.root";
			TFile *f = new TFile(fileName.data(), "read");
			TTree *zhTree = (TTree*) f->Get("dyTree");
			RooRealVar zM(fitMassName.data(), fitMassName.data(), 75, 105);
			RooDataSet ds("ds", "ds", zhTree, RooArgSet(zM));
			RooKeysPdf kest("kest", "kest", zM, ds, RooKeysPdf::MirrorBoth);

			RooRealVar mass("mass", "mass of Z boson", 0, -5, 5);
			RooRealVar sigma("sigma", "width of Gauss", 0.9, 0.05, 5.0);
			RooGaussian gauss("gauss", "gauss", zM, mass, sigma);
			RooFFTConvPdf sig("sig", "sig", zM, kest, gauss);

			sig.fitTo(ds, RooFit::NumCPU(12, 0));

			auto xFrameCorr = zM.frame();
			ds.plotOn(xFrameCorr, RooFit::MarkerStyle(24));
			if (dataSetType == "noRoccor") sig.plotOn(xFrameCorr, RooFit::LineColor(kRed));
			else sig.plotOn(xFrameCorr, RooFit::LineColor(kBlue));
			
			auto pullHist = xFrameCorr->pullHist();

			TCanvas *cComp = new TCanvas("cComp", "cComp", 800, 600);
			TPad *topPad = new TPad("topPad", "topPad", 0, 0.3, 1, 1);
			TPad *bottomPad = new TPad("bottomPad", "bottomPad", 0, 0, 1, 0.3);
			cComp->Draw();
			topPad->Draw();
			bottomPad->Draw();
			topPad->cd();
			topPad->SetBottomMargin(0);
			TLatex *yearMark = new TLatex();
			yearMark->SetTextFont(42);
			xFrameCorr->SetTitle("");
			xFrameCorr->Draw();
			xFrameCorr->GetYaxis()->SetTitle("A.U. / 0.3 GeV");
			xFrameCorr->GetYaxis()->SetTitleSize(0.05);
			xFrameCorr->GetYaxis()->SetLabelSize(0.05);
			xFrameCorr->GetYaxis()->SetTitleOffset(1);
			xFrameCorr->GetXaxis()->SetRangeUser(75, 105);
			topPad.Update()
			latexLeftPointX = 0.6
			if year == "2016APV":
				latexLeftPointX = 0.55
			yearMark.DrawLatexNDC(latexLeftPointX, 0.92, "{} RoccoR (13 TeV, {})".format(roccorStatus, year))
			bottomPad.cd()
			bottomPad.SetTopMargin(0)
			bottomPad.SetBottomMargin(0.3)
			pullHist.SetTitle()
			pullHist.SetMarkerStyle(24)
			pullHist.GetYaxis().SetTitle("Pull = #frac{MC - Fit}{#sigma_{MC}}")
			pullHist.GetYaxis().SetTitleSize(0.1)
			pullHist.GetYaxis().SetLabelSize(0.13)
			#pullHist.GetYaxis().SetNdivisions(2)
			#pullHist.GetYaxis().SetTickLength(0.01)
			pullHist.GetYaxis().SetTitleOffset(0.4)
			#pullHist.GetYaxis().SetLimits(-3.9, 3.9)
			pullHist.GetXaxis().SetTitle("M_{Z} [GeV]")
			pullHist.GetXaxis().SetTitleSize(0.13)
			pullHist.GetXaxis().SetLabelSize(0.13)
			pullHist.GetXaxis().SetTitleOffset(1.1)
			pullHist.GetXaxis().SetRangeUser(75, 105)
			pullHist.Draw("ap")
			bottomPad.Update()
			cComp.Update()
			cComp.SaveAs("chap6_{}_{}.pdf".format(dataSetType, year))

			hPdf = sig.createHistogram("hPdf", zM, ROOT.RooFit.Binning(100, 75, 105))
			massFit = hPdf.GetMean()
			massFitErr = hPdf.GetMeanError()
			fitResultPerYear = "{}_{}: mZ = {} +/- {}".format(year, dataSetType, massFit, massFitErr)
			print(fitResultPerYear)
			fitResult += "{}\n".format(fitResultPerYear)
		}
	}
}