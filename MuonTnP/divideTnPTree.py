import os

edgeList = [0, 45, 80, 120, 200, 350, 450, 600]

for index, binEdge in enumerate(edgeList):
    if binEdge != 600:
        lowerEdge = binEdge
        upperEdge = edgeList[index + 1]
        os.system("/cms/user/zhangzhuolin/TTreeReducer/TnPUtils/skimTree DoubleMuon.root DoubleMuon_TnP_2018UL_{}.root -c \"pt > {} && pt <= {}\"".format(index, lowerEdge, upperEdge))
    else: break
