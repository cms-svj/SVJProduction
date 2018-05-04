import FWCore.ParameterSet.Config as cms

process = cms.Process("demo")

process.load("Configuration.StandardSequences.Services_cff")
process.load("SVJ.Production.SoftDropAnalyzer_cfi")

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),
    secondaryFileNames = cms.untracked.vstring(),
    #eventsToProcess = cms.untracked.VEventRange('1:480')
)

"""
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(1),
  printVertex = cms.untracked.bool(False),
  src = cms.InputTag("genParticlesForJetsNoNu")
)


process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("genParticles"),                                                               
                                   printP4 = cms.untracked.bool(False),
                                   printPtEtaPhi = cms.untracked.bool(False),
                                   printVertex = cms.untracked.bool(False),
                                   printStatus = cms.untracked.bool(False),
                                   printIndex = cms.untracked.bool(False),
                                   status = cms.untracked.vint32( 1, 2, 4, 21, 22, 23, 33, 31, 41, 42, 43, 44, 51, 52, 53, 61, 62, 63, 71, 73, 83, 84, 91 )
                                   )
"""
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("softdropanalysis.root")
)

#process.p1 = cms.Path(process.SoftDropAnalyzer*process.printTree)

process.p1 = cms.Path(process.SoftDropAnalyzer)
