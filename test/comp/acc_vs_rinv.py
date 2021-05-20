import os,sys
import ROOT as r
from numpy import array
from multiprocessing import Pool

mZprime = 2500
xsec = 0.04977
lumi = 35920+41530+59740
dir = "root://cmseos.fnal.gov//store/user/pedrok/SVJ2017/ProductionV3/2018/GEN/"
ftemp = "step1_GEN_s-channel_mMed-2500_mDark-20_rinv-{:g}_alpha-peak_13TeV-pythia8_n-20000_part-1.root"
#ftemp = "step1_GEN_s-channel_mMed-2500_mDark-20_rinv-{:g}_alpha-peak_13TeV-pythia8_n-100000_part-1.root"

def fprint(msg):
    print(msg)
    sys.stdout.flush()

def rinvVal(val):
    tmp = "{:g}".format(val)
    result = tmp.replace(".","")
    return result

def getRinvInfo(rinv):
    # get MT from tree
    fname = dir+ftemp.format(rinv)
    file = r.TFile.Open(fname)
    tree = file.Get("Events")
    # aliases
    tree.SetAlias("GenJetsAK8","recoGenJets_ak8GenJetsNoNu__GEN.obj")
    tree.SetAlias("GenMET","recoGenMETs_genMetTrue__GEN.obj")
    tree.SetAlias("MTAK8","KMath::TransverseMass(GenJetsAK8[0].px()+GenJetsAK8[1].px(),GenJetsAK8[0].py()+GenJetsAK8[1].py(),sqrt((GenJetsAK8[0].energy()+GenJetsAK8[1].energy())^2-(GenJetsAK8[0].px()+GenJetsAK8[1].px())^2-(GenJetsAK8[0].py()+GenJetsAK8[1].py())^2-(GenJetsAK8[0].pz()+GenJetsAK8[1].pz())^2),GenMET.px(),GenMET.py(),0)")
    tree.SetAlias("RT","GenMET.pt()/MTAK8")
    tree.SetAlias("DeltaPhiMinAK8","min(abs(KMath::DeltaPhi(GenJetsAK8[0].phi(),GenMET.phi())),abs(KMath::DeltaPhi(GenJetsAK8[1].phi(),GenMET.phi())))+0")
    # cuts
    selbase = "GenJetsAK8[0].pt()>200&&GenJetsAK8[1].pt()>200&&abs(GenJetsAK8[0].eta())<2.4&&abs(GenJetsAK8[1].eta())<2.4&&abs(GenJetsAK8[0].eta()-GenJetsAK8[1].eta())<1.5&&MTAK8>1500&&DeltaPhiMinAK8<0.8"
    highCut = "0.25<RT"
    lowCut = "0.15<RT&&RT<=0.25"
    # histos and nevents
    hname = "MTAK8_rinv-{:g}".format(rinv)
    hname2 = hname.replace("-","").replace(".","")
    denom = int(tree.GetEntries())
    weight = lumi*xsec/denom
    hname = "{}_{}"
    drawname = "MTAK8>>{}(65,1500,8000)"
    cutname = "{}*({}&&{})"
    hnameH = hname.format(hname2,"highCut")
    drawnameH = drawname.format(hnameH)
    cutnameH = cutname.format(weight,selbase,highCut)
    numerH = tree.Draw(drawnameH,cutnameH,"goff")
    hH = r.gDirectory.Get(hnameH)
    hnameL = hname.format(hname2,"lowCut")
    drawnameL = drawname.format(hnameL)
    cutnameL = cutname.format(weight,selbase,lowCut)
    numerL = tree.Draw(drawnameL,cutnameL,"goff")
    hL = r.gDirectory.Get(hnameL)
    oname = "MTAK8_acc_mZprime2500_rinv-{:g}.root".format(rinv)
    ofile = r.TFile.Open(oname,"RECREATE")
    ofile.cd()
    dirH = ofile.mkdir("highCut_2018")
    dirH.cd()
    hH.Write("SVJ_mZprime2500_mDark20_rinv{}_alphapeak".format(rinvVal(rinv)))
    dirL = ofile.mkdir("lowCut_2018")
    dirL.cd()
    hL.Write("SVJ_mZprime2500_mDark20_rinv{}_alphapeak".format(rinvVal(rinv)))
    ofile.Close()
    fprint(rinv)
    return [rinv, oname, float(numerH)/denom, r.KMath.EffError(numerH,denom), float(numerL)/denom, r.KMath.EffError(numerL,denom)]

r.gROOT.ProcessLine('#include "KCode/KMath.h"')
rinvs = [float(x)/1000 for x in range(201)]
#rinvs = [0.0, 0.05, 0.1, 0.15, 0.2]

p = Pool(18)
result = p.map(getRinvInfo,rinvs)
goname = "MTAK8_acc_mZprime2500_graph.root"
#goname = "MTAK8_acc_mZprime2500_graph_100K.root"
outfile = r.TFile.Open(goname,"RECREATE")
acc_valH = []
acc_errH = []
acc_valL = []
acc_errL = []
olist = []
for item in sorted(result):
    olist.append(item[1])
    acc_valH.append(item[2])
    acc_errH.append(item[3])
    acc_valL.append(item[4])
    acc_errL.append(item[5])
olist.append(goname)

gname = "acc_vs_rinv_{}"
graphH = r.TGraphErrors(len(rinvs),array(rinvs),array(acc_valH),r.nullptr,array(acc_errH))
graphH.SetTitle("")
graphH.SetName(gname.format("highCut"))
graphH.Write()
graphL = r.TGraphErrors(len(rinvs),array(rinvs),array(acc_valL),r.nullptr,array(acc_errL))
graphL.SetTitle("")
graphL.SetName(gname.format("lowCut"))
graphL.Write()
outfile.Close()

os.system("hadd -f {0} {1} && rm {1}".format(goname.replace("graph","rinv02"),' '.join(olist)))
