// system include files
#include <memory>
#include <vector>
#include <string>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/JetReco/interface/BasicJet.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "FWCore/Utilities/interface/transform.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Common/interface/getRef.h"
#include "DataFormats/Common/interface/ValueMap.h"

//
// class declaration
//

class GenJetSubstructurePacker : public edm::stream::EDProducer<> {
   public:

      explicit GenJetSubstructurePacker(const edm::ParameterSet&);
      ~GenJetSubstructurePacker();

   private:
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      
      // ----------member data ---------------------------

      // data labels
      float                                        distMax_;      
      edm::EDGetTokenT<std::vector<reco::GenJet>>       jetToken_;
      edm::EDGetTokenT<std::vector<reco::BasicJet>>   algoToken_;
      std::vector<edm::EDGetTokenT<edm::ValueMap<float>>> floatTokens_;
      std::vector<std::string> floatLabels_;
};

GenJetSubstructurePacker::GenJetSubstructurePacker(const edm::ParameterSet& iConfig) :
  distMax_(iConfig.getParameter<double>("distMax")),
  jetToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("jetSrc"))),
  algoToken_(consumes<std::vector<reco::BasicJet>>(iConfig.getParameter<edm::InputTag>("algoTag"))),
  floatLabels_(iConfig.getParameter<std::vector<std::string>>("algoFloatLabels"))
{
  const auto& algoFloatTags(iConfig.getParameter<std::vector<edm::InputTag>>("algoFloatTags"));
  if (algoFloatTags.size()!=floatLabels_.size())
    throw cms::Exception("ParamMismatch") << "algoFloatTags size (" << algoFloatTags.size() << ") should match algoFloatLabels size (" << floatLabels_.size() << ")";
  for (unsigned j = 0; j < algoFloatTags.size(); ++j) {
    floatTokens_.emplace_back(consumes<edm::ValueMap<float>>(algoFloatTags[j]));
    produces<edm::ValueMap<float>>(floatLabels_[j]);
  }

  //register products
  produces<std::vector<reco::GenJet>>();
}


GenJetSubstructurePacker::~GenJetSubstructurePacker()
{
}


// ------------ method called to produce the data  ------------
void
GenJetSubstructurePacker::produce(edm::Event& iEvent, const edm::EventSetup&)
{  
  auto outputs = std::make_unique<std::vector<reco::GenJet>>();

  edm::Handle<std::vector<reco::GenJet>> jetHandle;
  edm::Handle<std::vector<reco::BasicJet>> algoHandle;
  std::vector<edm::Handle<edm::ValueMap<float>>> floatHandles;
  std::vector<std::vector<float>> floatVecs;

  iEvent.getByToken(jetToken_, jetHandle);
  iEvent.getByToken(algoToken_, algoHandle);
  for (const auto& tok : floatTokens_) {
    floatHandles.emplace_back();
    iEvent.getByToken(tok, floatHandles.back());
    floatVecs.emplace_back();
  }

  // Loop over the input jets that will be modified.
  for (auto const & ijet : *jetHandle) {
    // Copy the jet.
    outputs->push_back(ijet);

    // Loop over the substructure collections
    std::vector<edm::Ptr<reco::GenJet>> nextSubjets;

    unsigned jctr = 0;
    for (auto const & jjet : *algoHandle) {
      if (reco::deltaR(ijet, jjet) < distMax_) {
        auto jjetRef = edm::getRef(algoHandle, jctr);
        for (unsigned f = 0; f < floatHandles.size(); ++f) {
          const auto& floatHandle(floatHandles[f]);
          floatVecs[f].push_back((*floatHandle)[jjetRef]);
        }
        for (size_t ida = 0; ida < jjet.numberOfDaughters(); ++ida) {
          reco::CandidatePtr candPtr =  jjet.daughterPtr(ida);
          nextSubjets.emplace_back(candPtr);
        }
        break;
      }
      ++jctr;
    }

    std::vector<reco::CandidatePtr> daughtersInSubjets;
    std::vector<reco::CandidatePtr> daughtersNew;
    const std::vector<reco::CandidatePtr> & jdaus = outputs->back().daughterPtrVector();
    for (const auto & subjet : nextSubjets) {
      const std::vector<reco::CandidatePtr> & sjdaus = subjet->daughterPtrVector();
      // check that the subjet does not contain any extra constituents not contained in the jet
      bool skipSubjet = false;
      for (const reco::CandidatePtr & dau : sjdaus) {
        if (std::find(jdaus.begin(), jdaus.end(), dau) == jdaus.end()) {
          skipSubjet = true;
          break;
        }
      }
      if (skipSubjet) continue;

      daughtersInSubjets.insert(daughtersInSubjets.end(), sjdaus.begin(), sjdaus.end());
      daughtersNew.push_back( reco::CandidatePtr(subjet) );
    }
    for (const reco::CandidatePtr & dau : jdaus) {
      if (std::find(daughtersInSubjets.begin(), daughtersInSubjets.end(), dau) == daughtersInSubjets.end()) {
        daughtersNew.push_back( dau );
      }
    }
    outputs->back().clearDaughters();
    for (const auto & dau : daughtersNew) outputs->back().addDaughter(dau);
  }

  auto outputHandle = iEvent.put(std::move(outputs));
  //make new value maps
  for (unsigned f = 0; f < floatVecs.size(); ++f) {
    auto floatOutput = std::make_unique<edm::ValueMap<float>>();
    edm::ValueMap<float>::Filler filler(*floatOutput);
    filler.insert(outputHandle, floatVecs[f].begin(), floatVecs[f].end());
    filler.fill();
    iEvent.put(std::move(floatOutput), floatLabels_[f]);
  }

}

//define this as a plug-in
DEFINE_FWK_MODULE(GenJetSubstructurePacker);
