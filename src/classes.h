#include <vector>
#include "TLorentzVector.h"
#include "DataFormats/Common/interface/Wrapper.h"

namespace {
  struct dictionary {
    std::vector<TLorentzVector> vlv;
    std::vector<std::vector<TLorentzVector> > vvlv;
    edm::Wrapper<std::vector<TLorentzVector> > wvlv;
    edm::Wrapper<std::vector<std::vector<TLorentzVector> > > wvvlv;
  };
}
