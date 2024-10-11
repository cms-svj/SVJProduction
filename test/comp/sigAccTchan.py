from collections import OrderedDict
from ROOT import TGraph, TCanvas

# from generateScanTchan.py
acc = OrderedDict([
    ("mMed", ("m_{#Phi}",[600,800,1000,1500,2000,3000,4000],[1.88,3.89,4.84,5.59,4.41,3.35,3.31])),
    ("mDark", ("m_{dark}",[1,20,50,100],[6.18,4.41,4.46,4.61])),
    ("rinv", ("r_{inv}",[0.1,0.3,0.5,0.7],[1.81,4.41,4.95,4.32])),
])

for p,pdict in acc.iteritems():
    a, x, y = pdict
    x = pdict[1]
    y = pdict[2]
    y = [yy/100. for yy in y]

    from array import array
    xx = array('d', x)
    yy = array('d', y)

    gs = TGraph(len(x),xx,yy)
    gs.SetTitle("")
    gs.GetXaxis().SetTitle(a)
    gs.GetYaxis().SetTitle("acceptance")
    gs.GetYaxis().SetRangeUser(0,0.1)
    cy = TCanvas()
    gs.Draw("ap")
    oname = "acc_vs_"+p+"_tchan"
    cy.Print(oname+".png","png")
    cy.Print(oname+".pdf","pdf")
