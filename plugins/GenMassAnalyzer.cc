//framework headers
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

//analysis headers
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"

//ROOT headers
#include <TTree.h>
#include <TLorentzVector.h>

//STL headers
#include <vector>
#include <set>
#include <memory>
#include <cmath>
#include <iostream>
#include <typeinfo>
#include <algorithm>
#include <numeric>
using std::vector;
using std::set;

//user headers
#include "SVJ/Production/interface/common.h"
#include "SVJ/Production/interface/lester_mt2_bisect.h"
#include "SVJ/Production/interface/NjettinessHelper.h"
#include "SVJ/Production/interface/ECFHelper.h"

//
// class declaration
//

class darkIdList{
  public:
    // variables useful for jet identification
    set<int> DarkMediatorID_ = {4900001,4900002,4900003,4900004,4900005,4900006};
    set<int> DarkQuarkID_ = {4900101,4900102};
    set<int> DarkHadronID_ = {4900111,4900113,4900211,4900213};
    set<int> DarkGluonID_ = {4900021};
};

class usefulConst{
  public:
    double pTCut = 100;
    double coneSize = 0.8;
    double dpFractCut = 0.7;
};

class GenMassAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
  public:
    explicit GenMassAnalyzer(const edm::ParameterSet&);
    ~GenMassAnalyzer() {}

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

    struct GenNtuple {
      double DeltaPhi1 = 0.;
      double DeltaPhi2 = 0.;
      double DeltaPhiMin = 0.;
      vector<TLorentzVector> GenJetsAK8;
      vector<double> GenJetsAK8_AxisAverage;
      vector<double> GenJetsAK8_AxisMajor;
      vector<double> GenJetsAK8_AxisMinor;
      vector<double> GenJetsAK8_ECF1;
      vector<double> GenJetsAK8_ECF2;
      vector<double> GenJetsAK8_ECF3;
      vector<double> GenJetsAK8_MomentGirth;
      vector<double> GenJetsAK8_MomentHalf;
      vector<int> GenJetsAK8_Multiplicity;
      vector<double> GenJetsAK8_PtD;
      vector<double> GenJetsAK8_Tau1;
      vector<double> GenJetsAK8_Tau2;
      vector<double> GenJetsAK8_Tau3;
      vector<TLorentzVector> HVMesons;
      double MAOS = 0.;
      vector<TLorentzVector> METSystems;
      double MET = 0.;
      double METPhi = 0.;
      double MJJ = 0.;
      double Mmc = 0.;
      double MT = 0.;
      double MT2 = 0.;
      // added for SVJ t-channel jet categorization
      vector<TLorentzVector> AK8Jets;
      vector<double> AK8_dptFrac;
      vector<double> AK8Jets_Tau1;
      vector<double> AK8Jets_Tau2;
      vector<double> AK8Jets_Tau3;
      // soft drop jets for different jet categories
      vector<TLorentzVector> AK8_SDJets;
      vector<double> AK8_SDdptFrac;
      // for noNu vs. non-noNu jets comparison
      vector<double> pAK8_ptRatioNu;
      vector<double> pAK8_ptRatioConst;
      vector<int> svj_t_jetCat;
    };

  private:
    void beginJob() override;
    void doBeginRun_(const edm::Run&, const edm::EventSetup&) override {}
    void analyze(const edm::Event&, const edm::EventSetup&) override;
    void doEndRun_(const edm::Run&, const edm::EventSetup&) override {}
    void endJob() override {}

    // ----------member data ---------------------------
    edm::Service<TFileService> fs;
    TTree* tree;
    //for tree branches
    GenNtuple entry;
#ifndef CMSSW71X
    NjettinessHelper njhelper;
    ECFHelper echelper;
