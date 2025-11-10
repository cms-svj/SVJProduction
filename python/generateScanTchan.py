import FWCore.ParameterSet.Config as cms

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

# function to use pair of arrays as lookup table
def find_nearest(val,xy):
    x_array = np.asarray(xy[0])
    idx = (np.abs(x_array - val)).argmin()
    return xy[1][idx]

# function to retrieve multiplied relative acceptance
def get_acc(point,args):
    this_acc = 1.0
    for param,pval in point.iteritems():
        if param not in acc.keys(): continue
        pval = args.alpha_vals[pval] if param=="alpha" else pval
        this_acc *= find_nearest(pval,args.acc[param])/args.base_acc
    return this_acc

def get_oname(args):
    oname = "$CMSSW_BASE/src/SVJ/Production/batch/signals_tchan_scan{}.py".format('_'+args.suff if len(args.suff)>0 else '')
    return oname

def dump_flist(oname, flist):
    with open(os.path.expandvars(oname),'w') as ofile:
        lines = ["flist = ["] + ['    '+json.dumps(d)+',' for d in flist] + ["]"]
        ofile.write('\n'.join(lines))

def import_flist(fname):
    return __import__(fname.replace(".py","")).flist

def pop_keys(odict, keys):
    for key in keys:
        odict.pop(key)
    return odict


