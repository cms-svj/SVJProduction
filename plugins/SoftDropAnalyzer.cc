//framework headers
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h" 

//analysis headers
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Math/interface/deltaPhi.h"

//ROOT headers
#include <TTree.h>
#include <TLorentzVector.h>
 
//STL headers 
#include <vector>
#include <memory>
#include <cmath>
#include <iostream>
#include <numeric>
using std::vector;
// Stuff to sort the two part_DH lists the same way
template <typename TLorentzVector, typename Compare>
std::vector<std::size_t> sort_permutation(
    const std::vector<TLorentzVector>& vec,
    Compare& compare)
{
    std::vector<std::size_t> p(vec.size());
    std::iota(p.begin(), p.end(), 0);
    std::sort(p.begin(), p.end(),
        [&](std::size_t i, std::size_t j){ return compare(vec[i].Pt(), vec[j].Pt()); });
    return p;
}

template <typename TLorentzVector>
void apply_permutation_in_place(
    std::vector<TLorentzVector>& vec,
    const std::vector<std::size_t>& p)
{
    std::vector<bool> done(vec.size());
    for (std::size_t i = 0; i < vec.size(); ++i)
    {
        if (done[i])
        {
            continue;
        }
        done[i] = true;
        std::size_t prev_j = i;
        std::size_t j = p[i];
        while (i != j)
        {
            std::swap(vec[prev_j], vec[j]);
            done[j] = true;
            prev_j = j;
            j = p[j];
        }
    }
}
bool cmp(double a, double b)
{
    return a > b;
}

//
// class declaration
//

class SoftDropAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
	public:
		explicit SoftDropAnalyzer(const edm::ParameterSet&);
		~SoftDropAnalyzer() {}
	
		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
		
		struct GenNtuple {
			int evtNum = 0;
			int hasNoDarkMother = 0;
			TLorentzVector GenJetsAK8;
			TLorentzVector SDJets;
			int numDH = 0;
			vector<TLorentzVector> particleDH;
			vector<TLorentzVector> partonDH;
			vector<TLorentzVector> particleSDDH;
			vector<TLorentzVector> partonSDDH;
		};

	private:
		void beginJob() override;
		void doBeginRun_(const edm::Run&, const edm::EventSetup&) override {}
		void analyze(const edm::Event&, const edm::EventSetup&) override;
		void doEndRun_(const edm::Run&, const edm::EventSetup&) override {}
		void endJob() override {}
		
		// ----------member data ---------------------------
		edm::Service<TFileService> fs;
		TTree* tree;
		GenNtuple entry;

		//tokens
		edm::EDGetTokenT<vector<reco::GenJet>> tok_jet;
};

//
// constructors and destructor
//
SoftDropAnalyzer::SoftDropAnalyzer(const edm::ParameterSet& iConfig) :
	tree(NULL),
	tok_jet(consumes<vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("JetTag")))
{
	usesResource("TFileService");
}

//
// member functions
//

void SoftDropAnalyzer::beginJob()
{
	tree = fs->make<TTree>("tree","tree");
	
	tree->Branch("evtNum", &entry.evtNum, "evtNum/I");
	//tree->Branch("GenJetsAK8" , "vector<TLorentzVector>", &entry.GenJetsAK8, 32000, 0);
	tree->Branch("GenJetsAK8","GenJetsAK8",&entry.GenJetsAK8);
	//tree->Branch("SDJets" , "vector<TLorentzVector>", &entry.SDJets, 32000, 0);
	tree->Branch("SDJets","SDJets",&entry.SDJets);
	tree->Branch("hasNoDarkMother",&entry.hasNoDarkMother, "hasNoDarkMother/I");
	//tree->Branch("numDH" , &entry.numDH , "numDH/I");
	tree->Branch("particleDH","vector<TLorentzVector>",&entry.particleDH, 32000,0);
	tree->Branch("partonDH","vector<TLorentzVector>",&entry.partonDH, 32000,0);
	tree->Branch("particleSDDH","vector<TLorentzVector>",&entry.particleSDDH, 32000,0);
	tree->Branch("partonSDDH","vector<TLorentzVector>",&entry.partonSDDH, 32000,0);
}

