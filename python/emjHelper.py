import numpy as np
import os
import subprocess
from SVJ.Production.mgHelper import mgHelper
from SVJ.Production.pythiaInfo import pythiaInfo

from scipy.interpolate import CubicSpline

class emjHelper(mgHelper):
    # MadGraph template folder for each channel
    MG_DICT = {
        "s": "DMsimp_SVJ_s_spin1",
        "t": "DMsimp_SVJ_t",
        "tpair": "darkQCD_fv_up", # QCD pair prod. of top-philic scalar mediator X
    }
    SM_COUPLING = {
        'down': ([1,3,5], [0.0048, 0.093, 4.18]),
        'up': ([2, 4, 6], [0.0023, 1.275, 173.21])
    }

    def __init__(self):
        # Aligned mixing elements
        self.s12 = 0
        self.s13 = 0
        self.s23 = 0
        self.kappa0 = 1
        self.kap1 = 0
        self.kap2 = 0
        self.BuildMatrix()

    def setModel(self, channel, mMediator, mDark, kappa, mode='aligned', type='down', generate=True):
        self.mDark = mDark

        super().__init__(
            model="emj",
            mMediator = mMediator,
            mSqua = 2.0 * self.mDark,
            boost = 0.0,
            boostvar = "",
            sepproc = False,
            nMediator = None,
            yukawa = None,
        )
        self.kappa0 = kappa
        self.mode = mode
        self.type = type
        self.channel = channel

        # Validity check of configurations
        assert self.channel in emjHelper.MG_DICT.keys(), "Unknown channel"
        assert self.mode in ['aligned', 'unflavored'], "Unrecognized mode"
        assert self.type in emjHelper.SM_COUPLING.keys(), "Unknown coupling type"

        # the tpair MadGraph model (darkQCD_fv_up) and mediator decay X -> t + dark quark are up-type only
        if self.channel=="tpair" and type!="up": raise ValueError("channel=tpair only supports type=up, got: "+type)


    """Extended properties"""
    @property
    def mg_name(self)->str:
        return emjHelper.MG_DICT[self.channel]

    @property
    def sm_id(self)->list[int]: # PGDID list of coupled SM quarks
        return emjHelper.SM_COUPLING[self.type][0]

    @property
    def sm_mass(self)->list[float]: #PDG mass of coupled SM quarks
        return emjHelper.SM_COUPLING[self.type][0]

    @property
    def xsec(self)->float:
        xsec_file = "dict_xsec_Zprime.txt" if self.channel == "s" else "dict_xsec_pair.txt"
        cols = np.loadtxt(os.path.join(os.path.expandvars('$CMSSW_BASE'),'src/SVJ/Production/test/',xsec_file))
        xsec_spline = CubicSpline(cols[:,0], cols[:,1])
        num_med_colors = 3 if self.channel in ("t","tpair") else 1
        return xsec_spline(self.mMediator) * num_med_colors

    """Output filename settings"""
    def getOutName(self, signal=True, events=0, outpre='outpre', part=None, sanitize=False, gridpack=False):
        _outname = outpre
        if signal:
            _outname += '_{}-channel'.format(self.channel)
            _outname += '_mMed-{:g}'.format(self.mMediator)
            _outname += '_mDark-{:g}'.format(self.mDark)
            _outname += '_{}-{:g}'.format(
                'ctau' if (self.mode == 'unflavored' or self.channel == 'tpair') else 'kappa', self.kappa0)
            _outname += '_{}-{}'.format(self.mode, self.type)
        if events > 0: _outname += '_n-{:g}'.format(events)
        if part is not None:
            _outname += '_part-{:g}'.format(part)
        if sanitize:
            _outname = _outname.replace("-","_").replace(".","p")
        return _outname

    """Flavored coupling mixing matrix relatied items"""
    def BuildMatrix(self):
        # Generating the mixing matrix
        self.U12 = np.matrix([
            [np.sqrt(1 - self.s12**2), self.s12, 0],
            [-self.s12, np.sqrt(1 - self.s12**2), 0],
            [0, 0, 1],
        ])
        self.U13 = np.matrix([
            [np.sqrt(1 - self.s13**2), 0, self.s13],
            [0, 1, 0],
            [-self.s13, 0, np.sqrt(1 - self.s13**2)],
        ])
        self.U23 = np.matrix([
            [1, 0, 0],
            [0, np.sqrt(1 - self.s23**2), self.s23],
            [0, -self.s23, np.sqrt(1 - self.s23**2)],
        ])
        self.D = np.matrix([
            [self.kappa0 * (1 + self.kap1), 0, 0],
            [0, self.kappa0 * (1 + self.kap2), 0],
            [0, 0, self.kappa0 * (1 - self.kap1 - self.kap2)],
        ])
        self.kappa = self.U12 * self.U13 * self.U23 * self.D
        self.kNorm = float(np.square(self.kappa).sum())

    def gamma_pre(self):
        form = self.mDark
        return (3 * self.mDark * form**2) / (32 * np.pi * self.mMediator**4)

    def mass_factor(self, m1, m2):
        if (m1 + m2) * 1.05 > self.mDark:
            return 0
        else:
            ans = (m1 * m1 + m2 * m2)
            ans = ans * np.sqrt(1.0 - (((m1 + m2) / self.mDark)**2))
            ans = ans * np.sqrt(1.0 - (((m1 - m2) / self.mDark)**2))
            return ans

    def calc_gamma(self, dark1, dark2, sm1, sm2):
        k11 = self.kappa.item((dark1, sm1))
        k12 = self.kappa.item((dark1, sm2))
        k22 = self.kappa.item((dark2, sm2))
        k21 = self.kappa.item((dark2, sm1))

        m1 = self.sm_mass[sm1]
        m2 = self.sm_mass[sm2]
        if dark1 == dark2:
            ans = (k11 * k22)**2 * self.gamma_pre()
            ans = ans * self.mass_factor(m1, m2) / 2
            return ans
        elif sm1 == sm2:
            ans = (k11 * k22)**2 * self.gamma_pre()
            ans = ans * self.mass_factor(m1, m2)
            return ans
        else:
            ans = (k11 * k22 + k12 * k21)**2 * self.gamma_pre()
            ans = ans * self.mass_factor(m1, m2)
            return ans

    """Pythia settings"""
    def getPythiaSettings(self):
        return [
            *self._pythia_decay_range(),
            # Common dark sector configurations
            'HiddenValley:alphaOrder = 1',    # Let it run
            'HiddenValley:Ngauge = 3',    # Number of dark QCD colors
            'HiddenValley:FSR = on',
            'HiddenValley:fragment = on',
            'HiddenValley:nFlav = {nflv}'.format(nflv = self._pythia_hv_nFlav()),
            'HiddenValley:spinFv = 0',    # Spin of bi-fundamental res.
            'HiddenValley:pTminFSR = {ptmin}'.format(ptmin=1.1 * self.mSqua),
            '4900101:m0 = {mass}'.format(mass=self.mSqua),
            self._pythia_flavorflag(),
            *self._pythia_hv_lambda(), # Lambda settings depend on channel of interest
            # Main resonance production productions
            *self.MakeRes(),
            # Dark sector decay configurations
            *self.MakeDecay(),
        ]

    def _pythia_decay_range(self)->list[str]:
        return [
            'ParticleDecays:xyMax = 30000',   # in mm/c
            'ParticleDecays:zMax = 30000',    # in mm/c
            'ParticleDecays:limitCylinder = on',
        ]

    def _pythia_hv_nFlav(self)->int:
        # flavors used for the running: unflavored mode overrides the per-channel values
        # (tpair value adapted from https://github.com/chscherb/t-channel_dark_QCD)
        if self.mode == 'unflavored':
            return 7
        return {"s": 3, "t": 3, "tpair": 4}[self.channel]

    def _pythia_hv_lambda(self)->list[str]:
        lambda_lines = [
            'HiddenValley:Lambda = {0}'.format(self.mSqua),
        ] if self.channel != "tpair" else [
            'HiddenValley:alphaFSR = 0.7',
        ]
        if pythiaInfo.useSetLambda():
            lambda_lines.extend([
                'HiddenValley:setLambda = {x}'.format(x='off' if self.channel == 'tpair' else 'on'),
            ])
        return lambda_lines

    def _pythia_flavorflag(self)->str:
        return 'HiddenValley:{flagname} = {flag}'.format(
            flagname=pythiaInfo.emjFlavoredFlagname(),
            flag = 'off' if self.mode == 'unflavored' else 'on'
        )

    def MakeRes(self):
        """Pythia configuration for main heavy mediator production process"""
        res_production_lines = {
            "t": [ # Narrow width bi-fundemental pair production (Run 2 analyses)
                'HiddenValley:gg2DvDvbar = on',    # gg fusion
                'HiddenValley:qqbar2DvDvbar = on',    # qqbar annihilation
                '4900001:m0 = {mass}'.format(mass=self.mMediator),
                '4900001:mWidth = 10',
                *[ # Disabling all other mediators
                    '490000{other_med}:m0 = 50000'.format(other_med=other_med)
                    for other_med in [2, 3, 4, 5, 6]
                ]
            ],
            "s": [  # Z prime production
                'HiddenValley:ffbar2Zv = on',
                '4900023:m0 = {mMediator}'.format(mMediator=self.mMediator),
                '4900023:mWidth = 0.01',
                '4900023:oneChannel = 1 0.982 102 4900101 -4900101',
                *[ # Small fraction decay to SM quarks
                    '4900023:addChannel = 1 0.003 102 {qid} -{qid}'.format(qid=qid)
                    for qid in [1, 2, 3, 4, 5, 6]
                ],
                *[ # Disabling all other mediators
                    '490000{other_med}:m0 = 50000'.format(other_med=other_med)
                    for other_med in [1, 2, 3, 4, 5, 6]
                ]
            ],
            "tpair": [ # top-philic scalar mediator X (pair-produced via QCD in the LHE)
                'SLHA:allowUserOverride = on'
                '4900002:isResonance = on',
                '4900002:mayDecay = on',
                '4900002:isVisible = off',
                '4900002:oneChannel = 1 1.0 103 6 4900101',
                *[ # Disabling all other mediators
                    '490000{other_med}:m0 = 50000'.format(other_med=other_med)
                    for other_med in [1, 3, 4, 5, 6]
                ]
            ]
        }[self.channel]

        if self.channel in ("s", "tpair") or self.mode == 'unflavored':
            return res_production_lines

        # For flavored t-channel, add additional the mediator decay with appropriate branching fractions
        for sm_idx, sm_quark in enumerate(self.sm_id):
            for d_idx, dark_quark in enumerate([1, 2, 3]):
                res_production_lines.append(
                    '4900001:{mode}Channel = 1 {rate} 103 {smq} 490010{dq}'.format(
                        mode='one' if sm_idx == d_idx and sm_idx == 0 else 'add',
                        smq=sm_quark,
                        dq=dark_quark,
                        rate=self.kappa.item((d_idx, sm_idx))**2 / self.kNorm,
                    )
                )
        return res_production_lines

    def MakeDecay(self):
        if self.channel == 'tpair':
            # Fixed decay table: dark pions decay to up-type quark pairs (2nd + 1st gen,
            # equal BR) and are long-lived (emerging); ctau [mm] is set directly by 'kappa'.
            # The global lifetime cap is lifted in runSVJ.py (ParticleDecays:limitTau0 = off).
            q1 = self.sm_id[0]   # 1st-gen (u) for 'up'
            q2 = self.sm_id[1]   # 2nd-gen (c) for 'up'
            return [
                # dark mesons
                '4900111:m0 = {:g}'.format(self.mDark),
                '4900211:m0 = {:g}'.format(self.mDark),
                '4900113:m0 = {:g}'.format(4.0 * self.mDark),
                '4900213:m0 = {:g}'.format(4.0 * self.mDark),
                # dark pion -> up-type quark pairs => emerging
                '4900111:oneChannel = 1 0.5 91 {0} -{0}'.format(q2),
                '4900111:addChannel = 1 0.5 91 {0} -{0}'.format(q1),
                '4900211:oneChannel = 1 0.5 91 {0} -{0}'.format(q2),
                '4900211:addChannel = 1 0.5 91 {0} -{0}'.format(q1),
                # dark rho -> dark pion pair (+ tiny SM leak)
                '4900113:oneChannel = 1 0.999 0 4900111 4900111',
                '4900113:addChannel = 1 0.001 91 {0} -{0}'.format(q2),
                '4900213:oneChannel = 1 0.999 0 4900211 4900211',
                '4900213:addChannel = 1 0.001 91 {0} -{0}'.format(q2),
                # lifetime (ctau in mm; scan via 'kappa') + enable pseudoscalar decay
                '4900111:tau0 = {:g}'.format(self.kappa0),
                '4900211:tau0 = {:g}'.format(self.kappa0),
                '4900111:mayDecay = on',
                '4900211:mayDecay = on',
            ]
        if self.mode == 'unflavored':    # Special case for unflavored decay
            smid = 1 if self.type == 'down' else 2
            return [
                '4900111:m0 = {mass}'.format(mass=self.mDark),
                '4900211:m0 = {mass}'.format(mass=self.mDark),
                '4900111:tau0 = {lifetime}'.format(lifetime=self.kappa0),
                '4900211:tau0 = {lifetime}'.format(lifetime=self.kappa0),
                '4900113:m0 = {mass}'.format(mass=4 * self.mDark),
                '4900213:m0 = {mass}'.format(mass=4 * self.mDark),
                '4900111:oneChannel =  1 1.000  91     {id}     -{id}'.format(id=smid),
                '4900113:oneChannel =  1 0.999  91  4900111   4900111',
                '4900113:addchannel =  1 0.001  91     {id}     -{id}'.format(id=smid),
                '4900211:oneChannel =  1 1.000  91     {id}     -{id}'.format(id=smid),
                '4900213:oneChannel =  1 0.999  91  4900211   4900211',
                '4900213:addchannel =  1 0.001  91     {id}     -{id}'.format(id=smid),
            ]

        ## Remaining configurations can only be t-channel flavor-aligned
        assert self.channel == "t" and self.mode == 'aligned', "Option for 'aligned' mode can only be used with t-channel"
        def extend_decay(dark_meson, dark_comp1, dark_comp2):
            hbarc = 1.97e-13    # in GeV mm
            decay_lines = ['{dark_meson}:m0 = {mass}'.format(dark_meson=dark_meson, mass=self.mDark)]
            gamma_sum = sum([
                self.calc_gamma(dark_comp1, dark_comp2, i, j)
                for i in range(0, 3)
                for j in range(i, 3)
            ])
            if gamma_sum > 0:
                decay_lines.append('{dark_meson}:tau0 = {lifetime}'.format(
                    dark_meson=dark_meson, lifetime=hbarc / gamma_sum))
                decay_lines.extend([
                    '{dark_meson}:{set}Channel = 1 {rate} 91 {sm1} -{sm2}'.format(
                        dark_meson=dark_meson,
                        set='one' if i == 0 and j == 0 else 'add',
                        sm1=self.sm_id[i],
                        sm2=self.sm_id[j],
                        rate=self.calc_gamma(dark_comp1, dark_comp2, i, j) / gamma_sum)
                    for i in range(3)
                    for j in range(i, 3)
                ])
            return decay_lines

        # Defining some missing antiparticles
        flavored_decay = [
            '4900111:antiName = pivDiagbar',
            '4900113:antiName = rhovDiagbar',
        ]
        flavored_decay.extend(extend_decay(4900113, 0, 1))
        flavored_decay.extend(extend_decay(4900211, 0, 2))
        flavored_decay.extend(extend_decay(4900213, 1, 2))
        # Neutral PI is the same-flavor one
        neutral_pi_gamma_sum = [
            sum([
                self.calc_gamma(idx, idx, i, j)
                for i in range(0, 3)
                for j in range(i, 3)
            ])
            for idx in range(3)
        ]
        pi_comp = np.argmax(neutral_pi_gamma_sum)
        flavored_decay.extend(extend_decay(4900111, pi_comp, pi_comp))
        return flavored_decay


