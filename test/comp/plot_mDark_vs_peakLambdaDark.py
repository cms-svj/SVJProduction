import sys
import math
import pandas as pd
from ROOT import *
from numpy import array, zeros

name = "mDark_vs_peakLambdaDark"

df = pd.read_csv(name+".csv",sep=',')

haxis = TH1F("axis","",1,0,101)
haxis.GetYaxis().SetRangeUser(0,140)
haxis.GetXaxis().SetTitle("m_{dark} [GeV]")
haxis.GetYaxis().SetTitle("#Lambda_{dark}^{peak} [GeV]")
haxis.GetYaxis().SetTitleOffset(1.0)

npts = len(df["mass"])
graph = TGraphAsymmErrors(npts,array(df["mass"]),array(df["lambda"]),zeros(npts),zeros(npts),array(df["lambdaDnErr"]),array(df["lambdaUpErr"]))
graph.SetTitle("")
graph.SetMarkerStyle(20)
graph.SetMarkerColor(kBlue)
graph.SetLineColor(kBlue)

fit = TF1("fit","[0]*x^[1]",df["mass"].min(),df["mass"].max())
fit.SetParameters(3.2,0.8)
fit.SetLineStyle(2)
fit.SetLineColor(kRed)

can = TCanvas()
can.SetLeftMargin(0.13)
can.Draw()

haxis.Draw()
graph.Draw("pz same")
fit.Draw("same")

can.Print(name+".png","png")
can.Print(name+".eps","eps")
import os
os.popen("epstopdf "+name+".eps")
