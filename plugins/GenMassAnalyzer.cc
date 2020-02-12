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
#include <memory>
#include <cmath>
#include <iostream>
using std::vector;

//user headers
#include "SVJ/Production/interface/common.h"
#include "SVJ/Production/interface/lester_mt2_bisect.h"
#include "SVJ/Production/interface/NjettinessHelper.h"
#include "SVJ/Production/interface/ECFHelper.h"

//
// class declaration
//

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
	tok_part(consumes<vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("PartTag")))
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
	tree->Branch("GenJetsAK8" , "vector<TLorentzVector>", &entry.GenJetsAK8, 32000, 0);
	tree->Branch("GenJetsAK8_AxisAverage" , "vector<double>", &entry.GenJetsAK8_AxisAverage, 32000, 0);
	tree->Branch("GenJetsAK8_AxisMajor" , "vector<double>", &entry.GenJetsAK8_AxisMajor, 32000, 0);
	tree->Branch("GenJetsAK8_AxisMinor" , "vector<double>", &entry.GenJetsAK8_AxisMinor, 32000, 0);
	tree->Branch("GenJetsAK8_ECF1" , "vector<double>", &entry.GenJetsAK8_ECF1, 32000, 0);
	tree->Branch("GenJetsAK8_ECF2" , "vector<double>", &entry.GenJetsAK8_ECF2, 32000, 0);
	tree->Branch("GenJetsAK8_ECF3" , "vector<double>", &entry.GenJetsAK8_ECF3, 32000, 0);
	tree->Branch("GenJetsAK8_MomentGirth" , "vector<double>", &entry.GenJetsAK8_MomentGirth, 32000, 0);
	tree->Branch("GenJetsAK8_MomentHalf" , "vector<double>", &entry.GenJetsAK8_MomentHalf, 32000, 0);
	tree->Branch("GenJetsAK8_Multiplicity" , "vector<int>", &entry.GenJetsAK8_Multiplicity, 32000, 0);
	tree->Branch("GenJetsAK8_PtD" , "vector<double>", &entry.GenJetsAK8_PtD, 32000, 0);
	tree->Branch("GenJetsAK8_Tau1" , "vector<double>", &entry.GenJetsAK8_Tau1, 32000, 0);
	tree->Branch("GenJetsAK8_Tau2" , "vector<double>", &entry.GenJetsAK8_Tau2, 32000, 0);
	tree->Branch("GenJetsAK8_Tau3" , "vector<double>", &entry.GenJetsAK8_Tau3, 32000, 0);
	tree->Branch("HVMesons"   , "vector<TLorentzVector>", &entry.HVMesons, 32000, 0);
	tree->Branch("MAOS"       , &entry.MAOS             , "MAOS/D");
	tree->Branch("METSystems" , "vector<TLorentzVector>", &entry.METSystems, 32000, 0);
	tree->Branch("MET"        , &entry.MET              , "MET/D");
	tree->Branch("METPhi"     , &entry.METPhi           , "METPhi/D");
	tree->Branch("MJJ"        , &entry.MJJ              , "MJJ/D");
	tree->Branch("Mmc"        , &entry.Mmc              , "Mmc/D");
	tree->Branch("MT"         , &entry.MT               , "MT/D");
	tree->Branch("MT2"        , &entry.MT2              , "MT2/D");
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
