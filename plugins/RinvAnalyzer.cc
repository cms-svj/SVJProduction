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
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

//STL headers 
#include <vector>
#include <memory>
#include <cmath>
#include <iostream>
using std::vector;

//
// class declaration
//

class RinvAnalyzer : public edm::one::EDAnalyzer<> {
	public:
		explicit RinvAnalyzer(const edm::ParameterSet&);
		~RinvAnalyzer() {}
	
		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
		
	private:
		void beginJob() override;
		void doBeginRun_(const edm::Run&, const edm::EventSetup&) override {}
		void analyze(const edm::Event&, const edm::EventSetup&) override;
		void doEndRun_(const edm::Run&, const edm::EventSetup&) override {}
		void endJob() override;
		
		// ----------member data ---------------------------
		edm::EDGetTokenT<vector<reco::GenParticle>> tok_part;
		int nVector, nVectorInv, nPseudoscalar, nPseudoscalarInv;
};

//
// constructors and destructor
//
RinvAnalyzer::RinvAnalyzer(const edm::ParameterSet& iConfig) :
	tok_part(consumes<vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("PartTag"))),
	nVector(0), nVectorInv(0), nPseudoscalar(0), nPseudoscalarInv(0)
{
}

//
// member functions
//

void RinvAnalyzer::beginJob()
{
}

// ------------ method called on each new Event  ------------
void RinvAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	edm::Handle<vector<reco::GenParticle>> h_part;
	iEvent.getByToken(tok_part,h_part);
	
	for(const auto& i_part : *(h_part.product())){
		int hvpdgid = std::abs(i_part.pdgId()) - 4900000;
		if(hvpdgid==111 or hvpdgid==211){
			++nPseudoscalar;
			if(i_part.numberOfDaughters()>0 and std::abs(i_part.daughter(0)->pdgId())==51) ++nPseudoscalarInv;
		}
		else if(hvpdgid==113 or hvpdgid==213){
			++nVector;
			if(i_part.numberOfDaughters()>0 and std::abs(i_part.daughter(0)->pdgId())==53) ++nVectorInv;
		}
	}
}

void RinvAnalyzer::endJob()
{
	std::cout << "Pseudoscalar rinv = " << double(nPseudoscalarInv)/double(nPseudoscalar) << std::endl;
	std::cout << "Vector rinv = " << double(nVectorInv)/double(nVector) << std::endl;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void RinvAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	edm::ParameterSetDescription desc;
	desc.add<edm::InputTag>("PartTag",edm::InputTag("genParticles"));
	
	descriptions.add("RinvAnalyzer",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(RinvAnalyzer);
