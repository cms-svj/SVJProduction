// description: consider other particle IDs in madgraph-style generator-level HT filter

// system include files
#include <memory>
#include <string>
#include <vector>
#include <cmath>
#include <unordered_set>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDFilter.h"
#include "FWCore/Framework/interface/GetterOfProducts.h"
#include "FWCore/Framework/interface/ProcessMatch.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

class LHENParticleFilter : public edm::global::EDFilter<> {
	public:
		explicit LHENParticleFilter(const edm::ParameterSet&);
		~LHENParticleFilter() override {}

		bool filter(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

	private:
		// member data
		edm::GetterOfProducts<LHEEventProduct> getterOfProducts_;
		int min_, max_;
		std::unordered_set<int> particleIDs_;
};

LHENParticleFilter::LHENParticleFilter(const edm::ParameterSet& iConfig) :
	getterOfProducts_(edm::ProcessMatch("*"), this),
	min_(iConfig.getParameter<int>("min")),
	max_(iConfig.getParameter<int>("max"))
{
	callWhenNewProductsRegistered(getterOfProducts_);
	auto particle_vec = iConfig.getParameter<std::vector<int>>("particleIDs");
	particleIDs_ = std::unordered_set<int>(particle_vec.begin(),particle_vec.end());
}

bool LHENParticleFilter::filter(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
	std::vector<edm::Handle<LHEEventProduct> > handles;
	getterOfProducts_.fillHandles(iEvent, handles);

	int count = 0;
	if(!handles.empty()){
		edm::Handle<LHEEventProduct> evt = handles[0];
		const lhef::HEPEUP hepeup = evt->hepeup();
		const int nup = hepeup.NUP;
		const std::vector<int> idup = hepeup.IDUP;

		for(unsigned i = 0; i < (unsigned)nup; ++i){
			int PID = idup[i];
			if(particleIDs_.find(std::abs(PID))!=particleIDs_.end()) ++count;
		}
	}

	return ((min_<0 or count>=min_) and (max_<0 or count<=max_));
}

void LHENParticleFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	edm::ParameterSetDescription desc;
	desc.add<std::vector<int>>("particleIDs",{});
	desc.add<int>("min",-1);
	desc.add<int>("max",-1);

	descriptions.add("LHENParticleFilter",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(LHENParticleFilter);
