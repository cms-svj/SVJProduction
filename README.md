# SVJProduction

## GEN-SIM production

To make GEN-SIM samples, `CMSSW_7_1_26` is used.
All of the necessary setup (including installation of the latest Pythia8 version, CMSSW package updates and compilation, and checkout of this repo)
is performed by [setup.sh](./scripts/setup.sh):
```
wget https://raw.githubusercontent.com/kpedro88/SVJProduction/master/scripts/setup.sh
chmod +x setup.sh
./setup.sh -c CMSSW_7_1_26 -p
cd CMSSW_7_1_26/src
cmsenv
```