// ------------ method called on each new Event  ------------
void SoftDropAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	edm::Handle<vector<reco::GenJet>> h_jet;
	iEvent.getByToken(tok_jet,h_jet);

	int ctr = 0;
	for(const auto& i_jet : *(h_jet.product())){
		entry = GenNtuple();
		entry.evtNum = iEvent.id().event();

		


		if(ctr<2){ // only do this for the leading two jets in the event
			
			TLorentzVector vsj;
			unsigned numSDsubjets = 0;
			for(unsigned k = 0; k < i_jet.numberOfDaughters(); ++k){ // looking at all constituants of a jet
				const reco::Candidate* part = i_jet.daughter(k);
				unsigned numdau = part->numberOfDaughters();
				
				if(numdau>0) { //only subjets have daughters, so here we're looking at only the two (possible) subjets of the
					TLorentzVector vtmp(part->px(),part->py(),part->pz(),part->energy());
					vsj += vtmp;
					numSDsubjets++;
				}
				
			}
			//if (fabs(vsj.M2() - 400.) < 0.001) { // checking for m_jet == m_dark_quark, our "SoftDrop Mass Anomaly"
				entry.GenJetsAK8 = TLorentzVector(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());
				entry.SDJets = vsj;
				vector<const reco::Candidate*> darkMothers;
				for(unsigned k = 0; k < i_jet.numberOfDaughters(); ++k){ //one jet, loop over daughters. first one or two are SDsubjets
					if(k<numSDsubjets){
						const reco::GenJet* i_part = (const reco::GenJet*)i_jet.daughter(k);
						for(auto const& genPart : i_part->getGenConstituents()){
							int nMothers = 0;
							vector<const reco::Candidate*> motherList; 
							for(unsigned a=0; a < genPart->numberOfMothers(); a++){ // get direct parent(s)
								const reco::Candidate* mother = genPart->mother(a);
								motherList.push_back(mother); //add parents to list
								nMothers ++; // increase counter
							}
							int c = 0; //index for while loop
							double momPt = -99; // to match particles to the proper DM
							while(c < nMothers){
								const reco::Candidate* iMother = motherList.at(c);
								c++;
								//if(iMother->pdgId() > 4900000) { // once we find a DM mother, stop
								if((iMother->pdgId() == 4900111) or (iMother->pdgId() == -4900111)) {
									momPt = iMother->pt();
									if((std::find(darkMothers.begin(), darkMothers.end(), iMother) == darkMothers.end())){ //true if iMother is not in darkMothers
										darkMothers.push_back(iMother);
										entry.partonDH.emplace_back(iMother->px(),iMother->py(),iMother->pz(),iMother->energy());
										entry.particleDH.push_back(TLorentzVector());
										entry.partonSDDH.emplace_back(iMother->px(),iMother->py(),iMother->pz(),iMother->energy());
										entry.particleSDDH.push_back(TLorentzVector());
									}
									int dmctr = 0;
									for(const reco::Candidate* darkMother : darkMothers){//Associating a dark Mother with our particle
										if(darkMother->pt() == momPt) {
											TLorentzVector vtmp(genPart->px(),genPart->py(),genPart->pz(),genPart->energy());
											entry.particleDH.at(dmctr) += vtmp;
											entry.particleSDDH.at(dmctr) += vtmp;
										}
										dmctr++;
									}
									break;
								} else { // if we don't find a DM mother, go to grandmothers...
									for(unsigned b=0; b< iMother->numberOfMothers(); b++){
										motherList.push_back(iMother->mother(b));
										nMothers++;
									}
								}
								
							}
							// Some SD jets do not have any dark mothers. Statistically possible, but how probable?
							if(darkMothers.size() == 0) {
								entry.hasNoDarkMother = 1;
							}
							
						}
					} else {// do everything again, but start at genParticle level, instead of GenJet
						const reco::GenParticle* genPart = (const reco::GenParticle*)i_jet.daughter(k);
						int nMothers = 0;
						vector<const reco::Candidate*> motherList;
						for(unsigned a=0; a < genPart->numberOfMothers(); a++){
							const reco::Candidate* mother = genPart->mother(a);
							motherList.push_back(mother);
							nMothers ++;
						}
						int c = 0;
						double momPt = -99;
						while(c < nMothers){
							const reco::Candidate* iMother = motherList.at(c);
							c++;
							if(iMother->pdgId() > 4900000) {
								momPt = iMother->pt();
								if((std::find(darkMothers.begin(), darkMothers.end(), iMother) == darkMothers.end())){ //true if iMother is not in darkMothers
									darkMothers.push_back(iMother);
									entry.partonDH.emplace_back(iMother->px(),iMother->py(),iMother->pz(),iMother->energy());
									entry.particleDH.push_back(TLorentzVector());
								}
								int dmctr = 0;
								for(const reco::Candidate* darkMother : darkMothers){
									if(darkMother->pt() == momPt) {
										TLorentzVector vtmp(genPart->px(),genPart->py(),genPart->pz(),genPart->energy());
										entry.particleDH.at(dmctr) += vtmp;
									}
									dmctr++;
								}
								break;
							} else {
								for(unsigned b=0; b< iMother->numberOfMothers(); b++){
									motherList.push_back(iMother->mother(b));
									nMothers++;
								}
							}
						}
						// Some SD jets do not have any dark mothers. Statistically possible, but how probable?
						if(darkMothers.size() == 0) {
							entry.hasNoDarkMother = 1;
						}
					}
				}
				auto p = sort_permutation(entry.particleDH, cmp);

				apply_permutation_in_place(entry.partonDH,p);
				apply_permutation_in_place(entry.particleDH,p);

				auto pSD = sort_permutation(entry.particleSDDH, cmp);

				apply_permutation_in_place(entry.partonSDDH,pSD);
				apply_permutation_in_place(entry.particleSDDH,pSD);

				tree->Fill();//tree is filled for each jet
			//}// This belongs to the SD mass checker if statment
 		}
		ctr++;
		
	}
	
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void SoftDropAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	edm::ParameterSetDescription desc;
	desc.add<edm::InputTag>("JetTag",edm::InputTag("packedGenJetsAK8NoNu"));
	
	descriptions.add("SoftDropAnalyzer",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(SoftDropAnalyzer);
