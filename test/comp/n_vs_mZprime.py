import sys
from ROOT import *
from numpy import array
from multiprocessing import Pool

alpha = 0.5
dir = "root://cmseos.fnal.gov//store/user/pedrok/SVJ2017/TestProductionV9/"
ftemp = "step1_GEN_mZprime-{}_mDark-{}_rinv-0.3_alpha-"+str(alpha)+"_n-10000_part-1.root"

def getMZprimeInfo(optlist):
    mZprime = optlist[0]
    mDark = optlist[1]
    mZprime_val = float(mZprime)
    # get n particles from tree
    file = TFile.Open(dir+ftemp.format(mZprime,mDark))
    tree = file.Get("Events")
    h = TH1F("h"+mZprime,"h"+mZprime,200,0.,200.)
    tree.Draw("Sum$(4900111<=abs(recoGenParticles_genParticles__GEN.obj.pdgId())&&abs(recoGenParticles_genParticles__GEN.obj.pdgId())<=4900213)>>h"+mZprime,"","goff")
    # store values
    mZprime_mean = h.GetMean()
    mZprime_mean_err = h.GetMeanError()
    print(mZprime)
    sys.stdout.flush()
    return [mZprime_val, mZprime_mean, mZprime_mean_err]
    

mZprimes = ["1000","1500","2000","2500","3000","3500","4000"];

graphs = []
for im,mDark in enumerate(["5","10","20","50","75","100"]):
    # transform for map input
    mZprimes_input = [[i,mDark] for i in mZprimes]
    p = Pool(5)
    result = p.map(getMZprimeInfo,mZprimes_input)

    mZprime_val = []
    mZprime_val_err = []
    mZprime_mean = []
    mZprime_mean_err = []
    for item in sorted(result):
        mZprime_val.append(item[0])
        mZprime_val_err.append(0)
        mZprime_mean.append(item[1])
        mZprime_mean_err.append(item[2])

    graph = TGraphErrors(len(mZprime_val),array(mZprime_val),array(mZprime_mean),array(mZprime_val_err),array(mZprime_mean_err))
    graph.SetTitle("")
    graph.SetName("n_vs_mZprime_mDark_"+mDark)
    graph.SetMarkerStyle(20)
    graphs.append(graph)

outfile = TFile.Open("n_vs_mZprime_mDark_alpha-"+str(alpha)+".root","RECREATE")
for graph in graphs:
    graph.Write()
outfile.Close()
