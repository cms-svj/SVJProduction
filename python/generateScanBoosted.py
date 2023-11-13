import FWCore.ParameterSet.Config as cms

from SVJ.Production.svjHelper import svjHelper

from collections import OrderedDict
from copy import deepcopy
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np
import os, json

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
parser.add_argument("-n","--num", dest="num", type=int, default=1000, help="number of events per job for model point w/ weight 1.0 (before filter)")
parser.add_argument("-j","--jobs", dest="jobs", type=int, default=20, help="number of jobs")
parser.add_argument("-a","--acc", dest="acc", type=float, default=0.0, help="increase number of events based on acceptance up to this maximum factor")
args = parser.parse_args()

# complete set of parameter values
params = OrderedDict([
    ("mZprime", range(200,600,50)),
    ("mDark", [1,5,10]),
    ("rinv", [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
])

# cross sections
with open(os.path.expandvars('$CMSSW_BASE/src/SVJ/Production/test/dict_xsec_Zprime_boosted.txt'),'r') as xfile:
    xsecs = {int(xline.split('\t')[0]): float(xline.split('\t')[1]) for xline in xfile}

# acceptance values vs. each param
acc = OrderedDict([
    ("mDark", ([1,5,10],[0.12,0.12,0.11])),
    ("mZprime", ([200,250,300,350,400,450,500,550],[0.081,0.089,0.099,0.11,0.12,0.12,0.13,0.14])),
    ("rinv", ([0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],[0.017,0.024,0.045,0.082,0.11,0.12,0.13,0.13,0.12,0.11,0.081,0.058])),
])
base_mZprime = 350
base_index = acc["mZprime"][0].index(base_mZprime)
# acceptance w/ benchmark param values
base_acc = acc["mZprime"][1][base_index]
# include relative cross section in mZprime acc
base_xsec = xsecs[base_mZprime]
for i,mass in enumerate(acc["mZprime"][0]):
    acc["mZprime"][1][i] *= base_xsec/xsecs[mass]
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

# append process parameters for each model point
helper = svjHelper()
points = []
numevents_before = 0
numevents_after = 0
base_filter_eff = 0.5
flist = []
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

    maxEvents = int(args.num*weight)
    flist.append(OrderedDict([("channel", "s"), ("mMediator", mZprime), ("mDark", mDark), ("rinv", rinv), ("alpha", alpha), ("maxEvents", maxEvents)]))

    numevents_before += maxEvents*args.jobs
    numevents_after += maxEvents*args.jobs*filter_eff

# some info on the scan
print("This scan will contain "+str(len(sigs))+" model points, "+str(int(numevents_before))+" events before filter, "+str(int(numevents_after))+" events after filter")

with open(os.path.expandvars("$CMSSW_BASE/src/SVJ/Production/batch/signals_boosted_scan.py"),'w') as ofile:
    lines = ["flist = ["] + ['    '+json.dumps(d)+',' for d in flist] + ["]"]
    ofile.write('\n'.join(lines))
