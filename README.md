# SVJProduction

A repository for private production of CMS Run 3 simulated samples for dark QCD signal models.

Table of Contents
=================

* [Setup](#setup)
* [Overview](#overview)
* [Steps](#steps)
* [runSVJ script](#runsvj-script)
* [Basic usage](#basic-usage)
   * [Gen-level analysis](#gen-level-analysis)
   * [Gen-level for SUEP](#gen-level-for-suep)
   * [Gen-level for EMJ](#gen-level-for-emj)
* [Condor submission](#condor-submission)
   * [Example commands](#example-commands)
   * [Chain submission](#chain-submission)
   * [Ntuple production](#ntuple-production)
* [cmsDriver commands](#cmsdriver-commands)
   * [Pileup input files](#pileup-input-files)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->

## Setup

All of the necessary setup (including creation of CMSSW release areas, checkout of this repo, dependencies, and compilation) is performed by [setup.sh](./setup.sh).
The user's operating system (`slc7` or `el8`) is automatically detected.

```
wget https://raw.githubusercontent.com/cms-svj/SVJProduction/Run3/setup.sh
chmod +x setup.sh
./setup.sh
cd CMSSW_12_4_15/src
cmsenv
cd SVJ/Production
```

The setup script has several options:
* `-y [year]`: year to simulate, determines default CMSSW release (choices: 2022 2023) (default = 2022)
* `-c [release]`: CMSSW release(s) to install, comma-separated (default = CMSSW_12_4_15,CMSSW_12_6_5)
* `-f [fork]`: clone from specified fork (default = cms-svj)
* `-b [branch]`: clone specified branch (default = Run3)
* `-s [protocol]`: use protocol to clone (default = https, alternative = ssh)
* `-j [cores]`: # cores for CMSSW compilation (default = 8)
* `-h`: print help message and exit

## Overview

Run 3 MC production includes the following scenarios that use the corresponding CMSSW releases:
* 2022: `CMSSW_12_4_15` and `CMSSW_12_6_5` (NanoAOD)
* 2022EE: see 2022
* 2023: coming soon
* 2023BPix: see 2023

[Chain submission](#chain-submission) is the recommended way to produce samples.
Standalone Condor commands are also provided for reference or unusual cases.

## Steps

There are several available steps that may be chained together in multiple combinations.
The number in the list below indicates where the step appears in the chain.
In some combinations, some numbers may be skipped.

0. Gridpack
1. GEN, LHE-GEN, GEN-SIM, LHE-GEN-SIM
2. SIM
3. DIGI
4. RECO
5. MINIAOD
6. NANOAOD

## runSVJ script

The [runSVJ](./test/runSVJ.py) script is a wrapper that can customize and run any CMSSW config file. An alternative script [runMG.py](./test/runMG.py) handles MadGraph gridpack generation. These scripts share the same options:
* `maxEvents=[num]`: number of events to process (default = -1)
* `maxEventsIn=[num]`: number of events from input file (if different from `maxEvents`) (default = -1)
* `signal=[bool]`: whether this is a signal sample (default = True)
* `scan=[string]`: name of scan fragment
* `fragment=[string]`: name of file w/ `processParameters` fragment
* `madgraph=[bool]`: generation with MadGraph (instead of default Pythia8)
* `nogridpack=[bool]`: disable gridpack mode and just generate events (only for `runMG`) (default = False)
* `syst=[bool]`: enable systematics for generation with MadGraph (used in LHE step) (default = False)
* `model=[string]`: which dark QCD model to simulate (default = svj, alternative = suep, emj)
    * SVJ parameters:
        * `channel=[string]`: process to generate (default = s, alternative = t)
        * `boost=[float]`: applies a minimum cut of this value (default = 0.0)
        * `boostvar=[string]`: applies the above minimum cut to this variable (default = madpt, alternative = pt)
        * `mMediator=[val]`: mediator mass value (default = 3000.0)
        * `mDark=[val]`: dark hadron mass value (default = 20.0)
        * `rinv=[val]`: invisible fraction value (default = 0.3)
        * `alpha=[val]`: hidden sector force coupling value (default = peak)
        * `yukawa=[val]`: Yukawa coupling for bifundamental mediator (t channel) (default = 1.0)
        * `nMediator=[val]`: generate exclusive signal process based on number of on-shell mediators (default = -1 -> inclusive)
        * `sepproc=[bool]`: use exclusive signal process at gridpack level rather than LHE level (default = True)
        * `filterZ2=[bool]`: only keep events with an even number of stable dark hadrons (default = True)
    * SUEP parameters:
        * `channel=[string]`: process to generate (default = ggH, alternative = WH, ZH)
        * `mMediator=[val]`: mediator mass value (default = 3000.0)
        * `mDark=[val]`: dark hadron mass value (default = 20.0)
        * `temperature=[val]`: temperature for SUEP model (default = 2.0)
        * `decay=[string]`: decay mode for SUEP model (default = generic, alternative = darkPho, darkPhoHad)
        * `filterHT=[val]`: value of the gen-level HT cut on the SUEP analysis (default = -1.0, no cut)
    * EMJ parameters:
        * `mMediator=[val]`: mediator mass value (default = 3000.0)
        * `mDark=[val]`: dark hadron mass value (default = 20.0)
        * `kappa=[val]`: kappa0 coupling (for aligned mode) or ctau lifetime [mm] (for unflavored mode) (default = 1.0)
        * `mode=[string]`: mixing scenario to use (default = aligned, alternative = unflavored)
        * `type=[string]`: SM quark coupling type (default = down, alternative = up)
* `scout=[bool]`: keep scouting collections in miniAOD (default = False)
* `part=[num]`: part number when producing a sample in multiple jobs (default = 1)
* `indir=[str]`: directory for input file (local or logical)
* `inpre=[str]`: prefix for input file name
* `outpre=[list]`: list of prefixes for output file names (must be same length as list of output modules) (default = step_GEN)
* `output=[list]`: list of output module names (default = `sorted(process.outputModules_())`)
* `year=[str]`: which year to simulate (default = 0, for year-independent configs)
* `config=[str]`: config file to customize and run (default = step_GEN)
* `printEvents=[num]`: number of Pythia events to print (default = 1)
* `threads=[num]`: number of threads to run (default = 1)
* `streams=[num]`: number of streams to run (default = 0 -> streams = threads)
* `redir=[dir]`: xrootd redirector for input file
* `tmi=[bool]`: enable [TimeMemoryInfo](https://github.com/cms-sw/cmssw/blob/master/Validation/Performance/python/TimeMemoryInfo.py) for simple profiling (default = False)
* `dump=[bool]`: equivalent to `edmConfigDump`, but accounts for all command-line settings; exits without running (default = False)
   * for `runMG.py`, this option keeps the gridpack directory
* `dryrun=[bool]`: for `runMG.py`, stop before actually running MadGraph

## Basic usage

### Gen-level analysis

To run generator-level sample production interactively with example parameters:
```
cd SVJ/Production/test
cmsRun runSVJ.py year=2022 config=step_GEN outpre=step_GEN mMediator=3000.0 mDark=20.0 rinv=0.3 alpha=peak part=1 maxEvents=10
```

To run a Gen-level analyzer:
```
cmsRun runSVJ.py config=genmassanalyzer_cfg output=TFileService outpre=genmassanalysis inpre=step_GEN mMediator=3000.0 mDark=20.0 rinv=0.3 alpha=peak part=1 maxEvents=10
```

To run the softdrop algorithm on GenJets/GenParticles from an existing sample, and analyze the result:
```
cmsRun runSVJ.py config=softDropGenJets outpre=softdropgen indir=/store/user/lpcdarkqcd/SVJ2017/ProductionV5/GEN/ inpre=step_GEN redir=root://cmseos.fnal.gov/ mMediator=3000 mDark=20 rinv=0.3 alpha=peak maxEvents=500 part=1
cmsRun runSVJ.py config=softdropanalyzer_cfg outpre=softdropana output=TFileService inpre=softdropgen mMediator=3000 mDark=20 rinv=0.3 alpha=peak maxEvents=500 part=1
```

### Gen-level for SUEP

To run the sample production interactively for SUEP with example parameters:
```
cd SVJ/Production/test
cmsRun runSVJ.py model=suep year=2022 config=step_GEN outpre=step_GEN mMediator=125 mDark=2.0 temperature=2.0 decay=generic part=1 maxEvents=10
```

### Gen-level for EMJ

To run the sample production interactively for EMJ with example parameters:
```
cd SVJ/Production/test
cmsRun runSVJ.py model=emj year=2022 config=step_GEN outpre=step_GEN mMediator=1000.0 mDark=20.0 kappa=1 mode=aligned type=down part=1 maxEvents=10
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
python submitJobs.py -p -o root://cmseos.fnal.gov//store/user/YOURUSERNAME/myProduction -d signals2 -E 500 -N 20 --outpre step_GEN-SIM --config SVJ.Production.2016.step_GEN-SIM -s
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
* `--model [str]`: model to simulate (default = svj, alternative = suep, emj)
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
python submitJobs.py -p -d signalsV3_1 -E 10000 -N 1 --outpre step_GRIDPACK --gridpack -o root://cmseos.fnal.gov//store/user/lpcdarkqcd/SVJ2017/ProductionV5/GRIDPACK/ -s
```
LHE-GEN-SIM:
```
python submitJobs.py -p -d signalsV3_1 -E 1000 -N 100 -I 10000 --indir /store/user/lpcdarkqcd/SVJ2017/ProductionV5/GRIDPACK/ --inpre step_GRIDPACK --outpre step_LHE-GEN-SIM --year 2022 --config step_LHE-GEN-SIM --madgraph -o root://cmseos.fnal.gov//store/user/lpcdarkqcd/SVJ2017/ProductionV5/2022/GEN-SIM/ -s
```
GEN-SIM:
```
python submitJobs.py -p -d signalsV3_1 -E 1000 -N 100 --outpre step_GEN-SIM --year 2022 --config step_GEN-SIM -o root://cmseos.fnal.gov//store/user/lpcdarkqcd/SVJ2017/ProductionV5/2022/GEN-SIM/ -s
```
</details>

### Chain submission

The script [runProd.py](./batch/runProd.py) can create and submit a chain of jobs to run all\* signal production steps.
This script automates the creation of a [job chain](https://github.com/kpedro88/CondorProduction#job-chains).
It can be run from any CMSSW release in the chain and will execute each step in its appropriate CMSSW release.

\* Gridpack production should be run separately, since a single gridpack can be reused by multiple jobs.

Several predefined chains are provided:  
P8: 0. GEN-SIM, 1. DIGI, 2. RECO, 3. MINIAOD, 4. NANOAOD  
MG: 0. LHE-GEN-SIM, 1. DIGI, 2. RECO, 3. MINIAOD, 4. NANOAOD  

These predefined chains can be modified with the script's command-line options, or (as an exclusive option) a custom chain of steps can be used.

The script has several options:
* `-P, --predefined [chain]`: choose predefined chain
* `-C, --custom [steps]`: specify steps for custom chain
* `-M, --modify [op] [pos/name] [step]`: modify predefined chain  
    multiple ops can be given in one call, or option can be called multiple times  
    ops will be applied in order provided
    * op = insert, remove, change
    * pos/name = position (number) or name of step in predefined chain
    * step = name of step to insert/substitute
* `-S, --store [pos/name]`: store output for intermediate step(s) (position or name) (-1 or all: store all steps' output) (default: ["MINIAOD"])
* `-G, --global [opts]`: global arguments for submitJobs (use syntax: -G="...")
* `-L, --local [pos/name] [opts]`: local arguments for submitJobs for a specific step
* `-n, --name [name]`: base-level name for chain job
* `-k, --keep`: keep existing tarball(s) for job submission
* `-s, --submit`: submit chain jdl(s)
* `-y, --year [year]`: which year to simulate
* `-o, --output [dir]`: base-level output directory
* `-t, --tardir [dir]`: xrdcp address for CMSSW tarballs (default: None)
* `-c, --checkpoint`: enable checkpointing (if a job fails, save output files from previous job in chain)
* `-v, --verbose`: print verbose output (default: False)
* `-h, --help`: show this help message and exit

The options with lowercase short flags are related to options for `submitJobs.py` and `createChain.py`.
Other submitJobs options that should usually be specified using `-G` include:
mode, input dict(s), number of events per job, number of parts, resource requirements such as memory, any additional common arguments.

<details>
<summary>Example commands</summary>

Pythia-only generation:
```
python runProd.py -P P8 -G="-p -d signals_P8_ex -E 10 -N 1 --cpus 4 --memory 8000" -y 2016 -n chain2016_ -o root://cmseos.fnal.gov//store/user/lpcdarkqcd/SVJ2017/testRun3/ -t root://cmseos.fnal.gov//store/user/lpcdarkqcd/SVJ2017/testRun3/ -c -s
```

MadGraph+Pythia generation:
```
python submitJobs.py -p -d signals_MG_ex -E 10000 -N 1 --memory 4000 --outpre step_GRIDPACK --gridpack -o root://cmseos.fnal.gov//store/user/lpcdarkqcd/SVJ2017/testRun3/GRIDPACK -s
[wait for jobs to finish]
python runProd.py -P MG -G="-p -d signals_MG_ex --madgraph -E 10 -N 1 --cpus 4 --memory 8000" -L 0 "-I 10000 --indir /store/user/lpcdarkqcd/SVJ2017/testRun3/GRIDPACK --inpre step_GRIDPACK" -y 2016 -n chain2016_ -o root://cmseos.fnal.gov//store/user/lpcdarkqcd/SVJ2017/testRun3/ -t root://cmseos.fnal.gov//store/user/lpcdarkqcd/SVJ2017/testRun3/ -c -s
```
</details>

### Ntuple production

NanoAOD is the recommended format for ntuples in Run 3 and is produced by default.
MiniAOD files are also saved by default in case additional information needs to be added to the standard nanoAOD.
To get a list of the produced files (and associated metadata):
```
python submitJobs.py -y --actualEvents -K auto -d signalsV3_1 -E 1000 -N 100 --indir /store/user/lpcdarkqcd/SVJ2017/ProductionV5/2022/NANOAOD --inpre step_NANOAOD --outpre SVJ_2022
```

## cmsDriver commands

These commands are based on the [PdmVMcCampaigns twiki](https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMcCampaigns), specifically the pages for the `Run3Summer22` campaigns in McM.
The steps are: LHE-GEN, LHE-GEN-SIM, GEN, GEN-SIM, SIM, DIGI, DIGI-HLT, HLT, RECO, MINIAOD, NANOAOD.

<details>
<summary>Commands (2022):</summary>

```
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --eventcontent RAWSIM  --datatier GEN-SIM --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision  --step LHE,GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc --python_filename python/2022/step_LHE-GEN-SIM.py --no_exec
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --eventcontent RAWSIM  --datatier GEN --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision  --step LHE,GEN --geometry DB:Extended --era Run3 --no_exec --mc --python_filename python/2022/step_LHE-GEN.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --eventcontent RAWSIM  --datatier GEN-SIM --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc --python_filename python/2022/step_GEN-SIM.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --eventcontent RAWSIM  --datatier GEN --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN --geometry DB:Extended --era Run3 --no_exec --mc --python_filename python/2022/step_GEN.py --no_exec
cmsDriver.py  --eventcontent PREMIXRAW  --datatier GEN-SIM-RAW --fileout file:step0.root --pileup_input pileup.root --conditions 124X_mcRun3_2022_realistic_v12 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2022v12 --procModifiers premix_stage2,siPixelQualityRawToDigi --geometry DB:Extended --filein file:step-1.root --datamix PreMix --era Run3 --no_exec --mc --python_filename python/2022/step_DIGI.py --no_exec
cmsDriver.py  --eventcontent AODSIM  --datatier AODSIM --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_v12 --step RAW2DIGI,L1Reco,RECO,RECOSIM --procModifiers siPixelQualityRawToDigi --geometry DB:Extended --filein file:step-1.root --era Run3 --no_exec --mc --python_filename python/2022/step_RECO.py --no_exec
cmsDriver.py  --eventcontent MINIAODSIM  --datatier MINIAODSIM --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_v12 --step PAT --geometry DB:Extended --filein file:step-1.root --era Run3 --no_exec --mc --python_filename python/2022/step_MINIAOD.py --no_exec
cmsDriver.py  --eventcontent NANOAODSIM  --datatier NANOAODSIM --fileout file:step0.root --conditions 126X_mcRun3_2022_realistic_v2 --step NANO --scenario pp --filein file:step-1.root --era Run3,run3_nanoAOD_124 --no_exec --mc --python_filename python/2022/step_NANOAOD.py --no_exec
```
</details>

<details>
<summary>Commands (2022EE):</summary>

```
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --eventcontent RAWSIM  --datatier GEN-SIM --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc --python_filename python/2022EE/step_GEN-SIM.py --no_exec
cmsDriver.py SVJ/Production/python/EmptyFragment_cff.py --eventcontent RAWSIM  --datatier GEN --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision --step GEN --geometry DB:Extended --era Run3 --no_exec --mc --python_filename python/2022EE/step_GEN.py --no_exec
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --eventcontent RAWSIM  --datatier GEN-SIM --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision  --step LHE,GEN,SIM --geometry DB:Extended --era Run3 --no_exec --mc --python_filename python/2022EE/step_LHE-GEN-SIM.py --no_exec
cmsDriver.py SVJ/Production/python/HadronizerFragment_cff.py --eventcontent RAWSIM  --datatier GEN --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --beamspot Realistic25ns13p6TeVEarly2022Collision  --step LHE,GEN --geometry DB:Extended --era Run3 --no_exec --mc --python_filename python/2022EE/step_LHE-GEN.py --no_exec
cmsDriver.py  --eventcontent PREMIXRAW  --datatier GEN-SIM-RAW --fileout file:step0.root --pileup_input pileup.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2022v14 --procModifiers premix_stage2,siPixelQualityRawToDigi --geometry DB:Extended --filein file:step-1.root --datamix PreMix --era Run3 --no_exec --mc --python_filename python/2022EE/step_DIGI.py --no_exec
cmsDriver.py  --eventcontent AODSIM  --datatier AODSIM --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step RAW2DIGI,L1Reco,RECO,RECOSIM --procModifiers siPixelQualityRawToDigi --geometry DB:Extended --filein file:step-1.root --era Run3 --no_exec --mc --python_filename python/2022EE/step_RECO.py --no_exec
cmsDriver.py  --eventcontent MINIAODSIM  --datatier MINIAODSIM --fileout file:step0.root --conditions 124X_mcRun3_2022_realistic_postEE_v1 --step PAT --geometry DB:Extended --filein file:step-1.root --era Run3 --no_exec --mc --python_filename python/2022EE/step_MINIAOD.py --no_exec
cmsDriver.py  --eventcontent NANOAODSIM  --datatier NANOAODSIM --fileout file:step0.root --conditions 126X_mcRun3_2022_realistic_postEE_v1 --step NANO --scenario pp --filein file:step-1.root --era Run3,run3_nanoAOD_124 --no_exec --mc --python_filename python/2022EE/step_NANOAOD.py --no_exec
```
</details>

### Pileup input files

The script `picklePileupInput.py` can download the premixed pileup input file list, convert it to a Python list and pickle it, and upload it to EOS.

The premixed pileup input file lists in use are:
```
/Neutrino_E-10_gun/Run3Summer21PrePremix-Summer22_124X_mcRun3_2022_realistic_v11-v2/PREMIX
```
