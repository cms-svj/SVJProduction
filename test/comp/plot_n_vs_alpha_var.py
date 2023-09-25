import sys
import math
from ROOT import *

def lambda_fn(x):
    n_c = 2
    n_f = 2
    b0 = 11.0/6.0*n_c - 2.0/6.0*n_f
    if x==0: return 0
    lambdaHV = 1000*math.exp(-math.pi/(b0*x))
    return lambdaHV

def alpha_fn(x):
    n_c = 2
    n_f = 2
    b0 = 11.0/6.0*n_c - 2.0/6.0*n_f
    if x==0: return 0
    alpha = math.pi/(b0*math.log(1000/x))
    return alpha

def lambda_peak(x):
    return 3.2*math.pow(x,0.8)

alphamin = 0.05
alphamax = 1.05

mZprime = 3000
file = TFile.Open("n_vs_alpha_mDark_mZprime-"+str(mZprime)+".root")

graphs = []
color = kMagenta+2
mDark = 20
ymax = 0.0
leg = TLegend(0.575,0.425,0.9,0.85)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.05)
leg.SetTextFont(42)

graph = file.Get("n_vs_alpha_mDark_"+str(mDark))

pts = graph.GetY()
pts.SetSize(graph.GetN())
xpts = graph.GetX()
xpts.SetSize(graph.GetN())
ymax_tmp = max(list(pts))
ymax_idx = next(i for i,y in enumerate(list(pts)) if y==ymax_tmp)
ymax = max(ymax,ymax_tmp)

print("peak for mDark = "+str(mDark)+" :")
print("alpha = "+str(list(xpts)[ymax_idx-1:ymax_idx+2]))
print("nHV = "+str(list(pts)[ymax_idx-1:ymax_idx+2]))

graph.SetMarkerColor(color)
graphs.append(graph)
leg.AddEntry(nullptr,"m_{dark} = "+str(mDark)+" GeV","")

# define lines once ymax is known
ymax = math.floor(float(ymax))+2
ymax = ymax*2.0
lines = []

alpha_m = alpha_fn(mDark)
print("alpha_m = "+str(alpha_m))
line1 = TLine(alpha_m,0,alpha_m,ymax)
line1.SetLineStyle(7)
line1.SetLineWidth(2)
line1.SetLineColor(color)
lines.append(line1)
leg.AddEntry(line1,"#Lambda_{dark} = ^{}m_{dark}","l")

alpha_p = alpha_fn(lambda_peak(mDark))
print("alpha_p = "+str(alpha_p))
line2 = TLine(alpha_p,0,alpha_p,ymax)
line2.SetLineStyle(7)
line2.SetLineWidth(2)
line2.SetLineColor(kBlack)
lines.append(line2)
leg.AddEntry(line2,"#alpha_{dark}^{peak} (#Lambda_{dark} = ^{}3.2m_{dark}^{0.8})","l")
#leg.AddEntry(nullptr,"(#Lambda_{dark} = ^{}3.2m_{dark}^{0.8})","")

alpha_h = 1.5*alpha_p
line3 = TLine(alpha_h,0,alpha_h,ymax)
line3.SetLineStyle(7)
line3.SetLineWidth(2)
line3.SetLineColor(kBlue)
lines.append(line3)
leg.AddEntry(line3,"#alpha_{dark}^{high} = #frac{3}{2}^{}#alpha_{dark}^{peak}","l")

alpha_l = 0.5*alpha_p
line4 = TLine(alpha_l,0,alpha_l,ymax)
line4.SetLineStyle(7)
line4.SetLineWidth(2)
line4.SetLineColor(kRed)
lines.append(line4)
leg.AddEntry(line4,"#alpha_{dark}^{low} = #frac{1}{2}^{}#alpha_{dark}^{peak}","l")

can = TCanvas()
can.SetTopMargin(0.13)
can.SetLeftMargin(0.13)
can.Draw()

nbins = 10
haxis = TH1F("axis","",nbins,alphamin,alphamax)
haxis.GetXaxis().SetNdivisions(210)
haxis.GetXaxis().SetTitle("#alpha_{dark}")
haxis.GetYaxis().SetTitle("#LT^{}N_{#pi_{dark}} + ^{}N_{#rho_{dark}}#GT")
haxis.GetYaxis().SetRangeUser(0,ymax)
haxis.GetYaxis().SetTitleOffset(0.9)
haxis.Draw()

for graph in graphs:
    graph.Draw("p same")
for line in lines:
    line.Draw("same")
leg.Draw("same")

# make an axis on top for lambda
haxis2 = haxis.Clone("haxis2")
xaxis2 = haxis2.GetXaxis()
alphadelt = 0.1
for i in range(nbins):
    lval = lambda_fn(alphamin+0.05+i*alphadelt)
    lstr = "{:.0f}".format(lval) if lval>1 else "{:.2f}".format(lval)
    xaxis2.SetBinLabel(i+1,lstr)
ax_lambda = TGaxis(alphamin,ymax,alphamax,ymax,alphamin,alphamax,210,"-")
ax_lambda.ImportAxisAttributes(xaxis2)
ax_lambda.SetTitle("#Lambda_{dark} [GeV]")
ax_lambda.SetLabelOffset(0.025)
ax_lambda.Draw()

oname = "n_vs_alpha_mDark-"+str(mDark)+"_mZprime-"+str(mZprime)
can.Print(oname+".png","png")
can.Print(oname+".eps","eps")
import os
os.popen("epstopdf "+oname+".eps")
