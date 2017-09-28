import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

def getPythiaXsec(mZprime):
    xsec = 0.8 # should be a function of mZprime...
    return xsec

def getPythiaSettings(mZprime,mDark,rinv,alpha):
    mMin = mZprime-1
    mMax = mZprime+1
    mSqua = mDark/2. # dark scalar quark mass (also used for pTminFSR)
    mInv = mSqua - 0.1 # dark stable hadron mass

    # todo: include safety/sanity checks
    
    return [
        'HiddenValley:ffbar2Zv = on',
        # parameters for leptophobic Z'
        '4900023:m0 = {:g}'.format(mZprime),
        '4900023:mMin = {:g}'.format(mMin),
        '4900023:mMax = {:g}'.format(mMax),
        '4900023:mWidth = 0.01',
        '4900023:oneChannel = 1 0.982 102 4900101 -4900101',
        '4900023:addChannel = 1 0.003 102 1 -1',
        '4900023:addChannel = 1 0.003 102 2 -2',
        '4900023:addChannel = 1 0.003 102 3 -3',
        '4900023:addChannel = 1 0.003 102 4 -4',
        '4900023:addChannel = 1 0.003 102 5 -5',
        '4900023:addChannel = 1 0.003 102 6 -6',
        # hidden spectrum: HV-only meson, scalar quark, SM-coupled meson
        '4900211:m0 = {:g}'.format(mInv),
        '4900101:m0 = {:g}'.format(mSqua),
        '4900111:m0 = {:g}'.format(mDark),
        # other HV params
        'HiddenValley:Ngauge = 2',
        'HiddenValley:spinFv = 1',
        'HiddenValley:spinqv = 0',
        'HiddenValley:FSR = on',
        'HiddenValley:fragment = on',
        'HiddenValley:alphaOrder = 1',
        'HiddenValley:Lambda = {:g}'.format(alpha),
        'HiddenValley:nFlav = 1',
        'HiddenValley:probVector = 0.0',
        'HiddenValley:pTminFSR = {:g}'.format(mSqua),
        # branching - effective rinv
        '4900111:oneChannel = 1 {:g} 0 4900211 -4900211'.format(rinv),
        '4900111:addChannel = 1 {:g} 91 1 -1'.format(1.0-rinv),
        # decouple
        '4900001:m0 = 5000',
        '4900002:m0 = 5000',
        '4900003:m0 = 5000',
        '4900004:m0 = 5000',
        '4900005:m0 = 5000',
        '4900006:m0 = 5000',
        '4900011:m0 = 5000',
        '4900012:m0 = 5000',
        '4900013:m0 = 5000',
        '4900014:m0 = 5000',
        '4900015:m0 = 5000',
        '4900016:m0 = 5000',
        '4900113:m0 = 5000',
        '4900213:m0 = 5000',
    ]

options = VarParsing("analysis")
options.register("signal", True, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("mZprime", 2000.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("mDark", 20.0, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("rinv", 0.3, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("alpha", 0.1, VarParsing.multiplicity.singleton, VarParsing.varType.float)
options.register("part", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("indir", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("inpre", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("outpre", "step1", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("output", "RAWSIMoutput", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("config", "SVJ.Production.step1_GEN", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("threads", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("streams", 0, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("tmi", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.register("dump", False, VarParsing.multiplicity.singleton, VarParsing.varType.bool)
options.parseArguments()

# output name definition
_outname = options.outpre
if options.signal:
    _outname += "_mZprime-{:g}".format(options.mZprime)
    _outname += "_mDark-{:g}".format(options.mDark)
    _outname += "_rinv-{:g}".format(options.rinv)
    _outname += "_alpha-{:g}".format(options.alpha)
_outname += "_n-{:g}".format(options.maxEvents)
_outname += "_part-{:g}".format(options.part)
_outname += ".root"

_inname = ""
if len(options.inpre)>0:
    _inname = _outname.replace(options.outpre,options.inpre)
    if len(options.indir)>0: _inname = options.indir+"/"+_inname
    if not "root:" in options.indir: _inname = "file:"+_inname

# import process
process = getattr(__import__(options.config,fromlist=["process"]),"process")

# settings
process.maxEvents.input = cms.untracked.int32(options.maxEvents)
if len(_inname)>0: process.source.fileNames = cms.untracked.vstring(_inname)
else: process.source.firstEvent = cms.untracked.uint32((options.part-1)*options.maxEvents+1)
getattr(process,options.output).fileName = 'file:'+_outname

# reset all random numbers to ensure statistically distinct but reproducible jobs
from IOMC.RandomEngine.RandomServiceHelper import RandomNumberServiceHelper
randHelper = RandomNumberServiceHelper(process.RandomNumberGeneratorService)
randHelper.resetSeeds(options.maxEvents+options.part)

# generator settings
if options.signal and hasattr(process,'generator'):
    process.generator.crossSection = cms.untracked.double(getPythiaXsec(options.mZprime))
    process.generator.PythiaParameters.processParameters = cms.vstring(getPythiaSettings(options.mZprime,options.mDark,options.rinv,options.alpha))
    process.generator.maxEventsToPrint = cms.untracked.int32(1)

# genjet/met settings - treat HV mesons as invisible
_particles = ["genParticlesForJetsNoMuNoNu","genParticlesForJetsNoNu","genCandidatesForMET","genParticlesForMETAllVisible"]
for _prod in _particles:
    if hasattr(process,_prod):
        getattr(process,_prod).ignoreParticleIDs.append(4900211)
if hasattr(process,'recoGenJets') and hasattr(process,'recoAllGenJetsNoNu'):
    process.recoGenJets += process.recoAllGenJetsNoNu
if hasattr(process,'genJetParticles') and hasattr(process,'genParticlesForJetsNoNu'):
    process.genJetParticles += process.genParticlesForJetsNoNu
    getattr(process,options.output).outputCommands.extend([
        'keep *_genParticlesForJets_*_*',
        'keep *_genParticlesForJetsNoNu_*_*',
    ])

# miniAOD settings
if hasattr(process,'prunedGenParticles'):
    # keep HV particles
    process.prunedGenParticles.select.append("keep (4900001 <= abs(pdgId) <= 4900991 )")

# multithreading options
if options.threads>1:
    process.options.numberOfThreads = cms.untracked.uint32(options.threads)
    process.options.numberOfStreams = cms.untracked.uint32(options.streams if options.streams>0 else 0)

if options.tmi:
    from Validation.Performance.TimeMemoryInfo import customise
    process = customise(process)
    
if options.dump:
    print process.dumpPython()
    sys.exit(0)
