import os, math

class svjHelper(object):
    def __init__(self):
        with open(os.path.join(os.path.expandvars('$CMSSW_BASE'),'src/SVJ/Production/test/dict_xsec_Zprime.txt'),'r') as xfile:
            self.xsecs = {int(xline.split('\t')[0]): float(xline.split('\t')[1]) for xline in xfile}

    def getOutName(self,mZprime,mDark,rinv,alpha,events,signal=True,outpre="outpre",part=None):
        _outname = outpre
        if signal:
            _outname += "_mZprime-{:g}".format(mZprime)
            _outname += "_mDark-{:g}".format(mDark)
            _outname += "_rinv-{:g}".format(rinv)
            _outname += "_alpha-{:g}".format(alpha)
        _outname += "_n-{:g}".format(events)
        if part is not None:
            _outname += "_part-{:g}".format(part)
        return _outname

    def getPythiaXsec(self,mZprime):
        xsec = 1.0 
        # a function of mZprime
        if mZprime in self.xsecs: xsec = self.xsecs[mZprime]
        return xsec

    def getPythiaSettings(self,mZprime,mDark,rinv,alpha):
        mMin = mZprime-1
        mMax = mZprime+1
        mSqua = mDark/2. # dark scalar quark mass (also used for pTminFSR)

        # calculation of lambda to give desired alpha
        # see 1707.05326 fig2 for the equation: alpha = pi/(b * log(1 TeV / lambda)), b = 11/6*n_c - 2/6*n_f
        # n_c = HiddenValley:Ngauge, n_f = HiddenValley:nFlav
        # see also TimeShower.cc in Pythia8, PDG chapter 9 (Quantum chromodynamics), etc.
        n_c = 2
        n_f = 2
        b0 = 11.0/6.0*n_c - 2.0/6.0*n_f
        lambdaHV = 1000*math.exp(-math.pi/(b0*alpha))
    
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
            # hidden spectrum:
            # fermionic dark quark,
            # diagonal pseudoscalar meson, off-diagonal pseudoscalar meson, DM stand-in particle,
            # diagonal vector meson, off-diagonal vector meson, DM stand-in particle
            '4900101:m0 = {:g}'.format(mSqua),
            '4900111:m0 = {:g}'.format(mDark),
            '4900211:m0 = {:g}'.format(mDark),
            '51:m0 = 0.0',
            '51:isResonance = false',
            '4900113:m0 = {:g}'.format(mDark),
            '4900213:m0 = {:g}'.format(mDark),
            '53:m0 = 0.0',
            '53:isResonance = false',
            # other HV params
            'HiddenValley:Ngauge = {:d}'.format(n_c),
            # when Fv has spin 0, qv spin fixed at 1/2
            'HiddenValley:spinFv = 0',
            'HiddenValley:FSR = on',
            'HiddenValley:fragment = on',
            'HiddenValley:alphaOrder = 1',
            'HiddenValley:Lambda = {:g}'.format(lambdaHV),
            'HiddenValley:nFlav = {:d}'.format(n_f),
            'HiddenValley:probVector = 0.75',
            'HiddenValley:pTminFSR = {:g}'.format(mSqua),
            # branching - effective rinv (applies to all meson species b/c n_f >= 2)
            '4900111:oneChannel = 1 {:g} 0 51 -51'.format(rinv),
            '4900111:addChannel = 1 {:g} 91 1 -1'.format(1.0-rinv),
            '4900211:oneChannel = 1 {:g} 0 51 -51'.format(rinv),
            '4900211:addChannel = 1 {:g} 91 1 -1'.format(1.0-rinv),
            '4900113:oneChannel = 1 {:g} 0 53 -53'.format(rinv),
            '4900113:addChannel = 1 {:g} 91 1 -1'.format(1.0-rinv),
            '4900213:oneChannel = 1 {:g} 0 53 -53'.format(rinv),
            '4900213:addChannel = 1 {:g} 91 1 -1'.format(1.0-rinv),
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
        ]

