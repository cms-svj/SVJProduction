import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys
from SVJ.Production.svjHelper import svjHelper

options = VarParsing("analysis")
options.register("signal", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("mZprime", 2000.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("mDark", 20.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("rinv", 0.3, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("alpha", 0.1, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("filterZ2", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("part", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("indir", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("inpre", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("outpre", "step1", VarParsing.multiplicity.list, VarParsing.varType.string)
options.register("output", "", VarParsing.multiplicity.list, VarParsing.varType.string)
options.register("config", "SVJ.Production.step1_GEN", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("threads", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("streams", 0, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("redir", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("tmi", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("dump", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.parseArguments()

_helper = svjHelper()
_helper.setModel(options.mZprime,options.mDark,options.rinv,options.alpha)

# output name definition
_outname = _helper.getOutName(options.maxEvents,part=options.part,signal=options.signal)
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

# output settings
if len(options.output)==0: options.output = sorted(process.outputModules_())
if len(options.outpre)!=len(options.output):
    raise ValueError("Mismatch between # of output prefixes and # of output modules\n\tOutput modules are: "+", ".join(options.output))
for iout,output in enumerate(options.output):
    if not hasattr(process,output):
        raise ValueError("Unavailable output module: "+output)
    getattr(process,output).fileName = 'file:'+_outname.replace("outpre",options.outpre[iout])

# reset all random numbers to ensure statistically distinct but reproducible jobs
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randHelper = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randHelper.resetSeeds(options.maxEvents+options.part)

# generator settings
if options.signal and hasattr(process,'generator'):
    process.generator.crossSection = cms.untracked.double(_helper.xsec)
    process.generator.PythiaParameters.processParameters = cms.vstring(_helper.getPythiaSettings())
    process.generator.maxEventsToPrint = cms.untracked.int32(1)

# gen filter settings
# pythia implementation of model has 4900111/211 -> -51 51 and 4900113/213 -> -53 53
# this is a stand-in for direct production of a single stable dark meson in the hadronization
# stable mesons should be produced in pairs (Z2 symmetry),
# so require total number produced by pythia to be a multiple of 4
# require this separately for 111/211 and 113/213 (pseudoscalar vs. vector)
if options.signal and options.filterZ2 and hasattr(process,'ProductionFilterSequence'):
    process.darkhadronZ2filterPseudoscalar = cms.EDFilter("MCParticleModuloFilter",
		moduleLabel = cms.InputTag('generator'),
		particleID = cms.int32(51),
		multipleOf = cms.uint32(4),
		absID = cms.bool(True),
    )
    process.ProductionFilterSequence += process.darkhadronZ2filterPseudoscalar
    process.darkhadronZ2filterVector = process.darkhadronZ2filterPseudoscalar.clone(
        particleID = cms.int32(53),
    )
    process.ProductionFilterSequence += process.darkhadronZ2filterVector

# also filter out events with Zprime -> SM quarks
process.darkquarkFilter = cms.EDFilter("MCParticleModuloFilter",
    moduleLabel = cms.InputTag('generator'),
    particleID = cms.int32(4900101),
    multipleOf = cms.uint32(2),
    absID = cms.bool(True),
    min = cms.uint32(2),
    status = cms.int32(23),
)
process.ProductionFilterSequence += process.darkquarkFilter

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
        output_attr = getattr(process,output)
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
