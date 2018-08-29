import sys
import math
from ROOT import *

def lambda_fn(x):
    n_c = 2
    n_f = 2
    b0 = 11.0/6.0*n_c - 2.0/6.0*n_f
    if x[0]==0: return 0
    lambdaHV = 1000*math.exp(-math.pi/(b0*x[0]))
    return lambdaHV

def alpha_fn(x):
    n_c = 2
    n_f = 2
    b0 = 11.0/6.0*n_c - 2.0/6.0*n_f
    if x[0]==0: return 0
    alpha = math.pi/(b0*math.log(1000/x[0]))
    return alpha


mZprimemin = 1000
mZprimemax = 4000

alpha = 0.5
file = TFile.Open("n_vs_mZprime_mDark_alpha-"+str(alpha)+".root")

graphs = []
colors = [kBlack, kBlue, kMagenta+2, kRed, kCyan+2, kMagenta]
masses = ["5","10","20","50","75","100"]
ymax = 0.0
leg = TLegend(0.15,0.525,0.3,0.825)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.05)
leg.SetTextFont(42)
for im,mDark in enumerate(masses):
    graph = file.Get("n_vs_mZprime_mDark_"+mDark)

    pts = graph.GetY()
    pts.SetSize(graph.GetN())
    xpts = graph.GetX()
    xpts.SetSize(graph.GetN())
    ymax_tmp = max(list(pts))
    ymax_idx = next(i for i,y in enumerate(list(pts)) if y==ymax_tmp)
    ymax = max(ymax,ymax_tmp)

    print "peak for mDark = "+str(mDark)+" :"
    print "mZprime = "+str(list(xpts)[ymax_idx-1:ymax_idx+2])
    print "nHV = "+str(list(pts)[ymax_idx-1:ymax_idx+2])

    graph.SetMarkerColor(colors[im])
    graphs.append(graph)
    leg.AddEntry(graph,"m_{d} = "+mDark,"p")

can = TCanvas()
can.SetTopMargin(0.13)
can.SetLeftMargin(0.13)
can.Draw()

nbins = 10
haxis = TH1F("axis","",nbins,mZprimemin,mZprimemax)
haxis.GetXaxis().SetNdivisions(210)
haxis.GetXaxis().SetTitle("m_{Z'} [GeV]")
haxis.GetYaxis().SetTitle("#LTn_{HV}#GT")
haxis.GetYaxis().SetRangeUser(0,ymax)
haxis.GetYaxis().SetTitleOffset(0.9)
haxis.Draw()

for ig,graph in enumerate(graphs):
    graph.Draw("p same")
leg.Draw("same")

can.Print("n_vs_mZprime_mDark_alpha-"+str(alpha)+".png","png")
