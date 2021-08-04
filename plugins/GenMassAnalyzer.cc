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
#include "DataFormats/Math/interface/LorentzVector.h"

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
#include <unordered_set>
using std::vector;
using std::set;

//user headers
#include "SVJ/Production/interface/common.h"
#include "SVJ/Production/interface/lester_mt2_bisect.h"
#include "SVJ/Production/interface/NjettinessHelper.h"
#include "SVJ/Production/interface/ECFHelper.h"

typedef math::XYZTLorentzVector LorentzVector;

typedef std::unordered_set<unsigned> PidSet;
typedef const reco::Candidate* CandPtr;
typedef std::unordered_set<CandPtr> CandSet;
//
// class declaration
//

namespace darkIdList{
    // variables useful for jet identification
    PidSet DarkMediatorIDs_ = {4900001,4900002,4900003,4900004,4900005,4900006};
    PidSet DarkQuarkIDs_ = {4900101,4900102};
    PidSet DarkHadronIDs_ = {4900111,4900113,4900211,4900213};
    PidSet DarkGluonIDs_ = {4900021};
    PidSet DarkStableIDs_ = {51,52,53};
    PidSet SMQuarkIDs_ = {1,2,3,4,5,6,7,8};
};

namespace usefulConst{
    double pTCut = 0;
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
      vector<double> GenJetsAK8_dptFrac;
      // soft drop jets for different jet categories
      vector<TLorentzVector> GenJetsAK8_SDJets;
      vector<double> GenJetsAK8_SDdptFrac;
      // for noNu vs. Nu jets comparison
      vector<double> GenJetsAK8_ptRatioNu;
      vector<double> GenJetsAK8_ptRatioConst;
      vector<int> GenJetsAK8_hvCategory;
      vector<int> svj_t_MT2JetsID;
      double svj_t_MT2 = 0.;
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

    // Check and see if the pdgId belongs to a list of dark IDs
    bool isDark(const PidSet& darkList, CandPtr part) const {
      return isDark(darkList, part->pdgId());
    }

    bool isDark(const PidSet& darkList, int pid) const {
      return darkList.find(std::abs(pid)) != darkList.end();
    }

    bool isDark(const CandSet& darkList, CandPtr part) const {
      return darkList.find(part) != darkList.end();
    }

    bool isAncestor(const PidSet& darkList, CandPtr part) const {
      if(isDark(darkList, part)) return true;
      for(size_t i=0;i< part->numberOfMothers();i++)
      {
        if(isAncestor(darkList,part->mother(i))) return true;
      }
      return false;
    }

    // store the first daughters from the first dark mediator(s)
    void medDecay(CandPtr part, CandPtr& firstQdM1, CandPtr& firstQdM2, CandPtr& firstQsM1, CandPtr& firstQsM2, bool& secondDM, bool& secondSM) const {
      // loop through the daughters of the first dark mediator
      for(unsigned i = 0; i < part->numberOfDaughters(); i++){
        CandPtr dau = part->daughter(i);
        // if the first dark mediator's daughter is still a dark mediator, then check the daughters of this daughter dark mediator until we get daughters that are not dark mediator
        if(isDark(darkIdList::DarkMediatorIDs_,dau)) medDecay(dau,firstQdM1,firstQdM2,firstQsM1,firstQsM2,secondDM,secondSM);
        else{
          if(isDark(darkIdList::DarkQuarkIDs_,dau)){
            if(secondDM == false){
              firstQdM1 = dau;
              secondDM = true;
            }
            else firstQdM2 = dau;
          }
          else if(isDark(darkIdList::SMQuarkIDs_,dau)){
            if(secondSM == false){
              firstQsM1 = dau;
              secondSM = true;
            }
            else firstQsM2 = dau;
          }
        }
      }
    }

