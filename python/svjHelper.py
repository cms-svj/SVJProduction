import os, math, sys, shutil
from string import Template
from glob import glob

class quark(object):
    def __init__(self,id,mass):
        self.id = id
        self.mass = mass
        self.massrun = mass
        self.bf = 1
        self.on = True
        self.active = True # for running nf

    def __repr__(self):
        return str(self.id)+": m = "+str(self.mass)+", mr = "+str(self.massrun)+", on = "+str(self.on)+", bf = "+str(self.bf)

# follows Ellis, Stirling, Webber calculations
class massRunner(object):
    def __init__(self):
        # QCD scale in GeV
        self.Lambda = 0.218

    # RG terms, assuming nc = 3 (QCD)
    def c(self): return 1./math.pi
    def cp(self,nf): return (303.-10.*nf)/(72.*math.pi)
    def b(self,nf): return (33.-2.*nf)/(12.*math.pi)
    def bp(self,nf): return (153.-19.*nf)/(2.*math.pi*(33.-2.*nf))
    def alphaS(self,Q,nf): return 1./(self.b(nf)*math.log(Q**2/self.Lambda**2))

    # derived terms
    def cb(self,nf): return 12./(33.-2.*nf)
    def one_c_cp_bp_b(self,nf): return 1.+self.cb(nf)*(self.cp(nf)-self.bp(nf))

    # constant of normalization
    def mhat(self,mq,nfq):
        return mq/math.pow(self.alphaS(mq,nfq),self.cb(nfq))/self.one_c_cp_bp_b(nfq)

    # mass formula
    def m(self,mq,nfq,Q,nf):
        # temporary hack: exclude quarks w/ mq < Lambda
        alphaq = self.alphaS(mq,nfq)
        if alphaq < 0: return 0
        else: return self.mhat(mq,nfq)*math.pow(self.alphaS(Q,nf),self.cb(nf))*self.one_c_cp_bp_b(nf)

    # operation
    def run(self,quark,nfq,scale,nf):
        # run to specified scale and nf
        return self.m(quark.mass,nfq,scale,nf)

class quarklist(object):
    def __init__(self):
        # mass-ordered
        self.qlist = [
            quark(2,0.0023), # up
            quark(1,0.0048), # down
            quark(3,0.095),  # strange
            quark(4,1.275),  # charm
            quark(5,4.18),   # bottom
        ]
        self.scale = None
        self.runner = massRunner()

    def set(self,scale):
        self.scale = scale
        # mask quarks above scale
        for q in self.qlist:
            # for decays
            if scale is None or 2*q.mass < scale: q.on = True
            else: q.on = False
            # for nf running
            if scale is None or q.mass < scale: q.active = True
            else: q.active = False
        # compute running masses
        if scale is not None:
            qtmp = self.get(active=True)
            nf = len(qtmp)
            for iq,q in enumerate(qtmp):
                q.massrun = self.runner.run(q,iq,scale,nf)
        # or undo running
        else:
            for q in self.qlist:
                q.massrun = q.mass

    def reset(self):
        self.set(None)

    def get(self,active=False):
        return [q for q in self.qlist if (q.active if active else q.on)]