#endif
    //tokens
    edm::EDGetTokenT<vector<reco::GenMET>> tok_met;
    edm::EDGetTokenT<vector<reco::GenJet>> tok_jet;
    edm::EDGetTokenT<vector<reco::GenParticle>> tok_part;
    edm::EDGetTokenT<vector<reco::GenJet>> tok_packedjet;

    // functions for jet identification

    // Convert things to TLorentzVector
    template <typename T>
    TLorentzVector toTLV(const T& part_i){
        return TLorentzVector(part_i.px(),part_i.py(),part_i.pz(),part_i.energy());
    }

    // Check and see if the pdgId belongs to a list of dark IDs
    bool darkTruth(const set<int>& darklist, int pId)
    {
      return darklist.find(std::abs(pId)) != darklist.end();
    }

    // find the last daughters of a given gen particle
    template <typename T>
    void lastDau(vector<const reco::Candidate*>& lastD,const T& dHad)
    {
      // loop through the daughters of the last dark hadrons
      for (unsigned idH = 0; idH < dHad.numberOfDaughters(); idH++ )
      {
        const reco::Candidate* dauH = dHad.daughter(idH);
        int dauHID = std::abs(dauH->pdgId());
        // if a daughter doesn't have any more daughter, it is the last descendant
        if (dauH->numberOfDaughters() == 0 && (dauHID != 51 || dauHID || 52 || dauHID != 53)) // last particle that is not stable dark hadron
        {
          lastD.push_back(dauH);
        }
        // this effectively makes the algorithm go down the list of descendants until we get to the last descendants
        else if (dauH->numberOfDaughters() > 0)
        {
          lastDau(lastD,*dauH);
        }
      }
    }

    // Get lists of last dark particles in the event
    void lastDarkGQ(const set<int>& DarkIDList, int partid,
                    const reco::GenParticle& part_i,
                    vector<const reco::Candidate*>& lastD)
    {
      darkIdList dil;
      // store the index and TLorentzVector of the particle in "dPartList_label" and "dPartList" if its pdgID is dark and it is the last copy
      if (darkTruth(DarkIDList,partid) && part_i.isLastCopy())
      {
        TLorentzVector part_i_TL = toTLV(part_i);
        lastDau(lastD,part_i);
      }
    }
    // store the first daughters from the first dark mediator(s)
    void medDecay(const reco::Candidate* fdau,
                  vector<TLorentzVector>& fdQPartFM,
                  vector<TLorentzVector>& fdGPartFM,
                  vector<TLorentzVector>& fSMqPart)
    {
      // loop through the daughters of the first dark mediator
      for (unsigned mddi = 0; mddi < fdau->numberOfDaughters(); mddi++)
      {
        darkIdList dil;

        const reco::Candidate* mdd = fdau->daughter(mddi);
        int mddId = std::abs(mdd->pdgId());
        // if the first dark mediator's daughter is still a dark mediator, then check the daughters of this daughter dark mediator until we get daughters that are not dark mediator
        if (darkTruth(dil.DarkMediatorID_,mddId))
        {
          medDecay(mdd,fdQPartFM,fdGPartFM,fSMqPart);
        }
        else
        {
          TLorentzVector mdd_TL = toTLV(*mdd);
          if (darkTruth(dil.DarkQuarkID_,mddId)) fdQPartFM.push_back(mdd_TL);
          else if (darkTruth(dil.DarkGluonID_,mddId)) fdGPartFM.push_back(mdd_TL);
          else fSMqPart.push_back(mdd_TL);
        }
      }
    }
    // store the dark immediate daughters of the earliest dark particles
    template <typename Particle>
    void firstDark(int partid, const Particle& part_i,
                  vector<TLorentzVector>& fdMPart,
                  vector<TLorentzVector>& fdQPart,
                  vector<TLorentzVector>& fdGPart,
                  vector<TLorentzVector>& fdQPartFM,
                  vector<TLorentzVector>& fdGPartFM,
                  vector<TLorentzVector>& fSMqPart)
    {
      darkIdList dil;
      set<int> DarkIDs(dil.DarkMediatorID_);
      DarkIDs.insert( dil.DarkQuarkID_.begin(), dil.DarkQuarkID_.end());
      DarkIDs.insert( dil.DarkGluonID_.begin(), dil.DarkGluonID_.end());
      if(darkTruth(DarkIDs,partid))
      {
        const reco::Candidate* fmom = part_i.mother(0);
        int momId = std::abs(fmom->pdgId());
        // if a particle's mother is dark, we look at that mother's mother until we get to the non-dark mother. The daughter of this non-dark mother is the earliest dark particles. This logic is based on the idea that all particles must have come from the SM quarks of the colliding protons.
        if(darkTruth(DarkIDs,momId))
        {
          firstDark(momId,*fmom,fdMPart,fdQPart,fdGPart,fdQPartFM,fdGPartFM,fSMqPart);
        }
        else
        {
          for (unsigned dau_i = 0; dau_i < part_i.numberOfDaughters(); dau_i++)
          {
            const reco::Candidate* fdau = part_i.daughter(dau_i);
            int fdauId = std::abs(fdau->pdgId());
            TLorentzVector fdau_TL = toTLV(*fdau);
            if (darkTruth(dil.DarkMediatorID_,fdauId))
            {
              fdMPart.push_back(fdau_TL);
              medDecay(fdau,fdQPartFM,fdGPartFM,fSMqPart);
            }
            else if (darkTruth(dil.DarkQuarkID_,fdauId))
            {
              fdQPart.push_back(fdau_TL);
            }

            else if (darkTruth(dil.DarkGluonID_,fdauId))
            {
              fdGPart.push_back(fdau_TL);
            }
          }
        }
      }
    }
    // classify a jet as dark jet if there is a last dark particle within the jet radius
    void checkDark(const reco::GenJet& ijet,
                  vector<const reco::Candidate*>& lastD,
                  const int& idValue,
                  int& jCatLabel)
    {
      bool dMatch = false;
      usefulConst uc;
      // looping through all the last dark gluons and quarks
      for (unsigned i = 0 ; i < ijet.numberOfDaughters(); i ++ )
      {
        // see if any jet constituent is a last dark descendant
        if (std::find(lastD.begin(),lastD.end(),ijet.daughter(i)) != lastD.end())
        {
          dMatch = true;
        }
      }
      if (dMatch == true) // if more than one quarks/gluons fall into the cone of one jet we still have only one dark jet
      {
        jCatLabel += idValue;
      }
    }
    // calculate the dark pT fraction of one jet
      double darkPtFract(const reco::GenJet& adj,
                        const vector<const reco::Candidate*>& lastD)
      {
        TLorentzVector tot4vec;
        TLorentzVector dark4vec;
        auto anum = adj.numberOfDaughters();
        for (unsigned ani = 0; ani < anum; ani++)
        {
          const reco::Candidate* adj_dau = adj.daughter(ani);
          TLorentzVector prt = toTLV(*adj_dau);
          tot4vec += prt;
          if (std::find(lastD.begin(),lastD.end(),adj_dau) != lastD.end())
          {
            dark4vec += prt;
          }
        }
        double jetDarkF = dark4vec.Pt()/tot4vec.Pt();
        return jetDarkF;
      }
    // record first dark particles that are within the jets' radii
     void isfj(const vector<TLorentzVector>& fPart, const reco::GenJet& uj,
               const int& idValue,int& jCatLabel)
     {
       usefulConst uc;
       TLorentzVector ujTL = toTLV(uj);
       for (const auto& fP : fPart)
       {
         if (fP.DeltaR(ujTL) < uc.coneSize)
         {
           jCatLabel += idValue;
           break;
         }
       }

     }
    void fillSubs(vector<double>& etau1, vector<double>& etau2,
                vector<double>& etau3,
                const vector<reco::GenJet>& jet)
    {
      etau1.reserve(jet.size());
      etau2.reserve(jet.size());
      etau3.reserve(jet.size());
      for(const auto& i_jet : jet)
      {
        #ifndef CMSSW71X
            etau1.push_back(njhelper.getTau(1,i_jet));
            etau2.push_back(njhelper.getTau(2,i_jet));
            etau3.push_back(njhelper.getTau(3,i_jet));
        #endif
      }
    }
    // match jets from packedGenJetsAK8NoNu to jets from ak8GenJets by DeltaR between those jets
    void matchJet_to_NoNu(const vector<reco::GenJet>& jC_,
                          const edm::Handle<vector<reco::GenJet>>& h_packedjet,
                          vector<reco::GenJet>& pjC_,
                          vector<reco::GenJet>& mjC_)
    {
      usefulConst uc;
      for(unsigned j = 0; j < jC_.size() ; j++)
      {
        vector<double> pTList;
        vector<reco::GenJet> canJet;
        const reco::GenJet& jjet = jC_[j];
        // ijet is a jet of packedGenJetsAK8NoNu
        // jjet is a jet of ak8GenJets
        for(const auto& ijet : *(h_packedjet.product()))
        {
          if (ijet.pt() > uc.pTCut)
          {
            double dr = toTLV(jjet).DeltaR(toTLV(ijet));
            if (dr < uc.coneSize)
            {
              pTList.push_back(ijet.pt());
              canJet.push_back(ijet);
            }
          }
        }
        if (pTList.size() > 0)
        { // canJet is a list of all the ijets that are within delta R of the jjet
          // the jjet in canJet that has the highest pT is considered the jet matched to the jjet
          int maxPtInd = std::max_element(pTList.begin(),pTList.end()) - pTList.begin();
          pjC_.push_back(canJet[maxPtInd]);
          mjC_.push_back(jjet);
        }
      }
    }
    // calculate the pT ratio between a genJet and its matched noNu Jet
    void calcPtRatioNu(vector<reco::GenJet>& pjC_,
                      vector<reco::GenJet>& mjC_,
                      vector<double>& ptrat,
                      vector<double>& ptratConst)
    {
      ptrat.reserve(pjC_.size());
      ptratConst.reserve(pjC_.size());

      for (unsigned i = 0; i < pjC_.size(); i++)
      {
          const reco::GenJet& pjet = pjC_[i];
          const reco::GenJet& mjet = mjC_[i];
          ptrat.push_back(pjet.pt()/mjet.pt());
          TLorentzVector NuPt;
          for (unsigned j = 0; j < mjet.numberOfDaughters(); j++)
          {
            int pid = std::abs(mjet.daughter(j)->pdgId());
            if (pid != 51 && pid != 52 && pid != 53)
            {
              NuPt += toTLV(*mjet.daughter(j));
            }
          }
          ptratConst.push_back(NuPt.Pt()/mjet.pt());
      }
    }

    void fillAK8Jets(const vector<reco::GenJet>& genJets,
                    vector<TLorentzVector>& jetBranch,
                    const vector<int> jCatList,
                    vector<int>& svj_t_jetCat,
                    vector<double>& dFract,
                    const vector<const reco::Candidate*>& lastD)
    {
      jetBranch.reserve(genJets.size());
      svj_t_jetCat.reserve(genJets.size());
      for(unsigned i = 0; i < genJets.size(); i++)
      {
        const reco::GenJet& i_jet = genJets[i];
        const int jCat = jCatList[i];
        jetBranch.emplace_back(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());
        svj_t_jetCat.push_back(jCat);
        dFract.push_back(darkPtFract(i_jet, lastD));
      }
    }
    // constructing soft drop jet from the noNu jet sample
    void softDropJet(const vector<reco::GenJet>& pjC_,
                    const vector<reco::GenJet>& mjC_,
                    vector<TLorentzVector>& pjC_SDJ,
                    vector<double>& sddarkFract,
                    const vector<const reco::Candidate*>& lastD)
    {
      for(unsigned i = 0; i < pjC_.size(); i++)
      {
        const reco::GenJet& i_jet = pjC_[i];
        TLorentzVector vsj;
        for(unsigned k = 0; k < i_jet.numberOfDaughters(); k++) // looking at all constituants of a jet
        {
          const reco::Candidate* part = i_jet.daughter(k);
          unsigned numdau = part->numberOfDaughters();
          if(numdau>0) //only subjets have daughters
          {
            TLorentzVector vtmp = toTLV(*part);
            vsj += vtmp;
          }
        }

        if (vsj != TLorentzVector(0.,0.,0.,0.))
        {
          sddarkFract.push_back(darkPtFract(mjC_[i], lastD));
          pjC_SDJ.emplace_back(vsj.Px(),vsj.Py(),vsj.Pz(),vsj.Energy());
        }
      }
    }
    // // remove duplicates from vector of TLorentzVector
    void remove(std::vector<TLorentzVector> &v){
    	auto end = v.end();
    	for (auto i = v.begin(); i != end; ++i) {
    		end = std::remove(i + 1, end, *i);
    	}
    	v.erase(end, v.end());
    }
  };