    // store the dark immediate daughters of the earliest dark particles
    void firstDark(CandPtr part, CandSet& firstMd, CandSet& firstQd, CandSet& firstGd, CandPtr& firstQdM1, CandPtr& firstQdM2, CandPtr& firstQsM1, CandPtr& firstQsM2, bool& secondDM, bool& secondSM) const {
      PidSet DarkFirstIDs_;
      DarkFirstIDs_.insert( darkIdList::DarkMediatorIDs_.begin(), darkIdList::DarkMediatorIDs_.end());
      DarkFirstIDs_.insert( darkIdList::DarkQuarkIDs_.begin(), darkIdList::DarkQuarkIDs_.end());
      DarkFirstIDs_.insert( darkIdList::DarkGluonIDs_.begin(), darkIdList::DarkGluonIDs_.end());
      if(isDark(DarkFirstIDs_,part)){
        CandPtr parent = part->mother(0);
        if(isDark(DarkFirstIDs_,parent)) firstDark(parent, firstMd, firstQd, firstGd, firstQdM1, firstQdM2, firstQsM1, firstQsM2, secondDM, secondSM);
        else{
          //SM parent of first dark particles: fill first two vectors here, use mediators to fill second two vectors
          for(unsigned i = 0; i < part->numberOfDaughters(); i++){
            CandPtr dau = part->daughter(i);
            if (isDark(darkIdList::DarkMediatorIDs_,dau)){
              firstMd.insert(dau);
              medDecay(dau,firstQdM1,firstQdM2,firstQsM1,firstQsM2,secondDM,secondSM);
            }
            else if (isDark(darkIdList::DarkQuarkIDs_,dau)) firstQd.insert(dau);
            else if (isDark(darkIdList::DarkGluonIDs_,dau)) firstGd.insert(dau);
          }
        }
      }
    }

    // classify a jet as dark jet if there is a last dark particle within the jet radius
    int checkLast(const reco::GenJet& jet, CandSet stableDs, int value, double& frac) const {
      bool match = false;
      LorentzVector p4;
      LorentzVector totPt = jet.p4();
      for (unsigned i = 0 ; i < jet.numberOfDaughters(); i ++ ){
        // see if any jet constituent is a last dark descendant
        CandPtr dau = jet.daughter(i);
        if(isAncestor(darkIdList::DarkHadronIDs_,dau)){
            match = true;
            p4 += dau->p4();
        }
      }
      for(const auto& part : stableDs){
         if(reco::deltaR(jet, *part) < usefulConst::coneSize)
         {
           p4 += part->p4();
           totPt += part->p4();
         }
      }
      frac = p4.pt()/totPt.pt();
      return match ? value : 0;
    }

    // record first dark particles that are within the jets' radii
    int checkFirst(const reco::GenJet& jet, const CandSet& firstP, int value) const {
     for(const auto& part : firstP){
        if(reco::deltaR(jet, *part) < usefulConst::coneSize) return value;
     }
     return 0;
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
                          vector<reco::GenJet>& mjC_){
      for(unsigned j = 0; j < jC_.size() ; j++){
        double pTcan = 0;
        bool matched = false;
        const reco::GenJet* canJet;
        const reco::GenJet& jjet = jC_[j];
        // ijet is a jet of packedGenJetsAK8NoNu
        // jjet is a jet of ak8GenJets
        for(const auto& ijet : *(h_packedjet.product())){
          double ipT = ijet.pt();
          double dr = reco::deltaR(jjet, ijet);
          if (dr < usefulConst::coneSize && ipT > pTcan){
            pTcan = ipT;
            canJet = &ijet;
            matched = true;
          }
        }
        if (matched){
          pjC_.push_back(*canJet);
          mjC_.push_back(jjet);
        }
      }
    }