def gen_base(args):
    if not args.suff: args.suff = "base"

    # complete set of parameter values
    params = OrderedDict([
        ("mMed", range(500,1000,100)+range(1000,4100,500)),
        ("mDark", [1,5] + range(10,110,10)),
        ("rinv", [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
        ("yukawa", [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]),
    ])

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

    flists = [[],[]]
    alpha = "peak"
    for ilist, (flist, sigset) in enumerate(zip(flists,[sigs,sigs_gridpack])):
        for point in sorted(sigset):
            mMed = point[0]
            mDark = point[1]
            rinv = point[2]
            yukawa = point[3]

            flist.append(OrderedDict([
                ("channel", "t"),
                ("mMediator", mMed),
                ("mDark", mDark),
                ("rinv", rinv),
                ("alpha", alpha),
                ("yukawa", yukawa),
            ]))
            # used in later modes
            if ilist==0:
                flist[-1].update(OrderedDict([
                    ("lastPart", 0),
                    ("total", 0),
                ]))

    flist = flists[0]
    flist_gridpack = flists[1]

    print("This scan will contain {} model points".format(len(flist))
    print("This scan requires {} gridpacks".format(len(flist_gridpack))

    if not args.dryRun:
        oname = get_oname()
        dump_flist(oname, flist)
        oname2 = oname.replace(".py","_gridpack.py")
        dump_flist(oname2, flist_gridpack)

# common operations shared by "first" and "extend" modes
def gen_scan(args, weight_fn):
    flist_input = import_flist(args.input)
    flist_output = []
    flist = []
    # append parameters for each model point
    numevents_before = 0
    numevents_after = 0
    base_filter_eff = args.mg_filter_eff*args.p8_filter_eff
    # single-model quantities
    numprod_default = args.num*args.jobs*base_filter_eff
    numsel_default = numprod_default*(args.base_acc/100.)
    numprod_min = 1e10
    numprod_max = 0
    numsel_min = 1e10
    numsel_max = 0
    for sig in flist_input:
        flist_output.append(deepcopy(sig))

        filter_eff = base_filter_eff
        # rinv=0 : all events pass p8 filter
        if sig["rinv"]==0.0:
            filter_eff = args.mg_filter_eff

        firstPart = sig["lastPart"]+1
        total = sig["total"]

        # scaling (acceptance or extension)
        this_acc = get_acc(point,args)
        weight = weight_fn(point, args, total, this_acc)
        if weight==0:
            continue
        flist.append(deepcopy(sig))
        flist[-1] = pop_keys(flist[-1], ["lastPart","total"])

        maxEvents = args.num
        nParts = args.jobs
        if args.scale=="num":
            maxEvents = int(maxEvents*weight)
        elif args.scale=="jobs":
            nParts = int(nParts*weight)
        numevents_this = maxEvents*nParts
        total += numevents_this

        flist[-1].update(OrderedDict[("maxEvents", maxEvents), ("nParts", nParts), ("firstPart", firstPart)])
        # track total to allow extensions of extensions based on %
        flist_output[-1].update(OrderedDict[("lastPart", firstPart + nParts - 1), ("total", total)])

        # todo: make another version of these numbers using total instead of numevents_this
        numevents_filter = numevents_this*filter_eff
        numevents_before += numevents_this
        numevents_after += numevents_filter
        numprod_min = min(numprod_min, numevents_filter)
        numprod_max = max(numprod_max, numevents_filter)
        sel_acc = this_acc*args.base_acc/100.
        numsel_min = min(numsel_min, numevents_filter*sel_acc)
        numsel_max = max(numsel_max, numevents_filter*sel_acc)

    # some info on the scan
    print("This scan will contain "+str(len(sigs))+" model points, "+str(int(numevents_before))+" events before filter, "+str(int(numevents_after))+" events after filter")
    print("Number of events per model (after filter): {:0.0f} ({:0.0f}, {:0.0f})".format(numprod_default, numprod_min, numprod_max))
    print("Number of events per model (after filter & preselection): {:0.0f} ({:0.0f}, {:0.0f})".format(numsel_default, numsel_min, numsel_max))

    if not args.dryRun:
        # in-place update of base list with new totals
        dump_flist(args.input, flist_output)

        oname = get_oname(args)

        # todo: split by maxEvents*nParts using heap algorithm
        def split(coll, n):
            d, r = divmod(len(coll), n)
            return (coll[i*d+min(i,r) : (i+1)*d+min(i+1,r)] for i in range(n))

        flist = list(split(flist, args.parts))
        oname1 = oname
        if args.parts>1:
            oname1 = oname.replace(".py","_part{}.py")
        for part in range(args.parts):
            dump_flist(oname1.format(part+1), flist[part])

def gen_first(args):
    # safe/clipped version
    def clip_acc(point, args, total, this_acc):
        weight = 1.0
        # down-weight rinv=0 b/c all events pass p8 filter
        if point["rinv"]==0.0:
            weight = args.p8_filter_eff

        if args.acc > 1:
            this_acc = get_acc(point,args)
            min_weight = weight
            max_weight = weight*args.acc
            weight = np.clip(weight/this_acc,min_weight,max_weight)
        return weight

    gen_scan(args, clip_acc)

def gen_extend(args):
    # extension values
    flist_ext = __import__(args.extend.replace(".py","")).flist

    # check for extension weights
    def get_ext(point, args, total, this_acc):
        skip_keys = ["maxEvents", "nParts", "firstPart", "total"]
        try:
            match = next([d for d in flist_ext if all([d.get(key) == value for key, value in point.iteritems() if key not in skip_keys])])
        except:
            return 0

        # todo: separate max for this?
        new_total = total * match["extend"]
        weight = new_total/(args.num*args.jobs)
        return weight

    gen_scan(args, get_ext)

def main():
    _parser_common = ArgumentParser(add_help=False)
    _parser_common.add_argument("-x","--suff", dest="suff", type=str, default="", help="suffix for scan dictionary filename")
    _parser_common.add_argument("-d","--dryRun", dest="dryRun", default=False, action="store_true", help="dry run, i.e. do not create scan dictionaries, but just print info")

    _parser_scan = ArgumentParser(add_help=False)
    _parser_scan.add_argument("-n","--num", dest="num", type=int, default=2000, help="number of events per job for model point w/ weight 1.0 (before filter)")
    _parser_scan.add_argument("-j","--jobs", dest="jobs", type=int, default=20, help="number of jobs for model point w/ weight 1.0 (before filter)")
    _parser_scan.add_argument("-s","--scale", dest="scale", type=str, required=True, choices=["num","jobs"], help="scale up selected quantity based on acceptance weights")
    _parser_scan.add_argument("-p","--parts", dest="parts", type=int, default=1, help="split output job dictionary into multiple parts for submission")
    _parser_scan.add_argument("-i","--input", dest="input", type=str, default="", help=".py file with input base flist of samples")

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers()

    parser_base = subparsers.add_parser("base", help="generate base list of signals", parents=[_parser_common])
    parser_base.set_defaults(func=gen_base)

    parser_first = subparsers.add_parser("first", help="generate first scan (incl. acceptance weights)", parents=[_parser_common, _parser_scan])
    parser_first.add_argument("-a","--acc", dest="acc", type=float, default=0.0, help="increase number of events based on acceptance up to this maximum factor")
    parser_first.set_defaults(func=gen_first)

    parser_extend = subparsers.add_parser("extend", help="generate extension of scan (by percentage)", parents=[_parser_common, _parser_scan])
    parser_extend.add_argument("-e","--extend", dest="extend", type=str, default="", help=".py file with flist of samples to extend")
    parser_extend.set_defaults(func=gen_extend)

    args = parser.parse_args()
    # append some common values
    args.mg_filter_eff = 0.8
    args.p8_filter_eff = 0.5
    # convert named alpha values to numerical
    args.alpha_vals = {
        "peak": -2,
        "high": -1,
        "low": -3,
    }
    # acceptance values (%) vs. each param
    # no alpha variations; yukawa variations not done yet
    args.acc = OrderedDict([
        ("mMediator", ([600,800,1000,1500,2000,3000,4000],[1.88,3.89,4.84,5.59,4.41,3.35,3.31])),
        ("mDark", ([1,20,50,100],[6.18,4.41,4.46,4.61])),
        ("rinv", ([0.1,0.3,0.5,0.7],[1.81,4.41,4.95,4.32])),
        ("yukawa", ([1],[4.41])),
    ])
    # acceptance (%) w/ benchmark param values
    args.base_acc = 4.41

    args.func(args)

if __name__=="__main__":
    main()
