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
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"

//ROOT headers
#include <TTree.h>
#include <TLorentzVector.h>

//STL headers
#include <vector>
#include <memory>
#include <cmath>
#include <iostream>
#include <typeinfo>
#include <algorithm>
using std::vector;

//user headers
#include "SVJ/Production/interface/common.h"
#include "SVJ/Production/interface/lester_mt2_bisect.h"
#include "SVJ/Production/interface/NjettinessHelper.h"
#include "SVJ/Production/interface/ECFHelper.h"

//
// class declaration
//

class darkIdList{
	public:
		// variables useful for jet identification
		vector<int> DarkMediatorID_ = {4900001,4900002,4900003,4900004,4900005,4900006};
		vector<int> DarkQuarkID_ = {4900101,4900102};
		vector<int> DarkHadronID_ = {4900111,4900113,4900211,4900213};
		vector<int> DarkGluonID_ = {4900021};
};

class dJetsLab{
	public:
		reco::GenJet dark_jet;
		vector<std::string> cat_labels;
};

class GenMassAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
	public:
		explicit GenMassAnalyzer(const edm::ParameterSet&);
		~GenMassAnalyzer() {}

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

		struct GenNtuple {
			double DeltaPhi1 = 0.;
			double DeltaPhi2 = 0.;
			double DeltaPhiMin = 0.;
			vector<TLorentzVector> GenJetsAK8;
			vector<double> GenJetsAK8_AxisAverage;
			vector<double> GenJetsAK8_AxisMajor;
			vector<double> GenJetsAK8_AxisMinor;
			vector<double> GenJetsAK8_ECF1;
			vector<double> GenJetsAK8_ECF2;
			vector<double> GenJetsAK8_ECF3;
			vector<double> GenJetsAK8_MomentGirth;
			vector<double> GenJetsAK8_MomentHalf;
			vector<int> GenJetsAK8_Multiplicity;
			vector<double> GenJetsAK8_PtD;
			vector<double> GenJetsAK8_Tau1;
			vector<double> GenJetsAK8_Tau2;
			vector<double> GenJetsAK8_Tau3;
			vector<TLorentzVector> HVMesons;
			double MAOS = 0.;
			vector<TLorentzVector> METSystems;
			double MET = 0.;
			double METPhi = 0.;
			double MJJ = 0.;
			double Mmc = 0.;
			double MT = 0.;
			double MT2 = 0.;
			// added for extra jet categories
			vector<double> AK8_Tau1;
			vector<double> AK8_Tau2;
			vector<double> AK8_Tau3;
			vector<double> G_Tau1;
			vector<double> G_Tau2;
			vector<double> G_Tau3;
			vector<double> QM_Tau1;
			vector<double> QM_Tau2;
			vector<double> QM_Tau3;
			vector<double> Q_Tau1;
			vector<double> Q_Tau2;
			vector<double> Q_Tau3;
			vector<double> QM_QTau1;
			vector<double> QM_QTau2;
			vector<double> QM_QTau3;
			vector<double> QM_GTau1;
			vector<double> QM_GTau2;
			vector<double> QM_GTau3;
			vector<double> Q_GTau1;
			vector<double> Q_GTau2;
			vector<double> Q_GTau3;
			vector<double> G_SMTau1;
			vector<double> G_SMTau2;
			vector<double> G_SMTau3;
			vector<double> QM_SMTau1;
			vector<double> QM_SMTau2;
			vector<double> QM_SMTau3;
			vector<double> Q_SMTau1;
			vector<double> Q_SMTau2;
			vector<double> Q_SMTau3;
			vector<double> LD_lowDFTau1;
			vector<double> LD_lowDFTau2;
			vector<double> LD_lowDFTau3;
			vector<double> LD_highDFTau1;
			vector<double> LD_highDFTau2;
			vector<double> LD_highDFTau3;
			vector<double> LD_SMTau1;
			vector<double> LD_SMTau2;
			vector<double> LD_SMTau3;
			vector<double> SM_Tau1;
			vector<double> SM_Tau2;
			vector<double> SM_Tau3;
			vector<double> SMM_Tau1;
			vector<double> SMM_Tau2;
			vector<double> SMM_Tau3;
			// soft drop jets for different jet categories
			vector<TLorentzVector> AK8_SDJets;
			vector<TLorentzVector> G_SDJets;
			vector<TLorentzVector> QM_SDJets;
			vector<TLorentzVector> Q_SDJets;
			vector<TLorentzVector> QM_QSDJets;
			vector<TLorentzVector> QM_GSDJets;
			vector<TLorentzVector> Q_GSDJets;
			vector<TLorentzVector> G_SMSDJets;
			vector<TLorentzVector> QM_SMSDJets;
			vector<TLorentzVector> Q_SMSDJets;
			vector<TLorentzVector> LD_lowDFSDJets;
			vector<TLorentzVector> LD_highDFSDJets;
			vector<TLorentzVector> LD_SMSDJets;
			vector<TLorentzVector> SM_SDJets;
			vector<TLorentzVector> SMM_SDJets;
			vector<double> AK8_SDdptFrac;
			vector<double> G_SDdptFrac;
			vector<double> QM_SDdptFrac;
			vector<double> Q_SDdptFrac;
			vector<double> QM_QSDdptFrac;
			vector<double> QM_GSDdptFrac;
			vector<double> Q_GSDdptFrac;
			vector<double> G_SMSDdptFrac;
			vector<double> QM_SMSDdptFrac;
			vector<double> Q_SMSDdptFrac;
			vector<double> LD_lowDFSDdptFrac;
			vector<double> LD_highDFSDdptFrac;
			vector<double> LD_SMSDdptFrac;
			vector<double> SM_SDdptFrac;
			vector<double> SMM_SDdptFrac;
			// for noNu vs. non-noNu jets comparison
			vector<double> pG_ptRatioNu;
			vector<double> pQM_ptRatioNu;
			vector<double> pQ_ptRatioNu;
			vector<double> pQM_QptRatioNu;
			vector<double> pQM_GptRatioNu;
			vector<double> pQ_GptRatioNu;
			vector<double> pG_SMptRatioNu;
			vector<double> pQM_SMptRatioNu;
			vector<double> pQ_SMptRatioNu;
			vector<double> pLD_lowDFptRatioNu;
			vector<double> pLD_highDFptRatioNu;
			vector<double> pLD_SMptRatioNu;
			vector<double> pSM_ptRatioNu;
			vector<double> pSMM_ptRatioNu;
			vector<double> pG_ptRatioConst;
			vector<double> pQM_ptRatioConst;
			vector<double> pQ_ptRatioConst;
			vector<double> pQM_QptRatioConst;
			vector<double> pQM_GptRatioConst;
			vector<double> pQ_GptRatioConst;
			vector<double> pG_SMptRatioConst;
			vector<double> pQM_SMptRatioConst;
			vector<double> pQ_SMptRatioConst;
			vector<double> pLD_lowDFptRatioConst;
			vector<double> pLD_highDFptRatioConst;
			vector<double> pLD_SMptRatioConst;
			vector<double> pSM_ptRatioConst;
			vector<double> pSMM_ptRatioConst;
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
		//for tree branches
		GenNtuple entry;
#ifndef CMSSW71X
		NjettinessHelper njhelper;
		ECFHelper echelper;
#endif
		//tokens
		edm::EDGetTokenT<vector<reco::GenMET>> tok_met;
		edm::EDGetTokenT<vector<reco::GenJet>> tok_jet;
		edm::EDGetTokenT<vector<reco::GenParticle>> tok_part;
		edm::EDGetTokenT<vector<reco::GenJet>> tok_packedjet;

		// functions for jet identification
		TLorentzVector toTLV(const reco::GenParticle& part_i)
		{
			return TLorentzVector(part_i.px(),part_i.py(),part_i.pz(),part_i.energy());
		}

		TLorentzVector toTLV(const reco::Candidate* part_i)
		{
			return TLorentzVector(part_i->px(),part_i->py(),part_i->pz(),part_i->energy());
		}

		TLorentzVector toTLV(reco::GenJet i_jet)
		{
			return TLorentzVector(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());
		}

		int darkTruth(vector<int> darklist, int pId)
		{
			int dt = 0;
			for (auto &dark : darklist)
			{
				if (std::abs(pId) == dark)
				{
					dt = 1;
				}
			}
		  return dt;
		}
		// // function 'overloading' here, because dHad in the function argument can be
		// // GenParticle or Candidate*.
		void lastDau(vector<TLorentzVector>& lastD, const reco::Candidate* dHad) // find the last daughters
		{
			for (unsigned idH = 0; idH < dHad->numberOfDaughters(); idH++ )
			{
				const reco::Candidate* dauH = dHad->daughter(idH);
				int dauHID = dauH->pdgId();
				if (dauH->numberOfDaughters() == 0 && (dauHID != 51 || dauHID != 52 || dauHID != 53)) // last particle that is not stable dark hadron
				{
					TLorentzVector dauH_TL = toTLV(dauH);
					lastD.push_back(dauH_TL);
				}
				else if (dauH->numberOfDaughters() > 0)
				{
					lastDau(lastD,dauH);
				}
			}
		}

		void lastDau(vector<TLorentzVector>& lastD, const reco::GenParticle& dHad) // find the last daughters
		{
			for (unsigned idH = 0; idH < dHad.numberOfDaughters(); idH++ )
			{
				const reco::Candidate* dauH = dHad.daughter(idH);
				int dauHID = dauH->pdgId();
				if (dauH->numberOfDaughters() == 0 && (dauHID != 51 || dauHID != 52 || dauHID != 53)) // last particle that is not stable dark hadron
				{
					TLorentzVector dauH_TL = toTLV(dauH);
					lastD.push_back(dauH_TL);
				}
				else if (dauH->numberOfDaughters() > 0)
				{
					lastDau(lastD,dauH);
				}
			}
		}

		void lastDarkGQ(vector<int> DarkIDList, int partid, int part_ind,
										const reco::GenParticle& part_i,
										vector<TLorentzVector>& dPartList,
										vector<std::string>& dPartList_label,
										vector<TLorentzVector>& lastD)
		{
			darkIdList dil;

			if (darkTruth(DarkIDList,partid) && part_i.isLastCopy())
			{
				TLorentzVector part_i_TL = toTLV(part_i);
				dPartList.push_back(part_i_TL);
				dPartList_label.push_back('p' + std::to_string(part_ind));

				if (DarkIDList == dil.DarkHadronID_) // find last daughters of the last dark hadrons
				{
					lastDau(lastD,part_i);
				}
			}
		}

		void medDecay(const reco::Candidate* fdau,
									vector<TLorentzVector>& fdQPartFM,
									vector<TLorentzVector>& fdGPartFM,
									vector<TLorentzVector>& fSMqPart)
		{
			for (unsigned mddi = 0; mddi < fdau->numberOfDaughters(); mddi++)
			{
				darkIdList dil;

				const reco::Candidate* mdd = fdau->daughter(mddi);
				int mddId = mdd->pdgId();
				if (darkTruth(dil.DarkMediatorID_,mddId))
				{
					medDecay(mdd,fdQPartFM,fdGPartFM,fSMqPart);
				}
				else if (darkTruth(dil.DarkQuarkID_,mddId))
				{
					TLorentzVector mdd_TL = toTLV(mdd);
					fdQPartFM.push_back(mdd_TL);
				}
				else if (darkTruth(dil.DarkGluonID_,mddId))
				{
					TLorentzVector mdd_TL = toTLV(mdd);
					fdGPartFM.push_back(mdd_TL);
				}
				else
				{
					TLorentzVector mdd_TL = toTLV(mdd);
					fSMqPart.push_back(mdd_TL);
				}
			}
		}

		void firstDark(int partid, int part_ind, const reco::GenParticle& part_i,
									vector<TLorentzVector>& fdMPart,
									vector<TLorentzVector>& fdQPart,
									vector<TLorentzVector>& fdGPart,
									vector<TLorentzVector>& fdQPartFM,
									vector<TLorentzVector>& fdGPartFM,
									vector<TLorentzVector>& fSMqPart)
		{
			darkIdList dil;
			vector<int> DarkIDs = dil.DarkMediatorID_;
			DarkIDs.insert( DarkIDs.end(), dil.DarkQuarkID_.begin(), dil.DarkQuarkID_.end());
			DarkIDs.insert( DarkIDs.end(), dil.DarkGluonID_.begin(), dil.DarkGluonID_.end());

			if (part_ind < 20)
			{
				if (darkTruth(DarkIDs,partid) && part_i.numberOfMothers()==2)
				{
					for (unsigned dau_i = 0; dau_i < part_i.numberOfDaughters(); dau_i++)
					{
						const reco::Candidate* fdau = part_i.daughter(dau_i);
						int fdauId = fdau->pdgId();

						if (darkTruth(dil.DarkMediatorID_,fdauId))
						{
							TLorentzVector fdau_TL = toTLV(fdau);
							fdMPart.push_back(fdau_TL);
							medDecay(fdau,fdQPartFM,fdGPartFM,fSMqPart);
						}

						if (darkTruth(dil.DarkQuarkID_,fdauId))
						{
							TLorentzVector fdau_TL = toTLV(fdau);
							fdQPart.push_back(fdau_TL);
						}

						if (darkTruth(dil.DarkGluonID_,fdauId))
						{
							TLorentzVector fdau_TL = toTLV(fdau);
							fdGPart.push_back(fdau_TL);
						}
					}
				}

			}

		}

		double deltaRforTL(TLorentzVector TL1,TLorentzVector TL2){
			double phi1 = TL1.Phi();
			double phi2 = TL2.Phi();
			double eta1 = TL1.Eta();
			double eta2 = TL2.Eta();
			double dp = std::fabs(phi1 - phi2);
			if (dp > M_PI)
			{
				dp -= 2*M_PI;
			}
			double deltaR2 = (eta1 - eta2) * (eta1 - eta2) + dp * dp;
			return sqrt(deltaR2);
		}


		void checkDark(int& isDark,
									reco::GenJet ijet,
									vector<std::string>& dPartSet,
									vector<std::string> dPart_label,
									vector<TLorentzVector> dPart,
									vector<reco::GenJet>& dJets,
									vector<vector<std::string>>& dPartTrack)
		{
			for (unsigned idqCan = 0 ; idqCan < dPart.size(); idqCan ++ )
			{
				TLorentzVector dqCan = dPart[idqCan];
				std::string dqCan_label = dPart_label[idqCan];
				TLorentzVector ijet_TL = toTLV(ijet);
				double dR = deltaRforTL(ijet_TL, dqCan);
				if (dR<0.8)
				{
					isDark = 1;
					dPartSet.push_back(dqCan_label); // collecting all the dark particles in each dark jet
				}
			}

			if (isDark == 1) // if more than one quarks/gluons fall into the cone of one jet we still have only one dark jet
			{
				dPartTrack.push_back(dPartSet);
				dJets.push_back(ijet);
			}

		}

		void darkPtFract(vector<reco::GenJet> JetsList,
											vector<double>& wdpTFrac,
											vector<TLorentzVector> lastD)
		{
			for (unsigned iad = 0; iad < JetsList.size(); iad++)
			{
				TLorentzVector tot4vec = TLorentzVector(0.,0.,0.,0.);
				TLorentzVector dark4vec = TLorentzVector(0.,0.,0.,0.);
				const reco::GenJet& adj = JetsList[iad];
				auto anum = adj.numberOfDaughters();

				for (unsigned ani = 0; ani < anum; ani++)
				{
					TLorentzVector prt = toTLV(adj.daughter(ani));
					tot4vec += prt;

					if (std::find(lastD.begin(),lastD.end(),prt) != lastD.end())
					{
						dark4vec += prt;
					}

				}

				double jetDarkF = dark4vec.Pt()/tot4vec.Pt();
				wdpTFrac.push_back(jetDarkF);
			}
		}

		double darkPtFract(const reco::GenJet& adj,
											vector<TLorentzVector> lastD)
		{
			TLorentzVector tot4vec = TLorentzVector(0.,0.,0.,0.);
			TLorentzVector dark4vec = TLorentzVector(0.,0.,0.,0.);
			auto anum = adj.numberOfDaughters();

			for (unsigned ani = 0; ani < anum; ani++)
			{
				TLorentzVector prt = toTLV(adj.daughter(ani));
				tot4vec += prt;

				if (std::find(lastD.begin(),lastD.end(),prt) != lastD.end())
				{
					dark4vec += prt;
				}

			}

			double jetDarkF = dark4vec.Pt()/tot4vec.Pt();
			return jetDarkF;
		}

		void sortByDPt(vector<double>& dJPts, vector<reco::GenJet>& dJets, vector<vector<std::string>>& dPartTrack)
		{
			vector<double> sdJPts = dJPts; // sorted dark pt fractions
			vector<double> ddJPts = dJPts; // dummy dark pt fractions vector for sorting purpose

			vector<reco::GenJet> sdJets; // sorted dJets
			vector<vector<std::string>> sdPartTrack;

			sort(sdJPts.begin(),sdJPts.end());
			reverse(sdJPts.begin(),sdJPts.end());
			vector<int> sortIndex;

		  for (unsigned i = 0; i < sdJPts.size() ; i++)
		  {
		    for (unsigned j = 0; j < ddJPts.size(); j++)
		    {
		      if (sdJPts[i] == ddJPts[j])
		      {
		        ddJPts[j] = 999;
		        sortIndex.push_back(j);
		      }
		    }
		  }

			for (auto& newInd : sortIndex)
			{
				sdJets.push_back(dJets[newInd]);
				sdPartTrack.push_back(dPartTrack[newInd]);
			}

			dJPts = sdJPts;
			dJets = sdJets;
			dPartTrack = sdPartTrack;
		}

		void reclassToSM(vector<vector<std::string>>& dPartTrack,
										vector<reco::GenJet>& SMJets,
										vector<reco::GenJet>& dJets)
		{

			vector<vector<std::string>> dPlist = dPartTrack;

			for (unsigned i = 0; i < dPlist.size(); i++)
			{
				for (unsigned j = 0; j < dPlist.size(); j++)
				{
					if (i < j)
					{
						vector<int> comval;
						vector<std::string> list1 = dPlist[i];
		        vector<std::string> list2 = dPlist[j];

		        for (unsigned l1 = 0; l1 < list1.size(); l1++)
		        {
		          for (unsigned l2 = 0; l2 < list2.size(); l2++)
		          {
		            if (list1[l1] == list2[l2])
		            {
		              comval.push_back(l2);
		            }
		          }
		        }

						if (comval.size() > 0)
						{
							for (int k = comval.size() - 1; k >= 0; k--)
							{
								dPlist[j].erase(dPlist[j].begin() + comval[k]);
							}
						}

					}
				}
			}

			vector<int> indDel;

			for (unsigned ai = 0; ai < dPlist.size(); ai ++)
			{
				vector<std::string> arri = dPlist[ai];
				if (arri.size() == 0)
				{
					indDel.push_back(ai);
				}
			}

			for (int iidD = indDel.size() - 1; iidD >= 0; iidD--)
			{
				int idD = indDel[iidD];
				SMJets.push_back(dJets[idD]);
				dJets.erase(dJets.begin() + idD);
			}

		}

		void isfj(vector<TLorentzVector> fPart, const reco::GenJet& uj,
							std::string label, vector<std::string>& jlabels)
		{
			int isJ = 0;
			TLorentzVector ujTL = toTLV(uj);
			for (auto& fP : fPart)
			{
				if (deltaRforTL(fP,ujTL) < 0.8)
				{
					isJ = 1;
					break;
				}
			}
			if ((isJ) == 1)
			{
				jlabels.push_back(label);
			}

		}

		void DarkClass(vector<std::string> inOnly, vector<std::string> notIn,
									vector<std::string> djlab,
									const reco::GenJet& djjet,
									vector<reco::GenJet>& JetList)
		{
		  int tru = 1;
		  for (auto& ii : inOnly)
		  {
		      if (std::count(djlab.begin(), djlab.end(), ii) == 0)
		      {
		        tru = 0;
		      }
		  }

		  for (auto& ni : notIn)
		  {
		      if (std::count(djlab.begin(), djlab.end(), ni) > 0)
		      {
		        tru = 0;
		      }
		  }

		  if (tru == 1)
		  {
		    JetList.push_back(djjet);
		  }

		}

		void DarkClass(vector<std::string> inOnly, vector<std::string> notIn,
									vector<std::string> djlab,
									const reco::GenJet& djjet,
									vector<reco::GenJet>& lowDF_JetList,
									vector<reco::GenJet>& highDF_JetList,
									vector<TLorentzVector> lastD)
		{
		  int tru = 1;
		  for (auto& ii : inOnly)
		  {
		      if (std::count(djlab.begin(), djlab.end(), ii) == 0)
		      {
		        tru = 0;
		      }
		  }

		  for (auto& ni : notIn)
		  {
		      if (std::count(djlab.begin(), djlab.end(), ni) > 0)
		      {
		        tru = 0;
		      }
		  }

		  if (tru == 1 && darkPtFract(djjet,lastD) < 0.7)
		  {
		    lowDF_JetList.push_back(djjet);
		  }
			else if (tru == 1 && darkPtFract(djjet,lastD) >= 0.7)
		  {
		    highDF_JetList.push_back(djjet);
		  }
		}

		void fillSubs(vector<double>& etau1, vector<double>& etau2,
								vector<double>& etau3,
								vector<reco::GenJet> jet)
		{
			etau1.reserve(jet.size());
			etau2.reserve(jet.size());
			etau3.reserve(jet.size());

			for(const auto& i_jet : jet)
			{
				#ifndef CMSSW71X
						etau1.push_back(njhelper.getTau(1,i_jet));
						etau2.push_back(njhelper.getTau(2,i_jet));
						etau3.push_back(njhelper.getTau(3,i_jet));
				#endif

			}

		}

		void matchJet_to_NoNu(vector<reco::GenJet> jC_,
													edm::Handle<vector<reco::GenJet>> h_packedjet,
													vector<reco::GenJet>& pjC_,
													vector<reco::GenJet>& mjC_)
		{
			for(unsigned j = 0; j < jC_.size() ; j++)
			{
				vector<double> pTList;
				vector<reco::GenJet> canJet;

				const reco::GenJet& jjet = jC_[j];

				for(const auto& ijet : *(h_packedjet.product()))
				{
					if (ijet.pt() > 200)
					{
						double dr = deltaRforTL(toTLV(jjet),toTLV(ijet));
						if (dr < 0.8)
						{
							pTList.push_back(ijet.pt());
							canJet.push_back(ijet);
						}
					}
				}

				if (pTList.size() > 0)
				{ // find the jjet closest to the ijet
					int maxPtInd = std::max_element(pTList.begin(),pTList.end()) - pTList.begin();
					pjC_.push_back(canJet[maxPtInd]);
					mjC_.push_back(jjet);

				}

			}

		}

		void calcPtRatioNu(vector<reco::GenJet> pjC_,
											vector<reco::GenJet> mjC_,
											vector<double>& ptrat,
											vector<double>& ptratConst)
		{
			ptrat.reserve(pjC_.size());
			ptratConst.reserve(pjC_.size());

			for (unsigned i = 0; i < pjC_.size(); i++)
			{
					const reco::GenJet& pjet = pjC_[i];
					const reco::GenJet& mjet = mjC_[i];

					ptrat.push_back(pjet.pt()/mjet.pt());

					TLorentzVector NuPt;

					for (unsigned j = 0; j < mjet.numberOfDaughters(); j++)
					{
						int pid = mjet.daughter(j)->pdgId();
						if (pid != 51 && pid != 52 && pid != 53)
						{
							NuPt += toTLV(mjet.daughter(j));
						}
					}

					ptratConst.push_back(NuPt.Pt()/mjet.pt());
			}
		}

		void softDropJet(vector<reco::GenJet> pjC_,
										vector<reco::GenJet> mjC_,
										vector<TLorentzVector>& pjC_SDJ,
										vector<double>& sddarkFract,
										vector<TLorentzVector> lastD)
		{
			for(unsigned i = 0; i < pjC_.size(); i++)
			{
				const reco::GenJet& i_jet = pjC_[i];
				TLorentzVector vsj = TLorentzVector(0.,0.,0.,0.);
				for(unsigned k = 0; k < i_jet.numberOfDaughters(); k++) // looking at all constituants of a jet
				{
					const reco::Candidate* part = i_jet.daughter(k);
					unsigned numdau = part->numberOfDaughters();

					if(numdau>0) //only subjets have daughters, so here we're looking at only the two (possible) subjets of the
					{
						TLorentzVector vtmp(part->px(),part->py(),part->pz(),part->energy());
						vsj += vtmp;
					}

				}

				if (vsj != TLorentzVector(0.,0.,0.,0.))
				{
					sddarkFract.push_back(darkPtFract(mjC_[i], lastD));
					pjC_SDJ.emplace_back(vsj.Px(),vsj.Py(),vsj.Pz(),vsj.Energy());

				}
			}

		}

	};

