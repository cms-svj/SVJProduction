import FWCore.ParameterSet.Config as cms
import sys, os, shutil, subprocess
from glob import glob
from SVJ.Production.optSVJ import options, _helper

# make sure number of events is > 0 (otherwise madgraph crashes)
options.maxEvents = max(1,options.maxEvents)

# model name
_outname = _helper.getOutName(events=options.maxEvents)
_outname = _outname.replace("outpre",options._outpre[0])
_modname = _helper.getOutName(events=options.maxEvents,outpre="SVJ",sanitize=True)

# copy template files
data_path = os.path.expandvars("$CMSSW_BASE/src/SVJ/Production/data/"+_helper.mg_name)
mg_dir = os.path.join(os.getcwd(),_outname)
# remove output directory if it already exists
if os.path.isdir(mg_dir):
    shutil.rmtree(mg_dir)
shutil.copytree(data_path,mg_dir)

# PDF sets for signal
if options.year==2016: lhaid = 247000 # NNPDF23_lo_as_0130_qed for CUETP8M1
elif options.year==2017: lhaid = 315200 # NNPDF31_lo_as_0130 for CP2
elif options.year==2018: lhaid = 315200 # NNPDF31_lo_as_0130 for CP2

# populate parameters in cards
mg_model_dir, mg_input_dir = _helper.getMadGraphCards(mg_dir,lhaid,events=options.maxEvents)

# make tarball for madgraph (w/ correct folder name to be imported later)
mg_model_dir_new = os.path.join(mg_dir,_modname)
shutil.move(mg_model_dir,mg_model_dir_new)
shutil.make_archive(
    base_name = os.path.join(mg_input_dir,_modname),
    format = "tar",
    root_dir = mg_dir,
	base_dir = os.path.basename(mg_model_dir_new),
)

# run gridpack in genproductions dir (creates separate env)
gen_prod_dir = os.path.expandvars("$CMSSW_BASE/src/Configuration/GenProduction/bin/MadGraph5_aMCatNLO/")
# cleanup previous dir just in case
shutil.rmtree(os.path.join(gen_prod_dir,_modname),ignore_errors=True)
cmd = '''
set -e
cd {0}
ln -sf {1} .
eval `scram unsetenv -sh`
export DO_MG_SYSTEMATICS={6}
export GRIDPACK_NEVENTS={7}
./gridpack_generation.sh {2} {3}
mv {2}_*.tar.xz {4}
cd {4}
{5} {1}/{2}
'''.format(
    gen_prod_dir,
    mg_input_dir,
    _modname,
    os.path.basename(mg_input_dir),
    os.getcwd(),
    "echo" if options.dump else "rm -rf", # use options.dump to keep gridpack dir
    "true" if options.syst else "",
    options.maxEvents,
)
if options.dump: print cmd
subprocess.check_call(cmd, shell=True)

# move output to desired name
tfiles = glob(_modname+"*.tar.xz")
if len(tfiles)==1: shutil.move(tfiles[0],_outname+".tar.xz")
else:
    for tfile in tfiles:
        tfile2 = tfile.replace(_modname,_outname)
        shutil.move(tfile,tfile2)
