from SVJ.Production.SVJ_Boosted_Scan_TuneCP5_13TeV_pythia8_cff import points
from collections import OrderedDict
from array import array
import ROOT as r
r.gROOT.SetBatch(True)

def parseName(point):
    name = point["name"]
    namesplit = name.split('_')[1:]
    vals = OrderedDict()
    for n in namesplit:
        nsplit = n.split('-')
        try:
            vals[nsplit[0]] = float(nsplit[1])
        except:
            vals[nsplit[0]] = nsplit[1]
    vals["weight"] = point["weight"]
    return vals

parsed = [parseName(point) for point in points]

scans = [
    ("rinv", {"mDark": 1}),
    ("rinv", {"mDark": 5}),
    ("rinv", {"mDark": 10}),
]

axnames = {
    "mMed": "m_{Z'} [GeV]",
    "rinv": "r_{inv}",
    "mDark": "m_{dark} [GeV]",
}

for scan,params in scans:
    x = []
    y = []
    z = []
    for point in parsed:
        good_point = True
        for param,pval in params.iteritems():
            if point[param]!=pval: good_point = False
        if not good_point: continue
        x.append(point["mMed"])
        y.append(point[scan])
        z.append(point["weight"])
    xx = array('d',x)
    yy = array('d',y)
    zz = array('d',z)
    gwt = r.TGraph2D(len(x),xx,yy,zz)
    gwt.SetTitle("")
    gwt.GetXaxis().SetTitle(axnames["mMed"])
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