//
// constructors and destructor
//
GenMassAnalyzer::GenMassAnalyzer(const edm::ParameterSet& iConfig) :
  tree(NULL),
#ifndef CMSSW71X
  njhelper(iConfig.getParameter<edm::ParameterSet>("Nsubjettiness")),
  echelper(iConfig.getParameter<edm::ParameterSet>("ECF")),
#endif
  tok_met(consumes<vector<reco::GenMET>>(iConfig.getParameter<edm::InputTag>("METTag"))),
  tok_jet(consumes<vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("JetTag"))),
  tok_part(consumes<vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("PartTag"))),
  tok_packedjet(consumes<vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("PackedJetTag")))
{
  usesResource("TFileService");
#ifdef CMSSW71X
  std::cout << "GenMassAnalyzer: Warning - Nsubjettiness and ECF variables not available!" << std::endl;
#endif
}

//
// member functions
//

void GenMassAnalyzer::beginJob()
{
  asymm_mt2_lester_bisect::disableCopyrightMessage();

  tree = fs->make<TTree>("tree","tree");
  tree->Branch("DeltaPhi1"  , &entry.DeltaPhi1        , "DeltaPhi1/D");
  tree->Branch("DeltaPhi2"  , &entry.DeltaPhi2        , "DeltaPhi2/D");
  tree->Branch("DeltaPhiMin", &entry.DeltaPhiMin      , "DeltaPhiMin/D");
  tree->Branch("MAOS"       , &entry.MAOS             , "MAOS/D");
  tree->Branch("MET"        , &entry.MET              , "MET/D");
  tree->Branch("METPhi"     , &entry.METPhi           , "METPhi/D");
  tree->Branch("MJJ"        , &entry.MJJ              , "MJJ/D");
  tree->Branch("Mmc"        , &entry.Mmc              , "Mmc/D");
  tree->Branch("MT"         , &entry.MT               , "MT/D");
  tree->Branch("MT2"        , &entry.MT2              , "MT2/D");
  tree->Branch("GenJetsAK8" ,               "vector<TLorentzVector>", &entry.GenJetsAK8,              32000, 0);
  tree->Branch("GenJetsAK8_AxisAverage" ,   "vector<double>",         &entry.GenJetsAK8_AxisAverage,  32000, 0);
  tree->Branch("GenJetsAK8_AxisMajor" ,     "vector<double>",         &entry.GenJetsAK8_AxisMajor,    32000, 0);
  tree->Branch("GenJetsAK8_AxisMinor" ,     "vector<double>",         &entry.GenJetsAK8_AxisMinor,    32000, 0);
  tree->Branch("GenJetsAK8_ECF1" ,          "vector<double>",         &entry.GenJetsAK8_ECF1,         32000, 0);
  tree->Branch("GenJetsAK8_ECF2" ,          "vector<double>",         &entry.GenJetsAK8_ECF2,         32000, 0);
  tree->Branch("GenJetsAK8_ECF3" ,          "vector<double>",         &entry.GenJetsAK8_ECF3,         32000, 0);
  tree->Branch("GenJetsAK8_MomentGirth" ,   "vector<double>",         &entry.GenJetsAK8_MomentGirth,  32000, 0);
  tree->Branch("GenJetsAK8_MomentHalf" ,    "vector<double>",         &entry.GenJetsAK8_MomentHalf,   32000, 0);
  tree->Branch("GenJetsAK8_Multiplicity" ,  "vector<int>",            &entry.GenJetsAK8_Multiplicity, 32000, 0);
  tree->Branch("GenJetsAK8_PtD" ,           "vector<double>",         &entry.GenJetsAK8_PtD,          32000, 0);
  tree->Branch("GenJetsAK8_Tau1" ,          "vector<double>",         &entry.GenJetsAK8_Tau1,         32000, 0);
  tree->Branch("GenJetsAK8_Tau2" ,          "vector<double>",         &entry.GenJetsAK8_Tau2,         32000, 0);
  tree->Branch("GenJetsAK8_Tau3" ,          "vector<double>",         &entry.GenJetsAK8_Tau3,         32000, 0);
  tree->Branch("HVMesons"   ,               "vector<TLorentzVector>", &entry.HVMesons,                32000, 0);
  tree->Branch("METSystems" ,               "vector<TLorentzVector>", &entry.METSystems,              32000, 0);
  // added for extra jet categories
  tree->Branch("AK8Jets" ,                  "vector<TLorentzVector>", &entry.AK8Jets,                 32000, 0);
  tree->Branch("AK8_dptFrac",               "vector<double>",         &entry.AK8_dptFrac,             32000, 0);
  tree->Branch("AK8Jets_Tau1" ,             "vector<double>",         &entry.AK8Jets_Tau1,            32000, 0);
  tree->Branch("AK8Jets_Tau2" ,             "vector<double>",         &entry.AK8Jets_Tau2,            32000, 0);
  tree->Branch("AK8Jets_Tau3" ,             "vector<double>",         &entry.AK8Jets_Tau3,            32000, 0);
  // softdrop jet for different jet categories
  tree->Branch("AK8_SDJets",                "vector<TLorentzVector>", &entry.AK8_SDJets,              32000, 0);
  tree->Branch("AK8_SDdptFrac",             "vector<double>",         &entry.AK8_SDdptFrac,           32000, 0);
  // for noNu vs. non-noNu jets comparison
  tree->Branch("AK8_ptRatioNoNu_Nu" ,       "vector<double>",         &entry.pAK8_ptRatioNu,          32000, 0);
  tree->Branch("AK8_ptRatioConst" ,         "vector<double>",         &entry.pAK8_ptRatioConst,       32000, 0);
  tree->Branch("svj_t_jetCat" ,             "vector<int>",            &entry.svj_t_jetCat,            32000, 0);
}

