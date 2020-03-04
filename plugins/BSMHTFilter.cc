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

// handle CMSSW_7_1_X
#include "SVJ/Production/interface/common.h"

class BSMHTFilter : public edm::global::EDFilter<> {
	public:
		explicit BSMHTFilter(const edm::ParameterSet&);
		~BSMHTFilter() override {}

		bool filter(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

	private:
		// member data
		edm::GetterOfProducts<LHEEventProduct> getterOfProducts_;
		double htMin_;
		std::unordered_set<int> particleIDs_;
};

BSMHTFilter::BSMHTFilter(const edm::ParameterSet& iConfig) :
	getterOfProducts_(edm::ProcessMatch("*"), this),
	htMin_(iConfig.getParameter<double>("htMin"))
{
	callWhenNewProductsRegistered(getterOfProducts_);
	auto particle_vec = iConfig.getParameter<std::vector<int>>("particleIDs");
	//insert default madgraph particles
	particle_vec.insert(particle_vec.end(),{1,2,3,4,5,21});
	particleIDs_ = std::unordered_set<int>(particle_vec.begin(),particle_vec.end());
    //store the HT value
    produces<double>("");
}

bool BSMHTFilter::filter(edm::StreamID, edm::Event& iEvent, const edm::EventSetup& iSetup) const {
	double genHT = 0.0;

	std::vector<edm::Handle<LHEEventProduct> > handles;
	getterOfProducts_.fillHandles(iEvent, handles);

	if(!handles.empty()){
		edm::Handle<LHEEventProduct> evt = handles[0];
		const lhef::HEPEUP hepeup = evt->hepeup();
		const int nup = hepeup.NUP;
		const std::vector<int> idup = hepeup.IDUP;
		const std::vector<lhef::HEPEUP::FiveVector> pup = hepeup.PUP;
		const std::vector<int> istup = hepeup.ISTUP;
		const std::vector<std::pair<int,int>> momup = hepeup.MOTHUP;

		for(unsigned i = 0; i < (unsigned)nup; ++i){
			int PID    = idup[i];
			int status = istup[i];
			int mom1id = std::abs(idup[momup[i].first-1]);
			int mom2id = std::abs(idup[momup[i].second-1]);
			double px = (pup[i])[0];
			double py = (pup[i])[1];
			double pt = std::sqrt(px*px+py*py);

			// gen HT used to bin samples does not count top/W decay products
			if(status==1 and mom1id!=6 and mom1id!=24 and mom2id!=6 and mom2id!=24 and particleIDs_.find(std::abs(PID))!=particleIDs_.end()){
				genHT += pt;
			}
		}

	}

#ifndef CMSSW71X
	auto genHTptr = std::make_unique<double>(genHT);
    iEvent.put(std::move(genHTptr));
#else
    std::auto_ptr<double> genHTptr(new double(genHT));
    iEvent.put(genHTptr);
#endif
	return genHT > htMin_;
}

void BSMHTFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	edm::ParameterSetDescription desc;
	desc.add<std::vector<int>>("particleIDs",{});
	desc.add<double>("htMin",400);

	descriptions.add("BSMHTFilter",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(BSMHTFilter);
