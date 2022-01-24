#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/global/EDFilter.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/EDGetToken.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include <cmath>
#include <cstdlib>
#include <vector>
#include <atomic>

class GenJetPTFilter : public edm::global::EDFilter<> {
  public:
    explicit GenJetPTFilter(const edm::ParameterSet&);
    bool filter(edm::StreamID, edm::Event&, const edm::EventSetup&) const override;

    void incPass() const {nPass_++;}
    void incFail() const {nFail_++;}

    void endJob() override {
      if (verbose_) {
        float eff = nPass_ + nFail_ > 0 ? ((double)nPass_) / (nPass_ + nFail_) : 0.0 ;
        // Need this to *always* print, which is unreliable with CMSSW MessageLogger
        std::cout
          << "GenJetPTFilter efficiency: nPass: " << nPass_
          << "  nFail: " << nFail_
          << "  nTotal: " << nFail_ + nPass_
          << "  eff: " << eff
          << std::endl;
        }
      }

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    bool verbose_;
    // While mutables in a multi-threaded const class are terrible, I'd argue filters shouldn't be const,
    // and should count their passes and fails themselves rather than some producer.
    // At least it's okay for multithreading now.
    mutable std::atomic<int> nPass_;
    mutable std::atomic<int> nFail_;
    const double ptMin_;
    edm::EDGetTokenT<reco::GenJetCollection> inputTag_GenJetCollection_;
  };

using namespace std;

GenJetPTFilter::GenJetPTFilter(const edm::ParameterSet& iConfig):
  verbose_(iConfig.getParameter<bool>("verbose")),
  ptMin_(iConfig.getParameter<double>("ptMin"))
  {
    nPass_ = 0;
    nFail_ = 0;
    inputTag_GenJetCollection_ = consumes<reco::GenJetCollection>(
        iConfig.getUntrackedParameter<edm::InputTag>("inputTag_GenJetCollection", edm::InputTag("ak8GenJetsNoNu"))
        );
    }

bool GenJetPTFilter::filter(edm::StreamID, edm::Event& iEvent, const edm::EventSetup&) const {
  edm::Handle<vector<reco::GenJet> > handleGenJets;
  iEvent.getByToken(inputTag_GenJetCollection_, handleGenJets);
  const vector<reco::GenJet>* genJets = handleGenJets.product();
  for (unsigned i = 0; i < genJets->size(); i++) {
    const reco::GenJet* j = &((*genJets)[i]);
    if (j->p4().pt() > ptMin_) {
      incPass();
      return true;
      }
    }
  incFail();
  return false;
  }

void GenJetPTFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<double>("ptMin", 350.);
  desc.add<bool>("verbose", true);
  descriptions.add("GenJetPTFilter",desc);
}

DEFINE_FWK_MODULE(GenJetPTFilter);