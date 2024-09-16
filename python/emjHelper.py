import os
import numpy as np

class emjHelper(object):
    def __init__(self):
        cols = np.loadtxt(os.path.join(os.path.expandvars('$CMSSW_BASE'),'src/SVJ/Production/test/dict_xsec_pair.txt'))
        from scipy.interpolate import CubicSpline
        self.xsecs = CubicSpline(cols[:,0], cols[:,1])
        # Aligned mixing elements
        self.s12 = 0
        self.s13 = 0
        self.s23 = 0
        self.kappa0 = 1
        self.kap1 = 0
        self.kap2 = 0
        self.BuildMatrix()

    def setModel(self, channel, mMed, mDark, kappa, mode='aligned', type='down'):
        self.mMed = mMed
        self.mDark = mDark
        self.kappa0 = kappa 
        self.mode = mode
        self.type = type
        self.xsec = self.xsecs(self.mMed)*3 # number of colors
        self.channel = channel

        # Checking the alignment mode
        if self.mode == 'aligned':
            self.s12 = 0
            self.s13 = 0
            self.s23 = 0
            self.kap1 = 0
            self.kap2 = 0
        elif self.mode == 'unflavored':
            pass
        else:
            raise ValueError('Mode {} not recognized'.format(self.mode))
        self.BuildMatrix()

        # Checking the coupling type
        if self.type == 'down':
            self.sm_id = [1, 3, 5]
            self.sm_mass = [0.0048, 0.093, 4.18]
        elif self.type == 'up':
            self.sm_id = [2, 4, 6]
            self.sm_mass = [0.0023, 1.275, 173.21]
        else:
            raise ValueError('Type {} not recognized'.format(self.type))
        return

    def BuildMatrix(self):
        # Generatin the mixing matrix
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

    def getOutName(self, signal=True, events=0, outpre='outpre', part=None, sanitize=False, gridpack=False):
        _outname = outpre

        if signal:
            _outname += '_{}-channel'.format(self.channel)
            _outname += '_mMed-{:g}'.format(self.mMed)
            _outname += '_mDark-{:g}'.format(self.mDark)
            _outname += '_{}-{:g}'.format(
                'kappa' if self.mode != 'unflavored' else 'ctau', self.kappa0)
            _outname += '_{}-{}'.format(self.mode, self.type)
        if events > 0: _outname += '_n-{:g}'.format(events)
        if part is not None:
            _outname += '_part-{:g}'.format(part)
        if sanitize:
            _outname = _outname.replace("-","_").replace(".","p")
        return _outname

    def gamma_pre(self):
        form = self.mDark
        return (3 * self.mDark * form**2) / (32 * np.pi * self.mMed**4)

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

    def getPythiaSettings(self):
        lines = [
            'ParticleDecays:xyMax = 30000',    # in mm/c
            'ParticleDecays:zMax = 30000',    # in mm/c
            'ParticleDecays:limitCylinder = on',    # yes
        ]

        if self.channel == "t":
            t_process = [
                'HiddenValley:gg2DvDvbar = on',    # gg fusion
                'HiddenValley:qqbar2DvDvbar = on',    # qqbar annihilation
            ]
            lines.extend(t_process)
        elif self.channel == "s":
            s_process = [
                'HiddenValley:ffbar2Zv = on'
            ]
            lines.extend(s_process)

        lines.extend(
            [
                'HiddenValley:alphaOrder = 1',    # Let it run
                'HiddenValley:Ngauge = 3',    # Number of dark QCD colors
                'HiddenValley:FSR = on',
                'HiddenValley:fragment = on',
                # flavors used for the running
                'HiddenValley:nFlav = {nflv}'.format(nflv = 7 if self.mode == 'unflavored' else 3),
                # implements arXiv:1803.08080
                'HiddenValley:altHadronSpecies = {flag}'.format(flag = 'off' if self.mode == 'unflavored' else 'on'),
                'HiddenValley:spinFv = 0',    # Spin of bi-fundamental res.
                'HiddenValley:Lambda = {0}'.format(2 * self.mDark),
                'HiddenValley:pTminFSR = {ptmin}'.format(ptmin=2.2 * self.mDark),
                '4900101:m0 = {mass}'.format(mass=2 * self.mDark),
            ]
        )

        if self.mode == "unflavored" and self.channel == "s":
            lines.extend(
                [
                    '4900023:m0 = {mMed}'.format(mMed=self.mMed),
                    '4900023:mWidth = 0.01',  # Width of the Z' boson
                    '4900023:oneChannel = 1 0.982 102 4900101 -4900101',
                    '4900023:addChannel = 1 0.003 102 1 -1', 
                    '4900023:addChannel = 1 0.003 102 2 -2',
                    '4900023:addChannel = 1 0.003 102 3 -3',
                    '4900023:addChannel = 1 0.003 102 4 -4',
                    '4900023:addChannel = 1 0.003 102 5 -5',
                    '4900023:addChannel = 1 0.003 102 6 -6',
                ]
            )
    
        lines.extend(self.MakeRes())
        lines.extend(self.MakeDecay())
        return lines

    def MakeRes(self):
        lines = [
            # Mass of bi-fundamental resonance
            '4900001:m0 = {mass}'.format(mass=self.mMed),
            # Width of bi-fundamental resonance
            '4900001:mWidth = 10',
            # Other resonance masses are set to unreachable limits
            '4900002:m0 = 50000',
            '4900003:m0 = 50000',
            '4900004:m0 = 50000',
            '4900005:m0 = 50000',
            '4900006:m0 = 50000',
        ]

        if self.mode == 'unflavored':
            pass
        else:
            dark_list = [4900101, 4900102, 4900103]
            for sm_idx, sm_quark in enumerate(self.sm_id):
                for d_idx, dark_quark in enumerate(dark_list):
                    lines.append(
                        '4900001:{mode}Channel = 1 {rate} 103 {smq} {dq}'.format(
                            mode='one' if sm_idx == d_idx and sm_idx == 0 else 'add',
                            smq=sm_quark,
                            dq=dark_quark,
                            rate=self.kappa.item((d_idx, sm_idx))**2 / self.kNorm,
                        )
                    )
        return lines

    def MakeDecay(self):
        def gamma(dark_comp1, dark_comp2):
            return sum([
                self.calc_gamma(dark_comp1, dark_comp2, i, j)
                for i in range(0, 3)
                for j in range(i, 3)
            ])

        def extend_decay(dark_meson, dark_comp1, dark_comp2):
            # Physical constants
            hbarc = 1.97e-13    # in GeV mm

            ans = [
                '{dark_meson}:m0 = {mass}'.format(dark_meson=dark_meson, mass=self.mDark)
            ]
            gamma_sum = gamma(dark_comp1, dark_comp2)
            if gamma_sum > 0:
                ans.append('{dark_meson}:tau0 = {lifetime}'.format(
                    dark_meson=dark_meson, lifetime=hbarc / gamma_sum))
                ans.extend([
                    '{dark_meson}:{set}Channel = 1 {rate} 91 {sm1} -{sm2}'.format(
                        dark_meson=dark_meson,
                        set='one' if i == 0 and j == 0 else 'add',
                        sm1=self.sm_id[i],
                        sm2=self.sm_id[j],
                        rate=self.calc_gamma(dark_comp1, dark_comp2, i, j) / gamma_sum)
                    for i in range(3)
                    for j in range(i, 3)
                ])
            return ans
        
        decay_settings = []

        if self.mode == 'unflavored':    # Special case for unflavored decay
            smid = 1 if self.type == 'down' else 2
            decay_settings.extend(
                [
                    '4900111:m0 = {mass}'.format(mass=self.mDark),
                    '4900211:m0 = {mass}'.format(mass=self.mDark),
                    '4900111:tau0 = {lifetime}'.format(lifetime=self.kappa0),
                    '4900211:tau0 = {lifetime}'.format(lifetime=self.kappa0),
                    '4900113:m0 = {mass}'.format(mass=4 * self.mDark),
                    '4900213:m0 = {mass}'.format(mass=4 * self.mDark),
                    '4900111:0:all      =  1 1.000  91     {id}     -{id}'.format(id=smid),
                    '4900113:0:all      =  1 0.999  91  4900111   4900111',
                    '4900113:addchannel =  1 0.001  91     {id}     -{id}'.format(id=smid),
                    '4900211:oneChannel =  1 1.000  91     {id}     -{id}'.format(id=smid),
                    '4900213:oneChannel =  1 0.999  91  4900211   4900211',
                    '4900213:addchannel =  1 0.001  91     {id}     -{id}'.format(id=smid),
                ]
            )
            return decay_settings
        elif self.mode == 'aligned':
            # PDG ID should match with hidden valley definition
            # https://github.com/cms-svj/pythia8/tree/emj/306

            if self.channel == "s":
                raise ValueError("Option for mode {} not compatible with channel option {}".format(self.mode, self.channel))

            # Defining some missing antiparticles
            meson_decay = [
                '4900111:antiName = pivDiagbar',
                '4900113:antiName = rhovDiagbar',
            ]
            meson_decay.extend(extend_decay(4900113, 0, 1))
            meson_decay.extend(extend_decay(4900211, 0, 2))
            meson_decay.extend(extend_decay(4900213, 1, 2))

            # Neutral PI is the same-flavor one
            neutral_pi_gamma = [gamma(i, i) for i in range(3)]
            pi_comp = neutral_pi_gamma.index(max(neutral_pi_gamma))
            meson_decay.extend(extend_decay(4900111, pi_comp, pi_comp))

            return meson_decay
        else:
            # Dummy return statement
            return []

