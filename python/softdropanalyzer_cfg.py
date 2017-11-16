import FWCore.ParameterSet.Config as cms

process = cms.Process("demo")

process.load("Configuration.StandardSequences.Services_cff")
process.load("SVJ.Production.SoftDropAnalyzer_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),
    secondaryFileNames = cms.untracked.vstring()
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string("softdropanalysis.root")
)

process.p1 = cms.Path(process.SoftDropAnalyzer)
