import json

def writeBatchScript(path: str, listLen: int) -> None:
	with open(path, 'w') as fBatch:
		fBatch.write("executable = /afs/cern.ch/work/z/zhuolinz/MC/genproductions/Utilities/calculateXSectionAndFilterEfficiency/calculateXSectionAndFilterEfficiency.sh\n")
		fBatch.write('arguments = -f /afs/cern.ch/work/z/zhuolinz/MC/genproductions/Utilities/calculateXSectionAndFilterEfficiency/condor/dataset_$(ProcID).txt -c RunII -d MINIAODSIM\n')
		fBatch.write("output = $(ClusterID).$(ProcID).out\n")
		fBatch.write("error = $(ClusterID).$(ProcID).err\n")
		fBatch.write("log = $(ClusterID).$(ProcID).log\n")
		fBatch.write("Proxy_filename = x509up_u132269\n")
		fBatch.write("Proxy_path = /afs/cern.ch/user/z/zhuolinz/private/$(Proxy_filename)\n")
		fBatch.write("should_transfer_files = YES\n")
		fBatch.write("when_to_transfer_output = ON_EXIT\n")
		fBatch.write("transfer_input_files = $(Proxy_path) /afs/cern.ch/work/z/zhuolinz/MC/genproductions/Utilities/calculateXSectionAndFilterEfficiency/condor/dataset_$(ProcID).txt\n")
		fBatch.write("queue {}".format(listLen))

database = []
with open("../MCInfo2018.json", 'r') as f:
	database = json.load(f)

dasList = []
for dataset in database:
	if "DYJetsToLL_M-50_HT-" in dataset["dasName"] or "TTTo2L2Nu" in dataset["dasName"]:
	#if "QCD" in dataset["dasName"] or "DYJetsToLL_M-50_HT-" in dataset["dasName"] or "TTTo2L2Nu" in dataset["dasName"]:
		dasList.append(dataset["dasName"])

with open("temp/dataset_DY_TT.txt", 'w') as f:
	for dbs in dasList:
		f.write(dbs + '\n')
	
writeBatchScript("temp/test.sub", 1)