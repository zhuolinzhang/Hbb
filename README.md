# An Introduction to Hbb Repository

This repository is about my ZH(bb) analysis macros.

`ZpeakSig` is about the analysis of Z to mu+ mu-. This analyzer can only produce `TH1` histograms. `ZH` contains the analyzer and plot macros in my ZH(bb) work. The subfolder `plot` includes macros which I use to plot histograms, stack histograms, the ratio of Data/MC and the ratio of sideband/signal region . The plot macro is an OOP macro which can plot histograms of MC samples and data easily and plot Data/MC of different categories. . The class `Hist` is defined in `plotConfig.py`. The functions of plot are in `plotConfig.py`. 

`Cutflow` include two files. One is the analysis about the cut-flow of ZH cuts. The other is the fit of the invariant mass spectrum of dijet. 

`Tools` includes some macros which help me work more effective. Now there is a macro to create a lots of CRAB scripts. There also has a simple shell to submit massive jobs to CRAB at same time. There also some macros to make and modify the database `json` file. 

## To-do List

✔ Update analyzer from reading cut-off ntuple to no-cut ntuple

✔ Write a macro to cut ntuple

✔ Update all macros which are incompatible with the new workflow

❌ Reconstruct plot macros (apply tdrstyle)