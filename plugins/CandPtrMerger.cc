/* \class CandPtrMerger
 * 
 * Producer of merged Candidate forward pointer collection 
 *
 * \author: Lauren Hay
 *
 */
#include "FWCore/Framework/interface/MakerMacros.h"
#include "SVJ/Production/interface/UniqueMerger.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/PtrVector.h"

namespace edm {
  namespace clonehelper {
    template <typename T>
    struct CloneTrait<edm::PtrVector<T> > {
      typedef CopyPolicy<edm::Ptr<T>> type;
    };
  }  // namespace clonehelper
}  // namespace edm

typedef UniqueMerger<std::vector<edm::Ptr<reco::Candidate>>> CandPtrMerger;
typedef UniqueMerger<edm::PtrVector<reco::Candidate>> CandPtrVectorMerger;

DEFINE_FWK_MODULE(CandPtrMerger);
DEFINE_FWK_MODULE(CandPtrVectorMerger);
