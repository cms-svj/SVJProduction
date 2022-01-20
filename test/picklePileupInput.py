from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from Configuration.Applications.ConfigBuilder import filesFromList
import cPickle as pickle
from StringIO import StringIO
import os, sys

class NullIO(StringIO):
    def write(self, txt):
        pass

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--dir", type=str, default="", help="name of EOS output directory")
parser.add_argument("-v", "--verbose", default=False, action="store_true", help="print commands")
parser.add_argument("premix", type=str, help="name of premix dataset")
args = parser.parse_args()

flat_name = args.premix[1:].replace("/","_")+'.txt'
cmd = 'dasgoclient -query="file dataset={}" | sort > {}'.format(args.premix, flat_name)
if args.verbose: print(cmd)
os.system(cmd)

# suppress pointless printouts
sys.stdout = NullIO()
files = filesFromList(flat_name)
sys.stdout = sys.__stdout__

# store list
pickle_name = flat_name.replace(".txt",".pkl")
pickle.dump( files[0], open(pickle_name,"wb") )

if len(args.dir)>0:
    cmd2 = "xrdcp {0} {1}/{0}".format(pickle_name, args.dir)
    if args.verbose: print(cmd2)
    os.system(cmd2)
