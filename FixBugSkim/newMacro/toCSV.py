import uproot
from uproot.interpretation import library
import pandas as pd

tree = uproot.open("/Users/zhangzhuolin/Work/Hbb/SkimNtuple/newMacro/FlatTrees/ZHTree.root:ZHCandidates")
csv = tree.arrays(library='pd')

csv.to_csv('test.csv')