import sys
from ROOT import *
from numpy import array
from multiprocessing import Pool

mZprime = 3000
dir = "root://cmseos.fnal.gov//store/user/pedrok/SVJ2017/TestProductionV9/"
ftemp = "step1_GEN_mZprime-"+str(mZprime)+"_mDark-{}_rinv-0.3_alpha-{}_n-10000_part-1.root"

def getAlphaInfo(optlist):
    alpha = optlist[0]
    mDark = optlist[1]
    alpha_val = float(alpha)
    # get n particles from tree
    file = TFile.Open(dir+ftemp.format(mDark,alpha))
    tree = file.Get("Events")
    h = TH1F("h"+alpha,"h"+alpha,200,0.,200.)
    tree.Draw("Sum$(4900111<=abs(recoGenParticles_genParticles__GEN.obj.pdgId())&&abs(recoGenParticles_genParticles__GEN.obj.pdgId())<=4900213)>>h"+alpha,"","goff")
    # store values
    alpha_mean = h.GetMean()
    alpha_mean_err = h.GetMeanError()
    print(alpha)
    sys.stdout.flush()
    return [alpha_val, alpha_mean, alpha_mean_err]
    

alphas = ["0.05","0.15","0.1","0.25","0.2","0.35","0.3","0.45","0.4","0.55","0.5","0.65","0.6","0.75","0.7","0.85","0.8","0.95","0.9","1"]

graphs = []
for mDark,alphamin in zip(["1","5","10","20","50","75","100"],[0.15,0.2,0.225,0.275,0.35,0.4,0.45]):
    # transform for map input
    alphas_input = alphas[:]
    alphas_input.extend([str(round(alphamin+x/200.,3)) for x in range(0,21,1)])
    alphas_input = [[i,mDark] for i in sorted(set(alphas_input))]
    p = Pool(5)
    result = p.map(getAlphaInfo,alphas_input)

    alpha_val = []
    alpha_val_err = []
    alpha_mean = []
    alpha_mean_err = []
    for item in sorted(result):
        alpha_val.append(item[0])
        alpha_val_err.append(0)
        alpha_mean.append(item[1])
        alpha_mean_err.append(item[2])

    graph = TGraphErrors(len(alpha_val),array(alpha_val),array(alpha_mean),array(alpha_val_err),array(alpha_mean_err))
    graph.SetTitle("")
    graph.SetName("n_vs_alpha_mDark_"+mDark)
    graph.SetMarkerStyle(20)
    graphs.append(graph)

outfile = TFile.Open("n_vs_alpha_mDark_mZprime-"+str(mZprime)+".root","RECREATE")
for graph in graphs:
    graph.Write()
outfile.Close()
