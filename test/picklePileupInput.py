from Configuration.Applications.ConfigBuilder import filesFromList
import cPickle as pickle
from StringIO import StringIO
import sys

class NullIO(StringIO):
    def write(self, txt):
        pass

if len(sys.argv)>0:
    fname = sys.argv[1]
else:
    raise ValueError("Please specify input filename")

# suppress pointless printouts
sys.stdout = NullIO()
files = filesFromList(fname)
sys.stdout = sys.__stdout__

# store list
pickle.dump( files[0], open(fname.replace(".txt",".pkl"),"wb") )


