# SVJProduction

## Setup

All of the necessary setup (including checkout of this repo, dependencies, and CMSSW compilation) is performed by [setup.sh](./setup.sh).

### GEN-SIM production (2016)

To make GEN or GEN-SIM samples, `CMSSW_7_1_38` is used (which includes Pythia8.226).
```
wget https://raw.githubusercontent.com/kpedro88/SVJProduction/master/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_7_1_38
cd CMSSW_7_1_38/src
cmsenv
cd SVJ/Production
```

### MINIAOD production (2016)

To make MINIAOD (or DIGI/RECO/AOD) samples, `CMSSW_8_0_28` is used:
```
wget https://raw.githubusercontent.com/kpedro88/SVJProduction/master/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_8_0_28
cd CMSSW_8_0_28/src
cmsenv
cd SVJ/Production
```

### GEN-SIM production (2017)

To make GEN or GEN-SIM samples, `CMSSW_9_3_12` is used (which includes Pythia8.230).
```
wget https://raw.githubusercontent.com/kpedro88/SVJProduction/master/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_9_3_12
cd CMSSW_9_3_12/src
cmsenv
cd SVJ/Production
```

### MINIAOD production (2017)

To make MINIAOD (or DIGI/RECO/AOD) samples, `CMSSW_9_4_10` is used:
```
wget https://raw.githubusercontent.com/kpedro88/SVJProduction/master/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_9_4_10
cd CMSSW_9_4_10/src
cmsenv
cd SVJ/Production
```

2016 AOD samples can also be reprocessed in this release to get "miniAOD v3" output.

## Condor submission