if __name__ == "__main__":
    import argparse, re
    helper = emjHelper()

    parser = argparse.ArgumentParser('Calculation debugging for Emerging jets pythia settings')
    parser.add_argument('--mMediator', default=1000, type=float, help='Dark mediator mass [GeV]')
    parser.add_argument('--kappa', default=1, type=float, help='Kappa0 squared (factor to scale decay lifetime)')
    parser.add_argument('--mDark', default=10, type=float, help='Dark meson mass [GeV]')
    parser.add_argument('--type', default='down', type=str, choices=['down', 'up'], help='Alignment to SM up/down type SM quarks')
    parser.add_argument('--mode', default='aligned', type=str, choices=['aligned', 'unflavored'], help='Mixing scenarios to simulate')
    parser.add_argument('--channel', default='t', type=str, choices=['t', 's', 'tpair'], help='Channels to simulate')
    parser.add_argument('cmd', type=str, choices=['dumptime','dumpcard'], help='action to perform')

    args = parser.parse_args()

    if args.cmd == 'dumptime':
        for mDark in np.linspace(1.6, 100, 1000, endpoint=True):
            helper.setModel(args.channel, args.mMediator, mDark, args.kappa, args.mode, args.type)
            tau = [
                x for x in helper.getPythiaSettings()
                if re.match(r'^4900[12]1[13]:tau0', x)
            ]

            def get_time(pdg_id):
                m = [float(re.sub('=', '', re.sub('\d*:tau0', '', t))) for t in tau if re.match('^{}:tau0'.format(pdg_id), t)]
                if len(m):
                    return m[0]
                else:
                    return 1e12

            print('{:10g} {:16g} {:16g} {:16g} {:16g}'.format(mDark, get_time(4900111), get_time(4900113), get_time(4900211), get_time(4900213)))
    elif args.cmd == 'dumpcard':
        helper.setModel(args.channel, args.mMediator, args.mDark, args.kappa, args.mode, args.type)
        for line in helper.getPythiaSettings():
            print(line)
