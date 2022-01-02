import uproot
xsFile = uproot.open('./smXS/HiggsXS.root')
massTotal = xsFile['recoHiggsXS'].axis().centers()
print(massTotal)