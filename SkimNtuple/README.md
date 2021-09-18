# An Introduction to the `SkimNtuple` Toolkit

In the `cutByTTreeReader` folder, `ntupleReducerUL.cc` and `ntupleReducerReReco.cc`are used to skim `TTree`s for UL campaign and pre-UL campaign. This macro used `TTreeReader` to transform the `std::vector` stored in `TBranch`s to `float` and cut the `TTree`. But these macros are very slow, they are needed to submit to HTCondor. If these macros are executed locally, we will wait to the cows come home.

In the `cutByRDF` folder, `ntupleSkimmer.C` and `ntupleSkimmer.py` are used to skim `TTree`s. The RDataFrame is a very efficient framework. The speed of running RDF macros is dozens of times faster than `TTreeReader` macros. After my validation, these two macros can replace the old deprecated `TTreeReader` macros now. But I will keep old macros to some time to make sure there are no bugs in the RDF macros.

`SE2T3` is a useful tool that copies `.root` files from T2 to my T3. We can run `python3 T22T3.py --mode 1,2,3,4` to use different functions. The script can check the result of a CRAB job (has output files or not), copy files from T2 to T3, generate `HTCondor` bash scripts, and `hadd` scripts to merge `.root` files. The scripts in the `Tools` subfolder can be executed independently.

`GenerateReduceScript.py` and `GenerateReduceRDFScript.py` can generate `HTCondor` bash scripts (for IHEP lxslc) to execute skimmer. 