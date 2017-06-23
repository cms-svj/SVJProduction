//analysis headers
#include "Analysis/KCode/KMap.h"
#include "Analysis/KCode/KLegend.h"
#include "Analysis/KCode/KPlot.h"
#include "Analysis/KCode/KParser.h"
#include "Analysis/KCode/KStyle.h"

//ROOT headers
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TDirectory.h>

//STL headers
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <iostream>

using namespace std;

struct Var {
	string name;
	OptionMap* localOpt;
	KStyle* style;
	TH1F* hist = NULL;
};

vector<Var*> parseInput(string fname){
	vector<Var*> results;
	string line;
	ifstream infile(fname.c_str());
	if(infile.is_open()){
		while(getline(infile,line)){
			//skip commented lines
			if(line[0]=='#') continue;
			//skip blank lines
			if(line.size()<2) continue;
			
			vector<string> fields;
			KNamed* tmp = KParser::processNamed<1>(line);
			Var* var = new Var;
			var->name = tmp->fields[0];
			var->localOpt = tmp->localOpt();
			var->style = new KStyle("mass",NULL,var->localOpt);
			results.push_back(var);
		}
	}
	else {
		cout << "Input error: could not open input file \"" << fname << "\"." << endl;
	}
	return results;
}

void plotMasses(string filename, string input, vector<string> pformats={"png"}){
	TFile* file = TFile::Open(filename.c_str());
	if(!file) return;
	TTree* tree = (TTree*)file->Get("GenMassAnalyzer/tree");
	if(!tree) return;
	
	//process input file
	vector<Var*> vars = parseInput(input);
	if(vars.empty()) return;
	
	//get parameter info
	map<string,double> params;
	vector<string> fields;
	string fname = filename.substr(0,filename.size()-5);
	KParser::process(fname, '_', fields);
	for(const auto& field : fields){
		vector<string> subfields;
		KParser::process(field,'-',subfields);
		if(subfields.size()<2) continue;
		double tmp;
		stringstream stmp(subfields[1]);
		stmp >> tmp;
		params[subfields[0]] = tmp;
	}
	
	//make param strings
	vector<string> param_text;
	stringstream sp;
	sp << "#alpha_{d} = " << params["alpha"];
	param_text.push_back(sp.str());
	sp.str(string());
	sp << "r_{inv} = " << params["rinv"];
	param_text.push_back(sp.str());
	
	//make plot options
	OptionMap* globalOpt = new OptionMap();
	globalOpt->Set<string>("prelim_text","Simulation (work-in-progress)");
	globalOpt->Set<string>("lumi_text","(13 TeV)");
	globalOpt->Set<bool>("checkerr",false);
	globalOpt->Set<int>("npanel",1);
	globalOpt->Set<vector<string> >("extra_text",param_text);
	OptionMap* localOpt = new OptionMap();
	localOpt->Set<bool>("ratio",false);
	localOpt->Set<bool>("logy",false);

	//make output name and histos
	int nbins = 100;
	double xmin = 0.0;
	double xmax = 6000.0;
	double ymin = 0.0;
	double ymax = 0.0;
	string oname = "plotMasses_";
	for(const auto& var : vars){
		string hname = "h"+var->name;
		stringstream sh;
		sh << var->name << ">>" << hname << "(" << nbins << "," << xmin << "," << xmax << ")";
		tree->Draw(sh.str().c_str(),"","hist goff");
		var->hist = (TH1F*)gDirectory->Get(hname.c_str());
		if(var->hist){
			oname += "_"+var->name;
			var->hist->Scale(1.0/(var->hist->Integral(0,var->hist->GetNbinsX()+1)));
			if(var->hist->GetMaximum()>ymax) ymax = var->hist->GetMaximum();
			var->style->Format(var->hist);
		}
		else {
			cout << "Error: could not make histogram for " << var->name << endl;
		}
	}
	oname += "__"+fname;
	KParser::clean(oname);
	
	//make plot
	TH1F* hbase = new TH1F("hbase","",100,xmin,xmax);
	hbase->GetYaxis()->SetTitle("arbitrary units");
	hbase->GetXaxis()->SetTitle("mass [GeV]");
	hbase->GetYaxis()->SetRangeUser(ymin,ymax*1.1);
	KPlot* plot = new KPlot(oname,localOpt,globalOpt);
	plot->Initialize(hbase);
	KLegend* kleg = plot->GetLegend();
	TCanvas* can = plot->GetCanvas();
	TPad* pad1 = plot->GetPad1();
	pad1->cd();
	
	//make legend
	kleg->AddHist(plot->GetHisto()); //for tick sizes
	for(const auto& var : vars){
		string legname; var->localOpt->Get("legname",legname);
		string legopt; var->localOpt->Get("legopt",legopt);
		kleg->AddEntry(var->hist,legname,legopt);
	}
	kleg->Build(KLegend::right,KLegend::top);

	//draw blank histo for axes
	plot->DrawHist();
	
	//draw hists
	for(const auto& var : vars){
		var->hist->Draw(var->style->GetDrawOpt("same").c_str());
	}

	plot->GetHisto()->Draw("sameaxis"); //draw again so axes on top
	plot->DrawText();
	
	//print image
	for(const auto& pformat : pformats){
		can->Print((oname+"."+pformat).c_str(),pformat.c_str());
		//if(pformat=="eps") system(("epstopdf "+oname+".eps").c_str());
	}
}