import os,sys
sys.path.append(os.path.expandvars("$CMSSW_BASE/src/SVJ/Production/batch"))
from signals_boosted_scan import flist

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-n","--num", dest="num", type=int, default=1000, help="number of events per job for model point w/ weight 1.0 (before filter)")
args = parser.parse_args()

from array import array
import ROOT as r
r.gROOT.SetBatch(True)

scans = [
    ("rinv", {"mDark": 1}),
    ("rinv", {"mDark": 5}),
    ("rinv", {"mDark": 10}),
]

axnames = {
    "mMediator": "m_{Z'} [GeV]",
    "rinv": "r_{inv}",
    "mDark": "m_{dark} [GeV]",
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