Condor submission is supported for the LPC batch system or for the global pool via [CMS Connect](https://connect.uscms.org/).
Job submission and management is based on the [CondorProduction](https://github.com/kpedro88/CondorProduction) package.
Refer to the package documentation for basic details.

The [batch](./batch/) directory contains all of the relevant scripts.
If you make a copy of this directory and run the [submitJobs.py](./batch/submitJobs.py) script,
it will submit to Condor the specified number of jobs for the specified signal models. Example:
```
test/lnbatch.sh myProduction
cd myProduction
python submitJobs.py -p -o root://cmseos.fnal.gov//store/user/YOURUSERNAME/myProduction -d signals2 -E 500 -N 20 --outpre step1_GEN-SIM --config SVJ.Production.2016.step1_GEN-SIM -s
```
[submitJobs.py](./batch/submitJobs.py) can also:
* count the expected number of jobs to submit (for planning purposes),
* check for jobs which were completely removed from the queue and make a resubmission list,
* make an output file list for ntuple production.

The class [jobSubmitterSVJ.py](./batch/jobSubmitterSVJ.py) extends the class `jobSubmitter` from [CondorProduction](https://github.com/kpedro88/CondorProduction). It adds a few extra arguments:

Python:
* `-y, --getpy`: make python file list for ntuple production (new operation mode)
* `-d, --dicts [file]`: file with list of input dicts; each dict contains signal parameters (required)
* `-o, --output [dir]`: path to output directory in which root files will be stored (required)
* `-E, --maxEvents [num]`: number of events to process per job (default = 1)
* `-F, --firstPart [num]`: first part to process in case extending a sample (default = 1)
* `-N, --nParts [num]`: number of parts to process
* `-K, --skipParts [n1,n2,... or auto]`: comma-separated list of parts to skip (or auto, which checks existence of input files)
* `--indir [dir]`: input file directory (LFN)
* `--redir [dir]`: input file redirector (default = root://cmseos.fnal.gov/)
* `--inpre [str]`: input file prefix
* `--outpre [str]`: output file prefix (required)
* `--config [str]`: CMSSW config to run (required)
* `--actualEvents`: count actual number of events from each input file (for python file list, requires `-K auto`)
* `-A, --args [list]`: additional common args to use for all jobs (passed to [runSVJ.py](./Production/test/runSVJ.py))
* `-v, --verbose`: enable verbose output (default = False)

Shell (in [step2.sh](./batch/step2.sh)):
* `-o [dir]`: output directory
* `-j [jobname]`: job name
* `-p [part]`: part number
* `-x [redir]`: xrootd redirector

### Example commands

These examples are for generating 50,000 events with selected signal models, after profiling with 100 events.
They assume the basic [CondorProduction](https://github.com/kpedro88/CondorProduction) setup has already been performed.
To run for 2017, replace `.2016.` with `.2017.` in the argument of `--config` and `/2016/` with `/2017/` in the arguments of `--indir` and `-o`.

<details>
<summary>Commands:</summary>

GEN-SIM:
```
python submitJobs.py -p -d signals2 -E 1000 -N 100 --outpre step1_GEN-SIM --config SVJ.Production.2016.step1_GEN-SIM -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/GEN-SIM/ -s
```
DIGI:
```
python submitJobs.py -p -d signals2 -E 1000 -N 100 --indir /store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/GEN-SIM/ --inpre step1_GEN-SIM --outpre step2_DIGI --config SVJ.Production.2016.step2_DIGI -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/DIGI/ --cpus 4 --memory 5000 -s
```
RECO:
```
python submitJobs.py -p -d signals2 -E 1000 -N 100 --indir /store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/DIGI/ --inpre step2_DIGI --outpre step3_RECO --config SVJ.Production.2016.step3_RECO -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/RECO/ --cpus 4 --memory 3000 -s
```
DIGI-RECO: (alternative, only for 2017)
```
python submitJobs.py -p -d signals2 -E 1000 -N 100 --indir /store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/GEN-SIM/ --inpre step1_GEN-SIM --outpre step3_DIGI-RECO --config SVJ.Production.2016.step3_DIGI-RECO -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/RECO/ --cpus 4 --memory 3000 -s
```
MINIAOD:
```
python submitJobs.py -p -d signals2 -E 1000 -N 100 --indir /store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/RECO/ --inpre step3_RECO --outpre step4_MINIAOD --config SVJ.Production.2016.step4_MINIAOD -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/MINIAOD/ --cpus 4 -s
```
MINIAOD v3 (for 2016):
```
python submitJobs.py -p -d signals2 -E 1000 -N 100 --indir /store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/RECO/ --inpre step3_RECO --outpre step4_MINIAOD_2016 --config SVJ.Production.2017.step4_MINIAOD_2016 -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV2/2017/MINIAOD/ --cpus 4 -s
```
</details>

### Ntuple production

Ntuple production uses the [TreeMaker](https://github.com/TreeMaker/TreeMaker) repository. To prepare the file lists (and `WeightProducer` lines):
```
python submitJobs.py -y --actualEvents -K auto -d signals2 -E 1000 -N 100 --indir /store/user/lpcsusyhad/SVJ2017/ProductionV2/2016/MINIAOD --inpre step4_MINIAOD --outpre SVJ_2016
```
To submit the (mini-)ntuple jobs for signal and background, follow the [TreeMaker Condor submission instructions](https://github.com/TreeMaker/TreeMaker#submit-production-to-condor) and use the following commands:
```
python submitJobs.py -p -d svj -N 200 --cpus 4 -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV2/Ntuples/ --args "semivisible=True lostlepton=False hadtau=False doZinv=False doPDFs=False systematics=False redir=root://cmseos.fnal.gov/" -s
python submitJobs.py -p -d qcd_pt --cpus 4 -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV2/Ntuples/ --args "semivisible=True lostlepton=False hadtau=False doZinv=False doPDFs=False systematics=False" -s
```
N.B. these commands uses `submitJobs.py` from TreeMaker, not from this repository.

## runSVJ script

The [runSVJ](./test/runSVJ.py) script is a wrapper that can customize and run any CMSSW config file. Options:
* `maxEvents=[num]`: number of events to process (default = -1)
* `signal=[bool]`: whether this is a signal sample (default = True)
* `scan=[string]`: name of scan fragment
* `mZprime=[val]`: Zprime mass value (default = 2000.0)
* `mDark=[val]`: dark meson mass value (default = 20.0)
* `rinv=[val]`: invisible fraction value (default = 0.3)
* `alpha=[val]`: hidden sector force coupling value (default = 0.1)
* `filterZ2=[bool]`: only keep events with `N(4900211)%4==0` (default = True)
* `part=[num]`: part number when producing a sample in multiple jobs (default = 1)
* `indir=[str]`: directory for input file (local or logical)
* `inpre=[str]`: prefix for input file name
* `outpre=[list]`: list of prefixes for output file names (must be same length as list of output modules) (default = step1)
* `output=[list]`: list of output module names (default = `sorted(process.outputModules_())`)
* `config=[str]`: config file to customize and run (default = SVJ.Production.2016.step1_GEN)
* `threads=[num]`: number of threads to run (default = 1)
* `streams=[num]`: number of streams to run (default = 0 -> streams = threads)
* `redir=[dir]`: xrootd redirector for input file
* `tmi=[bool]`: enable [TimeMemoryInfo](https://github.com/cms-sw/cmssw/blob/master/Validation/Performance/python/TimeMemoryInfo.py) for simple profiling (default = False)
* `dump=[bool]`: equivalent to `edmConfigDump`, but accounts for all command-line settings; exits without running (default = False)

## GEN-level analysis

To run the sample production interactively with example parameters:
```
cd SVJ/Production/test
cmsRun runSVJ.py config=SVJ.Production.2016.step1_GEN outpre=step1 mZprime=3000.0 mDark=20.0 rinv=0.3 alpha=0.1 part=1 maxEvents=10
```

To generate background samples for GEN-level analysis:
```
cmsRun runSVJ.py config=SVJ.Production.2016.step1_GEN_QCDForPF_13TeV outpre=step1_QCD signal=0 part=1 maxEvents=10
```

The analysis code needs a newer version of CMSSW (to access newer versions of ROOT and fastjet).
Rerun the setup script as follows (the `-a` flag installs the analysis code dependency, my [Analysis](https://github.com/kpedro88/Analysis/tree/SVJ2017-gen) repo):
```
./setup.sh -c CMSSW_8_0_28 -a
```

To run the GEN-level analyzer:
```
cmsRun runSVJ.py config=SVJ.Production.genmassanalyzer_cfg output=TFileService outpre=genmassanalysis inpre=step1 mZprime=3000.0 mDark=20.0 rinv=0.3 alpha=0.1 part=1 maxEvents=10
cmsRun runSVJ.py config=SVJ.Production.genmassanalyzer_cfg output=TFileService outpre=genmassanalysis_QCD inpre=step1_QCD signal=0 part=1 maxEvents=10
```

For more ways to analyzer the output of the GEN-level analyzer, see the [Analysis](https://github.com/kpedro88/Analysis/tree/SVJ2017-gen) repo.

An alternative example of a semi-standalone macro is available in this repo:
```
root -l 'plotMasses.C+("genmassanalysis_mZprime-3000_mDark-20_rinv-0.3_alpha-0.1_n-10_part-1.root","input_masses.txt")'
```

To run the softdrop algorithm on GenJets/GenParticles from an existing sample, and analyze the result:
```
cmsRun runSVJ.py config=SVJ.Production.softDropGenJets outpre=softdropgen indir=/store/user/lpcsusyhad/SVJ2017/ProductionV2/GEN-SIM/ inpre=step1_GEN-SIM redir=root://cmseos.fnal.gov/ mZprime=3000 mDark=20 rinv=0.3 alpha=0.2 maxEvents=500 part=1
cmsRun runSVJ.py config=SVJ.Production.softdropanalyzer_cfg outpre=softdropana output=TFileService inpre=softdropgen mZprime=3000 mDark=20 rinv=0.3 alpha=0.2 maxEvents=500 part=1
```

## cmsDriver commands (2016)

<details>
<summary>Commands:</summary>

GEN only:
```
cmsDriver.py SVJ/Production/2016/EmptyFragment_cff --python_filename step1_GEN.py --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN --conditions MCRUN2_71_V3::All --beamspot Realistic50ns13TeVCollision --step GEN --magField 38T_PostLS1 --fileout file:step1.root --no_exec
cmsDriver.py QCDForPF_13TeV_TuneCUETP8M1_cfi --python_filename step1_GEN_QCDForPF_13TeV.py --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN --conditions MCRUN2_71_V3::All --beamspot Realistic50ns13TeVCollision --step GEN --magField 38T_PostLS1 --fileout file:step1.root --no_exec
```

GEN-SIM:
```
cmsDriver.py SVJ/Production/2016/EmptyFragment_cff --python_filename step1_GEN-SIM.py --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN-SIM --conditions MCRUN2_71_V3::All --beamspot Realistic50ns13TeVCollision --step GEN,SIM --magField 38T_PostLS1 --fileout file:step1.root --no_exec
```

DIGI:
```
cmsDriver.py step2 --python_filename step2_DIGI.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:@frozen2016 --nThreads 4 --datamix PreMix --era Run2_2016 --filein file:step1.root --fileout file:step2.root --pileup_input pileup.root --no_exec
```

RECO:
```
cmsDriver.py step3 --python_filename step3_RECO.py --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step RAW2DIGI,RECO,EI --nThreads 4 --era Run2_2016 --filein file:step2.root --fileout file:step3.root --no_exec
```

MINIAOD:
```
cmsDriver.py step4 --python_filename step4_MINIAOD.py --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --step PAT --nThreads 4 --era Run2_2016  --filein file:step3.root --fileout file:step4.root --no_exec
```
</details>


These commands are based on the [PdmVMcCampaigns twiki](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMcCampaigns),
specifically:
[RunIISummer15GS](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIISummer15GS),
[RunIISummer16DR80Premix](https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMCcampaignRunIISummer16DR80Premix),
[RunIISummer16MiniAODv2](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIISummer16MiniAODv2).

## cmsDriver commands (2017)

<details>
<summary>Commands:</summary>

GEN only:
```
cmsDriver.py SVJ/Production/2017/EmptyFragment_cff --python_filename step1_GEN.py --mc --eventcontent RAWSIM --datatier GEN --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN --nThreads 4 --geometry DB:Extended --era Run2_2017 --fileout file:step0.root --no_exec
```

GEN-SIM:
```
cmsDriver.py SVJ/Production/2017/EmptyFragment_cff --python_filename step1_GEN-SIM.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN,SIM --nThreads 4 --geometry DB:Extended --era Run2_2017 --fileout file:step0.root --no_exec
```

DIGI:
```
cmsDriver.py step2 --python_filename step2_DIGI.py --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 94X_mc2017_realistic_v10 --step DIGIPREMIX_S2,DATAMIX,L1,DIGI2RAW,HLT:2e34v40 --nThreads 8 --datamix PreMix --era Run2_2017  --filein file:step1.root --fileout file:step2.root --pileup_input pileup.root --no_exec
```

RECO:
```
cmsDriver.py step3 --python_filename step3_RECO.py --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v10 --step RAW2DIGI,RECO,EI --nThreads 8 --era Run2_2017 --filein file:step2.root --fileout file:step3.root --no_exec
```

MINIAOD:
```
cmsDriver.py step4 --python_filename step4_MINIAOD.py --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 94X_mc2017_realistic_v14 --step PAT --nThreads 4 --era Run2_2017,run2_miniAOD_94XFall17 --filein file:step3.root --fileout file:step4.root --no_exec
```

MINIAOD v3 (for 2016):
```
cmsDriver.py step4 --python_filename step4_MINIAOD_2016.py --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 94X_mcRun2_asymptotic_v3 --step PAT --nThreads 8 --era Run2_2016,run2_miniAOD_80XLegacy --filein file:step3.root --fileout file:step4.root --no_exec
```
</details>


These commands are based on the [PdmVMcCampaigns twiki](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMcCampaigns) and [McM](https://cms-pdmv.cern.ch/mcm/),
specifically:
[RunIIFall17GS](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIIFall17GS),
[RunIIFall17DRPremix](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIIFall17DRPremix),
[RunIIFall17MiniAODv2](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/BTV-RunIIFall17MiniAODv2-00024),
[RunIISummer16MiniAODv3](https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/B2G-RunIISummer16MiniAODv3-00003).

### Pileup input files

To download the premixed pileup input file list for 2016:
```
dasgoclient -query="file dataset=/Neutrino_E-10_gun/RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2/GEN-SIM-DIGI-RAW" | sort > Neutrino_E-10_gun_RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2_GEN-SIM-DIGI-RAW.txt
```

For quicker loading in Python, the text file is converted to a Python list and pickled using the script [picklePileupInput.py](./test/picklePileupInput.py):
```
python picklePileupInput.py Neutrino_E-10_gun_RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2_GEN-SIM-DIGI-RAW.txt
```
The pickled file can be retrieved from EOS:
```
xrdcp root://cmseos.fnal.gov//store/user/pedrok/SVJ2017/pileup/Neutrino_E-10_gun_RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2_GEN-SIM-DIGI-RAW.pkl
```
The config [step2_DIGI.py](./python/2016/step2_DIGI.py) will try to retrieve it automatically when it is run.

This procedure can be repeated for 2017 using the dataset:
```
/Neutrino_E-10_gun/RunIISummer17PrePremix-MCv2_correctPU_94X_mc2017_realistic_v9-v1/GEN-SIM-DIGI-RAW
```