class svjHelper(object):
    def __init__(self):
        with open(os.path.join(os.path.expandvars('$CMSSW_BASE'),'src/SVJ/Production/test/dict_xsec_Zprime.txt'),'r') as xfile:
            self.xsecs = {int(xline.split('\t')[0]): float(xline.split('\t')[1]) for xline in xfile}
        self.quarks = quarklist()
        self.alphaName = ""
        self.generate = None
        # parameters for lambda/alpha calculations
        self.n_c = 2
        self.n_f = 2
        self.b0 = 11.0/6.0*self.n_c - 2.0/6.0*self.n_f

    def setAlpha(self,alpha):
        self.alphaName = alpha
        # "empirical" formula
        lambda_peak = 3.2*math.pow(self.mDark,0.8)
        if self.alphaName=="peak":
            self.alpha = self.calcAlpha(lambda_peak)
        elif self.alphaName=="high":
            self.alpha = 1.5*self.calcAlpha(lambda_peak)
        elif self.alphaName=="low":
            self.alpha = 0.5*self.calcAlpha(lambda_peak)
        else:
            raise ValueError("unknown alpha request: "+alpha)

    # calculation of lambda to give desired alpha
    # see 1707.05326 fig2 for the equation: alpha = pi/(b * log(1 TeV / lambda)), b = 11/6*n_c - 2/6*n_f
    # n_c = HiddenValley:Ngauge, n_f = HiddenValley:nFlav
    # see also TimeShower.cc in Pythia8, PDG chapter 9 (Quantum chromodynamics), etc.

    def calcAlpha(self,lambdaHV):
        return math.pi/(self.b0*math.log(1000/lambdaHV))

    def calcLambda(self,alpha):
        return 1000*math.exp(-math.pi/(self.b0*alpha))

    # has to be "lambdaHV" because "lambda" is a keyword
    def setModel(self,channel,mMediator,mDark,rinv,alpha,yukawa=None,lambdaHV=None,generate=True,boost=0.,boostvar=None):
        # check for issues
        if channel!="s" and channel!="t": raise ValueError("Unknown channel: "+channel)
        # store the basic parameters
        self.channel = channel
        self.mg_name = "DMsimp_SVJ_s_spin1" if channel=="s" else "DMsimp_SVJ_t" if channel=="t" else ""
        self.generate = generate
        self.mMediator = mMediator
        self.mDark = mDark
        self.rinv = rinv
        if isinstance(alpha,str) and alpha[0].isalpha(): self.setAlpha(alpha)
        else: self.alpha = float(alpha)

        self.yukawa = None
        # yukawa not used by pythia "t-channel" generation (only includes strong pair prod)
        # but will still be included in name if provided in model setting
        if self.channel=="t":
            self.yukawa = yukawa
            if self.yukawa is None: raise ValueError("yukawa value must be provided for madgraph t-channel")

        # boosting
        allowed_boostvars = ["pt","madpt"]
        if boostvar is not None:
            if boostvar not in allowed_boostvars:
                raise ValueError("Unknown boost variable {}".format(boostvar))
            # some filters are implemented in madgraph
            if (boostvar=="madpt") and generate:
                raise ValueError("{} boostvar not compatible with Pythia-only generation".format(boostvar))
            self.boostvar = boostvar
            self.boost = boost
        else:
            self.boost = 0
            self.boostvar = ""

        # get more parameters
        self.xsec = self.getPythiaXsec(self.mMediator)
        self.mMin = self.mMediator-1
        self.mMax = self.mMediator+1
        self.mSqua = self.mDark/2. # dark scalar quark mass (also used for pTminFSR)

        # get limited set of quarks for decays (check mDark against quark masses, compute running)
        self.quarks.set(mDark)

        if lambdaHV is not None:
            self.lambdaHV = lambdaHV
            self.alpha = self.calcAlpha(self.lambdaHV)
        else:
            self.lambdaHV = self.calcLambda(self.alpha)

    def getOutName(self,events=0,signal=True,outpre="outpre",part=None,sanitize=False):
        _outname = outpre
        if signal:
            _outname += "_{}-channel".format(self.channel)
            _outname += "_mMed-{:g}".format(self.mMediator)
            _outname += "_mDark-{:g}".format(self.mDark)
            _outname += "_rinv-{:g}".format(self.rinv)
            if len(self.alphaName)>0: _outname += "_alpha-{}".format(self.alphaName)
            else: _outname += "_alpha-{:g}".format(self.alpha)
            if self.yukawa is not None: _outname += "_yukawa-{:g}".format(self.yukawa)
            if self.boost>0: _outname += "_{}{:g}".format(self.boostvar.upper(),self.boost)
        # todo: include tune in name? depends on year
        if self.generate is not None:
            if self.generate:
                _outname += "_13TeV-pythia8"
            else:
                _outname += "_13TeV-madgraphMLM-pythia8"
        if events>0: _outname += "_n-{:g}".format(events)
        if part is not None:
            _outname += "_part-{:g}".format(part)
        if sanitize:
            _outname = _outname.replace("-","_").replace(".","p")
        return _outname

    # allow access to all xsecs
    def getPythiaXsec(self,mMediator):
        xsec = 1.0
        # todo: get t-channel cross sections
        if self.channel=="t": return xsec
        # a function of mMediator
        if mMediator in self.xsecs: xsec = self.xsecs[mMediator]
        return xsec

    def invisibleDecay(self,mesonID,dmID):
        lines = ['{:d}:oneChannel = 1 {:g} 0 {:d} -{:d}'.format(mesonID,self.rinv,dmID,dmID)]
        return lines

    def visibleDecay(self,type,mesonID,dmID):
        theQuarks = self.quarks.get()
        if type=="simple":
            # just pick down quarks
            theQuarks = [q for q in theQuarks if q.id==1]
            theQuarks[0].bf = (1.0-self.rinv)
        elif type=="democratic":
            bfQuarks = (1.0-self.rinv)/float(len(theQuarks))
            for iq,q in enumerate(theQuarks):
                theQuarks[iq].bf = bfQuarks
        elif type=="massInsertion":
            denom = sum([q.massrun**2 for q in theQuarks])
            # hack for really low masses
            if denom==0.: return self.visibleDecay("democratic",mesonID,dmID)
            for q in theQuarks:
                q.bf = (1.0-self.rinv)*(q.massrun**2)/denom
        else:
            raise ValueError("unknown visible decay type: "+type)
        lines = ['{:d}:addChannel = 1 {:g} 91 {:d} -{:d}'.format(mesonID,q.bf,q.id,q.id) for q in theQuarks if q.bf>0]
        return lines

    def getPythiaSettings(self):
        # todo: include safety/sanity checks

        lines_schan = [
            # parameters for leptophobic Z'
            '4900023:m0 = {:g}'.format(self.mMediator),
            '4900023:mMin = {:g}'.format(self.mMin),
            '4900023:mMax = {:g}'.format(self.mMax),
            '4900023:mWidth = 0.01',
            '4900023:oneChannel = 1 0.982 102 4900101 -4900101',
            # SM quark couplings needed to produce Zprime from pp initial state
            '4900023:addChannel = 1 0.003 102 1 -1',
            '4900023:addChannel = 1 0.003 102 2 -2',
            '4900023:addChannel = 1 0.003 102 3 -3',
            '4900023:addChannel = 1 0.003 102 4 -4',
            '4900023:addChannel = 1 0.003 102 5 -5',
            '4900023:addChannel = 1 0.003 102 6 -6',
            # decouple
            '4900001:m0 = 50000',
            '4900002:m0 = 50000',
            '4900003:m0 = 50000',
            '4900004:m0 = 50000',
            '4900005:m0 = 50000',
            '4900006:m0 = 50000',
            '4900011:m0 = 50000',
            '4900012:m0 = 50000',
            '4900013:m0 = 50000',
            '4900014:m0 = 50000',
            '4900015:m0 = 50000',
            '4900016:m0 = 50000',
        ]

        # parameters for bifundamental mediators
        # (keep default flavor-diagonal couplings)
        bifunds = [4900001,4900002,4900003,4900004,4900005,4900006]
        lines_tchan = []
        for bifund in bifunds:
            lines_tchan.extend([
                '{:d}:m0 = {:g}'.format(bifund,self.mMediator),
                '{:d}:mMin = {:g}'.format(bifund,self.mMin),
                '{:d}:mMax = {:g}'.format(bifund,self.mMax),
                '{:d}:mWidth = 0.01'.format(bifund),
            ])
        lines_tchan.extend([
            # decouple
            '4900011:m0 = 50000',
            '4900012:m0 = 50000',
            '4900013:m0 = 50000',
            '4900014:m0 = 50000',
            '4900015:m0 = 50000',
            '4900016:m0 = 50000',
            '4900023:m0 = 50000',
        ])

        if self.generate:
            lines_schan.extend([
                'HiddenValley:ffbar2Zv = on',
            ])
            # pythia can only generate pair prod of bifundamental
            lines_tchan.extend([
                'HiddenValley:gg2DvDvbar = on',
                'HiddenValley:gg2UvUvbar = on',
                'HiddenValley:gg2SvSvbar = on',
                'HiddenValley:gg2CvCvbar = on',
                'HiddenValley:gg2BvBvbar = on',
                'HiddenValley:gg2TvTvbar = on',
                'HiddenValley:qqbar2DvDvbar = on',
                'HiddenValley:qqbar2UvUvbar = on',
                'HiddenValley:qqbar2SvSvbar = on',
                'HiddenValley:qqbar2CvCvbar = on',
                'HiddenValley:qqbar2BvBvbar = on',
                'HiddenValley:qqbar2TvTvbar = on',
            ])

        lines_decay = [
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
        ]
        # branching - effective rinv (applies to all meson species b/c n_f >= 2)
        # pseudoscalars have mass insertion decay, vectors have democratic decay
        lines_decay += self.invisibleDecay(4900111,51)
        lines_decay += self.visibleDecay("massInsertion",4900111,51)
        lines_decay += self.invisibleDecay(4900211,51)
        lines_decay += self.visibleDecay("massInsertion",4900211,51)
        lines_decay += self.invisibleDecay(4900113,53)
        lines_decay += self.visibleDecay("democratic",4900113,53)
        lines_decay += self.invisibleDecay(4900213,53)
        lines_decay += self.visibleDecay("democratic",4900213,53)

        lines = []
        if self.channel=="s": lines = lines_schan + lines_decay
        elif self.channel=="t": lines = lines_tchan + lines_decay

        return lines

    def getJetMatchSettings(self):
        lines = [
            'JetMatching:setMad = off', # if 'on', merging parameters are set according to LHE file
            'JetMatching:scheme = 1', # 1 = scheme inspired by Madgraph matching code
            'JetMatching:merge = on', # master switch to activate parton-jet matching. when off, all external events accepted
            'JetMatching:jetAlgorithm = 2', # 2 = SlowJet clustering
            'JetMatching:etaJetMax = 5.', # max eta of any jet
            'JetMatching:coneRadius = 1.0', # gives the jet R parameter
            'JetMatching:slowJetPower = 1', # -1 = anti-kT algo, 1 = kT algo. Only kT w/ SlowJet is supported for MadGraph-style matching
            'JetMatching:qCut = 125.', # this is the actual merging scale. should be roughly equal to xqcut in MadGraph
            'JetMatching:nJetMax = 2', # number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', # off for MLM matching, turn on for shower-kT matching
        ]

        return lines

    def getMadGraphCards(self,base_dir,lhaid,events=1,cores=1):
        if base_dir[-1]!='/': base_dir = base_dir+'/'

        # helper for templates
        def fill_template(inname, outname=None, **kwargs):
            if outname is None: outname = inname
            with open(inname,'r') as temp:
                old_lines = Template(temp.read())
                new_lines = old_lines.substitute(**kwargs)
            with open(inname,'w') as temp:
                temp.write(new_lines)
            if inname!=outname:
                shutil.move(inname,outname)

        mg_model_dir = os.path.expandvars(base_dir+"mg_model_templates")

        # replace parameters in relevant file
        param_args = dict(
            mediator_mass = "{:g}".format(self.mMediator),
            dark_quark_mass = "{:g}".format(self.mSqua),
        )
        if self.yukawa is not None: param_args["dark_yukawa"] = "{:g}".format(self.yukawa)
        fill_template(
            os.path.join(mg_model_dir,"parameters.py"),
            **param_args
        )

        # use parameters to generate card
        sys.path.append(mg_model_dir)
        from write_param_card import ParamCardWriter
        param_card_file = os.path.join(mg_model_dir,"param_card.dat")
        ParamCardWriter(param_card_file, generic=True)

        mg_input_dir = os.path.expandvars(base_dir+"mg_input_templates")
        modname = self.getOutName(events=events,outpre="SVJ",sanitize=True)
        template_paths = [p for ftype in ["dat","patch"] for p in glob(os.path.join(mg_input_dir, "*."+ftype))]
        for template in template_paths:
            fill_template(
                os.path.join(mg_input_dir,template),
                os.path.join(mg_input_dir,template.replace("modelname",modname)),
                modelName = modname,
                totalEvents = "{:g}".format(events),
                cores = "{:g}".format(cores),
                lhaid = "{:g}".format(lhaid),
                madpt = "{:g}".format(self.boost if self.boostvar=="madpt" else 0.),
            )

        return mg_model_dir, mg_input_dir
