# SVJProduction

## Setup

All of the necessary setup (including checkout of this repo, dependencies, and CMSSW compilation) is performed by [setup.sh](./setup.sh).

For Run 2 ultra-legacy MC production (2016APV, 2016, 2017, 2018), `CMSSW_10_6_29_patch1` is used.
```
wget https://raw.githubusercontent.com/cms-svj/SVJProduction/master/setup.sh
chmod +x setup.sh
./setup.sh
cd CMSSW_10_6_29_patch1/src
cmsenv
cd SVJ/Production
```

The setup script has several options:
* `-c [release]`: CMSSW release to install (default = CMSSW_10_6_29_patch1)
* `-f [fork]`: clone from specified fork (default = cms-svj)
* `-b [branch]`: clone specified branch (default = Run2_UL)
* `-s [protocol]`: use protocol to clone (default = https, alternative = ssh)
* `-j [cores]`: # cores for CMSSW compilation (default = 8)
* `-t`: install HLT releases
* `-h`: print help message and exit

For more details about the `-t` option, see [HLT in UL](#hlt-in-ul) below.

## Steps

There are several available steps that may be chained together in multiple combinations.
The number in the list below indicates where the step appears in the chain.
In some combinations, some numbers may be skipped.

0. Gridpack
1. GEN, LHE-GEN, GEN-SIM, LHE-GEN-SIM
2. SIM
3. DIGI, DIGI-HLT
4. HLT
5. RECO
6. MINIAOD
7. NANOAOD

### HLT in UL

The HLT configuration is only valid in the actual CMSSW release cycle that was used online for a specific data-taking period.
Therefore, a true simulation of the HLT requires using an older CMSSW release:
`CMSSW_8_0_33_UL` for 2016, `CMSSW_9_4_14_UL_patch1` for 2017, `CMSSW_10_2_16_UL` for 2018.
The standalone HLT step can only be executed in the respective release for each year,
which can be optionally installed along with the main UL 10_6_X release used for the other steps.

If the older releases are not installed, or the HLT simulation is not needed, the separate DIGI-HLT step can be used instead.
This step uses a highly simplified HLT configuration designed for relvals.
Therefore, the trigger-related contents from this step will not correspond to the data,
but all the other contents (GEN, RECO, MINIAOD, etc.) will be the same.

## runSVJ script

The [runSVJ](./test/runSVJ.py) script is a wrapper that can customize and run any CMSSW config file. An alternative script [runMG.py](./test/runMG.py) handles MadGraph gridpack generation. These scripts share the same options:
* `maxEvents=[num]`: number of events to process (default = -1)
* `maxEventsIn=[num]`: number of events from input file (if different from `maxEvents`) (default = -1)
* `signal=[bool]`: whether this is a signal sample (default = True)
* `scan=[string]`: name of scan fragment
* `fragment=[string]`: name of file w/ `processParameters` fragment
* `madgraph=[bool]`: generation with MadGraph (instead of default Pythia8)
* `nogridpack=[bool]`: disable gridpack mode and just generate events (only for `runMG`) (default = False)
* `syst=[bool]`: enable systematics for generation with MadGraph (default = False)
* `suep=[bool]`: run SUEP simulation (default = False)
* `channel=[string]`: process to generate (default = s, alternative = t)
* `boost=[float]`: applies a minimum HT cut of whatever value was passed (default = 0.0)
* `mMediator=[val]`: mediator mass value (default = 3000.0)
* `mDark=[val]`: dark hadron mass value (default = 20.0)
* `rinv=[val]`: invisible fraction value (default = 0.3)
* `alpha=[val]`: hidden sector force coupling value (default = peak)
* `yukawa=[val]`: Yukawa coupling for bifundamental mediator (t channel) (default = 1.0)
* `temperature=[val]`: temperature for SUEP model (default = 2.0)
* `decay=[str]`: decay mode for SUEP model (default = generic)
* `filterZ2=[bool]`: only keep events with `N(4900211)%4==0` (default = True)
* `scout=[bool]`: keep scouting collections in miniAOD (default = False)
* `part=[num]`: part number when producing a sample in multiple jobs (default = 1)
* `indir=[str]`: directory for input file (local or logical)
* `inpre=[str]`: prefix for input file name
* `outpre=[list]`: list of prefixes for output file names (must be same length as list of output modules) (default = step1)
* `output=[list]`: list of output module names (default = `sorted(process.outputModules_())`)
* `year=[str]`: which year to simulate (default = 0, for year-independent configs)
* `config=[str]`: config file to customize and run (default = step1_GEN)
* `threads=[num]`: number of threads to run (default = 1)
* `streams=[num]`: number of streams to run (default = 0 -> streams = threads)
* `redir=[dir]`: xrootd redirector for input file
* `tmi=[bool]`: enable [TimeMemoryInfo](https://github.com/cms-sw/cmssw/blob/master/Validation/Performance/python/TimeMemoryInfo.py) for simple profiling (default = False)
* `dump=[bool]`: equivalent to `edmConfigDump`, but accounts for all command-line settings; exits without running (default = False)
   * for `runMG.py`, this option keeps the gridpack directory
* `dryrun=[bool]`: for `runMG.py`, stop before actually running MadGraph

## Basic usage

### GEN-level analysis

To run generator-level sample production interactively with example parameters:
```
cd SVJ/Production/test
cmsRun runSVJ.py year=2016 config=step1_GEN outpre=step1 mMediator=3000.0 mDark=20.0 rinv=0.3 alpha=0.1 part=1 maxEvents=10
```

To run a GEN-level analyzer:
```
cmsRun runSVJ.py config=genmassanalyzer_cfg output=TFileService outpre=genmassanalysis inpre=step1 mMediator=3000.0 mDark=20.0 rinv=0.3 alpha=0.1 part=1 maxEvents=10
```

To run the softdrop algorithm on GenJets/GenParticles from an existing sample, and analyze the result:
```
cmsRun runSVJ.py config=softDropGenJets outpre=softdropgen indir=/store/user/lpcsusyhad/SVJ2017/ProductionV3/GEN-SIM/ inpre=step1_GEN-SIM redir=root://cmseos.fnal.gov/ mMediator=3000 mDark=20 rinv=0.3 alpha=0.2 maxEvents=500 part=1
cmsRun runSVJ.py config=softdropanalyzer_cfg outpre=softdropana output=TFileService inpre=softdropgen mMediator=3000 mDark=20 rinv=0.3 alpha=0.2 maxEvents=500 part=1
```

### Gen-level for SUEP

To run the sample production interactively for SUEP with example parameters:
```
cd SVJ/Production/test
cmsRun runSVJ.py suep=1 year=2018 config=step1_GEN outpre=step1 mMediator=125 mDark=2.0 temperature=2.0 decay=generic part=1 maxEvents=10
```

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
* `-I, --maxEventsIn [num]`: number of events from input file (if different from `-E`) (default = 1)
* `-F, --firstPart [num]`: first part to process in case extending a sample (default = 1)
* `-N, --nParts [num]`: number of parts to process
* `-K, --skipParts [n1,n2,... or auto]`: comma-separated list of parts to skip (or auto, which checks existence of input files)
* `--indir [dir]`: input file directory (LFN)
* `--redir [dir]`: input file redirector (default = root://cmseos.fnal.gov/)
* `--inpre [str]`: input file prefix
* `--outpre [str]`: output file prefix (required)
* `--config [str]`: CMSSW config to run (required unless madgraph)
* `--year [num]`: which year to simulate
* `--gridpack`: gridpack production
* `--madgraph`: sample generated w/ madgraph (rather than pythia)
* `--suep`: run SUEP simulation
* `--actualEvents`: count actual number of events from each input file (for python file list, requires `-K auto`)
* `-A, --args [list]`: additional common args to use for all jobs (passed to [runSVJ.py](./test/runSVJ.py))
* `-v, --verbose`: enable verbose output (default = False)
* `--chain-name [str]`: value for job.chainName (default = )

Shell (in [step2.sh](./batch/step2.sh)):
* `-o [dir]`: output directory
* `-j [jobname]`: job name
* `-p [part]`: part number
* `-x [redir]`: xrootd redirector
* `-m [mode]`: running mode (madgraph or normal)

### Example commands

These examples show how to submit batch jobs for a specific step,
demonstrating several different methods for generating 50,000 events with selected signal models.

The basic [CondorProduction](https://github.com/kpedro88/CondorProduction) setup has already been performed by the setup script.

<details>
<summary>Commands:</summary>

Gridpack:
```
python submitJobs.py -p -d signalsV3_1 -E 50000 -N 1 --outpre step0_GRIDPACK --year 2016 --gridpack -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV4/2016/GRIDPACK/ -s
```
LHE-GEN-SIM:
```
python submitJobs.py -p -d signalsV3_1 -E 1000 -N 100 -I 50000 --indir /store/user/lpcsusyhad/SVJ2017/ProductionV4/2016/GRIDPACK/ --inpre step0_GRIDPACK --outpre step1_LHE-GEN-SIM --year 2016 --config step1_LHE-GEN-SIM --madgraph -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV4/2016/GEN-SIM/ -s
```
GEN-SIM:
```
python submitJobs.py -p -d signalsV3_1 -E 1000 -N 100 --outpre step1_GEN-SIM --year 2016 --config step1_GEN-SIM -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV4/2016/GEN-SIM/ -s
```
</details>

### Chain submission

(to be added)

### Ntuple production

To prepare the file lists (and associated metadata):
```
python submitJobs.py -y --actualEvents -K auto -d signalsV3_1 -E 1000 -N 100 --indir /store/user/lpcsusyhad/SVJ2017/ProductionV4/2016/MINIAOD --inpre step4_MINIAOD --outpre SVJ_2016
```

Ntuple production uses the [TreeMaker](https://github.com/TreeMaker/TreeMaker) repository, which has its own [Condor submission instructions](https://github.com/TreeMaker/TreeMaker#submit-production-to-condor).
To submit the ntuple jobs:
```
python submitJobs.py -p -d svj -N 200 --cpus 4 -o root://cmseos.fnal.gov//store/user/lpcsusyhad/SVJ2017/ProductionV4/Ntuples/ --args "redir=root://cmseos.fnal.gov/" -s
```
N.B. this command uses `submitJobs.py` from TreeMaker, not from this repository.

## cmsDriver commands

These commands are based on the [PdmVMcCampaigns twiki](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMcCampaigns), specifically the pages for the `RunIISummer20` campaigns.
The steps are: LHE-GEN, LHE-GEN-SIM, GEN, GEN-SIM, SIM, DIGI, DIGI-HLT, HLT, RECO, MINIAOD, NANOAOD.

<details>
<summary>Commands (2016APV):</summary>

```
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_mcRun2_asymptotic_preVFP_v8 --beamspot Realistic25ns13TeV2016Collision --step LHE,GEN --geometry DB:Extended --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step1_LHE-GEN.py --no_exec
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 106X_mcRun2_asymptotic_preVFP_v8 --beamspot Realistic25ns13TeV2016Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step1_LHE-GEN-SIM.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_mcRun2_asymptotic_preVFP_v8 --beamspot Realistic25ns13TeV2016Collision --step GEN --geometry DB:Extended --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step1_GEN.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 106X_mcRun2_asymptotic_preVFP_v8 --beamspot Realistic25ns13TeV2016Collision --step GEN,SIM --geometry DB:Extended --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step1_GEN-SIM.py --no_exec
cmsDriver.py step1 --mc --eventcontent RAWSIM --runUnscheduled --datatier GEN-SIM --conditions 106X_mcRun2_asymptotic_preVFP_v8 --beamspot Realistic25ns13TeV2016Collision --step SIM --nThreads 8 --geometry DB:Extended --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step2_SIM.py --no_exec
cmsDriver.py step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_mcRun2_asymptotic_preVFP_v8 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --pileup_input pileup.root --python_filename python/2016APV/step3_DIGI.py --no_exec
cmsDriver.py step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_mcRun2_asymptotic_preVFP_v8 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2016 --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --pileup_input pileup.root --python_filename python/2016APV/step3_DIGI-HLT.py --no_exec
cmsDriver.py step1 --mc --eventcontent RAWSIM --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*" --datatier GEN-SIM-RAW --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:25ns15e33_v4 --nThreads 8 --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step4_HLT.py --no_exec
cmsDriver.py step1 --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 106X_mcRun2_asymptotic_preVFP_v8 --step RAW2DIGI,L1Reco,RECO,RECOSIM --nThreads 8 --geometry DB:Extended --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step5_RECO.py --no_exec
cmsDriver.py step1 --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 106X_mcRun2_asymptotic_preVFP_v8 --step PAT --procModifiers run2_miniAOD_UL --nThreads 8 --geometry DB:Extended --era Run2_2016_HIPM  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step6_MINIAOD.py --no_exec
cmsDriver.py step1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mcRun2_asymptotic_preVFP_v9 --step NANO --nThreads 8 --era Run2_2016,run2_nanoAOD_106Xv1  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016APV/step7_NANOAOD.py --no_exec
```
</details>

<details>
<summary>Commands (2016):</summary>

```
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step LHE,GEN --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step1_LHE-GEN.py --no_exec
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step1_LHE-GEN-SIM.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step GEN --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step1_GEN.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step GEN,SIM --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step1_GEN-SIM.py --no_exec
cmsDriver.py step1 --mc --eventcontent RAWSIM --runUnscheduled --datatier GEN-SIM --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step SIM --nThreads 8 --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step2_SIM.py --no_exec
cmsDriver.py step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_mcRun2_asymptotic_v13 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --pileup_input pileup.root --python_filename python/2016/step3_DIGI.py --no_exec
cmsDriver.py step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_mcRun2_asymptotic_v13 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2016 --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --pileup_input pileup.root --python_filename python/2016/step3_DIGI-HLT.py --no_exec
cmsDriver.py step1 --mc --eventcontent RAWSIM --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*" --datatier GEN-SIM-RAW --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:25ns15e33_v4 --nThreads 8 --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step4_HLT.py --no_exec
cmsDriver.py step1 --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 106X_mcRun2_asymptotic_v13 --step RAW2DIGI,L1Reco,RECO,RECOSIM --nThreads 8 --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step5_RECO.py --no_exec
cmsDriver.py step1 --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 106X_mcRun2_asymptotic_v13 --step PAT --procModifiers run2_miniAOD_UL --nThreads 8 --geometry DB:Extended --era Run2_2016  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step6_MINIAOD.py --no_exec
cmsDriver.py step1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mcRun2_asymptotic_v15 --step NANO --nThreads 8 --era Run2_2016,run2_nanoAOD_106Xv1  --filein file:step-1.root --fileout file:step0.root --python_filename python/2016/step7_NANOAOD.py --no_exec
```
</details>

<details>
<summary>Commands (2017):</summary>

```
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step LHE,GEN --geometry DB:Extended --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step1_LHE-GEN.py --no_exec
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step1_LHE-GEN-SIM.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN --geometry DB:Extended --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step1_GEN.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN,SIM --geometry DB:Extended --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step1_GEN-SIM.py --no_exec
cmsDriver.py step1 --mc --eventcontent RAWSIM --runUnscheduled --datatier GEN-SIM --conditions 106X_mc2017_realistic_v6 --beamspot Realistic25ns13TeVEarly2017Collision --step SIM --nThreads 8 --geometry DB:Extended --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step2_SIM.py --no_exec
cmsDriver.py step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_mc2017_realistic_v6 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --pileup_input pileup.root --python_filename python/2017/step3_DIGI.py --no_exec
cmsDriver.py step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_mc2017_realistic_v6 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2017 --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --pileup_input pileup.root --python_filename python/2017/step3_DIGI-HLT.py --no_exec
cmsDriver.py step1 --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 94X_mc2017_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2e34v40 --nThreads 8 --geometry DB:Extended --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step4_HLT.py --no_exec
cmsDriver.py step1 --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 106X_mc2017_realistic_v6 --step RAW2DIGI,L1Reco,RECO,RECOSIM --nThreads 8 --geometry DB:Extended --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step5_RECO.py --no_exec
cmsDriver.py step1 --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 106X_mc2017_realistic_v9 --step PAT --procModifiers run2_miniAOD_UL --nThreads 8 --geometry DB:Extended --era Run2_2017  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step6_MINIAOD.py --no_exec
cmsDriver.py step1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mc2017_realistic_v8 --step NANO --nThreads 8 --era Run2_2017,run2_nanoAOD_106Xv1  --filein file:step-1.root --fileout file:step0.root --python_filename python/2017/step7_NANOAOD.py --no_exec
```
</details>

<details>
<summary>Commands (2018):</summary>

```
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step1_LHE-GEN.py --no_exec
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step1_LHE-GEN-SIM.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN --geometry DB:Extended --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step1_GEN.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --geometry DB:Extended --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step1_GEN-SIM.py --no_exec
cmsDriver.py step1 --mc --eventcontent RAWSIM --runUnscheduled --datatier GEN-SIM --conditions 106X_upgrade2018_realistic_v11_L1v1 --beamspot Realistic25ns13TeVEarly2018Collision --step SIM --nThreads 8 --geometry DB:Extended --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step2_SIM.py --no_exec
cmsDriver.py step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --pileup_input pileup.root --python_filename python/2018/step3_DIGI.py --no_exec
cmsDriver.py step1 --mc --eventcontent PREMIXRAW --runUnscheduled --datatier GEN-SIM-DIGI --conditions 106X_upgrade2018_realistic_v11_L1v1 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --pileup_input pileup.root --python_filename python/2018/step3_DIGI-HLT.py --no_exec
cmsDriver.py step1 --mc --eventcontent RAWSIM --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v15 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:2018v32 --nThreads 8 --geometry DB:Extended --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step4_HLT.py --no_exec
cmsDriver.py step1 --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 106X_upgrade2018_realistic_v11_L1v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --nThreads 8 --geometry DB:Extended --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step5_RECO.py --no_exec
cmsDriver.py step1 --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 106X_upgrade2018_realistic_v16_L1v1 --step PAT --procModifiers run2_miniAOD_UL --nThreads 8 --geometry DB:Extended --era Run2_2018  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step6_MINIAOD.py --no_exec
cmsDriver.py step1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_upgrade2018_realistic_v15_L1v1 --step NANO --nThreads 8 --era Run2_2018,run2_nanoAOD_106Xv1  --filein file:step-1.root --fileout file:step0.root --python_filename python/2018/step7_NANOAOD.py --no_exec
```
</details>

### Pileup input files

The script `picklePileupInput.py` can download the premixed pileup input file list, convert it to a Python list and pickle it, and upload it to EOS.

The premixed pileup input file lists in use are:
```
/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX
/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL17_106X_mc2017_realistic_v6-v3/PREMIX
/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL18_106X_upgrade2018_realistic_v11_L1v1-v2/PREMIX
```
