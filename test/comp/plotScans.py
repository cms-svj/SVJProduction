from SVJ.Production.SVJ_Scan_2016_TuneCUETP8M1_13TeV_pythia8_cff import points
from collections import OrderedDict
from array import array
from ROOT import *

# convert named alpha values to numerical
alpha_vals = {
    "peak": -2.0,
    "high": -1.0,
    "low": -3.0,
}

def parseName(point):
    name = point["name"]
    namesplit = name.split('_')[1:]
    vals = OrderedDict()
    for n in namesplit:
        nsplit = n.split('-')
        vals[nsplit[0]] = alpha_vals[nsplit[1]] if nsplit[0]=="alpha" else float(nsplit[1])
    vals["weight"] = point["weight"]
    return vals

parsed = [parseName(point) for point in points]

scans = OrderedDict([
    ("mDark", {"rinv": 0.3, "alpha": alpha_vals["peak"]}),
    ("alpha", {"rinv": 0.3, "mDark": 20.0}),
    ("rinv", {"mDark": 20.0, "alpha": alpha_vals["peak"]}),
])

axnames = {
    "mZprime": "m_{Z'} [GeV]",
    "rinv": "r_{inv}",
    "mDark": "m_{dark} [GeV]",
    "alpha": "#alpha_{dark}",
}

for scan,params in scans.iteritems():
    x = []
    y = []
    z = []
    for point in parsed:
        good_point = True
        for param,pval in params.iteritems():
            if point[param]!=pval: good_point = False
        if not good_point: continue
        x.append(point["mZprime"])
        y.append(point[scan])
        z.append(point["weight"])
    xx = array('d',x)
    yy = array('d',y)
    zz = array('d',z)
    gwt = TGraph2D(len(x),xx,yy,zz)
    gwt.SetTitle("")
    gwt.GetXaxis().SetTitle(axnames["mZprime"])
    gwt.GetYaxis().SetTitle(axnames[scan])
    gwt.GetZaxis().SetTitle("weight")
    cwt = TCanvas()
    cwt.SetRightMargin(cwt.GetLeftMargin())
    # view in xy plane
    cwt.SetTheta(89.9999)
    cwt.SetPhi(0.00001)
#    cwt.SetLogz(1)
    gwt.GetXaxis().SetTitleOffset(1.1)
    gwt.GetYaxis().SetTitleOffset(1.35)
    gwt.GetZaxis().SetTitleOffset(0.9)
    gwt.Draw("PCOLZ")
    oname = "weight_scan_"+scan
    cwt.Print(oname+".png","png")
    cwt.Print(oname+".eps","eps")
    import os
    os.popen("epstopdf "+oname+".eps")
