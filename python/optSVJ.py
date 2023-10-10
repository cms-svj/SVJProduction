import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from SVJ.Production.svjHelper import svjHelper
from SVJ.Production.suepHelper import suepHelper
from SVJ.Production.emjHelper import emjHelper
import os

options = VarParsing("analysis")
options.register("signal", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("scan", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("fragment", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("madgraph", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("nogridpack", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("syst", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("model", "svj", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("channel", "s", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("boost", 0.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("boostvar", "madpt", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("mMediator", 3000.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("mDark", 20.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("rinv", 0.3, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("alpha", "peak", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("yukawa", 1.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("nMediator", -1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("sepproc", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("filterZ2", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("temperature", 2.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("filterHT", -1.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("decay", "generic", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("kappa", 1.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("mode", "aligned", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("type", "down", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("scout", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("part", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("indir", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("inpre", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("outpre", "step_GEN", VarParsing.multiplicity.list, VarParsing.varType.string)
options.register("output", "", VarParsing.multiplicity.list, VarParsing.varType.string)
options.register("year", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("config", "step_GEN", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("maxEventsIn", -1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("printEvents", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("threads", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("streams", 0, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("redir", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("tmi", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("dump", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("dryrun", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.parseArguments()

# safety checks to handle multiple years
cmssw_version = os.getenv("CMSSW_VERSION")
cmssw_major = int(cmssw_version.split('_')[1])
cmssw_minor = int(cmssw_version.split('_')[2])
# all years can use 106X
if not (cmssw_major==10 and cmssw_minor==6):
    if options.year.startswith("2016") and not (cmssw_major==8):
	    raise ValueError("2016 config should not be used in non-2016 CMSSW version ("+cmssw_version+")")
    elif options.year=="2017" and not (cmssw_major==9):
	    raise ValueError("2017 config should not be used in non-2017 CMSSW version ("+cmssw_version+")")
    elif options.year=="2018" and not (cmssw_major==10):
	    raise ValueError("2018 config should not be used in non-2018 CMSSW version ("+cmssw_version+")")

# incompatible args
if len(options.scan)>0 and len(options.fragment)>0:
    raise ValueError("scan and fragment are incompatible options, pick one!")

# check events
if options.maxEventsIn==-1: options.maxEventsIn = options.maxEvents

# make full config name using year
options.config = "SVJ.Production."+(str(options.year)+"." if len(options.year)>0 else "")+options.config

# this is needed because options.outpre is not really a list
setattr(options,"_outpre",[x for x in options.outpre])
if len(options.scan)>0:
    options._outpre = [x+"_"+options.scan for x in options._outpre]
    if len(options.inpre)>0: options.inpre += "_"+options.scan
elif len(options.fragment)>0:
    options._outpre = [x+"_"+options.fragment for x in options._outpre]
    if len(options.inpre)>0: options.inpre += "_"+options.fragment

if options.model=="svj":
    _helper = svjHelper()
    _helper.setModel(options.channel,options.mMediator,options.mDark,options.rinv,options.alpha,generate=None if options.scan else not options.madgraph,boost=options.boost,boostvar=options.boostvar,yukawa=options.yukawa,nMediator=options.nMediator,sepproc=options.sepproc)
elif options.model=="suep":
    # change default
    if options.channel=='s': options.channel = 'ggH'
    _helper = suepHelper()
    _helper.setModel(options.channel,options.mMediator,options.mDark,options.temperature,options.decay)
    options.filterZ2 = False
elif options.model=="emj":
    _helper = emjHelper()
    _helper.setModel(options.mMediator,options.mDark,options.kappa,options.mode,options.type)
    options.filterZ2 = False
    options.channel = ""
else:
    raise ValueError("Unknown model {}".format(options.model))
