from Configuration.Applications.ConfigBuilder import filesFromList
import cPickle as pickle
from StringIO import StringIO
import sys

class NullIO(StringIO):
    def write(self, txt):
        pass

# suppress pointless printouts
sys.stdout = NullIO()
files = filesFromList("Neutrino_E-10_gun_RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2_GEN-SIM-DIGI-RAW.txt")
sys.stdout = sys.__stdout__

# store list
pickle.dump( files[0], open("Neutrino_E-10_gun_RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2_GEN-SIM-DIGI-RAW.pkl","wb") )