if __name__ == "__main__":
    import argparse, re
    helper = emjHelper()

    parser = argparse.ArgumentParser('Calculation debugging for Emerging jets pythia settings')
    parser.add_argument('--mMed', default=1000, type=float, help='Dark mediator mass [GeV]')
    parser.add_argument('--kappa', default=1, type=float, help='Kappa0 squared (factor to scale decay lifetime)')
    parser.add_argument('--mDark', default=10, type=float, help='Dark meson mass [GeV]')
    parser.add_argument('--type', default='down', type=str, choices=['down', 'up'], help='Alignment to SM up/down type SM quarks')
    parser.add_argument('--mode', default='aligned', type=str, choices=['aligned', 'unflavored'], help='Mixing scenarios to simulate')
    parser.add_argument('--channel', default='t', type=str, choices=['t', 's'], help='Channels to simulate')
    parser.add_argument('cmd', type=str, choices=['dumptime','dumpcard'], help='action to perform')

    args = parser.parse_args()

    if args.cmd == 'dumptime':
        for mDark in np.linspace(1.6, 100, 1000, endpoint=True):
            helper.setModel(args.channel, args.mMed, mDark, args.kappa, args.mode, args.type)
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
        helper.setModel(args.channel, args.mMed, args.mDark, args.kappa, args.mode, args.type)
        for line in helper.getPythiaSettings():
            print(line)

