#include <algorithm>
#include <iostream>
#include <iterator>
#include <fstream>
#include <string>
#include <memory>

#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "SVJ/Production/interface/common.h"
#ifndef CMSSW71X
#include "FWCore/Utilities/interface/propagate_const.h"
#endif
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include "HepMC/IO_GenEvent.h"

class HepMCEventWriterNew : public edm::one::EDAnalyzer<edm::one::WatchRuns> {
public:
  explicit HepMCEventWriterNew(const edm::ParameterSet &params);
  ~HepMCEventWriterNew() override;

protected:
  void beginRun(const edm::Run &run, const edm::EventSetup &es) override;
  void endRun(const edm::Run &run, const edm::EventSetup &es) override;
  void analyze(const edm::Event &event, const edm::EventSetup &es) override;

private:
#ifndef CMSSW71X
  edm::propagate_const<HepMC::IO_GenEvent *> output_;
#else
  HepMC::IO_GenEvent* output_;
#endif
  edm::InputTag hepMCProduct_;
  edm::EDGetTokenT<edm::HepMCProduct> hepMCToken_;
};

HepMCEventWriterNew::HepMCEventWriterNew(const edm::ParameterSet &params)
    : hepMCProduct_(params.getParameter<edm::InputTag>("hepMCProduct")),
      hepMCToken_(consumes<edm::HepMCProduct>(hepMCProduct_))
 {}

HepMCEventWriterNew::~HepMCEventWriterNew() {}

void HepMCEventWriterNew::beginRun(const edm::Run &run, const edm::EventSetup &es) {
  output_ = new HepMC::IO_GenEvent("GenEvent_ASCII.dat", std::ios::out);
}

void HepMCEventWriterNew::endRun(const edm::Run &run, const edm::EventSetup &es) {
#ifndef CMSSW71X
  if (output_)
    delete output_.get();
#endif
}

void HepMCEventWriterNew::analyze(const edm::Event &event, const edm::EventSetup &es) {
  edm::Handle<edm::HepMCProduct> product;
  event.getByToken(hepMCToken_, product);

  const HepMC::GenEvent *evt = product->GetEvent();

  output_->write_event(evt);
}

DEFINE_FWK_MODULE(HepMCEventWriterNew);