//
// constructors and destructor
//
GenMassAnalyzer::GenMassAnalyzer(const edm::ParameterSet& iConfig) :
	tree(NULL),
#ifndef CMSSW71X
	njhelper(iConfig.getParameter<edm::ParameterSet>("Nsubjettiness")),
	echelper(iConfig.getParameter<edm::ParameterSet>("ECF")),
#endif
	tok_met(consumes<vector<reco::GenMET>>(iConfig.getParameter<edm::InputTag>("METTag"))),
	tok_jet(consumes<vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("JetTag"))),
	tok_part(consumes<vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("PartTag"))),
	tok_packedjet(consumes<vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("PackedJetTag")))
{
	usesResource("TFileService");
#ifdef CMSSW71X
	std::cout << "GenMassAnalyzer: Warning - Nsubjettiness and ECF variables not available!" << std::endl;
#endif
}


//
// member functions
//

void GenMassAnalyzer::beginJob()
{
	asymm_mt2_lester_bisect::disableCopyrightMessage();

	tree = fs->make<TTree>("tree","tree");

	tree->Branch("DeltaPhi1"  , &entry.DeltaPhi1        , "DeltaPhi1/D");
	tree->Branch("DeltaPhi2"  , &entry.DeltaPhi2        , "DeltaPhi2/D");
	tree->Branch("DeltaPhiMin", &entry.DeltaPhiMin      , "DeltaPhiMin/D");
	tree->Branch("GenJetsAK8" , "vector<TLorentzVector>", &entry.GenJetsAK8, 32000, 0);
	tree->Branch("GenJetsAK8_AxisAverage" , "vector<double>", &entry.GenJetsAK8_AxisAverage, 32000, 0);
	tree->Branch("GenJetsAK8_AxisMajor" , "vector<double>", &entry.GenJetsAK8_AxisMajor, 32000, 0);
	tree->Branch("GenJetsAK8_AxisMinor" , "vector<double>", &entry.GenJetsAK8_AxisMinor, 32000, 0);
	tree->Branch("GenJetsAK8_ECF1" , "vector<double>", &entry.GenJetsAK8_ECF1, 32000, 0);
	tree->Branch("GenJetsAK8_ECF2" , "vector<double>", &entry.GenJetsAK8_ECF2, 32000, 0);
	tree->Branch("GenJetsAK8_ECF3" , "vector<double>", &entry.GenJetsAK8_ECF3, 32000, 0);
	tree->Branch("GenJetsAK8_MomentGirth" , "vector<double>", &entry.GenJetsAK8_MomentGirth, 32000, 0);
	tree->Branch("GenJetsAK8_MomentHalf" , "vector<double>", &entry.GenJetsAK8_MomentHalf, 32000, 0);
	tree->Branch("GenJetsAK8_Multiplicity" , "vector<int>", &entry.GenJetsAK8_Multiplicity, 32000, 0);
	tree->Branch("GenJetsAK8_PtD" , "vector<double>", &entry.GenJetsAK8_PtD, 32000, 0);
	tree->Branch("GenJetsAK8_Tau1" , "vector<double>", &entry.GenJetsAK8_Tau1, 32000, 0);
	tree->Branch("GenJetsAK8_Tau2" , "vector<double>", &entry.GenJetsAK8_Tau2, 32000, 0);
	tree->Branch("GenJetsAK8_Tau3" , "vector<double>", &entry.GenJetsAK8_Tau3, 32000, 0);
	tree->Branch("HVMesons"   , "vector<TLorentzVector>", &entry.HVMesons, 32000, 0);
	tree->Branch("MAOS"       , &entry.MAOS             , "MAOS/D");
	tree->Branch("METSystems" , "vector<TLorentzVector>", &entry.METSystems, 32000, 0);
	tree->Branch("MET"        , &entry.MET              , "MET/D");
	tree->Branch("METPhi"     , &entry.METPhi           , "METPhi/D");
	tree->Branch("MJJ"        , &entry.MJJ              , "MJJ/D");
	tree->Branch("Mmc"        , &entry.Mmc              , "Mmc/D");
	tree->Branch("MT"         , &entry.MT               , "MT/D");
	tree->Branch("MT2"        , &entry.MT2              , "MT2/D");
	// added for extra jet categories
	tree->Branch("AK8_Tau1" , "vector<double>", &entry.AK8_Tau1, 32000, 0);
	tree->Branch("AK8_Tau2" , "vector<double>", &entry.AK8_Tau2, 32000, 0);
	tree->Branch("AK8_Tau3" , "vector<double>", &entry.AK8_Tau3, 32000, 0);
	tree->Branch("G_Tau1" , "vector<double>", &entry.G_Tau1, 32000, 0);
	tree->Branch("G_Tau2" , "vector<double>", &entry.G_Tau2, 32000, 0);
	tree->Branch("G_Tau3" , "vector<double>", &entry.G_Tau3, 32000, 0);
	tree->Branch("QM_Tau1" , "vector<double>", &entry.QM_Tau1, 32000, 0);
	tree->Branch("QM_Tau2" , "vector<double>", &entry.QM_Tau2, 32000, 0);
	tree->Branch("QM_Tau3" , "vector<double>", &entry.QM_Tau3, 32000, 0);
	tree->Branch("Q_Tau1" , "vector<double>", &entry.Q_Tau1, 32000, 0);
	tree->Branch("Q_Tau2" , "vector<double>", &entry.Q_Tau2, 32000, 0);
	tree->Branch("Q_Tau3" , "vector<double>", &entry.Q_Tau3, 32000, 0);
	tree->Branch("QM_QTau1" , "vector<double>", &entry.QM_QTau1, 32000, 0);
	tree->Branch("QM_QTau2" , "vector<double>", &entry.QM_QTau2, 32000, 0);
	tree->Branch("QM_QTau3" , "vector<double>", &entry.QM_QTau3, 32000, 0);
	tree->Branch("QM_GTau1" , "vector<double>", &entry.QM_GTau1, 32000, 0);
	tree->Branch("QM_GTau2" , "vector<double>", &entry.QM_GTau2, 32000, 0);
	tree->Branch("QM_GTau3" , "vector<double>", &entry.QM_GTau3, 32000, 0);
	tree->Branch("Q_GTau1" , "vector<double>", &entry.Q_GTau1, 32000, 0);
	tree->Branch("Q_GTau2" , "vector<double>", &entry.Q_GTau2, 32000, 0);
	tree->Branch("Q_GTau3" , "vector<double>", &entry.Q_GTau3, 32000, 0);
	tree->Branch("G_SMTau1" , "vector<double>", &entry.G_SMTau1, 32000, 0);
	tree->Branch("G_SMTau2" , "vector<double>", &entry.G_SMTau2, 32000, 0);
	tree->Branch("G_SMTau3" , "vector<double>", &entry.G_SMTau3, 32000, 0);
	tree->Branch("QM_SMTau1" , "vector<double>", &entry.QM_SMTau1, 32000, 0);
	tree->Branch("QM_SMTau2" , "vector<double>", &entry.QM_SMTau2, 32000, 0);
	tree->Branch("QM_SMTau3" , "vector<double>", &entry.QM_SMTau3, 32000, 0);
	tree->Branch("Q_SMTau1" , "vector<double>", &entry.Q_SMTau1, 32000, 0);
	tree->Branch("Q_SMTau2" , "vector<double>", &entry.Q_SMTau2, 32000, 0);
	tree->Branch("Q_SMTau3" , "vector<double>", &entry.Q_SMTau3, 32000, 0);
	tree->Branch("LD_lowDFTau1" , "vector<double>", &entry.LD_lowDFTau1, 32000, 0);
	tree->Branch("LD_lowDFTau2" , "vector<double>", &entry.LD_lowDFTau2, 32000, 0);
	tree->Branch("LD_lowDFTau3" , "vector<double>", &entry.LD_lowDFTau3, 32000, 0);
	tree->Branch("LD_highDFTau1" , "vector<double>", &entry.LD_highDFTau1, 32000, 0);
	tree->Branch("LD_highDFTau2" , "vector<double>", &entry.LD_highDFTau2, 32000, 0);
	tree->Branch("LD_highDFTau3" , "vector<double>", &entry.LD_highDFTau3, 32000, 0);
	tree->Branch("LD_SMTau1" , "vector<double>", &entry.LD_SMTau1, 32000, 0);
	tree->Branch("LD_SMTau2" , "vector<double>", &entry.LD_SMTau2, 32000, 0);
	tree->Branch("LD_SMTau3" , "vector<double>", &entry.LD_SMTau3, 32000, 0);
	tree->Branch("SM_Tau1" , "vector<double>", &entry.SM_Tau1, 32000, 0);
	tree->Branch("SM_Tau2" , "vector<double>", &entry.SM_Tau2, 32000, 0);
	tree->Branch("SM_Tau3" , "vector<double>", &entry.SM_Tau3, 32000, 0);
	tree->Branch("SMM_Tau1" , "vector<double>", &entry.SMM_Tau1, 32000, 0);
	tree->Branch("SMM_Tau2" , "vector<double>", &entry.SMM_Tau2, 32000, 0);
	tree->Branch("SMM_Tau3" , "vector<double>", &entry.SMM_Tau3, 32000, 0);
	// softdrop jet for different jet categories
	tree->Branch("AK8_SDJets","vector<TLorentzVector>",&entry.AK8_SDJets,32000, 0);
	tree->Branch("G_SDJets","vector<TLorentzVector>",&entry.G_SDJets,32000, 0);
	tree->Branch("QM_SDJets","vector<TLorentzVector>",&entry.QM_SDJets,32000, 0);
	tree->Branch("Q_SDJets","vector<TLorentzVector>",&entry.Q_SDJets,32000, 0);
	tree->Branch("QM_QSDJets","vector<TLorentzVector>",&entry.QM_QSDJets,32000, 0);
	tree->Branch("QM_GSDJets","vector<TLorentzVector>",&entry.QM_GSDJets,32000, 0);
	tree->Branch("Q_GSDJets","vector<TLorentzVector>",&entry.Q_GSDJets,32000, 0);
	tree->Branch("G_SMSDJets","vector<TLorentzVector>",&entry.G_SMSDJets,32000, 0);
	tree->Branch("QM_SMSDJets","vector<TLorentzVector>",&entry.QM_SMSDJets,32000, 0);
	tree->Branch("Q_SMSDJets","vector<TLorentzVector>",&entry.Q_SMSDJets,32000, 0);
	tree->Branch("LD_lowDFSDJets","vector<TLorentzVector>",&entry.LD_lowDFSDJets,32000, 0);
	tree->Branch("LD_highDFSDJets","vector<TLorentzVector>",&entry.LD_highDFSDJets,32000, 0);
	tree->Branch("LD_SMSDJets","vector<TLorentzVector>",&entry.LD_SMSDJets,32000, 0);
	tree->Branch("SM_SDJets","vector<TLorentzVector>",&entry.SM_SDJets,32000, 0);
	tree->Branch("SMM_SDJets","vector<TLorentzVector>",&entry.SMM_SDJets,32000, 0);

	tree->Branch("G_SDdptFrac","vector<double>",&entry.G_SDdptFrac,32000, 0);
	tree->Branch("QM_SDdptFrac","vector<double>",&entry.QM_SDdptFrac,32000, 0);
	tree->Branch("Q_SDdptFrac","vector<double>",&entry.Q_SDdptFrac,32000, 0);
	tree->Branch("QM_QSDdptFrac","vector<double>",&entry.QM_QSDdptFrac,32000, 0);
	tree->Branch("QM_GSDdptFrac","vector<double>",&entry.QM_GSDdptFrac,32000, 0);
	tree->Branch("Q_GSDdptFrac","vector<double>",&entry.Q_GSDdptFrac,32000, 0);
	tree->Branch("G_SMSDdptFrac","vector<double>",&entry.G_SMSDdptFrac,32000, 0);
	tree->Branch("QM_SMSDdptFrac","vector<double>",&entry.QM_SMSDdptFrac,32000, 0);
	tree->Branch("Q_SMSDdptFrac","vector<double>",&entry.Q_SMSDdptFrac,32000, 0);
	tree->Branch("LD_lowDFSDdptFrac","vector<double>",&entry.LD_lowDFSDdptFrac,32000, 0);
	tree->Branch("LD_highDFSDdptFrac","vector<double>",&entry.LD_highDFSDdptFrac,32000, 0);
	tree->Branch("LD_SMSDdptFrac","vector<double>",&entry.LD_SMSDdptFrac,32000, 0);
	tree->Branch("SM_SDdptFrac","vector<double>",&entry.SM_SDdptFrac,32000, 0);
	tree->Branch("SMM_SDdptFrac","vector<double>",&entry.SMM_SDdptFrac,32000, 0);
	// for noNu vs. non-noNu jets comparison
	tree->Branch("G_ptRatioNoNu_Nu" , "vector<double>", &entry.pG_ptRatioNu, 32000, 0);
	tree->Branch("QM_ptRatioNoNu_Nu" , "vector<double>", &entry.pQM_ptRatioNu, 32000, 0);
	tree->Branch("Q_ptRatioNoNu_Nu" , "vector<double>", &entry.pQ_ptRatioNu, 32000, 0);
	tree->Branch("QM_QptRatioNu" , "vector<double>", &entry.pQM_QptRatioNu, 32000, 0);
	tree->Branch("QM_GptRatioNu" , "vector<double>", &entry.pQM_GptRatioNu, 32000, 0);
	tree->Branch("Q_GptRatioNu" , "vector<double>", &entry.pQ_GptRatioNu, 32000, 0);
	tree->Branch("G_SMptRatioNu" , "vector<double>", &entry.pG_SMptRatioNu, 32000, 0);
	tree->Branch("QM_SMptRatioNu" , "vector<double>", &entry.pQM_SMptRatioNu, 32000, 0);
	tree->Branch("Q_SMptRatioNu" , "vector<double>", &entry.pQ_SMptRatioNu, 32000, 0);
	tree->Branch("LD_lowDFptRatioNu" , "vector<double>", &entry.pLD_lowDFptRatioNu, 32000, 0);
	tree->Branch("LD_highDFptRatioNu" , "vector<double>", &entry.pLD_highDFptRatioNu, 32000, 0);
	tree->Branch("LD_SMptRatioNu" , "vector<double>", &entry.pLD_SMptRatioNu, 32000, 0);
	tree->Branch("SM_ptRatioNu" , "vector<double>", &entry.pSM_ptRatioNu, 32000, 0);
	tree->Branch("SMM_ptRatioNu" , "vector<double>", &entry.pSMM_ptRatioNu, 32000, 0);
	tree->Branch("G_ptRatioConst" , "vector<double>", &entry.pG_ptRatioConst, 32000, 0);
	tree->Branch("QM_ptRatioConst" , "vector<double>", &entry.pQM_ptRatioConst, 32000, 0);
	tree->Branch("Q_ptRatioConst" , "vector<double>", &entry.pQ_ptRatioConst, 32000, 0);
	tree->Branch("QM_QptRatioConst" , "vector<double>", &entry.pQM_QptRatioConst, 32000, 0);
	tree->Branch("QM_GptRatioConst" , "vector<double>", &entry.pQM_GptRatioConst, 32000, 0);
	tree->Branch("Q_GptRatioConst" , "vector<double>", &entry.pQ_GptRatioConst, 32000, 0);
	tree->Branch("G_SMptRatioConst" , "vector<double>", &entry.pG_SMptRatioConst, 32000, 0);
	tree->Branch("QM_SMptRatioConst" , "vector<double>", &entry.pQM_SMptRatioConst, 32000, 0);
	tree->Branch("Q_SMptRatioConst" , "vector<double>", &entry.pQ_SMptRatioConst, 32000, 0);
	tree->Branch("LD_lowDFptRatioConst" , "vector<double>", &entry.pLD_lowDFptRatioConst, 32000, 0);
	tree->Branch("LD_highDFptRatioConst" , "vector<double>", &entry.pLD_highDFptRatioConst, 32000, 0);
	tree->Branch("LD_SMptRatioConst" , "vector<double>", &entry.pLD_SMptRatioConst, 32000, 0);
	tree->Branch("SM_ptRatioConst" , "vector<double>", &entry.pSM_ptRatioConst, 32000, 0);
	tree->Branch("SMM_ptRatioConst" , "vector<double>", &entry.pSMM_ptRatioConst, 32000, 0);
}

