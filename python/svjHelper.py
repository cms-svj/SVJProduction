class svjHelper(object):
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
        xsec = 0.8 # should be a function of mZprime...
        return xsec

    def getPythiaSettings(self,mZprime,mDark,rinv,alpha):
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

