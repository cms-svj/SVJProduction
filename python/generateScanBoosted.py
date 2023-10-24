import FWCore.ParameterSet.Config as cms

from SVJ.Production.svjHelper import svjHelper

from collections import OrderedDict
from copy import deepcopy
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np

# implementation of recursive loop over any number of dimensions
# creates grid of all possible combinations of parameter values
def varyAll(pos,paramlist,sig,sigs):
    param = paramlist[pos][0]
    vals = paramlist[pos][1]
    for v in vals:
        stmp = sig[:]+[v]
        # check if last param
        if pos+1==len(paramlist):
            sigs.add(tuple(stmp))
        else:
            varyAll(pos+1,paramlist,stmp,sigs)

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-n","--num", dest="num", type=int, default=20000, help="number of events for model point w/ weight 1.0 (before filter)")
parser.add_argument("-a","--acc", dest="acc", type=float, default=0.0, help="increase number of events based on acceptance up to this maximum factor")
args = parser.parse_args()

# specification of tunes
tune_loc = "Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi"
tune_block = "pythia8CP5SettingsBlock"
tune_suff = "TuneCP5_13TeV_pythia8"
gen_tag = "cms.InputTag('generator','unsmeared')"

# complete set of parameter values
params = OrderedDict([
    ("mZprime", range(200,600,50)),
    ("mDark", [1,5,10]),
    ("rinv", [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
])

# acceptance values vs. each param
acc = OrderedDict([
    ("mDark", ([1,5,10],[0.13,0.12,0.11])),
    ("mZprime", ([200,250,300,350,400,450,500,550],[0.079,0.088,0.098,0.11,0.11,0.12,0.13,0.14])),
    ("rinv", ([0.1,0.3,0.7],[0.044,0.11,0.12])),
])
# acceptance w/ benchmark param values
base_acc = 0.11
# function to use pair of arrays as lookup table
def find_nearest(val,xy):
    x_array = np.asarray(xy[0])
    idx = (np.abs(x_array - val)).argmin()
    return xy[1][idx]
# function to retrieve multiplied relative acceptance
def get_acc(point):
    this_acc = 1.0
    for param,pval in point.iteritems():
        this_acc *= find_nearest(pval,acc[param])/base_acc
    return this_acc

# set to accumulate all scan points
sigs = set()

# 3D scan
params_3D = deepcopy(params)
varyAll(0,list(params_3D.iteritems()),[],sigs)
'''
# 2D scans vs. rinv
params_rinv = deepcopy(params)
params_rinv["mDark"] = [10]
varyAll(0,list(params_rinv.iteritems()),[],sigs)

# 2D scans vs. mDark
params_mDark = deepcopy(params)
params_mDark["rinv"] = [0.3]
varyAll(0,list(params_mDark.iteritems()),[],sigs)
'''
# format first part of output config
first_part = """
import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from {0} import * 
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)
""".format(tune_loc)

# append process parameters for each model point
helper = svjHelper()
points = []
numevents_before = 0
numevents_after = 0
base_filter_eff = 0.5
for point in sorted(sigs):
    mZprime = point[0]
    mDark = point[1]
    rinv = point[2]
    alpha = "peak"

    weight = 1.0
    filter_eff = base_filter_eff
    # down-weight rinv=0 b/c all events pass filter
    if rinv==0.0:
        weight = 0.5
        filter_eff = 1.0
    
    # account for relative acceptance
    if args.acc > 1:
        this_acc = get_acc(OrderedDict([("mZprime",mZprime),("mDark",mDark),("rinv",rinv)]))
        min_weight = weight
        max_weight = weight*args.acc
        weight = np.clip(weight/this_acc,min_weight,max_weight)

    helper.setModel("s",mZprime,mDark,rinv,alpha)
    
    pdict = {
        'weight': weight,
        'processParameters': helper.getPythiaSettings(),
        'name': helper.getOutName(outpre="SVJ"),
    }
    points.append(pdict)
    numevents_before += args.num*weight
    numevents_after += args.num*weight*filter_eff

# some info on the scan
print("This scan will contain "+str(len(sigs))+" model points, "+str(int(numevents_before))+" events before filter, "+str(int(numevents_after))+" events after filter")

# format last part of config (loop over all points)
# todo: get gridpack path
last_part = """
for point in points:
    basePythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock, 
        {0},
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(point['processParameters']),
        JetMatchingParameters = cms.vstring(),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            '{1}',
            'pythia8PSweightsSettings',
            'processParameters',
        )
    )

    generator.RandomizedParameters.append(
        cms.PSet(
            GridpackPath = cms.string(''),
            ConfigWeight = cms.double(point['weight']),
            ConfigDescription = cms.string(point['name']),
            PythiaParameters = basePythiaParameters,
        ),
    )

darkhadronZ2filter = cms.EDFilter("MCParticleModuloFilter",
    moduleLabel = {2},
    particleIDs = cms.vint32(51,53),
    multipleOf = cms.uint32(4),
    absID = cms.bool(True),
)

darkquarkFilter = cms.EDFilter("MCParticleModuloFilter",
    moduleLabel = {2},
    particleIDs = cms.vint32(4900101),
    multipleOf = cms.uint32(2),
    absID = cms.bool(True),
    min = cms.uint32(2),
    status = cms.int32(23),
)

ProductionFilterSequence = cms.Sequence(generator+darkhadronZ2filter+darkquarkFilter)
""".format(tune_block,tune_block.replace("Block",""),gen_tag)

with open("SVJ_Boosted_Scan_"+tune_suff+"_cff.py",'w') as ofile:
    ofile.write(first_part)
    ofile.write("\npoints = "+str(points)+"\n")
    ofile.write(last_part)
