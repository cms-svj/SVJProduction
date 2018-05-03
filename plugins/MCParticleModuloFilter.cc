// description: select events where the multiplicity of specified particle is a multiple of provided number

// system include files
#include <memory>
#include <string>
#include <cmath>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

class MCParticleModuloFilter : public edm::global::EDFilter<> {
	public:
		explicit MCParticleModuloFilter(const edm::ParameterSet&);
		~MCParticleModuloFilter() override {}

		bool filter(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

	private:
		// member data
		const edm::EDGetTokenT<edm::HepMCProduct> token_;
		int particleID_;
		unsigned multipleOf_;
		bool absID_;
};

MCParticleModuloFilter::MCParticleModuloFilter(const edm::ParameterSet& iConfig) :
	token_(consumes<edm::HepMCProduct>(iConfig.getParameter<edm::InputTag>("moduleLabel"))),
	particleID_(iConfig.getParameter<int>("particleID")),
	multipleOf_(iConfig.getParameter<unsigned>("multipleOf")),
	absID_(iConfig.getParameter<bool>("absID"))
{

}

bool MCParticleModuloFilter::filter(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
	// get input
	edm::Handle<edm::HepMCProduct> h_evt;
	iEvent.getByToken(token_,h_evt);
	const HepMC::GenEvent * myGenEvent = h_evt->GetEvent();
	
	unsigned sum_part = 0;
	for(auto i_part = myGenEvent->particles_begin(); i_part != myGenEvent->particles_end(); ++i_part){
		int id_part = (*i_part)->pdg_id();
		if(absID_) id_part = std::abs(id_part);
		if(id_part == particleID_) ++sum_part;
	}
	
	return (sum_part % multipleOf_ == 0);
}

void MCParticleModuloFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	edm::ParameterSetDescription desc;
	desc.add<edm::InputTag>("moduleLabel",edm::InputTag("generator","unsmeared"));
	desc.add<int>("particleID",0);
	desc.add<unsigned>("multipleOf",1);
	desc.add<bool>("absID",false);

	descriptions.add("MCParticleModuloFilter",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MCParticleModuloFilter);
