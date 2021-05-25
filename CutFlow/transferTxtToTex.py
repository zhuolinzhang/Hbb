import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--input", type=str, help="The input .txt file path")
parser.add_argument("--output", type=str, help="The output .tex file path")
args = parser.parse_args()

def checkOutPath(path):
    newPathList = path.split('/')
    newPathList.pop()
    str = '/'
    newPath = str.join(newPathList)
    if os.path.exists(newPath): pass
    else: os.mkdir(newPath)

df = pd.read_csv(args.input, delimiter='\t')
df = df.set_index("Name")
checkOutPath(args.output)
df.to_latex(args.output)