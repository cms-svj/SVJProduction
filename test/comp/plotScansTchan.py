import os,sys
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/SVJ/Production/batch"))
from signals_tchan_scan_part0 import flist as flist0
from signals_tchan_scan_part1 import flist as flist1
from signals_tchan_scan_part2 import flist as flist2
flist = flist0+flist1+flist2

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-n","--num", dest="num", type=int, default=2000, help="number of events per job for model point w/ weight 1.0 (before filter)")
args = parser.parse_args()

from array import array
import ROOT as r
r.gROOT.SetBatch(True)

scans = [
    ("mDark", {"rinv": 0.3, "yukawa": 1.0}),
    ("rinv", {"mDark": 20, "yukawa": 1.0}),
    ("yukawa", {"mDark": 20, "rinv": 0.3}),
]

axnames = {
    "mMediator": "m_{Z'} [GeV]",
    "rinv": "r_{inv}",
    "mDark": "m_{dark} [GeV]",
    "yukawa": "#lambda_{dark}",
}

for scan,params in scans:
    x = []
    y = []
    z = []
    for point in flist:
        good_point = True
        for param,pval in params.iteritems():
            if point[param]!=pval: good_point = False
        if not good_point: continue
        x.append(point["mMediator"])
        y.append(point[scan])
        z.append(float(point["maxEvents"])/float(args.num))
    xx = array('d',x)
    yy = array('d',y)
    zz = array('d',z)
    gwt = r.TGraph2D(len(x),xx,yy,zz)
    gwt.SetTitle("")
    gwt.GetXaxis().SetTitle(axnames["mMediator"])
    gwt.GetYaxis().SetTitle(axnames[scan])
    gwt.GetZaxis().SetTitle("weight")
    cwt = r.TCanvas()
    cwt.SetRightMargin(cwt.GetLeftMargin())
    # view in xy plane
    cwt.SetTheta(89.9999)
    cwt.SetPhi(0.00001)
#    cwt.SetLogz(1)
    gwt.GetXaxis().SetTitleOffset(1.1)
    gwt.GetYaxis().SetTitleOffset(1.35)
    gwt.GetZaxis().SetTitleOffset(0.9)
    gwt.Draw("PCOLZ")
    params_name = "_".join(["{}-{}".format(key,val) for key,val in sorted(params.iteritems())])
    oname = "weight_scan_{}_{}".format(scan,params_name)
    print(oname)
    cwt.Print(oname+".png","png")
    cwt.Print(oname+".pdf","pdf")
