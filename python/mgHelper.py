from string import Template
import os, sys, shutil
from glob import glob

class mgHelper(object):

    def __init__(
        self,
        model,
        mMediator,
        mSqua,
        boost=0.0,
        boostvar = None,
        sepproc = False,
        nMediator = None,
        yukawa = None,
    ):
        self.model = model
        self.mMediator = mMediator
        self.mSqua = mSqua
        self.boost = boost
        self.boostvar = boostvar
        self.sepproc = sepproc
        self.nMediator = nMediator
        self.yukawa = yukawa

    def getJetMatchSettings(self, qCut=125., nJetMax=2):
        lines = [
            'JetMatching:setMad = off', # if 'on', merging parameters are set according to LHE file
            'JetMatching:scheme = 1', # 1 = scheme inspired by Madgraph matching code
            'JetMatching:merge = on', # master switch to activate parton-jet matching. when off, all external events accepted
            'JetMatching:jetAlgorithm = 2', # 2 = SlowJet clustering
            'JetMatching:etaJetMax = 5.', # max eta of any jet
            'JetMatching:coneRadius = 1.0', # gives the jet R parameter
            'JetMatching:slowJetPower = 1', # -1 = anti-kT algo, 1 = kT algo. Only kT w/ SlowJet is supported for MadGraph-style matching
            'JetMatching:qCut = {:g}'.format(qCut), # this is the actual merging scale. should be roughly equal to xqcut in MadGraph
            'JetMatching:nJetMax = {:d}'.format(nJetMax), # number of partons in born matrix element for highest multiplicity
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
        modname = self.getOutName(events=events,outpre=self.model.upper(),sanitize=True,gridpack=True)
        template_paths = [p for ftype in ["dat","patch"] for p in glob(os.path.join(mg_input_dir, "*."+ftype))]
        for template in template_paths:
            fname_orig = os.path.join(mg_input_dir,template)
            fname_new = os.path.join(mg_input_dir,template.replace("modelname",modname))
            fill_template(
                fname_orig,
                fname_new,
                modelName = modname,
                totalEvents = "{:g}".format(events),
                cores = "{:g}".format(cores),
                lhaid = "{:g}".format(lhaid),
                # for boosted
                madpt = "{:g}".format(self.boost if self.boostvar=="madpt" else 0.),
                # for t-channel
                procInclusive = "" if not self.sepproc or self.nMediator is None else "#",
                procPair = "" if self.sepproc and self.nMediator==2 else "#",
                procSingle = "" if self.sepproc and self.nMediator==1 else "#",
                procNonresonant = "" if self.sepproc and self.nMediator==0 else "#",
            )

        return mg_model_dir, mg_input_dir