// ------------ method called on each new Event  ------------
void GenMassAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	darkIdList did;
	entry = GenNtuple();

	edm::Handle<vector<reco::GenMET>> h_met;
	iEvent.getByToken(tok_met,h_met);

	edm::Handle<vector<reco::GenJet>> h_jet;
	iEvent.getByToken(tok_jet,h_jet);

	edm::Handle<vector<reco::GenParticle>> h_part;
	iEvent.getByToken(tok_part,h_part);

	edm::Handle<vector<reco::GenJet>> h_packedjet;
	iEvent.getByToken(tok_packedjet,h_packedjet);

  // Grouping jets in different categories
	// This part of the code is a modified version of v3_darkdentifier.py
	vector<reco::GenJet> dJets;
	vector<reco::GenJet> SMJets;

	vector<TLorentzVector> dQPart; // last dark quarks
	vector<TLorentzVector> dGPart; // last dark gluons
	vector<TLorentzVector> dHPart; // last dark hadrons
	vector<TLorentzVector> lastD; // last daughters of dHPart
	vector<std::string> dQPart_label;
	vector<std::string> dGPart_label;
	vector<std::string> dHPart_label;

	vector<TLorentzVector> fdQPart; // first dark quarks
	vector<TLorentzVector> fdGPart; // first dark gluons
	vector<TLorentzVector> fdMPart; // first dark mediators

	vector<TLorentzVector> fdQPartFM; // first dark quarks from the dark mediator
	vector<TLorentzVector> fdGPartFM; // first dark gluons from the dark mediator
	vector<TLorentzVector> fSMqPart;  // first quarks from the dark mediator decay

	vector<TLorentzVector> stableD; // stable dark hadrons

	vector<reco::GenJet> AK8Jets;
	vector<reco::GenJet> G_;
	vector<reco::GenJet> QM_;
	vector<reco::GenJet> Q_;
	vector<reco::GenJet> QM_Q;
	vector<reco::GenJet> QM_G;
	vector<reco::GenJet> Q_G;
	vector<reco::GenJet> G_SM;
	vector<reco::GenJet> QM_SM;
	vector<reco::GenJet> Q_SM;
	vector<reco::GenJet> LD_lowDF;
	vector<reco::GenJet> LD_highDF;
	vector<reco::GenJet> LD_SM;
	vector<reco::GenJet> SMM_;
	vector<reco::GenJet> SM_;
	// same categories as above, but for packedGenJetsAK8NoNu
	vector<reco::GenJet> pAK8Jets;
	vector<reco::GenJet> pG_;
	vector<reco::GenJet> pQM_;
	vector<reco::GenJet> pQ_;
	vector<reco::GenJet> pQM_Q;
	vector<reco::GenJet> pQM_G;
	vector<reco::GenJet> pQ_G;
	vector<reco::GenJet> pG_SM;
	vector<reco::GenJet> pQM_SM;
	vector<reco::GenJet> pQ_SM;
	vector<reco::GenJet> pLD_lowDF;
	vector<reco::GenJet> pLD_highDF;
	vector<reco::GenJet> pLD_SM;
	vector<reco::GenJet> pSMM_;
	vector<reco::GenJet> pSM_;
	// The ak8genjets that are matched to packedGenJetsAK8NoNu
	// useful for dark pt fraction estimation
	vector<reco::GenJet> mAK8Jets;
	vector<reco::GenJet> mG_;
	vector<reco::GenJet> mQM_;
	vector<reco::GenJet> mQ_;
	vector<reco::GenJet> mQM_Q;
	vector<reco::GenJet> mQM_G;
	vector<reco::GenJet> mQ_G;
	vector<reco::GenJet> mG_SM;
	vector<reco::GenJet> mQM_SM;
	vector<reco::GenJet> mQ_SM;
	vector<reco::GenJet> mLD_lowDF;
	vector<reco::GenJet> mLD_highDF;
	vector<reco::GenJet> mLD_SM;
	vector<reco::GenJet> mSMM_;
	vector<reco::GenJet> mSM_;

	if(h_jet->size() > 0)
	{
		int part_ind = 0;
		for (const auto& part_i : *(h_part.product())) // loop over gen particles
		{
			part_ind ++;
			int partid = part_i.pdgId();

			lastDarkGQ(did.DarkQuarkID_,partid,part_ind,part_i,dQPart,dQPart_label,lastD);
			lastDarkGQ(did.DarkGluonID_,partid,part_ind,part_i,dGPart,dGPart_label,lastD);
			lastDarkGQ(did.DarkHadronID_,partid,part_ind,part_i,dHPart,dHPart_label,lastD);
			firstDark(partid,part_ind,part_i,fdMPart,fdQPart,fdGPart,fdQPartFM,fdGPartFM,fSMqPart);

			if (partid == 51 || partid == 52 || partid == 53)
			{
				TLorentzVector part_i_TL = toTLV(part_i);
				stableD.push_back(part_i_TL);
				lastD.push_back(part_i_TL);
			}
		}

		// std::cout << "Event" <<"\n\n";
		// finding jets that contain dark gluons/quarks/both

		vector<TLorentzVector> dPart = dQPart;
		dPart.insert( dPart.end(), dGPart.begin(), dGPart.end());
		vector<std::string> dPart_label = dQPart_label;
		dPart_label.insert( dPart_label.end(), dGPart_label.begin(), dGPart_label.end());

		vector<vector<std::string>> dPartTrack; // keeping track of which dark jet contains which dark particles

		for(const auto& ijet : *(h_jet.product()))
		{
			int isDark = 0;
			if (ijet.pt() > 200)
			{
				AK8Jets.push_back(ijet);
				vector<std::string> dPartSet;
				checkDark(isDark,ijet,dPartSet,dPart_label,dPart,dJets,dPartTrack);
				if (isDark == 0)
				{
					SMJets.push_back(ijet);
				}
			}
		}

		vector<double> dJPts; // dark jets' dark pT fraction
		darkPtFract(dJets, dJPts, lastD);

		// pick the dark jet with the largest fraction of dark pT to associate with the dark quarks/gluons within the jet
		// if any of those particles happen to be in some other jets, they don't count as particles in those jets.
		// have to do this, because about 10% of the dark jets can be reclassified as SM jets.
		sortByDPt(dJPts,dJets,dPartTrack); // sort the lists based on dark pT fraction.

		reclassToSM(dPartTrack,SMJets,dJets);
		// Further reclassifying jets
		vector<std::string> relab = {"dq","dg","dqm","SMqm","lD"};
		vector<dJetsLab> dJetswL;

		// SM jets into mediator SM and non-mediator SM
		for(const auto& smj : SMJets)
		{
			int SMM_tr = 0;
			TLorentzVector smjTL = toTLV(smj);
			for(const auto& smmq : fSMqPart)
			{
				if (deltaRforTL(smmq,smjTL) < 0.8)
				{
					SMM_tr = 1;
					break;
				}
			}

			if (SMM_tr == 1)
			{
				SMM_.push_back(smj);
			}
			else
			{
				SM_.push_back(smj);
			}

		}

		// classifying dark jets
		vector<TLorentzVector> lastDPL = dQPart;
		lastDPL.insert( lastDPL.end(), dGPart.begin(), dGPart.end());

		for(const auto& udj : dJets)
		{
			vector<std::string> jlabels;
			isfj(fdQPart, udj, "dq", jlabels);
			isfj(fdGPart, udj, "dg", jlabels);
			isfj(fdQPartFM, udj, "dqm", jlabels);
			isfj(fSMqPart, udj, "SMqm", jlabels);
			isfj(lastDPL, udj, "lD", jlabels);
			dJetsLab udjj;
			udjj.dark_jet = udj;
			udjj.cat_labels = jlabels;
			dJetswL.push_back(udjj);
		}

		for(const auto& djl : dJetswL)
		{
			const reco::GenJet& djjet = djl.dark_jet;
			vector<std::string> djlab = djl.cat_labels;

			DarkClass({"dg","lD"}, {"dq","dqm","SMqm"}, djlab, djjet, G_);
		 	DarkClass({"dqm","lD"}, {"dq","dg","SMqm"}, djlab, djjet, QM_);
		  DarkClass({"dq","lD"}, {"dqm","dg","SMqm"}, djlab, djjet, Q_);
		 	DarkClass({"dqm","dq","lD"}, {"dg","SMqm"}, djlab, djjet, QM_Q);
			DarkClass({"dqm","dg","lD"}, {"dq","SMqm"}, djlab, djjet, QM_G);
		 	DarkClass({"dq","dg","lD"}, {"dqm","SMqm"}, djlab, djjet, Q_G);
		  DarkClass({"dg","SMqm","lD"}, {"dq","dqm"}, djlab, djjet, G_SM);
		 	DarkClass({"dqm","SMqm","lD"}, {"dq","dg"}, djlab, djjet, QM_SM);
		 	DarkClass({"dq","SMqm","lD"}, {"dg","dqm"}, djlab, djjet, Q_SM);
		  DarkClass({"lD"}, {"dq","dqm","dg","SMqm"}, djlab, djjet, LD_lowDF, LD_highDF,lastD);
		 	DarkClass({"lD","SMqm"}, {"dq","dqm","dg"}, djlab, djjet, LD_SM);

		}
	}

	matchJet_to_NoNu(AK8Jets, h_packedjet, pAK8Jets, mAK8Jets);
	matchJet_to_NoNu(G_, h_packedjet, pG_, mG_);
	matchJet_to_NoNu(QM_, h_packedjet, pQM_, mQM_);
	matchJet_to_NoNu(Q_, h_packedjet, pQ_, mQ_);
	matchJet_to_NoNu(QM_Q, h_packedjet, pQM_Q, mQM_Q);
	matchJet_to_NoNu(QM_G, h_packedjet, pQM_G, mQM_G);
	matchJet_to_NoNu(Q_G, h_packedjet, pQ_G, mQ_G);
	matchJet_to_NoNu(G_SM, h_packedjet, pG_SM, mG_SM);
	matchJet_to_NoNu(QM_SM, h_packedjet, pQM_SM, mQM_SM);
	matchJet_to_NoNu(Q_SM, h_packedjet, pQ_SM, mQ_SM);
	matchJet_to_NoNu(LD_lowDF, h_packedjet, pLD_lowDF, mLD_lowDF);
	matchJet_to_NoNu(LD_highDF, h_packedjet, pLD_highDF, mLD_highDF);
	matchJet_to_NoNu(LD_SM, h_packedjet, pLD_SM, mLD_SM);
	matchJet_to_NoNu(SM_, h_packedjet, pSM_, mSM_);
	matchJet_to_NoNu(SMM_, h_packedjet, pSMM_, mSMM_);

	calcPtRatioNu(pG_,mG_,entry.pG_ptRatioNu,entry.pG_ptRatioConst);
	calcPtRatioNu(pQM_,mQM_,entry.pQM_ptRatioNu,entry.pQM_ptRatioConst);
	calcPtRatioNu(pQ_,mQ_,entry.pQ_ptRatioNu,entry.pQ_ptRatioConst);
	calcPtRatioNu(pQM_Q,mQM_Q,entry.pQM_QptRatioNu,entry.pQM_QptRatioConst);
	calcPtRatioNu(pQM_G,mQM_G,entry.pQM_GptRatioNu,entry.pQM_GptRatioConst);
	calcPtRatioNu(pQ_G,mQ_G,entry.pQ_GptRatioNu,entry.pQ_GptRatioConst);
	calcPtRatioNu(pG_SM,mG_SM,entry.pG_SMptRatioNu,entry.pG_SMptRatioConst);
	calcPtRatioNu(pQM_SM,mQM_SM,entry.pQM_SMptRatioNu,entry.pQM_SMptRatioConst);
	calcPtRatioNu(pQ_SM,mQ_SM,entry.pQ_SMptRatioNu,entry.pQ_SMptRatioConst);
	calcPtRatioNu(pLD_lowDF,mLD_lowDF,entry.pLD_lowDFptRatioNu,entry.pLD_lowDFptRatioConst);
	calcPtRatioNu(pLD_highDF,mLD_highDF,entry.pLD_highDFptRatioNu,entry.pLD_highDFptRatioConst);
	calcPtRatioNu(pLD_SM,mLD_SM,entry.pLD_SMptRatioNu,entry.pLD_SMptRatioConst);
	calcPtRatioNu(pSM_,mSM_,entry.pSM_ptRatioNu,entry.pSM_ptRatioConst);
	calcPtRatioNu(pSMM_,mSMM_,entry.pSMM_ptRatioNu,entry.pSMM_ptRatioConst);

	softDropJet(pAK8Jets, mAK8Jets, entry.AK8_SDJets, entry.AK8_SDdptFrac, lastD);
	softDropJet(pG_, mG_, entry.G_SDJets, entry.G_SDdptFrac, lastD);
	softDropJet(pQM_, mQM_, entry.QM_SDJets, entry.QM_SDdptFrac, lastD);
	softDropJet(pQ_, mQ_, entry.Q_SDJets, entry.Q_SDdptFrac, lastD);
	softDropJet(pQM_Q, mQM_Q, entry.QM_QSDJets, entry.QM_QSDdptFrac, lastD);
	softDropJet(pQM_G, mQM_G, entry.QM_GSDJets, entry.QM_GSDdptFrac, lastD);
	softDropJet(pQ_G, mQ_G, entry.Q_GSDJets, entry.Q_GSDdptFrac, lastD);
	softDropJet(pG_SM, mG_SM, entry.G_SMSDJets, entry.G_SMSDdptFrac, lastD);
	softDropJet(pQM_SM, mQM_SM, entry.QM_SMSDJets, entry.QM_SMSDdptFrac, lastD);
	softDropJet(pQ_SM, mQ_SM, entry.Q_SMSDJets, entry.Q_SMSDdptFrac, lastD);
	softDropJet(pLD_lowDF, mLD_lowDF, entry.LD_lowDFSDJets, entry.LD_lowDFSDdptFrac, lastD);
	softDropJet(pLD_highDF, mLD_highDF, entry.LD_highDFSDJets, entry.LD_highDFSDdptFrac, lastD);
	softDropJet(pLD_SM, mLD_SM, entry.LD_SMSDJets, entry.LD_SMSDdptFrac, lastD);
	softDropJet(pSM_, mSM_, entry.SM_SDJets, entry.SM_SDdptFrac, lastD);
	softDropJet(pSMM_, mSMM_, entry.SMM_SDJets, entry.SMM_SDdptFrac, lastD);

	fillSubs(entry.AK8_Tau1, entry.AK8_Tau2, entry.AK8_Tau3, AK8Jets);
	fillSubs(entry.G_Tau1, entry.G_Tau2, entry.G_Tau3, G_);
	fillSubs(entry.QM_Tau1, entry.QM_Tau2, entry.QM_Tau3, QM_);
	fillSubs(entry.Q_Tau1, entry.Q_Tau2, entry.Q_Tau3, Q_);
	fillSubs(entry.QM_QTau1, entry.QM_QTau2, entry.QM_QTau3, QM_Q);
	fillSubs(entry.QM_GTau1, entry.QM_GTau2, entry.QM_GTau3, QM_G);
	fillSubs(entry.Q_GTau1, entry.Q_GTau2, entry.Q_GTau3, Q_G);
	fillSubs(entry.G_SMTau1, entry.G_SMTau2, entry.G_SMTau3, G_SM);
	fillSubs(entry.QM_SMTau1, entry.QM_SMTau2, entry.QM_SMTau3, QM_SM);
	fillSubs(entry.Q_SMTau1, entry.Q_SMTau2, entry.Q_SMTau3, Q_SM);
	fillSubs(entry.LD_lowDFTau1, entry.LD_lowDFTau2, entry.LD_lowDFTau3, LD_lowDF);
	fillSubs(entry.LD_highDFTau1, entry.LD_highDFTau2, entry.LD_highDFTau3, LD_highDF);
	fillSubs(entry.LD_SMTau1, entry.LD_SMTau2, entry.LD_SMTau3, LD_SM);
	fillSubs(entry.SM_Tau1, entry.SM_Tau2, entry.SM_Tau3, SM_);
	fillSubs(entry.SMM_Tau1, entry.SMM_Tau2, entry.SMM_Tau3, SMM_);

	entry.GenJetsAK8.reserve(h_jet->size());
	entry.GenJetsAK8_MomentGirth.reserve(h_jet->size());
	entry.GenJetsAK8_MomentHalf.reserve(h_jet->size());
	entry.GenJetsAK8_Multiplicity.reserve(h_jet->size());
	entry.GenJetsAK8_PtD.reserve(h_jet->size());
	entry.GenJetsAK8_AxisMajor.reserve(h_jet->size());
	entry.GenJetsAK8_AxisMinor.reserve(h_jet->size());
	entry.GenJetsAK8_AxisAverage.reserve(h_jet->size());
	entry.GenJetsAK8_Tau1.reserve(h_jet->size());
	entry.GenJetsAK8_Tau2.reserve(h_jet->size());
	entry.GenJetsAK8_Tau3.reserve(h_jet->size());
	entry.GenJetsAK8_ECF1.reserve(h_jet->size());
	entry.GenJetsAK8_ECF2.reserve(h_jet->size());
	entry.GenJetsAK8_ECF3.reserve(h_jet->size());
	for(const auto& i_jet : *(h_jet.product())){
		entry.GenJetsAK8.emplace_back(i_jet.px(),i_jet.py(),i_jet.pz(),i_jet.energy());

		//calculate jet moments & other vars
		//some borrowed from RecoJets/JetProducers/plugins/QGTagger.cc
		double momentGirth = 0.0;
		double momentHalf = 0.0;
		double sumPt = 0.0, sumPt2 = 0.0;
		double sumDeta = 0.0, sumDphi = 0.0, sumDeta2 = 0.0, sumDphi2 = 0.0, sumDetaDphi = 0.0;
		for(unsigned k = 0; k < i_jet.numberOfDaughters(); ++k){
			const reco::CandidatePtr& i_part = i_jet.daughterPtr(k);
			if(i_part.isNonnull() and i_part.isAvailable()){
				double dphi = reco::deltaPhi(i_jet.phi(),i_part->phi());
				double deta = i_part->eta() - i_jet.eta();
				double dR = reco::deltaR(i_jet.p4(),i_part->p4());
				double pT = i_part->pt();
				double pT2 = pT*pT;

				momentGirth += pT*dR;
				momentHalf += pT*std::sqrt(dR);
				sumPt += pT;
				sumPt2 += pT2;
				sumDeta += deta*pT2;
				sumDphi += dphi*pT2;
				sumDeta2 += deta*deta*pT2;
				sumDphi2 += dphi*dphi*pT2;
				sumDetaDphi += deta*dphi*pT2;
			}
		}
		//finish axis calculations (eigenvectors)
		sumDeta /= sumPt2;
		sumDphi /= sumPt2;
		sumDeta2 /= sumPt2;
		sumDphi2 /= sumPt2;
		sumDetaDphi /= sumPt2;
		double a = 0.0, b = 0.0, c = 0.0, d = 0.0;
		a = sumDeta2 - sumDeta*sumDeta;
		b = sumDphi2 - sumDphi*sumDphi;
		c = sumDeta*sumDphi - sumDetaDphi;
		d = std::sqrt(std::fabs((a-b)*(a-b)+4*c*c));
		double axis1 = (a+b+d)>0 ? std::sqrt(0.5*(a+b+d)) : 0.0;
		double axis2 = (a+b-d)>0 ? std::sqrt(0.5*(a+b-d)) : 0.0;
		double axisA = std::sqrt(axis1*axis1 + axis2*axis2);

		//store values
		entry.GenJetsAK8_MomentGirth.push_back(momentGirth/i_jet.pt());
		entry.GenJetsAK8_MomentHalf.push_back(momentHalf/i_jet.pt());
		entry.GenJetsAK8_Multiplicity.push_back(i_jet.numberOfDaughters());
		entry.GenJetsAK8_PtD.push_back(std::sqrt(sumPt2)/sumPt);
		entry.GenJetsAK8_AxisMajor.push_back(axis1);
		entry.GenJetsAK8_AxisMinor.push_back(axis2);
		entry.GenJetsAK8_AxisAverage.push_back(axisA);

		//calculate nsubjettiness & ECFs
#ifndef CMSSW71X
		entry.GenJetsAK8_Tau1.push_back(njhelper.getTau(1,i_jet));
		entry.GenJetsAK8_Tau2.push_back(njhelper.getTau(2,i_jet));
		entry.GenJetsAK8_Tau3.push_back(njhelper.getTau(3,i_jet));

		auto ECFresult = echelper.getECFs(i_jet);
		entry.GenJetsAK8_ECF1.push_back(ECFresult[0]);
		entry.GenJetsAK8_ECF2.push_back(ECFresult[1]);
		entry.GenJetsAK8_ECF3.push_back(ECFresult[2]);
#endif
	}

	TLorentzVector vpartsSum;
	for(const auto& i_part : *(h_part.product())){
		if(std::abs(i_part.pdgId())==4900211){
			entry.HVMesons.emplace_back(i_part.px(),i_part.py(),i_part.pz(),i_part.energy());
			vpartsSum += entry.HVMesons.back();
		}
	}

	const auto& i_met = h_met->front();
	double METx = i_met.px();
	double METy = i_met.py();
	entry.MET = i_met.pt();
	entry.METPhi = i_met.phi();

	//only fill these parts if there are >=2 jets
	if(entry.GenJetsAK8.size()>=2){
		//delta phi
		entry.DeltaPhi1 = std::abs(reco::deltaPhi(entry.GenJetsAK8[0].Phi(),entry.METPhi));
		entry.DeltaPhi2 = std::abs(reco::deltaPhi(entry.GenJetsAK8[1].Phi(),entry.METPhi));
		entry.DeltaPhiMin = std::min(entry.DeltaPhi1,entry.DeltaPhi2);

		//masses
		TLorentzVector vjj = entry.GenJetsAK8[0] + entry.GenJetsAK8[1];
		entry.MJJ = vjj.M();

		//include all jets in MC mass
		TLorentzVector vmc = vjj + vpartsSum;
		entry.Mmc = vmc.M();

		//assume MET is massless
		entry.MT = asymm_mt2_lester_bisect::MT(vjj.Px(),METx,vjj.Py(),METy,vjj.M(),0.0);

		entry.MT2 = asymm_mt2_lester_bisect::get_mT2(
			entry.GenJetsAK8[0].M(), entry.GenJetsAK8[0].Px(), entry.GenJetsAK8[0].Py(),
			entry.GenJetsAK8[1].M(), entry.GenJetsAK8[1].Px(), entry.GenJetsAK8[1].Py(),
			METx, METy, 0.0, 0.0, 0
		);

		//get invisible systems from MT2
		auto MET0 = asymm_mt2_lester_bisect::ben_findsols(entry.MT2,
			entry.GenJetsAK8[0].Px(), entry.GenJetsAK8[0].Py(), entry.GenJetsAK8[0].M(), 0.0,
			entry.GenJetsAK8[1].Px(), entry.GenJetsAK8[1].Py(),
			METx, METy, entry.GenJetsAK8[1].M(), 0.0
		);
		double MET0x = MET0.first;
		double MET0y = MET0.second;
		double MET0t = std::sqrt(std::pow(MET0x,2)+std::pow(MET0y,2));
		double MET1x = METx - MET0x;
		double MET1y = METy - MET0y;
		double MET1t = std::sqrt(std::pow(MET1x,2)+std::pow(MET1y,2));

		//use MAOS scheme 2 ("modified") to estimate longitudinal momenta of invisible systems
		double MET0z = MET0t*entry.GenJetsAK8[0].Pz()/entry.GenJetsAK8[0].Pt();
		double MET1z = MET1t*entry.GenJetsAK8[1].Pz()/entry.GenJetsAK8[1].Pt();

		vector<TLorentzVector> mets;
		mets.emplace_back(MET0x,MET0y,MET0z,0.0);
		mets.emplace_back(MET1x,MET1y,MET1z,0.0);
		entry.METSystems = mets;

		//construct invariant mass of parent
		TLorentzVector vparent = vjj + mets[0] + mets[1];
		entry.MAOS = vparent.M();
	}

	//fill tree
	tree->Fill();
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void GenMassAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	edm::ParameterSetDescription desc;
	desc.add<edm::InputTag>("PackedJetTag",edm::InputTag("packedGenJetsAK8NoNu"));
	desc.add<edm::InputTag>("METTag",edm::InputTag("genMetTrue"));
	desc.add<edm::InputTag>("JetTag",edm::InputTag("ak8GenJets"));
	desc.add<edm::InputTag>("PartTag",edm::InputTag("genParticles"));

	edm::ParameterSetDescription desc_nj;
	desc_nj.add<unsigned>("measureDefinition",0);
	desc_nj.add<double>("beta",1.0);
	desc_nj.add<double>("R0",0.8);
	desc_nj.add<double>("Rcutoff",999.0);
	desc_nj.add<unsigned>("axesDefinition",6);
	desc_nj.add<int>("nPass",999);
	desc_nj.add<double>("akAxesR0",999.0);
	desc.add<edm::ParameterSetDescription>("Nsubjettiness", desc_nj);

	edm::ParameterSetDescription desc_ec;
	desc_ec.add<vector<unsigned>>("Njets",{1,2,3});
	desc_ec.add<double>("beta",1.0);
	desc.add<edm::ParameterSetDescription>("ECF", desc_ec);

	descriptions.add("GenMassAnalyzer",desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(GenMassAnalyzer);