    // match particles from mediator to jets
    void matchPFMtoJet(CandPtr& part, vector<LorentzVector>& matchedJets,
      const reco::GenJet& jet, int& nPartPerJet, int& t_MT2JetID, const int& mt2ID)
    {
      if(reco::deltaR(jet,*part) < usefulConst::coneSize and jet.pt()>100)
      {
        matchedJets.push_back(jet.p4());
        nPartPerJet ++;
        t_MT2JetID = mt2ID;
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
          LorentzVector NuPt;
          for (unsigned j = 0; j < mjet.numberOfDaughters(); j++)
          {
            CandPtr mdau = mjet.daughter(i);
            if (isDark(darkIdList::DarkStableIDs_,mdau))
            {
              NuPt += mdau->p4();
            }
          }
          ptratConst.push_back(NuPt.Pt()/mjet.pt());
      }
    }
    // for ak8GenJets collection
    void fillAK8Jets(const vector<reco::GenJet>& genJets,
                    vector<TLorentzVector>& jetBranch)
    {
      jetBranch.reserve(genJets.size());
      for(unsigned i = 0; i < genJets.size(); i++)
      {
        const reco::GenJet& i_jet = genJets[i];
        jetBranch.emplace_back(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());
      }
    }

    // constructing soft drop jet from the noNu jet sample for ak8GenJets collection
    void softDropJet(const vector<reco::GenJet>& pjC_,
                    const vector<reco::GenJet>& mjC_,
                    vector<TLorentzVector>& pjC_SDJ,
                    vector<double>& sddarkFract,
                    CandSet stableDs)
    {
      for(unsigned i = 0; i < pjC_.size(); i++)
      {
        const reco::GenJet& i_jet = pjC_[i];
        LorentzVector vsj;
        for(unsigned k = 0; k < i_jet.numberOfDaughters(); k++) // looking at all constituants of a jet
        {
          const reco::Candidate* part = i_jet.daughter(k);
          unsigned numdau = part->numberOfDaughters();
          if(numdau>0) //only subjets have daughters
          {
            LorentzVector vtmp = part->p4();
            vsj += vtmp;
          }
        }

        if (vsj != LorentzVector(0.,0.,0.,0.))
        {
          double frac = 0;
          checkLast(mjC_[i],stableDs,1,frac);
          sddarkFract.push_back(frac);
          pjC_SDJ.emplace_back(vsj.Px(),vsj.Py(),vsj.Pz(),vsj.energy());
        }
      }
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
  tree->Branch("GenJetsAK8_darkPtFrac",        "vector<double>",         &entry.GenJetsAK8_dptFrac,      32000, 0);
  // softdrop jet for different jet categories
  tree->Branch("GenJetsAK8_SDJets",         "vector<TLorentzVector>", &entry.GenJetsAK8_SDJets,       32000, 0);
  tree->Branch("GenJetsAK8_SDdptFrac",      "vector<double>",         &entry.GenJetsAK8_SDdptFrac,    32000, 0);
  // for noNu vs. non-noNu jets comparison
  tree->Branch("GenJetsAK8_ptRatioNu" ,     "vector<double>",         &entry.GenJetsAK8_ptRatioNu,    32000, 0);
  tree->Branch("GenJetsAK8_ptRatioConst" ,  "vector<double>",         &entry.GenJetsAK8_ptRatioConst, 32000, 0);
  tree->Branch("GenJetsAK8_hvCategory" ,    "vector<int>",            &entry.GenJetsAK8_hvCategory,   32000, 0);
  tree->Branch("svj_t_MT2JetsID" ,          "vector<int>",            &entry.svj_t_MT2JetsID,         32000, 0);
  tree->Branch("svj_t_MT2",                 &entry.svj_t_MT2,         "svj_t_MT2/D");
}

// ------------ method called on each new Event  ------------
void GenMassAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
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
  CandPtr firstQdM1, firstQdM2, firstQsM1, firstQsM2;
  CandSet stableDs, firstMd, firstQd, firstGd, firstQdM, firstQsM;
  vector<LorentzVector> dQM1Js,dQM2Js,SMM1Js,SMM2Js;
  vector<int> t_MT2JetsID;
  vector<reco::GenJet> AK8Jets;
  vector<reco::GenJet> pAK8Jets;
  // The ak8genjets that are matched to packedGenJetsAK8NoNu
  // useful for dark pt fraction estimation
  vector<reco::GenJet> mAK8Jets;
  bool secondDM = false;
  bool secondSM = false;
  bool manyParticlesPerJet = false;
  entry.GenJetsAK8.reserve(h_jet->size());
  for(const auto& i_part : *(h_part.product())){
    firstDark(&i_part, firstMd, firstQd, firstGd, firstQdM1, firstQdM2, firstQsM1, firstQsM2,secondDM,secondSM);
    if(static_cast<const reco::GenParticle*>(&i_part)->isLastCopy() and isDark(darkIdList::DarkStableIDs_,&i_part)) stableDs.insert(&i_part);
  }
  firstQdM.insert(firstQdM1);
  firstQdM.insert(firstQdM2);
  firstQsM.insert(firstQsM1);
  firstQsM.insert(firstQsM2);
  //loop over gen jets
  for(const auto& i_jet : *(h_jet.product())){
    if(i_jet.pt() > usefulConst::pTCut){
      int category = 0;
      double frac = 0;
      entry.GenJetsAK8.emplace_back(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());
      AK8Jets.push_back(i_jet);
      category += checkLast(i_jet,stableDs,1,frac);
      category += checkFirst(i_jet, firstQd,  2);
      category += checkFirst(i_jet, firstGd,  4);
      category += checkFirst(i_jet, firstQdM, 8);
      category += checkFirst(i_jet, firstQsM, 16);
      entry.GenJetsAK8_hvCategory.push_back(category);
      entry.GenJetsAK8_dptFrac.push_back(frac);
      // t-channel MT2 Right Combination
      if(firstMd.size()==2){
        int t_MT2JetID = 0;
        int nPartPerJet = 0;
        matchPFMtoJet(firstQdM1,dQM1Js,i_jet,nPartPerJet,t_MT2JetID,1);
        matchPFMtoJet(firstQdM2,dQM2Js,i_jet,nPartPerJet,t_MT2JetID,2);
        matchPFMtoJet(firstQsM1,SMM1Js,i_jet,nPartPerJet,t_MT2JetID,3);
        matchPFMtoJet(firstQsM2,SMM2Js,i_jet,nPartPerJet,t_MT2JetID,4);
        t_MT2JetsID.push_back(t_MT2JetID);
        if(nPartPerJet > 1) manyParticlesPerJet = true;
      }
    }
  }
  bool oneJetPerParticle = dQM1Js.size() == 1 && dQM2Js.size() == 1 && SMM1Js.size() == 1 && SMM2Js.size() == 1;
  if(oneJetPerParticle && !manyParticlesPerJet)
  {
    const auto& i_met = h_met->front();
    double METx = i_met.px();
    double METy = i_met.py();
    LorentzVector FJet0 = dQM1Js[0] + SMM1Js[0];
    LorentzVector FJet1 = dQM2Js[0] + SMM2Js[0];
    double t_mt2 = asymm_mt2_lester_bisect::get_mT2(
      FJet0.M(), FJet0.Px(), FJet0.Py(),
      FJet1.M(), FJet1.Px(), FJet1.Py(),
      METx, METy, 0.0, 0.0, 0
    );
    entry.svj_t_MT2 = t_mt2;
  }
  else
  {
    vector<int> zeros(AK8Jets.size(),0);
    t_MT2JetsID = zeros;
  }
  for(const auto& mt2ID: t_MT2JetsID) entry.svj_t_MT2JetsID.push_back(mt2ID);
  // matchJet_to_NoNu(AK8Jets, h_packedjet, pAK8Jets, mAK8Jets);
  calcPtRatioNu(pAK8Jets, mAK8Jets, entry.GenJetsAK8_ptRatioNu, entry.GenJetsAK8_ptRatioConst);
  softDropJet(pAK8Jets, mAK8Jets, entry.GenJetsAK8_SDJets, entry.GenJetsAK8_SDdptFrac,stableDs);

  // entry.GenJetsAK8.reserve(h_jet->size());
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
    // entry.GenJetsAK8.emplace_back(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());

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
  desc.add<edm::InputTag>("JetTag",edm::InputTag("ak8GenJetsNoNu"));
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
