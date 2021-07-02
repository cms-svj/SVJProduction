import FWCore.ParameterSet.Config as cms

process = cms.Process('GenSub')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:step1.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Output definition

process.jetoutput = cms.OutputModule("PoolOutputModule",
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('file:step2.root'),
    outputCommands = cms.untracked.vstring(
        'keep *_genParticles_*_*',
        'keep *_genParticlesForJetsNoNu_*_*',
    ),
    splitLevel = cms.untracked.int32(0)
)

# helper function
def addModule(mod, process, step, prefix, suffix, output, base, module):
    mod[base] = prefix+base+suffix
    setattr(process, mod[base], module)
    step += getattr(process, mod[base])
    if output is not None: output.outputCommands.append('keep *_{}_*_*'.format(mod[base]))
    return mod, process

# a mini jet toolbox for genjets
def addGenSub(process, step, output, size, prefix, suffix, src, sub=True):
    from RecoJets.Configuration.RecoGenJets_cff import ak4GenJets
    mod = {}
    mod, process = addModule(mod, process, step, prefix, suffix, None if sub else output,
        "GenJets",
        ak4GenJets.clone(
            rParam = size,
            src = src,
        ),
    )
    mod, process = addModule(mod, process, step, prefix, suffix, output,
        "GenJetsArea",
        getattr(process,mod["GenJets"]).clone(
            doAreaFastjet = True,
        ),
    )
    if not sub: return process
    mod, process = addModule(mod, process, step, prefix, suffix, output,
        "GenJetsSoftDrop",
        getattr(process,mod["GenJetsArea"]).clone(
            R0 = cms.double(size),
            useSoftDrop = cms.bool(True),
            zcut = cms.double(0.1),
            beta = cms.double(0.0),
            useExplicitGhosts = cms.bool(True),
            writeCompound = cms.bool(True),
            jetCollInstanceName = cms.string("SubJets"),
        ),
    )
    from RecoJets.JetProducers.ECFAdder_cfi import ECFAdder
    mod, process = addModule(mod, process, step, prefix, suffix, None,
        "ECFNbeta1",
        ECFAdder.clone(
            src = mod["GenJetsSoftDrop"],
            ecftype = "N",
        ),
    )
    mod, process = addModule(mod, process, step, prefix, suffix, None,
        "ECFNbeta2",
        getattr(process,mod["ECFNbeta1"]).clone(
            alpha = 2.0,
            beta = 2.0,
        ),
    )
    mod, process = addModule(mod, process, step, prefix, suffix, output,
        "GenJetsPacked",
        cms.EDProducer("GenJetSubstructurePacker",
            jetSrc = cms.InputTag(mod["GenJetsArea"]),
            distMax = cms.double(size),
            algoTag = cms.InputTag(mod["GenJetsSoftDrop"]),
           	algoFloatTags = cms.VInputTag(
				cms.InputTag(mod["ECFNbeta1"],"ecfN1"),
				cms.InputTag(mod["ECFNbeta1"],"ecfN2"),
				cms.InputTag(mod["ECFNbeta1"],"ecfN3"),
				cms.InputTag(mod["ECFNbeta2"],"ecfN1"),
				cms.InputTag(mod["ECFNbeta2"],"ecfN2"),
				cms.InputTag(mod["ECFNbeta2"],"ecfN3"),
			),
			algoFloatLabels = cms.vstring(
				"ecfN1b1",
				"ecfN2b1",
				"ecfN3b1",
				"ecfN1b2",
				"ecfN2b2",
				"ecfN3b2",
			)
        ),
    )
    return process

process.jet_step = cms.Path()
process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.jetoutput)

# normal AK15 GenJets
process = addGenSub(process, process.jet_step, process.jetoutput, size=1.5, prefix="ak15", suffix="NoNu", src="genParticlesForJetsNoNu")

# GenJets made from dark hadrons
process.darkHadronsForJets = cms.EDProducer("GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        'drop *',
        'keep (abs(pdgId)==4900111 || abs(pdgId)==4900113 || abs(pdgId)==4900211 || abs(pdgId)==4900213) && statusFlags().isLastCopy()',
    ),
)
process.jet_step += process.darkHadronsForJets
process.jetoutput.outputCommands.append('keep *_darkHadronsForJets_*_*')
process = addGenSub(process, process.jet_step, process.jetoutput, size=1.5, prefix="ak15", suffix="Dark", src="darkHadronsForJets")

# GenJetsNu w/ actual dark hadrons instead of fake DM decay products
process.stableDarkHadronsForJets = cms.EDFilter("CandPtrSelector",
    src = cms.InputTag("genParticles"),
    cut = cms.string("numberOfDaughters>0 && abs(daughter(0).pdgId)>=51 && abs(daughter(0).pdgId)<=53"), # keep particles that decayed to DM particles
    filter = cms.bool(False),
)
process.jet_step += process.stableDarkHadronsForJets
process.jetoutput.outputCommands.append('keep *_stableDarkHadronsForJets_*_*')
process.genParticlesForJetsNuDark = cms.EDProducer("CandPtrVectorMerger",
    src = cms.VInputTag("genParticlesForJetsNoNu","stableDarkHadronsForJets"), # merge with NoNu collection
    skipNulls = cms.bool(False),
    warnOnSkip = cms.bool(False),
)
process.jet_step += process.genParticlesForJetsNuDark
process.jetoutput.outputCommands.append('keep *_genParticlesForJetsNuDark_*_*')
process = addGenSub(process, process.jet_step, process.jetoutput, size=0.8, prefix="ak8", suffix="NuDark", src="genParticlesForJetsNuDark", sub=False)

# Schedule definition
process.schedule = cms.Schedule(process.jet_step)
process.schedule.extend([process.endjob_step,process.output_step])
