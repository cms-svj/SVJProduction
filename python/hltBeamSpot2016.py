import math
import FWCore.ParameterSet.Config as cms

def fixHLTBeamSpot2016(process):
    """Make the 2016 HLT beam spot consistent with the generated vertices.

    In MC the HLT has no scalers, so hltOnlineBeamSpot falls back to BeamSpotObjectsRcd from the 80X GT
    (80X_mcRun2_asymptotic_2016_TrancheIV_v6), which is the old Realistic50ns13TeVCollision beam spot, while GEN-SIM (106X)
    smears the vertices with Realistic25ns13TeV2016Collision: ~130 um offset in x. The 2016 HLT pixel vertices only fit z
    and take x,y from the beam spot, so e.g. scouting PF candidates fail the 100 um vertex association.
    This provides BeamSpotObjectsRcd from the generator vertex-smearing parameters instead.
    """
    from IOMC.EventVertexGenerators.VtxSmearedParameters_cfi import Realistic25ns13TeV2016CollisionVtxSmearingParameters as vtx
    from RecoVertex.BeamSpotProducer.BeamSpotFakeParameters_cfi import BeamSpotFakeConditions

    if vtx.Alpha.value()!=0. or vtx.Phi.value()!=0.:
        raise ValueError("fixHLTBeamSpot2016: non-zero Alpha/Phi in the vertex smearing (beam tilt) is not handled")
    # luminous region width sqrt(Emittance*BetaStar/2)
    width = math.sqrt(vtx.Emittance.value()*vtx.BetaStar.value()/2.)

    process.beamSpotFromVtxSmearing = BeamSpotFakeConditions.clone(
        getDataFromFile = cms.bool(False),
        X0 = cms.double(vtx.X0.value()),
        Y0 = cms.double(vtx.Y0.value()),
        Z0 = cms.double(vtx.Z0.value()),
        dxdz = cms.double(0.),
        dydz = cms.double(0.),
        sigmaZ = cms.double(vtx.SigmaZ.value()),
        widthX = cms.double(width),
        widthY = cms.double(width),
        emittanceX = cms.double(0.),
        emittanceY = cms.double(0.),
        betaStar = cms.double(0.),
    )
    # override the GT beam spot (ESPrefer takes the ESSource type and its label)
    process.es_prefer_beamSpotFromVtxSmearing = cms.ESPrefer("BeamSpotFakeConditions", "beamSpotFromVtxSmearing")

    # keep the beam spot used by the HLT, for checks
    if hasattr(process, "RAWSIMoutput"):
        process.RAWSIMoutput.outputCommands.append('keep recoBeamSpot_hltOnlineBeamSpot_*_*')

    return process
