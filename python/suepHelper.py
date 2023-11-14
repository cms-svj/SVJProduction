import FWCore.ParameterSet.Config as cms
import os, math, sys

class suepHelper(object):
    allowed_channels = ["ggH","ZH","WH"]
    def __init__(self):
        # todo: get list of Higgs xsecs vs mass?
        self.xsecs = []
        # pdg ids
        self.idMediator = 25
        self.idDark = 999999
        self.idPho = 999998
        pass

    def setModel(self,channel,mMediator,mDark,temperature,decay):
        # store the basic parameters
        if channel not in self.allowed_channels: raise ValueError("Unknown channel: {}".format(channel))
        self.channel = channel
        self.mMediator = mMediator
        self.mDark = mDark
        self.temperature = temperature
        self.decay = decay

        # get more parameters
        self.xsec = 1
        self.mMin = self.mMediator-1
        self.mMax = self.mMediator+1
        self.mPho = 1. # full hadronic (previously "generic" is set to 1)
        if   decay == "darkPho"   : self.mPho = 0.5 # GeV    
        elif decay == "darkPhoHad": self.mPho = 0.7 # GeV, allows more pion decays

    def getOutName(self,events=0,signal=True,outpre="outpre",part=None,sanitize=False,gridpack=False):
        _outname = outpre
        if signal:
            _outname += "_{}-channel".format(self.channel)
            _outname += "_mMed-{:g}".format(self.mMediator)
            _outname += "_mDark-{:g}".format(self.mDark)
            _outname += "_temp-{:g}".format(self.temperature)
            _outname += "_decay-{}".format(self.decay)
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
        if self.decay!="generic" and self.decay!="darkPho" and self.decay!="darkPhoHad": 
            raise ValueError("Unknown decay mode: "+self.decay)
        if 2.0*self.mPho > self.mDark : 
            raise ValueError("dark photon mass {} more than 2x dark meson mass {}".format(self.mPho, self.mDark) )
        # SM vs. BSM based on mass
        lines_prod = [
            '{}:m0 = {:g}'.format(self.idMediator,self.mMediator),
        ]
        lines_channel = {}
        if self.mMediator==125.0:
            lines_channel["ggH"] = [
                'HiggsSM:all = off',
                'HiggsSM:gg2H = on',
            ]
            lines_channel["WH"] = [
                'HiggsSM:all = off',
                'HiggsSM:ffbar2HW = on',
                '24:onMode = off',
                '24:onIfAny = 11 13 15', # leptonic
                '24:mMin = 0.1',
            ]
            lines_channel["ZH"] = [
                'HiggsSM:all = off',
                'HiggsSM:ffbar2HZ = on',
                '23:onMode = off',
                '23:onIfAny = 11 13 15', # leptonic
                '23:mMin = 0.1',
            ]
        else:
            lines_BSM = [
                # parameters for mediator (Higgs)
                'Higgs:useBSM = on',
                'HiggsH1:coup2d = 1',
                'HiggsH1:coup2u = 0',
                'HiggsH1:coup2Z = 0',
                'HiggsH1:coup2W = 0',
                'HiggsH1:coup2l = 0',
            ]
            lines["ggH"] = lines_BSM + [
                'HiggsBSM:gg2H1 = on',
            ]
            lines["WH"] = lines_BSM + [
                'HiggsBSM:ffbar2H1W = on',
                '24:onMode = off',
                '24:onIfAny = 11 13 15', # leptonic
                '24:mMin = 0.1',
            ]
            lines["ZH"] = lines_BSM + [
                'HiggsBSM:ffbar2H1Z = on',
                '23:onMode = off',
                '23:onIfAny = 11 13 15', # leptonic
                '23:mMin = 0.1',
            ]
        # We decay each dark meson two 2 dark photons (pdg code 999998) 
        # Each dark photon in turn decays to SM fermions
        # The dark photon branching ratios are mass dependent, 
        # see e.g. arxiv:1505.07459. Values used here are approximate.
        lines = lines_prod + lines_channel[self.channel] + [
            'Check:event = off',
            # add a dark meson and dark photon 
            '{}:all = GeneralResonance void 0 0 0 {:g} 0.001 0.0 0.0 0.0'.format(self.idDark,self.mDark),
            '{}:all = GeneralResonance void 1 0 0 {:g} 0.001 0.0 0.0 0.0'.format(self.idPho,self.mPho),
            # define dark meson decay
            '{}:addChannel = 1 1.0 101 {} {} '.format(self.idDark,self.idPho,self.idPho), # 100% br to dark photons
        ]

        # define dark photon decay
        if self.decay=="darkPho":
            lines.append('{}:addChannel = 1 0.40 101 11 -11 '.format(self.idPho)  )#40% br to e+ e-
            lines.append('{}:addChannel = 1 0.40 101 13 -13 '.format(self.idPho)  )#40% br to m+ m-
            lines.append('{}:addChannel = 1 0.20 101 211 -211 '.format(self.idPho))#20% br to pi+ pi-
        elif self.decay=="darkPhoHad":
            lines.append('{}:addChannel = 1 0.15 101 11 -11 '.format(self.idPho)  )#15% br to e+ e-
            lines.append('{}:addChannel = 1 0.15 101 13 -13 '.format(self.idPho)  )#15% br to m+ m-
            lines.append('{}:addChannel = 1 0.70 101 211 -211 '.format(self.idPho))#70% br to pi+ pi-
        else : # "generic" uubar
            lines.append('{}:addChannel = 1 1.0 101 211 -211 '.format(self.idPho)) #100% br to pi+ pi-

        return lines

    def getHookSettings(self):
        pset = cms.PSet(
            pluginName = cms.string("SuepDecay"),
            temperature = cms.double(self.temperature),
            idMediator = cms.int32(self.idMediator),
            idDark = cms.int32(self.idDark),
        )

        return pset
