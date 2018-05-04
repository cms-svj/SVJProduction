import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('SoftDropGenJets',eras.Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#added for large scale:
process.load("SVJ.Production.SoftDropAnalyzer_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:step1.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

#added for large scale:
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("softdropanalysis.root")
)

# Other statements
from RecoJets.Configuration.RecoGenJets_cff import ak8GenJetsNoNu
process.ak8GenJetsNoNuArea = ak8GenJetsNoNu.clone(
    doAreaFastjet = cms.bool(True),
)

process.ak8GenJetsNoNuSoftDrop = ak8GenJetsNoNu.clone(
    useSoftDrop = cms.bool(True),
    zcut = cms.double(0.1),
    beta = cms.double(0.0),
    R0   = cms.double(0.5),
    useExplicitGhosts = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets"),
    doAreaFastjet = cms.bool(True),
)

process.packedGenJetsAK8NoNu = cms.EDProducer("GenJetSubstructurePacker",
    jetSrc = cms.InputTag("ak8GenJetsNoNuArea"),
    distMax = cms.double(0.8),
    algoTags = cms.VInputTag(
        cms.InputTag("ak8GenJetsNoNuSoftDrop"),
    ),
)



from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v6', '')

# Path and EndPath definitions
process.jet_step = cms.Path(process.ak8GenJetsNoNuArea+process.ak8GenJetsNoNuSoftDrop+process.packedGenJetsAK8NoNu+process.SoftDropAnalyzer)
process.endjob_step = cms.EndPath(process.endOfProcess)

# Schedule definition
process.schedule = cms.Schedule(process.jet_step)
process.schedule.extend([process.endjob_step])

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(4)
process.options.numberOfStreams=cms.untracked.uint32(0)
