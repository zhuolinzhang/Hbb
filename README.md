# An Introduction to Hbb Repository

This repository is about my ZH(bb) analysis macros.

`ZpeakSig` is about the analysis of Z to mu+ mu-. This analysis is the signal process. `ZpeakBkg` is about the analysis of the background processes. Background proccesses include
diboson background, Z+jets background, ttbar background, single t background, and QCD background. However, the analysis methods are same. I separate them unintentionally. 

`zpeakCutflow` is the analysis about the cut-flow of signal process and background process. The scripts are too old and too naive. I don't plan to use them any more. So this folder is planned to **abolish**.

`Tools` include some macros which help me work more effective. Now there is a macro to create a lots of CRAB scripts. There also has a simple shell to submit massive jobs to CRAB at same time. There also some macros to make and modify the database json file. I plan to add some combine macros in this folder.

`PlotMacros` include macros which I use to plot histograms, stack histograms and Data/MC figure. The `DistributionStacks.py` can plot histograms of MC samples and data easily and plot Data/MC of different categories. 

**Attention:** There are some serious errors in the ZH analyzer macro. This analyzer will be reconstruct very soon. 