// ------------ method called on each new Event  ------------
void GenMassAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  darkIdList did;
  usefulConst uc;
  entry = GenNtuple();

  edm::Handle<vector<reco::GenMET>> h_met;
  iEvent.getByToken(tok_met,h_met);

  edm::Handle<vector<reco::GenJet>> h_jet;
  iEvent.getByToken(tok_jet,h_jet);

  edm::Handle<vector<reco::GenParticle>> h_part;
  iEvent.getByToken(tok_part,h_part);

  edm::Handle<vector<reco::GenJet>> h_packedjet;
  iEvent.getByToken(tok_packedjet,h_packedjet);

  // Grouping jets in different categories
  // This part of the code is a modified version of v3_darkdentifier.py
  vector<const reco::Candidate*> lastD; // last daughters of dHPart
  vector<int> jCatList;
  vector<TLorentzVector> fdQPart; // first dark quarks
  vector<TLorentzVector> fdGPart; // first dark gluons
  vector<TLorentzVector> fdMPart; // first dark mediators
  vector<TLorentzVector> fdQPartFM; // first dark quarks from the dark mediator
  vector<TLorentzVector> fdGPartFM; // first dark gluons from the dark mediator
  vector<TLorentzVector> fSMqPart;  // first quarks from the dark mediator decay
  vector<TLorentzVector> stableD; // stable dark hadrons
  vector<reco::GenJet> AK8Jets;
  // same categories as above, but for packedGenJetsAK8NoNu
  vector<reco::GenJet> pAK8Jets;
  // The ak8genjets that are matched to packedGenJetsAK8NoNu
  // useful for dark pt fraction estimation
  vector<reco::GenJet> mAK8Jets;

  if(h_jet->size() > 0)
  {
    int part_ind = 0;
    for (const auto& part_i : *(h_part.product())) // loop over gen particles
    {
      part_ind ++;
      int partid = std::abs(part_i.pdgId());
      lastDarkGQ(did.DarkHadronID_, partid, part_i, lastD);
      firstDark(partid,part_i,fdMPart,fdQPart,fdGPart,fdQPartFM,fdGPartFM,fSMqPart);
      if (partid == 51 || partid == 52 || partid == 53)
      {
        TLorentzVector part_i_TL = toTLV(part_i);
        stableD.push_back(part_i_TL);
      }
    }
    // removing duplicates from each vector; tried doing this using set, but set doesn't work with TLorentzVectors...
    remove(fdMPart);
    remove(fdQPart);
    remove(fdGPart);
    remove(fdQPartFM);
    remove(fdGPartFM);
    remove(fSMqPart);
    // std::cout << "Event" <<"\n\n";
    // finding jets that contain last dark descendants
    for(const auto& ijet : *(h_jet.product()))
    {
      if (ijet.pt() > uc.pTCut)
      {
        int jCatLabel = 0;
        AK8Jets.push_back(ijet);
        set<int> dPartSet;
        checkDark(ijet,lastD,1,jCatLabel);
        isfj(fdQPart,   ijet, 2, jCatLabel);
        isfj(fdGPart,   ijet, 4, jCatLabel);
        isfj(fdQPartFM, ijet, 8, jCatLabel);
        isfj(fSMqPart,  ijet, 16, jCatLabel);
        jCatList.push_back(jCatLabel);
      }
    }
  }
  matchJet_to_NoNu(AK8Jets, h_packedjet, pAK8Jets, mAK8Jets);
  calcPtRatioNu(pAK8Jets, mAK8Jets, entry.pAK8_ptRatioNu, entry.pAK8_ptRatioConst);
  fillAK8Jets(AK8Jets, entry.AK8Jets, jCatList, entry.svj_t_jetCat, entry.AK8_dptFrac, lastD);
  softDropJet(pAK8Jets, mAK8Jets, entry.AK8_SDJets, entry.AK8_SDdptFrac, lastD);
  fillSubs(entry.AK8Jets_Tau1, entry.AK8Jets_Tau2, entry.AK8Jets_Tau3, AK8Jets);

  entry.GenJetsAK8.reserve(h_jet->size());
  entry.GenJetsAK8_MomentGirth.reserve(h_jet->size());
  entry.GenJetsAK8_MomentHalf.reserve(h_jet->size());
  entry.GenJetsAK8_Multiplicity.reserve(h_jet->size());
  entry.GenJetsAK8_PtD.reserve(h_jet->size());
  entry.GenJetsAK8_AxisMajor.reserve(h_jet->size());
  entry.GenJetsAK8_AxisMinor.reserve(h_jet->size());
  entry.GenJetsAK8_AxisAverage.reserve(h_jet->size());
  entry.GenJetsAK8_Tau1.reserve(h_jet->size());
  entry.GenJetsAK8_Tau2.reserve(h_jet->size());
  entry.GenJetsAK8_Tau3.reserve(h_jet->size());
  entry.GenJetsAK8_ECF1.reserve(h_jet->size());
  entry.GenJetsAK8_ECF2.reserve(h_jet->size());
  entry.GenJetsAK8_ECF3.reserve(h_jet->size());

  for(const auto& i_jet : *(h_jet.product())){
    entry.GenJetsAK8.emplace_back(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());

    //calculate jet moments & other vars
    //some borrowed from RecoJets/JetProducers/plugins/QGTagger.cc
    double momentGirth = 0.0;
    double momentHalf = 0.0;
    double sumPt = 0.0, sumPt2 = 0.0;
    double sumDeta = 0.0, sumDphi = 0.0, sumDeta2 = 0.0, sumDphi2 = 0.0, sumDetaDphi = 0.0;
    for(unsigned k = 0; k < i_jet.numberOfDaughters(); ++k){
      const reco::CandidatePtr& i_part = i_jet.daughterPtr(k);
      if(i_part.isNonnull() and i_part.isAvailable()){
        double dphi = reco::deltaPhi(i_jet.phi(),i_part->phi());
        double deta = i_part->eta() - i_jet.eta();
        double dR = reco::deltaR(i_jet.p4(),i_part->p4());
        double pT = i_part->pt();
        double pT2 = pT*pT;

        momentGirth += pT*dR;
        momentHalf += pT*std::sqrt(dR);
        sumPt += pT;
        sumPt2 += pT2;
        sumDeta += deta*pT2;
        sumDphi += dphi*pT2;
        sumDeta2 += deta*deta*pT2;
        sumDphi2 += dphi*dphi*pT2;
        sumDetaDphi += deta*dphi*pT2;
      }
    }
    //finish axis calculations (eigenvectors)
    sumDeta /= sumPt2;
    sumDphi /= sumPt2;
    sumDeta2 /= sumPt2;
    sumDphi2 /= sumPt2;
    sumDetaDphi /= sumPt2;
    double a = 0.0, b = 0.0, c = 0.0, d = 0.0;
    a = sumDeta2 - sumDeta*sumDeta;
    b = sumDphi2 - sumDphi*sumDphi;
    c = sumDeta*sumDphi - sumDetaDphi;
    d = std::sqrt(std::fabs((a-b)*(a-b)+4*c*c));
    double axis1 = (a+b+d)>0 ? std::sqrt(0.5*(a+b+d)) : 0.0;
    double axis2 = (a+b-d)>0 ? std::sqrt(0.5*(a+b-d)) : 0.0;
    double axisA = std::sqrt(axis1*axis1 + axis2*axis2);

    //store values
    entry.GenJetsAK8_MomentGirth.push_back(momentGirth/i_jet.pt());
    entry.GenJetsAK8_MomentHalf.push_back(momentHalf/i_jet.pt());
    entry.GenJetsAK8_Multiplicity.push_back(i_jet.numberOfDaughters());
    entry.GenJetsAK8_PtD.push_back(std::sqrt(sumPt2)/sumPt);
    entry.GenJetsAK8_AxisMajor.push_back(axis1);
    entry.GenJetsAK8_AxisMinor.push_back(axis2);
    entry.GenJetsAK8_AxisAverage.push_back(axisA);

    //calculate nsubjettiness & ECFs
#ifndef CMSSW71X
    entry.GenJetsAK8_Tau1.push_back(njhelper.getTau(1,i_jet));
    entry.GenJetsAK8_Tau2.push_back(njhelper.getTau(2,i_jet));
    entry.GenJetsAK8_Tau3.push_back(njhelper.getTau(3,i_jet));

    auto ECFresult = echelper.getECFs(i_jet);
    entry.GenJetsAK8_ECF1.push_back(ECFresult[0]);
    entry.GenJetsAK8_ECF2.push_back(ECFresult[1]);
    entry.GenJetsAK8_ECF3.push_back(ECFresult[2]);
#endif
  }

  TLorentzVector vpartsSum;
  for(const auto& i_part : *(h_part.product())){
    if(std::abs(i_part.pdgId())==4900211){
      entry.HVMesons.emplace_back(i_part.px(),i_part.py(),i_part.pz(),i_part.energy());
      vpartsSum += entry.HVMesons.back();
    }
  }

  const auto& i_met = h_met->front();
  double METx = i_met.px();
  double METy = i_met.py();
  entry.MET = i_met.pt();
  entry.METPhi = i_met.phi();

  //only fill these parts if there are >=2 jets
  if(entry.GenJetsAK8.size()>=2){
    //delta phi
    entry.DeltaPhi1 = std::abs(reco::deltaPhi(entry.GenJetsAK8[0].Phi(),entry.METPhi));
    entry.DeltaPhi2 = std::abs(reco::deltaPhi(entry.GenJetsAK8[1].Phi(),entry.METPhi));
    entry.DeltaPhiMin = std::min(entry.DeltaPhi1,entry.DeltaPhi2);

    //masses
    TLorentzVector vjj = entry.GenJetsAK8[0] + entry.GenJetsAK8[1];
    entry.MJJ = vjj.M();

    //include all jets in MC mass
    TLorentzVector vmc = vjj + vpartsSum;
    entry.Mmc = vmc.M();

    //assume MET is massless
    entry.MT = asymm_mt2_lester_bisect::MT(vjj.Px(),METx,vjj.Py(),METy,vjj.M(),0.0);

    entry.MT2 = asymm_mt2_lester_bisect::get_mT2(
      entry.GenJetsAK8[0].M(), entry.GenJetsAK8[0].Px(), entry.GenJetsAK8[0].Py(),
      entry.GenJetsAK8[1].M(), entry.GenJetsAK8[1].Px(), entry.GenJetsAK8[1].Py(),
      METx, METy, 0.0, 0.0, 0
    );

    //get invisible systems from MT2
    auto MET0 = asymm_mt2_lester_bisect::ben_findsols(entry.MT2,
      entry.GenJetsAK8[0].Px(), entry.GenJetsAK8[0].Py(), entry.GenJetsAK8[0].M(), 0.0,
      entry.GenJetsAK8[1].Px(), entry.GenJetsAK8[1].Py(),
      METx, METy, entry.GenJetsAK8[1].M(), 0.0
    );
    double MET0x = MET0.first;
    double MET0y = MET0.second;
    double MET0t = std::sqrt(std::pow(MET0x,2)+std::pow(MET0y,2));
    double MET1x = METx - MET0x;
    double MET1y = METy - MET0y;
    double MET1t = std::sqrt(std::pow(MET1x,2)+std::pow(MET1y,2));

    //use MAOS scheme 2 ("modified") to estimate longitudinal momenta of invisible systems
    double MET0z = MET0t*entry.GenJetsAK8[0].Pz()/entry.GenJetsAK8[0].Pt();
    double MET1z = MET1t*entry.GenJetsAK8[1].Pz()/entry.GenJetsAK8[1].Pt();

    vector<TLorentzVector> mets;
    mets.emplace_back(MET0x,MET0y,MET0z,0.0);
    mets.emplace_back(MET1x,MET1y,MET1z,0.0);
    entry.METSystems = mets;

    //construct invariant mass of parent
    TLorentzVector vparent = vjj + mets[0] + mets[1];
    entry.MAOS = vparent.M();
  }

  //fill tree
  tree->Fill();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void GenMassAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("PackedJetTag",edm::InputTag("packedGenJetsAK8NoNu"));
  desc.add<edm::InputTag>("METTag",edm::InputTag("genMetTrue"));
  desc.add<edm::InputTag>("JetTag",edm::InputTag("ak8GenJets"));
  desc.add<edm::InputTag>("PartTag",edm::InputTag("genParticles"));

  edm::ParameterSetDescription desc_nj;
  desc_nj.add<unsigned>("measureDefinition",0);
  desc_nj.add<double>("beta",1.0);
  desc_nj.add<double>("R0",0.8);
  desc_nj.add<double>("Rcutoff",999.0);
  desc_nj.add<unsigned>("axesDefinition",6);
  desc_nj.add<int>("nPass",999);
  desc_nj.add<double>("akAxesR0",999.0);
  desc.add<edm::ParameterSetDescription>("Nsubjettiness", desc_nj);

  edm::ParameterSetDescription desc_ec;
  desc_ec.add<vector<unsigned>>("Njets",{1,2,3});
  desc_ec.add<double>("beta",1.0);
  desc.add<edm::ParameterSetDescription>("ECF", desc_ec);

  descriptions.add("GenMassAnalyzer",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(GenMassAnalyzer);
