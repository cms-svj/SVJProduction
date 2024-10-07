import FWCore.ParameterSet.Config as cms

from SVJ.Production.svjHelper import svjHelper

from collections import OrderedDict
from copy import deepcopy
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np
import math, os, json

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
parser.add_argument("-n","--num", dest="num", type=int, default=2000, help="number of events per job for model point w/ weight 1.0 (before filter)")
parser.add_argument("-j","--jobs", dest="jobs", type=int, default=20, help="number of jobs")
parser.add_argument("-a","--acc", dest="acc", type=float, default=0.0, help="increase number of events based on acceptance up to this maximum factor")
parser.add_argument("-p","--parts", dest="parts", type=int, default=1, help="split output job dictionary into multiple parts for submission")
args = parser.parse_args()

# specification of tunes
tune_loc = "Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi"
tune_block = "pythia8CP5SettingsBlock"
tune_suff = "TuneCP5_13TeV_pythia8"
gen_tag = "cms.InputTag('generator','unsmeared')"

# complete set of parameter values
params = OrderedDict([
    ("mMed", range(500,1000,100)+range(1000,4100,500)),
    ("mDark", [1,5] + range(10,110,10)),
    ("rinv", [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
    ("yukawa", [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]),
])

# convert named alpha values to numerical
alpha_vals = {
    "peak": -2,
    "high": -1,
    "low": -3,
}
# acceptance values (%) vs. each param
# no alpha variations; yukawa variations not done yet
acc = OrderedDict([
    ("mMed", ([600,800,1000,1500,2000,3000,4000],[1.88,3.89,4.84,5.59,4.41,3.35,3.31])),
    ("mDark", ([1,20,50,100],[6.18,4.41,4.46,4.61])),
    ("rinv", ([0.1,0.3,0.5,0.7],[1.81,4.41,4.95,4.32])),
    ("yukawa", ([1],[4.41])),
])
# acceptance (%) w/ benchmark param values
base_acc = 4.41
# function to use pair of arrays as lookup table
def find_nearest(val,xy):
    x_array = np.asarray(xy[0])
    idx = (np.abs(x_array - val)).argmin()
    return xy[1][idx]
# function to retrieve multiplied relative acceptance
def get_acc(point):
    this_acc = 1.0
    for param,pval in point.iteritems():
        pval = alpha_vals[pval] if param=="alpha" else pval
        this_acc *= find_nearest(pval,acc[param])/base_acc
    return this_acc

# set to accumulate all scan points
sigs = set()
sigs_gridpack = set()

# enforce mdark max value
def mdark_max(mMed):
    mdark = (mMed/(30*3.2))**1.25
    mdark_ceil10 = int(math.ceil(mdark/10.))*10
    mdark_ceil10 = max(20,min(mdark_ceil10, 100))
    return mdark_ceil10
for mMed in params["mMed"]:
    mdark = mdark_max(mMed)

    # 2D scans vs. rinv
    params_rinv = deepcopy(params)
    params_rinv["mMed"] = [mMed]
    params_rinv["mDark"] = [20]
    params_rinv["yukawa"] = [1.0]
    varyAll(0,list(params_rinv.iteritems()),[],sigs)

    # 2D scans vs. mDark
    params_mDark = deepcopy(params)
    params_mDark["mMed"] = [mMed]
    params_mDark["mDark"] = [1,5] + range(10,mdark+10,10)
    params_mDark["rinv"] = [0.3]
    params_mDark["yukawa"] = [1.0]
    varyAll(0,list(params_mDark.iteritems()),[],sigs)
    varyAll(0,list(params_mDark.iteritems()),[],sigs_gridpack)

    # 2D scans vs. yukawa
    params_yukawa = deepcopy(params)
    params_yukawa["mMed"] = [mMed]
    params_yukawa["mDark"] = [20]
    params_yukawa["rinv"] = [0.3]
    varyAll(0,list(params_yukawa.iteritems()),[],sigs)
    varyAll(0,list(params_yukawa.iteritems()),[],sigs_gridpack)

# append process parameters for each model point
helper = svjHelper()
points = []
numevents_before = 0
numevents_after = 0
mg_filter_eff = 0.8
p8_filter_eff = 0.5
base_filter_eff = mg_filter_eff*p8_filter_eff
alpha = "peak"
flist = []
# single-model quantities
numsel_default = args.num*args.jobs*base_filter_eff*(base_acc/100.)
numsel_min = 1e10
numsel_max = 0
for point in sorted(sigs):
    mMed = point[0]
    mDark = point[1]
    rinv = point[2]
    yukawa = point[3]

    weight = 1.0
    filter_eff = base_filter_eff
    # down-weight rinv=0 b/c all events pass p8 filter
    if rinv==0.0:
        filter_eff = mg_filter_eff
        weight = p8_filter_eff

    # account for relative acceptance
    this_acc = 1
    if args.acc > 1:
        this_acc = get_acc(OrderedDict([("mMed",mMed),("mDark",mDark),("rinv",rinv),("yukawa",yukawa)]))
        min_weight = weight
        max_weight = weight*args.acc
        weight = np.clip(weight/this_acc,min_weight,max_weight)

    maxEvents = int(args.num*weight)
    flist.append(OrderedDict([("channel", "t"), ("mMediator", mMed), ("mDark", mDark), ("rinv", rinv), ("alpha", alpha), ("yukawa", yukawa), ("maxEvents", maxEvents)]))

    numevents_this = maxEvents*args.jobs
    numevents_filter = numevents_this*filter_eff
    numevents_before += numevents_this
    numevents_after += numevents_filter
    sel_acc = this_acc*base_acc/100.
    numsel_min = min(numsel_min, numevents_filter*sel_acc)
    numsel_max = max(numsel_max, numevents_filter*sel_acc)

flist_gridpack = []
for point in sorted(sigs_gridpack):
    mMed = point[0]
    mDark = point[1]
    rinv = point[2]
    yukawa = point[3]

    flist_gridpack.append(OrderedDict([("channel", "t"), ("mMediator", mMed), ("mDark", mDark), ("rinv", rinv), ("alpha", alpha), ("yukawa", yukawa)]))

# some info on the scan
print("This scan will contain "+str(len(sigs))+" model points, "+str(int(numevents_before))+" events before filter, "+str(int(numevents_after))+" events after filter")
print("Number of events per model (after filter & preselection): {:0.0f} ({:0.0f}, {:0.0f})".format(numsel_default, numsel_min, numsel_max))

oname = "$CMSSW_BASE/src/SVJ/Production/batch/signals_tchan_scan.py"

def split(coll, n):
    d, r = divmod(len(coll), n)
    return (coll[i*d+min(i,r) : (i+1)*d+min(i+1,r)] for i in range(n))

flist = list(split(flist, args.parts))
oname1 = oname
if args.parts>1:
	oname1 = oname.replace(".py","_part{}.py")
for part in range(args.parts):
    with open(os.path.expandvars(oname1.format(part+1)),'w') as ofile:
        lines = ["flist = ["] + ['    '+json.dumps(d)+',' for d in flist[part]] + ["]"]
        ofile.write('\n'.join(lines))

oname2 = oname.replace(".py","_gridpack.py")
with open(os.path.expandvars(oname2),'w') as ofile:
    lines = ["flist = ["] + ['    '+json.dumps(d)+',' for d in flist_gridpack] + ["]"]
    ofile.write('\n'.join(lines))
