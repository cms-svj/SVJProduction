import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys, os
from SVJ.Production.svjHelper import svjHelper

options = VarParsing("analysis")
options.register("signal", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("scan", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("mZprime", 2000.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("mDark", 20.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("rinv", 0.3, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("alpha", "0.1", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("filterZ2", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("part", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("indir", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("inpre", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("outpre", "step1", VarParsing.multiplicity.list, VarParsing.varType.string)
options.register("output", "", VarParsing.multiplicity.list, VarParsing.varType.string)
options.register("config", "SVJ.Production.2016.step1_GEN", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("threads", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("streams", 0, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("redir", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("tmi", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("dump", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.parseArguments()

# safety checks to handle multiple years
cmssw_version = os.getenv("CMSSW_VERSION")
cmssw_major = int(cmssw_version.split('_')[1])
if ".2016." in options.config and not (cmssw_major==7 or cmssw_major==8):
	raise ValueError("2016 config ("+options.config+") should not be used in non-2016 CMSSW version ("+cmssw_version+")")
elif ".2017." in options.config and not (cmssw_major==9):
	raise ValueError("2017 config ("+options.config+") should not be used in non-2017 CMSSW version ("+cmssw_version+")")
elif ".2018." in options.config and not (cmssw_major==10):
	raise ValueError("2018 config ("+options.config+") should not be used in non-2018 CMSSW version ("+cmssw_version+")")

# this is needed because options.outpre is not really a list
outpre = [x for x in options.outpre]
if len(options.scan)>0:
    outpre = [x+"_"+options.scan for x in outpre]
    if len(options.inpre)>0: options.inpre += "_"+options.scan

_helper = svjHelper()
_helper.setModel(options.mZprime,options.mDark,options.rinv,options.alpha)

# output name definition
_outname = _helper.getOutName(options.maxEvents,part=options.part,signal=options.signal and len(options.scan)>0)
_outname += ".root"

_inname = ""
if len(options.inpre)>0:
    _inname = _outname.replace("outpre",options.inpre)
    if len(options.indir)>0: _inname = options.indir+"/"+_inname
    if len(options.redir)>0 and _inname[0:6]=="/store": _inname = options.redir+_inname
    if _inname[0:6]!="/store" and _inname[0:5]!="root:": _inname = "file:"+_inname

# import process
process = getattr(__import__(options.config,fromlist=["process"]),"process")

# input settings
process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if len(_inname)>0: process.source.fileNames = cms.untracked.vstring(_inname)
else: process.source.firstEvent = cms.untracked.uint32((options.part-1)*options.maxEvents+1)
if len(options.scan)>0: process.source.numberEventsInLuminosityBlock = cms.untracked.uint32(200)

# output settings
oprocess = process if (not hasattr(process,'subProcesses') or len(process.subProcesses)==0) else process.subProcesses[-1].process()
if len(options.output)==0: options.output = sorted(oprocess.outputModules_())
if len(outpre)!=len(options.output):
    raise ValueError("Mismatch between # of output prefixes and # of output modules\n\tOutput prefixes are: "+", ".join(outpre)+"\n\tOutput modules are: "+", ".join(options.output))
for iout,output in enumerate(options.output):
    if len(output)==0: continue
    if not hasattr(oprocess,output):
        raise ValueError("Unavailable output module: "+output)
    getattr(oprocess,output).fileName = 'file:'+_outname.replace("outpre",outpre[iout])

# reset all random numbers to ensure statistically distinct but reproducible jobs
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randHelper = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randHelper.resetSeeds(options.maxEvents+options.part)

if options.signal:
    if len(options.scan)>0:
        if hasattr(process,'generator'):
            process.generator = getattr(__import__("SVJ.Production."+options.scan+"_cff",fromlist=["generator"]),"generator")
    else:
        # generator settings
        if hasattr(process,'generator'):
            process.generator.crossSection = cms.untracked.double(_helper.xsec)
            process.generator.PythiaParameters.processParameters = cms.vstring(_helper.getPythiaSettings())
            process.generator.maxEventsToPrint = cms.untracked.int32(1)

    # gen filter settings
    # pythia implementation of model has 4900111/211 -> -51 51 and 4900113/213 -> -53 53
    # this is a stand-in for direct production of a single stable dark meson in the hadronization
    # stable mesons should be produced in pairs (Z2 symmetry),
    # so require total number produced by pythia to be a multiple of 4
    # do *not* require this separately for 111/211 and 113/213 (pseudoscalar vs. vector)
    if options.filterZ2 and hasattr(process,'ProductionFilterSequence'):
        process.darkhadronZ2filter = cms.EDFilter("MCParticleModuloFilter",
            moduleLabel = cms.InputTag('generator'),
            particleIDs = cms.vint32(51,53),
            multipleOf = cms.uint32(4),
            absID = cms.bool(True),
        )
        process.ProductionFilterSequence += process.darkhadronZ2filter
        if ".2017." in options.config or ".2018." in options.config: process.darkhadronZ2filter.moduleLabel = cms.InputTag('generator','unsmeared')

    # also filter out events with Zprime -> SM quarks
    if hasattr(process,'ProductionFilterSequence'):
        process.darkquarkFilter = cms.EDFilter("MCParticleModuloFilter",
            moduleLabel = cms.InputTag('generator'),
            particleIDs = cms.vint32(4900101),
            multipleOf = cms.uint32(2),
            absID = cms.bool(True),
            min = cms.uint32(2),
            status = cms.int32(23),
        )
        process.ProductionFilterSequence += process.darkquarkFilter
        if ".2017." in options.config or ".2018." in options.config: process.darkquarkFilter.moduleLabel = cms.InputTag('generator','unsmeared')

# genjet/met settings - treat DM stand-ins as invisible
_particles = ["genParticlesForJetsNoMuNoNu","genParticlesForJetsNoNu","genCandidatesForMET","genParticlesForMETAllVisible"]
for _prod in _particles:
    if hasattr(process,_prod):
        getattr(process,_prod).ignoreParticleIDs.extend([51,52,53])
if hasattr(process,'recoGenJets') and hasattr(process,'recoAllGenJetsNoNu'):
    process.recoGenJets += process.recoAllGenJetsNoNu
if hasattr(process,'genJetParticles') and hasattr(process,'genParticlesForJetsNoNu'):
    process.genJetParticles += process.genParticlesForJetsNoNu
    for output in options.output:
        if len(output)==0: continue
        output_attr = getattr(oprocess,output)
        if hasattr(output_attr,"outputCommands"):
            output_attr.outputCommands.extend([
                'keep *_genParticlesForJets_*_*',
                'keep *_genParticlesForJetsNoNu_*_*',
            ])

# miniAOD settings
_pruned = ["prunedGenParticlesWithStatusOne","prunedGenParticles"]
for _prod in _pruned:
    if hasattr(process,_prod):
        # keep HV & DM particles
        getattr(process,_prod).select.extend([
            "keep (4900001 <= abs(pdgId) <= 4900991 )",
            "keep (51 <= abs(pdgId) <= 53)",
        ])

# multithreading options
if options.threads>0:
    if not hasattr(process,"options"):
        process.options = cms.untracked.PSet()
    process.options.numberOfThreads = cms.untracked.uint32(options.threads)
    process.options.numberOfStreams = cms.untracked.uint32(options.streams if options.streams>0 else 0)

if options.tmi:
    from Validation.Performance.TimeMemoryInfo import customise
    process = customise(process)
    
if options.dump:
    print process.dumpPython()
    sys.exit(0)
