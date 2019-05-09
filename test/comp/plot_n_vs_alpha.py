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


alphamin = 0.05
alphamax = 1.05

mZprime = 3000
file = TFile.Open("n_vs_alpha_mDark_mZprime-"+str(mZprime)+".root")

graphs = []
colors = [kPink-9, kBlack, kBlue, kMagenta+2, kRed, kCyan+2, kMagenta]
masses = ["1","5","10","20","50","75","100"]
ymax = 0.0
leg = TLegend(0.75,0.525,0.9,0.825)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.05)
leg.SetTextFont(42)
for im,mDark in enumerate(masses):
    graph = file.Get("n_vs_alpha_mDark_"+mDark)

    pts = graph.GetY()
    pts.SetSize(graph.GetN())
    xpts = graph.GetX()
    xpts.SetSize(graph.GetN())
    ymax_tmp = max(list(pts))
    ymax_idx = next(i for i,y in enumerate(list(pts)) if y==ymax_tmp)
    ymax = max(ymax,ymax_tmp)

    print "peak for mDark = "+str(mDark)+" :"
    print "alpha = "+str(list(xpts)[ymax_idx-1:ymax_idx+2])
    print "nHV = "+str(list(pts)[ymax_idx-1:ymax_idx+2])

    graph.SetMarkerColor(colors[im])
    graphs.append(graph)
    leg.AddEntry(graph,"m_{d} = "+mDark,"p")

# define lines once ymax is known
ymax = math.floor(float(ymax))+2
lines = []
for im,mDark in enumerate(masses):
    alpha_m = alpha_fn([float(mDark)])
    line = TLine(alpha_m,0,alpha_m,ymax)
    line.SetLineStyle(7)
    line.SetLineWidth(2)
    line.SetLineColor(colors[im])
    lines.append(line)

can = TCanvas()
can.SetTopMargin(0.13)
can.SetLeftMargin(0.13)
can.Draw()

nbins = 10
haxis = TH1F("axis","",nbins,alphamin,alphamax)
haxis.GetXaxis().SetNdivisions(210)
haxis.GetXaxis().SetTitle("#alpha_{dark}")
haxis.GetYaxis().SetTitle("#LTN_{#pi_{dark}} + N_{#rho_{dark}}#GT")
haxis.GetYaxis().SetRangeUser(0,ymax)
haxis.GetYaxis().SetTitleOffset(0.9)
haxis.Draw()

for ig,graph in enumerate(graphs):
    graph.Draw("p same")
    lines[ig].Draw("same")
leg.Draw("same")

# make an axis on top for lambda
haxis2 = haxis.Clone("haxis2")
xaxis2 = haxis2.GetXaxis()
alphadelt = 0.1
for i in range(nbins):
    lval = lambda_fn([alphamin+0.05+i*alphadelt])
    lstr = "{:.0f}".format(lval) if lval>1 else "{:.2f}".format(lval)
    xaxis2.SetBinLabel(i+1,lstr)
ax_lambda = TGaxis(alphamin,ymax,alphamax,ymax,alphamin,alphamax,210,"-")
ax_lambda.ImportAxisAttributes(xaxis2)
ax_lambda.SetTitle("#Lambda_{dark} [GeV]")
ax_lambda.SetLabelOffset(0.025)
ax_lambda.Draw()

oname = "n_vs_alpha_mDark_mZprime-"+str(mZprime)
can.Print(oname+".png","png")
can.Print(oname+".eps","eps")
import os
os.popen("epstopdf "+oname+".eps")
