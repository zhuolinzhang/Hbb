import argparse
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--mode", type=int, help='''1 - Only check results
2 - Check results and copy files 
3 - Check results, copy files and merge files''')
arg = parser.parse_args() 