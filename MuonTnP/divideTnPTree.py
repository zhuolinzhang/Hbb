import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-n", help="name of dataset")
parser.add_argument("-c", default="2018UL", help="campaign of dataset")
args = parser.parse_args()

ptEdgeList = [15, 20, 25, 30, 40, 50, 60, 120]
absEtaEdgeList = [0, 0.9, 1.2, 2.1, 2.4]

for etaIndex, etaHistEdge in enumerate(absEtaEdgeList):
	if etaHistEdge != 2.4:
		etaBinLow = etaHistEdge
		etaBinUp = absEtaEdgeList[etaIndex + 1]
	else: break
	for ptIndex, ptHistEdge in enumerate(ptEdgeList):
		if ptHistEdge != 120:
			ptBinLow = ptHistEdge
			ptBinUp = ptEdgeList[ptIndex + 1]
			print("Cut {}<abseta<={} {}<pt<={}".format(etaBinLow, etaBinUp, ptBinLow, ptBinUp))
			os.system("/cms/user/zhangzhuolin/TTreeReducer/TnPUtils/skimTree {0}.root {0}_TnP_{1}_{2}_{3}.root -c \"abseta > {4} && abseta <= {5} && pt > {6} && pt <= {7}\"".format(args.n, args.c, etaIndex, ptIndex, etaBinLow, etaBinUp, ptBinLow, ptBinUp))
		else: continue