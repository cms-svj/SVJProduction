import os, math

class quark(object):
    def __init__(self,id,mass):
        self.id = id
        self.mass = mass
        self.bf = 1

class svjHelper(object):
    def __init__(self):
        with open(os.path.join(os.path.expandvars('$CMSSW_BASE'),'src/SVJ/Production/test/dict_xsec_Zprime.txt'),'r') as xfile:
            self.xsecs = {int(xline.split('\t')[0]): float(xline.split('\t')[1]) for xline in xfile}
        self.quarks = [
            quark(1,0.0048),
            quark(2,0.0023),
            quark(3,0.095),
            quark(4,1.275),
            quark(5,4.18),
        ]

    def setModel(self,mZprime,mDark,rinv,alpha):
        # store the basic parameters
        self.mZprime = mZprime
        self.mDark = mDark
        self.rinv = rinv
        self.alpha = alpha

        # get more parameters
        self.xsec = self.getPythiaXsec(self.mZprime)
        self.mMin = self.mZprime-1
        self.mMax = self.mZprime+1
        self.mSqua = self.mDark/2. # dark scalar quark mass (also used for pTminFSR)

        # calculation of lambda to give desired alpha
        # see 1707.05326 fig2 for the equation: alpha = pi/(b * log(1 TeV / lambda)), b = 11/6*n_c - 2/6*n_f
        # n_c = HiddenValley:Ngauge, n_f = HiddenValley:nFlav
        # see also TimeShower.cc in Pythia8, PDG chapter 9 (Quantum chromodynamics), etc.
        self.n_c = 2
        self.n_f = 2
        b0 = 11.0/6.0*self.n_c - 2.0/6.0*self.n_f
        self.lambdaHV = 1000*math.exp(-math.pi/(b0*self.alpha))

    def getOutName(self,events,signal=True,outpre="outpre",part=None):
        _outname = outpre
        if signal:
            _outname += "_mZprime-{:g}".format(self.mZprime)
            _outname += "_mDark-{:g}".format(self.mDark)
            _outname += "_rinv-{:g}".format(self.rinv)
            _outname += "_alpha-{:g}".format(self.alpha)
        _outname += "_n-{:g}".format(events)
        if part is not None:
            _outname += "_part-{:g}".format(part)
        return _outname

    # allow access to all xsecs
    def getPythiaXsec(self,mZprime):
        xsec = 1.0 
        # a function of mZprime
        if mZprime in self.xsecs: xsec = self.xsecs[mZprime]
        return xsec

    # check mDark against quark masses
    def getQuarks(self):
        return [q for q in self.quarks if q.mass < self.mDark]

    def invisibleDecay(self,mesonID,dmID):
        lines = ['{:d}:oneChannel = 1 {:g} 0 {:d} -{:d}'.format(mesonID,self.rinv,dmID,dmID)]
        return lines

    def visibleDecay(self,type,mesonID,dmID):
        theQuarks = self.getQuarks()
        if type=="simple":
            theQuarks = [self.quarks[0]]
            theQuarks[0].bf = (1.0-self.rinv)
        if type=="democratic":
            bfQuarks = (1.0-self.rinv)/float(len(theQuarks))
            for iq,q in enumerate(theQuarks):
                theQuarks[iq].bf = bfQuarks
        elif type=="massInsertion":
            denom = sum([q.mass**2 for q in theQuarks])
            for iq,q in enumerate(theQuarks):
                theQuarks[iq].bf = (1.0-self.rinv)*(q.mass**2)/denom
        else:
            raise ValueError("unknown visible decay type: "+type)
        lines = ['{:d}:addChannel = 1 {:g} 91 {:d} -{:d}'.format(mesonID,q.bf,q.id,q.id) for q in theQuarks]
        return lines

    def getPythiaSettings(self):
        # todo: include safety/sanity checks
        
        lines = [
            'HiddenValley:ffbar2Zv = on',
            # parameters for leptophobic Z'
            '4900023:m0 = {:g}'.format(self.mZprime),
            '4900023:mMin = {:g}'.format(self.mMin),
            '4900023:mMax = {:g}'.format(self.mMax),
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
            '4900101:m0 = {:g}'.format(self.mSqua),
            '4900111:m0 = {:g}'.format(self.mDark),
            '4900211:m0 = {:g}'.format(self.mDark),
            '51:m0 = 0.0',
            '51:isResonance = false',
            '4900113:m0 = {:g}'.format(self.mDark),
            '4900213:m0 = {:g}'.format(self.mDark),
            '53:m0 = 0.0',
            '53:isResonance = false',
            # other HV params
            'HiddenValley:Ngauge = {:d}'.format(self.n_c),
            # when Fv has spin 0, qv spin fixed at 1/2
            'HiddenValley:spinFv = 0',
            'HiddenValley:FSR = on',
            'HiddenValley:fragment = on',
            'HiddenValley:alphaOrder = 1',
            'HiddenValley:Lambda = {:g}'.format(self.lambdaHV),
            'HiddenValley:nFlav = {:d}'.format(self.n_f),
            'HiddenValley:probVector = 0.75',
            'HiddenValley:pTminFSR = {:g}'.format(self.mSqua),
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
        # branching - effective rinv (applies to all meson species b/c n_f >= 2)
        # pseudoscalars have mass insertion decay, vectors have democratic decay
        lines += self.invisibleDecay(4900111,51)
        lines += self.visibleDecay("massInsertion",4900111,51)
        lines += self.invisibleDecay(4900211,51)
        lines += self.visibleDecay("massInsertion",4900211,51)
        lines += self.invisibleDecay(4900113,53)
        lines += self.visibleDecay("democratic",4900113,53)
        lines += self.invisibleDecay(4900213,53)
        lines += self.visibleDecay("democratic",4900213,53)

        return lines

