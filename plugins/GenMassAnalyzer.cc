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
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/Math/interface/deltaPhi.h"

//ROOT headers
#include <TTree.h>
#include <TLorentzVector.h>
 
//STL headers 
#include <vector>
#include <memory>
#include <cmath>
using std::vector;

//user headers
#include "SVJ/Production/interface/lester_mt2_bisect.h"

//
// class declaration
//

class GenMassAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
	public:
		explicit GenMassAnalyzer(const edm::ParameterSet&);
		~GenMassAnalyzer() {}
	
		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
		
		struct GenNtuple {
			vector<TLorentzVector> GenJetsAK8;
			vector<TLorentzVector> HVMesons;
			vector<TLorentzVector> METSystems;
			double MET = 0.;
			double METPhi = 0.;
			double DeltaPhi1 = 0.;
			double DeltaPhi2 = 0.;
			double DeltaPhiMin = 0.;
			double MJJ = 0.;
			double MT = 0.;
			double Mmc = 0.;
			double MT2 = 0.;
			double MAOS = 0.;
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
	tok_met(consumes<vector<reco::GenMET>>(iConfig.getParameter<edm::InputTag>("METTag"))),
	tok_jet(consumes<vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("JetTag"))),
	tok_part(consumes<vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("PartTag")))
{
	usesResource("TFileService");
}

//
// member functions
//

void GenMassAnalyzer::beginJob()
{
	asymm_mt2_lester_bisect::disableCopyrightMessage();
	
	tree = fs->make<TTree>("tree","tree");
	
	tree->Branch("GenJetsAK8" , "vector<TLorentzVector>", &entry.GenJetsAK8, 32000, 0);
	tree->Branch("HVMesons"   , "vector<TLorentzVector>", &entry.HVMesons, 32000, 0);
	tree->Branch("METSystems" , "vector<TLorentzVector>", &entry.METSystems, 32000, 0);
	tree->Branch("MET"        , &entry.MET              , "MET/D");
	tree->Branch("METPhi"     , &entry.METPhi           , "METPhi/D");
	tree->Branch("DeltaPhi1"  , &entry.DeltaPhi1        , "DeltaPhi1/D");
	tree->Branch("DeltaPhi2"  , &entry.DeltaPhi2        , "DeltaPhi2/D");
	tree->Branch("DeltaPhiMin", &entry.DeltaPhiMin      , "DeltaPhiMin/D");
	tree->Branch("MJJ"        , &entry.MJJ              , "MJJ/D");
	tree->Branch("MT"         , &entry.MT               , "MT/D");
	tree->Branch("Mmc"        , &entry.Mmc              , "Mmc/D");
	tree->Branch("MT2"        , &entry.MT2              , "MT2/D");
	tree->Branch("MAOS"       , &entry.MAOS             , "MT2/D");
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
	
	vector<TLorentzVector> jets;
	jets.reserve(h_jet->size());
	TLorentzVector vjetsSum;
	for(const auto& i_jet : *(h_jet.product())){
		jets.emplace_back(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());
		vjetsSum += jets.back();
	}
	entry.GenJetsAK8 = jets;
	
	vector<TLorentzVector> parts;
	TLorentzVector vpartsSum;
	for(const auto& i_part : *(h_part.product())){
		if(std::abs(i_part.pdgId())==4900211){
			parts.emplace_back(i_part.px(),i_part.py(),i_part.pz(),i_part.energy());
			vpartsSum += parts.back();
		}
	}
	entry.HVMesons = parts;
	
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
		TLorentzVector vmc = vjetsSum + vpartsSum;
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
  descriptions.add("GenMassAnalyzer",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(GenMassAnalyzer);
