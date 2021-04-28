import FWCore.ParameterSet.Config as cms

process = cms.Process("demo")

process.load("Configuration.StandardSequences.Services_cff")
process.load("SVJ.Production.GenMassAnalyzer_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),
    secondaryFileNames = cms.untracked.vstring()
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("genmassanalysis.root")
)

process.p1 = cms.Path(process.GenMassAnalyzer)

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

# Path and EndPath definitions
process.jet_step = cms.Path(process.ak8GenJetsNoNuArea+process.ak8GenJetsNoNuSoftDrop+process.packedGenJetsAK8NoNu)
