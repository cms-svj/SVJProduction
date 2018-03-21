// this is a really terrible hack to avoid compiling this in CMSSW_7_1_X
#ifdef FASTJET_VERSION_NUMBER

// system include files
#include <memory>
#include <vector>

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
      edm::EDGetTokenT<std::vector<reco::GenJet> >       jetToken_;
      std::vector<edm::InputTag>                   algoTags_;
      std::vector< edm::EDGetTokenT< std::vector<reco::BasicJet> > >   algoTokens_;
};

GenJetSubstructurePacker::GenJetSubstructurePacker(const edm::ParameterSet& iConfig) :
  distMax_( iConfig.getParameter<double>("distMax") ),
  jetToken_(consumes<std::vector<reco::GenJet> >( iConfig.getParameter<edm::InputTag>("jetSrc") )),
  algoTags_ (iConfig.getParameter<std::vector<edm::InputTag> > ( "algoTags" ))
{
  algoTokens_ =edm::vector_transform(algoTags_, [this](edm::InputTag const & tag){return consumes< std::vector<reco::BasicJet> >(tag);});

  //register products
  produces<std::vector<reco::GenJet> > ();
}


GenJetSubstructurePacker::~GenJetSubstructurePacker()
{
}


// ------------ method called to produce the data  ------------
void
GenJetSubstructurePacker::produce(edm::Event& iEvent, const edm::EventSetup&)
{  

  std::unique_ptr< std::vector<reco::GenJet> > outputs( new std::vector<reco::GenJet> );
 
  edm::Handle< std::vector<reco::GenJet> > jetHandle;
  std::vector< edm::Handle< std::vector<reco::BasicJet> > > algoHandles;

  iEvent.getByToken( jetToken_, jetHandle );
  algoHandles.resize( algoTags_.size() );
  for ( size_t i = 0; i < algoTags_.size(); ++i ) {
    iEvent.getByToken( algoTokens_[i], algoHandles[i] ); 
  }

  // Loop over the input jets that will be modified.
  for ( auto const & ijet : *jetHandle  ) {
    // Copy the jet.
    outputs->push_back( ijet );

    // Loop over the substructure collections
    for ( auto const & ialgoHandle : algoHandles ) {      
      std::vector< edm::Ptr<reco::GenJet> > nextSubjets;

      for ( auto const & jjet : *ialgoHandle ) {
        
        if ( reco::deltaR( ijet, jjet ) < distMax_ ) {
          for ( size_t ida = 0; ida < jjet.numberOfDaughters(); ++ida ) {

            reco::CandidatePtr candPtr =  jjet.daughterPtr( ida);
            nextSubjets.push_back( edm::Ptr<reco::GenJet> ( candPtr ) );
          }
          break;
        }
        
      }

      std::vector<reco::CandidatePtr> daughtersInSubjets;
      std::vector<reco::CandidatePtr> daughtersNew;
      const std::vector<reco::CandidatePtr> & jdaus = outputs->back().daughterPtrVector();
      for ( const auto & subjet : nextSubjets) {
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
  }

  iEvent.put(std::move(outputs));

}

//define this as a plug-in
DEFINE_FWK_MODULE(GenJetSubstructurePacker);

#endif
