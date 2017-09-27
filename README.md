# SVJProduction

## GEN-SIM production

To make GEN-SIM samples, `CMSSW_7_1_28` is used (which includes the latest version of Pythia8, 8.226).
All of the necessary setup (including CMSSW compilation, and checkout of this repo)
is performed by [setup.sh](./scripts/setup.sh):
```
wget https://raw.githubusercontent.com/kpedro88/SVJProduction/master/scripts/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_7_1_28
cd CMSSW_7_1_28/src
cmsenv
```

To run the sample production interactively with example parameters:
```
cd SVJ/Production/test
cmsRun runSVJ.py config=SVJ.Production.step1_GEN output=RAWSIMoutput outpre=step1 mZprime=3000.0 mDark=20.0 rinv=0.3 alpha=0.1 part=1 maxEvents=10
```

To generate background samples for GEN-level analysis:
```
cmsRun runSVJ.py config=SVJ.Production.step1_GEN_QCDForPF_13TeV output=RAWSIMoutput outpre=step1_QCD signal=0 part=1 maxEvents=10
```

## GEN-level analysis

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

## cmsDriver commands

GEN only:
```
cmsDriver.py SVJ/Production/EmptyFragment_cff --python_filename step1_GEN.py --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN-SIM --conditions MCRUN2_71_V3::All --beamspot Realistic50ns13TeVCollision --step GEN --magField 38T_PostLS1 --fileout file:step1.root --no_exec
cmsDriver.py QCDForPF_13TeV_TuneCUETP8M1_cfi --python_filename step1_GEN_QCDForPF_13TeV.py --mc --eventcontent RAWSIM --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --datatier GEN-SIM --conditions MCRUN2_71_V3::All --beamspot Realistic50ns13TeVCollision --step GEN --magField 38T_PostLS1 --fileout file:step1.root --no_exec
```
