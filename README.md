# An Introduction to Hbb Repository

This repository is about my ZH(bb) analysis macros.

`ZpeakSig` is about the analysis of Z to mu+ mu-. This analysis is the signal process. `ZpeakBkg` is about the analysis of the background processes. Background proccesses include
diboson background, Z+jets background, ttbar background, single t background, and QCD background. However, the analysis methods are same. I separate them unintentionally. But the analyzer in these folders can only
fill the TH1 histograms. So I will not use these macros for ZH analysis.

`ZH` contains the analyzer and plot macros in my ZH(bb) work. The subfolder `PlotMacros` includes macros which I use to plot histograms, stack histograms and Data/MC figure. The `DistributionStacks.py` can plot histograms of MC samples and data easily and plot Data/MC of different categories. 

`Cutflow` is the analysis about the cut-flow of dijet signal process and background process. 

`Tools` includes some macros which help me work more effective. Now there is a macro to create a lots of CRAB scripts. There also has a simple shell to submit massive jobs to CRAB at same time. There also some macros to make and modify the database json file. 

