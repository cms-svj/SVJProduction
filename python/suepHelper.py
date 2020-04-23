import FWCore.ParameterSet.Config as cms
import os, math, sys

class suepHelper(object):
    def __init__(self):
        # todo: get list of Higgs xsecs vs mass?
        self.xsecs = []
        # pdg ids
        self.idMediator = 25
        self.idDark = 999999
        self.idPho = 999998
        pass

    def setModel(self,mMediator,mDark,temperature):
        # store the basic parameters
        self.mMediator = mMediator
        self.mDark = mDark
        self.temperature = temperature

        # get more parameters
        self.xsec = 1
        self.mMin = self.mMediator-1
        self.mMax = self.mMediator+1
        self.mPho = self.mDark/2. # dark photon mass

    def getOutName(self,events=0,signal=True,outpre="outpre",part=None,sanitize=False):
        _outname = outpre
        if signal:
            _outname += "_mMed-{:g}".format(self.mMediator)
            _outname += "_mDark-{:g}".format(self.mDark)
            _outname += "_temp-{:g}".format(self.temperature)
        # todo: include tune in name? depends on year
        _outname += "_13TeV-pythia8"
        if events>0: _outname += "_n-{:g}".format(events)
        if part is not None:
            _outname += "_part-{:g}".format(part)
        if sanitize:
            _outname = _outname.replace("-","_").replace(".","p")
        return _outname

    # allow access to all xsecs
    def getPythiaXsec(self,mMediator):
        xsec = 1.0
        # a function of mMediator
        if mMediator in self.xsecs: xsec = self.xsecs[mMediator]
        return xsec

    def getPythiaSettings(self):
        # todo: include safety/sanity checks

        lines = [
            # Momentum is not exactly conserved due to small numerical errors, turn off checks to prevent pythia aborting
            'Check:event = off',
            # parameters for mediator (Higgs)
            'HiggsSM:all = on',
            '{}:mayDecay = off'.format(self.idMediator),
            '{}:m0 = {:g}'.format(self.idMediator,self.mMediator),
            # parameters for dark meson (simple decay to u ubar)
            '{}:all = GeneralResonance void 0 0 0 {:g} 0.001 0.0 0.0 0.0'.format(self.idDark,self.mDark),
            '{}:oneChannel = 1 1.0 101 1 -1'.format(self.idDark),
        ]

        return lines

    def getHookSettings(self):
        pset = cms.PSet(
            temperature = cms.double(self.temperature),
            idMediator = cms.int32(self.idMediator),
            idDark = cms.int32(self.idDark)
        )

        return pset
