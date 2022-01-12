#ifndef ECFHelper_h
#define ECFHelper_h

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "fastjet/contrib/EnergyCorrelator.hh"
#include "DataFormats/JetReco/interface/GenJet.h"
#include <utility>

//based on RecoJets/JetProducers/interface/ECFAdder.h

class ECFHelper {
	public:
		explicit ECFHelper(const edm::ParameterSet& iConfig);
		virtual ~ECFHelper() {}
		std::vector<double> getECFs(const reco::GenJet& object) const;
		
	private:
		std::vector<unsigned> Njets_;
		double                beta_ ;
		
		std::vector<std::unique_ptr<fastjet::contrib::EnergyCorrelator> > routine_; 
};

ECFHelper::ECFHelper(const edm::ParameterSet& iConfig) :
	Njets_(iConfig.getParameter<std::vector<unsigned> >("Njets")),
	beta_(iConfig.getParameter<double>("beta"))
{
	routine_.reserve(Njets_.size());
	for (auto n : Njets_){
		routine_.push_back(std::make_unique<fastjet::contrib::EnergyCorrelator>(n, beta_, fastjet::contrib::EnergyCorrelator::pt_R));
	}
}

std::vector<double> ECFHelper::getECFs(const reco::GenJet& object) const
{
	std::vector<fastjet::PseudoJet> FJparticles;
	for(unsigned k = 0; k < object.numberOfDaughters(); ++k){
		const reco::CandidatePtr& dp = object.daughterPtr(k);
		if(dp.isNonnull() && dp.isAvailable())
			FJparticles.push_back(fastjet::PseudoJet(dp->px(), dp->py(), dp->pz(), dp->energy()));
	}
    fastjet::JetDefinition jetDef(fastjet::antikt_algorithm, 999);
    fastjet::ClusterSequence thisClustering_basic(FJparticles, jetDef);
    std::vector<fastjet::PseudoJet> out_jets_basic = thisClustering_basic.inclusive_jets(0);
    
	std::vector<double> result;
	result.reserve(routine_.size());
	for(unsigned index = 0; index < routine_.size(); ++index){
		if(out_jets_basic.size()!=1) result.push_back(-1);
		else result.push_back(routine_[index]->result(out_jets_basic[0]));
	}
	
	return result;
}

#endif
