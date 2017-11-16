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
#include "DataFormats/JetReco/interface/BasicJet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

//ROOT headers
#include <TTree.h>
#include <TLorentzVector.h>
 
//STL headers 
#include <vector>
#include <memory>
#include <cmath>
#include <iostream>
using std::vector;

//
// class declaration
//

class SoftDropAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
	public:
		explicit SoftDropAnalyzer(const edm::ParameterSet&);
		~SoftDropAnalyzer() {}
	
		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
		
	private:
		void beginJob() override;
		void doBeginRun_(const edm::Run&, const edm::EventSetup&) override {}
		void analyze(const edm::Event&, const edm::EventSetup&) override;
		void doEndRun_(const edm::Run&, const edm::EventSetup&) override {}
		void endJob() override {}
		
		// ----------member data ---------------------------
		edm::Service<TFileService> fs;
		TTree* tree;

		//tokens
		edm::EDGetTokenT<vector<reco::BasicJet>> tok_jet;
};

//
// constructors and destructor
//
SoftDropAnalyzer::SoftDropAnalyzer(const edm::ParameterSet& iConfig) :
	tree(NULL),
	tok_jet(consumes<vector<reco::BasicJet>>(iConfig.getParameter<edm::InputTag>("JetTag")))
{
	usesResource("TFileService");
}

//
// member functions
//

void SoftDropAnalyzer::beginJob()
{
//	tree = fs->make<TTree>("tree","tree");	
}

// ------------ method called on each new Event  ------------
void SoftDropAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	edm::Handle<vector<reco::BasicJet>> h_jet;
	iEvent.getByToken(tok_jet,h_jet);

	int ctr = 0;
	for(const auto& i_jet : *(h_jet.product())){
		if(ctr==2) break;
		TLorentzVector vsj;
		for(unsigned k = 0; k < i_jet.numberOfDaughters(); ++k){
			const reco::Candidate* part = i_jet.daughter(k);
			unsigned numdau = part->numberOfDaughters();
			//only subjets have daughters
			if(numdau>0) {
				TLorentzVector vtmp(part->px(),part->py(),part->pz(),part->energy());
				vsj += vtmp;
			}
		}
		std::cout << "jet " << ctr << ", m_sd = " << vsj.M() << std::endl;
		ctr++;
	}
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void SoftDropAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	edm::ParameterSetDescription desc;
	desc.add<edm::InputTag>("JetTag",edm::InputTag("ak8GenJetsNoNuSoftDrop"));
	
	descriptions.add("SoftDropAnalyzer",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(SoftDropAnalyzer);
