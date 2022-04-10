import sys
import math
import pandas as pd
from ROOT import *
from numpy import array, zeros

name = "mDark_vs_peakLambdaDark"

df = pd.read_csv(name+".csv",sep=',')

haxis = TH1F("axis","",1,0,101)
haxis.GetYaxis().SetRangeUser(0,140)
haxis.GetXaxis().SetTitle("m_{#pi_{D}} [GeV]")
haxis.GetYaxis().SetTitle("#Lambda_{D}^{peak} [GeV]")
haxis.GetYaxis().SetTitleOffset(1.0)

npts = len(df["mass"])
graph = TGraphAsymmErrors(npts,array([float(x) for x in df["mass"]]),array(df["lambda"]),zeros(npts),zeros(npts),array(df["lambdaDnErr"]),array(df["lambdaUpErr"]))
graph.SetTitle("")
graph.SetMarkerStyle(20)
graph.SetMarkerColor(kBlue)
graph.SetLineColor(kBlue)

fit = TF1("fit","[0]*x^[1]",df["mass"].min(),df["mass"].max())
#fit.SetParameters(3.2,0.8)
fit.FixParameter(0,3.2)
fit.FixParameter(1,0.8)
fit.SetLineStyle(2)
fit.SetLineColor(kRed)

leg = TLegend(0.2,0.75,0.5,0.9)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextSize(0.05)
leg.SetTextFont(42)
leg.AddEntry(fit, "#Lambda_{D}^{peak} = 3.2^{}m_{#pi_{D}}^{0.8}", "l")

# get chi2 and adjust ndf
graph.Fit(fit,"N")
fit.SetNDF(fit.GetNDF()-fit.GetNpar())
#leg.AddEntry(nullptr, "#chi^{2} / ^{}n_{dof} = "+"{:.1f}".format(fit.GetChisquare())+" / {}".format(fit.GetNDF()), "")

can = TCanvas()
can.SetLeftMargin(0.13)
can.Draw()

haxis.Draw()
graph.Draw("pz same")
fit.Draw("same")
leg.Draw()

can.Print(name+".png","png")
can.Print(name+".pdf","pdf")
