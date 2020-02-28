import FWCore.ParameterSet.Config as cms
import sys, os, shutil, subprocess
from SVJ.Production.optSVJ import options, _helper

# model name
_outname = _helper.getOutName(options.maxEvents)
_outname = _outname.replace("outpre",options.outpre[0])

# copy template files
data_path = os.path.expand("$CMSSW_BASE/src/SVJ/Production/data/"+_helper.mg_name)
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

# make tarball for madgraph
shutil.make_archive(
    base_name = mg_input_dir,
    format = "tar",
    root_dir = mg_dir,
	base_dir = os.path.basename(mg_model_dir),
)

# run gridpack in genproductions dir (creates separate env)
gen_prod_dir = os.path.expand("$CMSSW_BASE/src/Configuration/GenProductions/bin/MadGraph5_aMCatNLO/")
cmd = '''
cd {0}
ln -sf {1} .
eval `scram unsetenv -sh`
export DO_MG_SYSTEMATICS={6}
./gridpack_generation.sh {2} {3}
mv {2}_*.tar.xz {4}
cd {4}
{5} {1}/{2}
'''.format(
    gen_prod_dir,
    mg_input_dir,
    _outname,
    os.path.basename(mg_input_dir),
    os.getcwd(),
    "echo" if options.dump else "rm -rf", # use options.dump to keep gridpack dir
    "true" if options.syst else "",
)
if options.dump: print cmd
subprocess.check_call(cmd, shell=True)
