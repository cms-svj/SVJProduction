# This file was automatically created by FeynRules 2.3.28
# Mathematica version: 11.0.0 for Mac OS X x86 (64-bit) (July 28, 2016)
# Date: Tue 6 Jun 2017 18:37:13


from object_library import all_decays, Decay
import particles as P


Decay_b = Decay(name = 'Decay_b',
                particle = P.b,
                partial_widths = {(P.sb11,P.gv11):'((3*ls**2*MB**2 + 3*ls**2*Mgv11**2 - 3*ls**2*Msb11**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv11**2 + Mgv11**4 - 2*MB**2*Msb11**2 - 2*Mgv11**2*Msb11**2 + Msb11**4))/(96.*cmath.pi*abs(MB)**3)',
                                  (P.sb12,P.gv12):'((3*ls**2*MB**2 + 3*ls**2*Mgv12**2 - 3*ls**2*Msb12**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv12**2 + Mgv12**4 - 2*MB**2*Msb12**2 - 2*Mgv12**2*Msb12**2 + Msb12**4))/(96.*cmath.pi*abs(MB)**3)',
                                  (P.sb21,P.gv21):'((3*ls**2*MB**2 + 3*ls**2*Mgv21**2 - 3*ls**2*Msb21**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv21**2 + Mgv21**4 - 2*MB**2*Msb21**2 - 2*Mgv21**2*Msb21**2 + Msb21**4))/(96.*cmath.pi*abs(MB)**3)',
                                  (P.sb22,P.gv22):'((3*ls**2*MB**2 + 3*ls**2*Mgv22**2 - 3*ls**2*Msb22**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv22**2 + Mgv22**4 - 2*MB**2*Msb22**2 - 2*Mgv22**2*Msb22**2 + Msb22**4))/(96.*cmath.pi*abs(MB)**3)',
                                  (P.W__minus__,P.t):'(((3*ee**2*MB**2)/(2.*sw**2) + (3*ee**2*MT**2)/(2.*sw**2) + (3*ee**2*MB**4)/(2.*MW**2*sw**2) - (3*ee**2*MB**2*MT**2)/(MW**2*sw**2) + (3*ee**2*MT**4)/(2.*MW**2*sw**2) - (3*ee**2*MW**2)/sw**2)*cmath.sqrt(MB**4 - 2*MB**2*MT**2 + MT**4 - 2*MB**2*MW**2 - 2*MT**2*MW**2 + MW**4))/(96.*cmath.pi*abs(MB)**3)'})

Decay_gv11 = Decay(name = 'Decay_gv11',
                   particle = P.gv11,
                   partial_widths = {(P.sb11__tilde__,P.b):'((3*ls**2*MB**2 + 3*ls**2*Mgv11**2 - 3*ls**2*Msb11**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv11**2 + Mgv11**4 - 2*MB**2*Msb11**2 - 2*Mgv11**2*Msb11**2 + Msb11**4))/(32.*cmath.pi*abs(Mgv11)**3)',
                                     (P.sc11__tilde__,P.c):'((Mgv11**2 - Msc11**2)*(3*ls**2*Mgv11**2 - 3*ls**2*Msc11**2))/(32.*cmath.pi*abs(Mgv11)**3)',
                                     (P.sd11__tilde__,P.d):'((Mgv11**2 - Msd11**2)*(3*ls**2*Mgv11**2 - 3*ls**2*Msd11**2))/(32.*cmath.pi*abs(Mgv11)**3)',
                                     (P.ss11__tilde__,P.s):'((Mgv11**2 - Mss11**2)*(3*ls**2*Mgv11**2 - 3*ls**2*Mss11**2))/(32.*cmath.pi*abs(Mgv11)**3)',
                                     (P.st11__tilde__,P.t):'((3*ls**2*Mgv11**2 - 3*ls**2*Mst11**2 + 3*ls**2*MT**2)*cmath.sqrt(Mgv11**4 - 2*Mgv11**2*Mst11**2 + Mst11**4 - 2*Mgv11**2*MT**2 - 2*Mst11**2*MT**2 + MT**4))/(32.*cmath.pi*abs(Mgv11)**3)',
                                     (P.su11__tilde__,P.u):'((Mgv11**2 - Msu11**2)*(3*ls**2*Mgv11**2 - 3*ls**2*Msu11**2))/(32.*cmath.pi*abs(Mgv11)**3)'})

Decay_gv12 = Decay(name = 'Decay_gv12',
                   particle = P.gv12,
                   partial_widths = {(P.sb12__tilde__,P.b):'((3*ls**2*MB**2 + 3*ls**2*Mgv12**2 - 3*ls**2*Msb12**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv12**2 + Mgv12**4 - 2*MB**2*Msb12**2 - 2*Mgv12**2*Msb12**2 + Msb12**4))/(32.*cmath.pi*abs(Mgv12)**3)',
                                     (P.sc12__tilde__,P.c):'((Mgv12**2 - Msc12**2)*(3*ls**2*Mgv12**2 - 3*ls**2*Msc12**2))/(32.*cmath.pi*abs(Mgv12)**3)',
                                     (P.sd12__tilde__,P.d):'((Mgv12**2 - Msd12**2)*(3*ls**2*Mgv12**2 - 3*ls**2*Msd12**2))/(32.*cmath.pi*abs(Mgv12)**3)',
                                     (P.ss12__tilde__,P.s):'((Mgv12**2 - Mss12**2)*(3*ls**2*Mgv12**2 - 3*ls**2*Mss12**2))/(32.*cmath.pi*abs(Mgv12)**3)',
                                     (P.st12__tilde__,P.t):'((3*ls**2*Mgv12**2 - 3*ls**2*Mst12**2 + 3*ls**2*MT**2)*cmath.sqrt(Mgv12**4 - 2*Mgv12**2*Mst12**2 + Mst12**4 - 2*Mgv12**2*MT**2 - 2*Mst12**2*MT**2 + MT**4))/(32.*cmath.pi*abs(Mgv12)**3)',
                                     (P.su12__tilde__,P.u):'((Mgv12**2 - Msu12**2)*(3*ls**2*Mgv12**2 - 3*ls**2*Msu12**2))/(32.*cmath.pi*abs(Mgv12)**3)'})

Decay_gv21 = Decay(name = 'Decay_gv21',
                   particle = P.gv21,
                   partial_widths = {(P.sb21__tilde__,P.b):'((3*ls**2*MB**2 + 3*ls**2*Mgv21**2 - 3*ls**2*Msb21**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv21**2 + Mgv21**4 - 2*MB**2*Msb21**2 - 2*Mgv21**2*Msb21**2 + Msb21**4))/(32.*cmath.pi*abs(Mgv21)**3)',
                                     (P.sc21__tilde__,P.c):'((Mgv21**2 - Msc21**2)*(3*ls**2*Mgv21**2 - 3*ls**2*Msc21**2))/(32.*cmath.pi*abs(Mgv21)**3)',
                                     (P.sd21__tilde__,P.d):'((Mgv21**2 - Msd21**2)*(3*ls**2*Mgv21**2 - 3*ls**2*Msd21**2))/(32.*cmath.pi*abs(Mgv21)**3)',
                                     (P.ss21__tilde__,P.s):'((Mgv21**2 - Mss21**2)*(3*ls**2*Mgv21**2 - 3*ls**2*Mss21**2))/(32.*cmath.pi*abs(Mgv21)**3)',
                                     (P.st21__tilde__,P.t):'((3*ls**2*Mgv21**2 - 3*ls**2*Mst21**2 + 3*ls**2*MT**2)*cmath.sqrt(Mgv21**4 - 2*Mgv21**2*Mst21**2 + Mst21**4 - 2*Mgv21**2*MT**2 - 2*Mst21**2*MT**2 + MT**4))/(32.*cmath.pi*abs(Mgv21)**3)',
                                     (P.su21__tilde__,P.u):'((Mgv21**2 - Msu21**2)*(3*ls**2*Mgv21**2 - 3*ls**2*Msu21**2))/(32.*cmath.pi*abs(Mgv21)**3)'})

Decay_gv22 = Decay(name = 'Decay_gv22',
                   particle = P.gv22,
                   partial_widths = {(P.sb22__tilde__,P.b):'((3*ls**2*MB**2 + 3*ls**2*Mgv22**2 - 3*ls**2*Msb22**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv22**2 + Mgv22**4 - 2*MB**2*Msb22**2 - 2*Mgv22**2*Msb22**2 + Msb22**4))/(32.*cmath.pi*abs(Mgv22)**3)',
                                     (P.sc22__tilde__,P.c):'((Mgv22**2 - Msc22**2)*(3*ls**2*Mgv22**2 - 3*ls**2*Msc22**2))/(32.*cmath.pi*abs(Mgv22)**3)',
                                     (P.sd22__tilde__,P.d):'((Mgv22**2 - Msd22**2)*(3*ls**2*Mgv22**2 - 3*ls**2*Msd22**2))/(32.*cmath.pi*abs(Mgv22)**3)',
                                     (P.ss22__tilde__,P.s):'((Mgv22**2 - Mss22**2)*(3*ls**2*Mgv22**2 - 3*ls**2*Mss22**2))/(32.*cmath.pi*abs(Mgv22)**3)',
                                     (P.st22__tilde__,P.t):'((3*ls**2*Mgv22**2 - 3*ls**2*Mst22**2 + 3*ls**2*MT**2)*cmath.sqrt(Mgv22**4 - 2*Mgv22**2*Mst22**2 + Mst22**4 - 2*Mgv22**2*MT**2 - 2*Mst22**2*MT**2 + MT**4))/(32.*cmath.pi*abs(Mgv22)**3)',
                                     (P.su22__tilde__,P.u):'((Mgv22**2 - Msu22**2)*(3*ls**2*Mgv22**2 - 3*ls**2*Msu22**2))/(32.*cmath.pi*abs(Mgv22)**3)'})

Decay_H = Decay(name = 'Decay_H',
                particle = P.H,
                partial_widths = {(P.b,P.b__tilde__):'((-12*MB**2*yb**2 + 3*MH**2*yb**2)*cmath.sqrt(-4*MB**2*MH**2 + MH**4))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.t,P.t__tilde__):'((3*MH**2*yt**2 - 12*MT**2*yt**2)*cmath.sqrt(MH**4 - 4*MH**2*MT**2))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.ta__minus__,P.ta__plus__):'((MH**2*ytau**2 - 4*MTA**2*ytau**2)*cmath.sqrt(MH**4 - 4*MH**2*MTA**2))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.W__minus__,P.W__plus__):'(((3*ee**4*vev**2)/(4.*sw**4) + (ee**4*MH**4*vev**2)/(16.*MW**4*sw**4) - (ee**4*MH**2*vev**2)/(4.*MW**2*sw**4))*cmath.sqrt(MH**4 - 4*MH**2*MW**2))/(16.*cmath.pi*abs(MH)**3)',
                                  (P.Z,P.Z):'(((9*ee**4*vev**2)/2. + (3*ee**4*MH**4*vev**2)/(8.*MZ**4) - (3*ee**4*MH**2*vev**2)/(2.*MZ**2) + (3*cw**4*ee**4*vev**2)/(4.*sw**4) + (cw**4*ee**4*MH**4*vev**2)/(16.*MZ**4*sw**4) - (cw**4*ee**4*MH**2*vev**2)/(4.*MZ**2*sw**4) + (3*cw**2*ee**4*vev**2)/sw**2 + (cw**2*ee**4*MH**4*vev**2)/(4.*MZ**4*sw**2) - (cw**2*ee**4*MH**2*vev**2)/(MZ**2*sw**2) + (3*ee**4*sw**2*vev**2)/cw**2 + (ee**4*MH**4*sw**2*vev**2)/(4.*cw**2*MZ**4) - (ee**4*MH**2*sw**2*vev**2)/(cw**2*MZ**2) + (3*ee**4*sw**4*vev**2)/(4.*cw**4) + (ee**4*MH**4*sw**4*vev**2)/(16.*cw**4*MZ**4) - (ee**4*MH**2*sw**4*vev**2)/(4.*cw**4*MZ**2))*cmath.sqrt(MH**4 - 4*MH**2*MZ**2))/(32.*cmath.pi*abs(MH)**3)'})

Decay_sb11 = Decay(name = 'Decay_sb11',
                   particle = P.sb11,
                   partial_widths = {(P.b,P.gv11__tilde__):'((-3*ls**2*MB**2 - 3*ls**2*Mgv11**2 + 3*ls**2*Msb11**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv11**2 + Mgv11**4 - 2*MB**2*Msb11**2 - 2*Mgv11**2*Msb11**2 + Msb11**4))/(48.*cmath.pi*abs(Msb11)**3)'})

Decay_sb12 = Decay(name = 'Decay_sb12',
                   particle = P.sb12,
                   partial_widths = {(P.b,P.gv12__tilde__):'((-3*ls**2*MB**2 - 3*ls**2*Mgv12**2 + 3*ls**2*Msb12**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv12**2 + Mgv12**4 - 2*MB**2*Msb12**2 - 2*Mgv12**2*Msb12**2 + Msb12**4))/(48.*cmath.pi*abs(Msb12)**3)'})

Decay_sb21 = Decay(name = 'Decay_sb21',
                   particle = P.sb21,
                   partial_widths = {(P.b,P.gv21__tilde__):'((-3*ls**2*MB**2 - 3*ls**2*Mgv21**2 + 3*ls**2*Msb21**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv21**2 + Mgv21**4 - 2*MB**2*Msb21**2 - 2*Mgv21**2*Msb21**2 + Msb21**4))/(48.*cmath.pi*abs(Msb21)**3)'})

Decay_sb22 = Decay(name = 'Decay_sb22',
                   particle = P.sb22,
                   partial_widths = {(P.b,P.gv22__tilde__):'((-3*ls**2*MB**2 - 3*ls**2*Mgv22**2 + 3*ls**2*Msb22**2)*cmath.sqrt(MB**4 - 2*MB**2*Mgv22**2 + Mgv22**4 - 2*MB**2*Msb22**2 - 2*Mgv22**2*Msb22**2 + Msb22**4))/(48.*cmath.pi*abs(Msb22)**3)'})

Decay_sc11 = Decay(name = 'Decay_sc11',
                   particle = P.sc11,
                   partial_widths = {(P.c,P.gv11__tilde__):'((-Mgv11**2 + Msc11**2)*(-3*ls**2*Mgv11**2 + 3*ls**2*Msc11**2))/(48.*cmath.pi*abs(Msc11)**3)'})

Decay_sc12 = Decay(name = 'Decay_sc12',
                   particle = P.sc12,
                   partial_widths = {(P.c,P.gv12__tilde__):'((-Mgv12**2 + Msc12**2)*(-3*ls**2*Mgv12**2 + 3*ls**2*Msc12**2))/(48.*cmath.pi*abs(Msc12)**3)'})

Decay_sc21 = Decay(name = 'Decay_sc21',
                   particle = P.sc21,
                   partial_widths = {(P.c,P.gv21__tilde__):'((-Mgv21**2 + Msc21**2)*(-3*ls**2*Mgv21**2 + 3*ls**2*Msc21**2))/(48.*cmath.pi*abs(Msc21)**3)'})

Decay_sc22 = Decay(name = 'Decay_sc22',
                   particle = P.sc22,
                   partial_widths = {(P.c,P.gv22__tilde__):'((-Mgv22**2 + Msc22**2)*(-3*ls**2*Mgv22**2 + 3*ls**2*Msc22**2))/(48.*cmath.pi*abs(Msc22)**3)'})

Decay_sd11 = Decay(name = 'Decay_sd11',
                   particle = P.sd11,
                   partial_widths = {(P.d,P.gv11__tilde__):'((-Mgv11**2 + Msd11**2)*(-3*ls**2*Mgv11**2 + 3*ls**2*Msd11**2))/(48.*cmath.pi*abs(Msd11)**3)'})

Decay_sd12 = Decay(name = 'Decay_sd12',
                   particle = P.sd12,
                   partial_widths = {(P.d,P.gv12__tilde__):'((-Mgv12**2 + Msd12**2)*(-3*ls**2*Mgv12**2 + 3*ls**2*Msd12**2))/(48.*cmath.pi*abs(Msd12)**3)'})

Decay_sd21 = Decay(name = 'Decay_sd21',
                   particle = P.sd21,
                   partial_widths = {(P.d,P.gv21__tilde__):'((-Mgv21**2 + Msd21**2)*(-3*ls**2*Mgv21**2 + 3*ls**2*Msd21**2))/(48.*cmath.pi*abs(Msd21)**3)'})

Decay_sd22 = Decay(name = 'Decay_sd22',
                   particle = P.sd22,
                   partial_widths = {(P.d,P.gv22__tilde__):'((-Mgv22**2 + Msd22**2)*(-3*ls**2*Mgv22**2 + 3*ls**2*Msd22**2))/(48.*cmath.pi*abs(Msd22)**3)'})

Decay_ss11 = Decay(name = 'Decay_ss11',
                   particle = P.ss11,
                   partial_widths = {(P.s,P.gv11__tilde__):'((-Mgv11**2 + Mss11**2)*(-3*ls**2*Mgv11**2 + 3*ls**2*Mss11**2))/(48.*cmath.pi*abs(Mss11)**3)'})

Decay_ss12 = Decay(name = 'Decay_ss12',
                   particle = P.ss12,
                   partial_widths = {(P.s,P.gv12__tilde__):'((-Mgv12**2 + Mss12**2)*(-3*ls**2*Mgv12**2 + 3*ls**2*Mss12**2))/(48.*cmath.pi*abs(Mss12)**3)'})

Decay_ss21 = Decay(name = 'Decay_ss21',
                   particle = P.ss21,
                   partial_widths = {(P.s,P.gv21__tilde__):'((-Mgv21**2 + Mss21**2)*(-3*ls**2*Mgv21**2 + 3*ls**2*Mss21**2))/(48.*cmath.pi*abs(Mss21)**3)'})

Decay_ss22 = Decay(name = 'Decay_ss22',
                   particle = P.ss22,
                   partial_widths = {(P.s,P.gv22__tilde__):'((-Mgv22**2 + Mss22**2)*(-3*ls**2*Mgv22**2 + 3*ls**2*Mss22**2))/(48.*cmath.pi*abs(Mss22)**3)'})

Decay_st11 = Decay(name = 'Decay_st11',
                   particle = P.st11,
                   partial_widths = {(P.t,P.gv11__tilde__):'((-3*ls**2*Mgv11**2 + 3*ls**2*Mst11**2 - 3*ls**2*MT**2)*cmath.sqrt(Mgv11**4 - 2*Mgv11**2*Mst11**2 + Mst11**4 - 2*Mgv11**2*MT**2 - 2*Mst11**2*MT**2 + MT**4))/(48.*cmath.pi*abs(Mst11)**3)'})

Decay_st12 = Decay(name = 'Decay_st12',
                   particle = P.st12,
                   partial_widths = {(P.t,P.gv12__tilde__):'((-3*ls**2*Mgv12**2 + 3*ls**2*Mst12**2 - 3*ls**2*MT**2)*cmath.sqrt(Mgv12**4 - 2*Mgv12**2*Mst12**2 + Mst12**4 - 2*Mgv12**2*MT**2 - 2*Mst12**2*MT**2 + MT**4))/(48.*cmath.pi*abs(Mst12)**3)'})

Decay_st21 = Decay(name = 'Decay_st21',
                   particle = P.st21,
                   partial_widths = {(P.t,P.gv21__tilde__):'((-3*ls**2*Mgv21**2 + 3*ls**2*Mst21**2 - 3*ls**2*MT**2)*cmath.sqrt(Mgv21**4 - 2*Mgv21**2*Mst21**2 + Mst21**4 - 2*Mgv21**2*MT**2 - 2*Mst21**2*MT**2 + MT**4))/(48.*cmath.pi*abs(Mst21)**3)'})

Decay_st22 = Decay(name = 'Decay_st22',
                   particle = P.st22,
                   partial_widths = {(P.t,P.gv22__tilde__):'((-3*ls**2*Mgv22**2 + 3*ls**2*Mst22**2 - 3*ls**2*MT**2)*cmath.sqrt(Mgv22**4 - 2*Mgv22**2*Mst22**2 + Mst22**4 - 2*Mgv22**2*MT**2 - 2*Mst22**2*MT**2 + MT**4))/(48.*cmath.pi*abs(Mst22)**3)'})

Decay_su11 = Decay(name = 'Decay_su11',
                   particle = P.su11,
                   partial_widths = {(P.u,P.gv11__tilde__):'((-Mgv11**2 + Msu11**2)*(-3*ls**2*Mgv11**2 + 3*ls**2*Msu11**2))/(48.*cmath.pi*abs(Msu11)**3)'})

Decay_su12 = Decay(name = 'Decay_su12',
                   particle = P.su12,
                   partial_widths = {(P.u,P.gv12__tilde__):'((-Mgv12**2 + Msu12**2)*(-3*ls**2*Mgv12**2 + 3*ls**2*Msu12**2))/(48.*cmath.pi*abs(Msu12)**3)'})

Decay_su21 = Decay(name = 'Decay_su21',
                   particle = P.su21,
                   partial_widths = {(P.u,P.gv21__tilde__):'((-Mgv21**2 + Msu21**2)*(-3*ls**2*Mgv21**2 + 3*ls**2*Msu21**2))/(48.*cmath.pi*abs(Msu21)**3)'})

Decay_su22 = Decay(name = 'Decay_su22',
                   particle = P.su22,
                   partial_widths = {(P.u,P.gv22__tilde__):'((-Mgv22**2 + Msu22**2)*(-3*ls**2*Mgv22**2 + 3*ls**2*Msu22**2))/(48.*cmath.pi*abs(Msu22)**3)'})

Decay_t = Decay(name = 'Decay_t',
                particle = P.t,
                partial_widths = {(P.st11,P.gv11):'((3*ls**2*Mgv11**2 - 3*ls**2*Mst11**2 + 3*ls**2*MT**2)*cmath.sqrt(Mgv11**4 - 2*Mgv11**2*Mst11**2 + Mst11**4 - 2*Mgv11**2*MT**2 - 2*Mst11**2*MT**2 + MT**4))/(96.*cmath.pi*abs(MT)**3)',
                                  (P.st12,P.gv12):'((3*ls**2*Mgv12**2 - 3*ls**2*Mst12**2 + 3*ls**2*MT**2)*cmath.sqrt(Mgv12**4 - 2*Mgv12**2*Mst12**2 + Mst12**4 - 2*Mgv12**2*MT**2 - 2*Mst12**2*MT**2 + MT**4))/(96.*cmath.pi*abs(MT)**3)',
                                  (P.st21,P.gv21):'((3*ls**2*Mgv21**2 - 3*ls**2*Mst21**2 + 3*ls**2*MT**2)*cmath.sqrt(Mgv21**4 - 2*Mgv21**2*Mst21**2 + Mst21**4 - 2*Mgv21**2*MT**2 - 2*Mst21**2*MT**2 + MT**4))/(96.*cmath.pi*abs(MT)**3)',
                                  (P.st22,P.gv22):'((3*ls**2*Mgv22**2 - 3*ls**2*Mst22**2 + 3*ls**2*MT**2)*cmath.sqrt(Mgv22**4 - 2*Mgv22**2*Mst22**2 + Mst22**4 - 2*Mgv22**2*MT**2 - 2*Mst22**2*MT**2 + MT**4))/(96.*cmath.pi*abs(MT)**3)',
                                  (P.W__plus__,P.b):'(((3*ee**2*MB**2)/(2.*sw**2) + (3*ee**2*MT**2)/(2.*sw**2) + (3*ee**2*MB**4)/(2.*MW**2*sw**2) - (3*ee**2*MB**2*MT**2)/(MW**2*sw**2) + (3*ee**2*MT**4)/(2.*MW**2*sw**2) - (3*ee**2*MW**2)/sw**2)*cmath.sqrt(MB**4 - 2*MB**2*MT**2 + MT**4 - 2*MB**2*MW**2 - 2*MT**2*MW**2 + MW**4))/(96.*cmath.pi*abs(MT)**3)'})

Decay_ta__minus__ = Decay(name = 'Decay_ta__minus__',
                          particle = P.ta__minus__,
                          partial_widths = {(P.W__minus__,P.vt):'((MTA**2 - MW**2)*((ee**2*MTA**2)/(2.*sw**2) + (ee**2*MTA**4)/(2.*MW**2*sw**2) - (ee**2*MW**2)/sw**2))/(32.*cmath.pi*abs(MTA)**3)'})

Decay_W__plus__ = Decay(name = 'Decay_W__plus__',
                        particle = P.W__plus__,
                        partial_widths = {(P.c,P.s__tilde__):'(ee**2*MW**4)/(16.*cmath.pi*sw**2*abs(MW)**3)',
                                          (P.t,P.b__tilde__):'(((-3*ee**2*MB**2)/(2.*sw**2) - (3*ee**2*MT**2)/(2.*sw**2) - (3*ee**2*MB**4)/(2.*MW**2*sw**2) + (3*ee**2*MB**2*MT**2)/(MW**2*sw**2) - (3*ee**2*MT**4)/(2.*MW**2*sw**2) + (3*ee**2*MW**2)/sw**2)*cmath.sqrt(MB**4 - 2*MB**2*MT**2 + MT**4 - 2*MB**2*MW**2 - 2*MT**2*MW**2 + MW**4))/(48.*cmath.pi*abs(MW)**3)',
                                          (P.u,P.d__tilde__):'(ee**2*MW**4)/(16.*cmath.pi*sw**2*abs(MW)**3)',
                                          (P.ve,P.e__plus__):'(ee**2*MW**4)/(48.*cmath.pi*sw**2*abs(MW)**3)',
                                          (P.vm,P.mu__plus__):'(ee**2*MW**4)/(48.*cmath.pi*sw**2*abs(MW)**3)',
                                          (P.vt,P.ta__plus__):'((-MTA**2 + MW**2)*(-(ee**2*MTA**2)/(2.*sw**2) - (ee**2*MTA**4)/(2.*MW**2*sw**2) + (ee**2*MW**2)/sw**2))/(48.*cmath.pi*abs(MW)**3)'})

Decay_Z = Decay(name = 'Decay_Z',
                particle = P.Z,
                partial_widths = {(P.b,P.b__tilde__):'((-7*ee**2*MB**2 + ee**2*MZ**2 - (3*cw**2*ee**2*MB**2)/(2.*sw**2) + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) - (17*ee**2*MB**2*sw**2)/(6.*cw**2) + (5*ee**2*MZ**2*sw**2)/(6.*cw**2))*cmath.sqrt(-4*MB**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.c,P.c__tilde__):'(MZ**2*(-(ee**2*MZ**2) + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (17*ee**2*MZ**2*sw**2)/(6.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.d,P.d__tilde__):'(MZ**2*(ee**2*MZ**2 + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (5*ee**2*MZ**2*sw**2)/(6.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.e__minus__,P.e__plus__):'(MZ**2*(-(ee**2*MZ**2) + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (5*ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.mu__minus__,P.mu__plus__):'(MZ**2*(-(ee**2*MZ**2) + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (5*ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.s,P.s__tilde__):'(MZ**2*(ee**2*MZ**2 + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (5*ee**2*MZ**2*sw**2)/(6.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sb11__tilde__,P.sb11):'(((-4*ee**2*Msb11**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msb11**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sb12__tilde__,P.sb12):'(((-4*ee**2*Msb12**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msb12**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sb21__tilde__,P.sb21):'(((-4*ee**2*Msb21**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msb21**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sb22__tilde__,P.sb22):'(((-4*ee**2*Msb22**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msb22**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sc11__tilde__,P.sc11):'(((-16*ee**2*Msc11**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msc11**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sc12__tilde__,P.sc12):'(((-16*ee**2*Msc12**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msc12**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sc21__tilde__,P.sc21):'(((-16*ee**2*Msc21**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msc21**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sc22__tilde__,P.sc22):'(((-16*ee**2*Msc22**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msc22**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sd11__tilde__,P.sd11):'(((-4*ee**2*Msd11**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msd11**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sd12__tilde__,P.sd12):'(((-4*ee**2*Msd12**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msd12**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sd21__tilde__,P.sd21):'(((-4*ee**2*Msd21**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msd21**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.sd22__tilde__,P.sd22):'(((-4*ee**2*Msd22**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msd22**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.ss11__tilde__,P.ss11):'(((-4*ee**2*Mss11**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Mss11**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.ss12__tilde__,P.ss12):'(((-4*ee**2*Mss12**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Mss12**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.ss21__tilde__,P.ss21):'(((-4*ee**2*Mss21**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Mss21**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.ss22__tilde__,P.ss22):'(((-4*ee**2*Mss22**2*sw**2)/(3.*cw**2) + (ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Mss22**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.st11__tilde__,P.st11):'(((-16*ee**2*Mst11**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Mst11**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.st12__tilde__,P.st12):'(((-16*ee**2*Mst12**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Mst12**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.st21__tilde__,P.st21):'(((-16*ee**2*Mst21**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Mst21**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.st22__tilde__,P.st22):'(((-16*ee**2*Mst22**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Mst22**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.su11__tilde__,P.su11):'(((-16*ee**2*Msu11**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msu11**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.su12__tilde__,P.su12):'(((-16*ee**2*Msu12**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msu12**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.su21__tilde__,P.su21):'(((-16*ee**2*Msu21**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msu21**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.su22__tilde__,P.su22):'(((-16*ee**2*Msu22**2*sw**2)/(3.*cw**2) + (4*ee**2*MZ**2*sw**2)/(3.*cw**2))*cmath.sqrt(-4*Msu22**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.t,P.t__tilde__):'((-11*ee**2*MT**2 - ee**2*MZ**2 - (3*cw**2*ee**2*MT**2)/(2.*sw**2) + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (7*ee**2*MT**2*sw**2)/(6.*cw**2) + (17*ee**2*MZ**2*sw**2)/(6.*cw**2))*cmath.sqrt(-4*MT**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.ta__minus__,P.ta__plus__):'((-5*ee**2*MTA**2 - ee**2*MZ**2 - (cw**2*ee**2*MTA**2)/(2.*sw**2) + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (7*ee**2*MTA**2*sw**2)/(2.*cw**2) + (5*ee**2*MZ**2*sw**2)/(2.*cw**2))*cmath.sqrt(-4*MTA**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.u,P.u__tilde__):'(MZ**2*(-(ee**2*MZ**2) + (3*cw**2*ee**2*MZ**2)/(2.*sw**2) + (17*ee**2*MZ**2*sw**2)/(6.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.ve,P.ve__tilde__):'(MZ**2*(ee**2*MZ**2 + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.vm,P.vm__tilde__):'(MZ**2*(ee**2*MZ**2 + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.vt,P.vt__tilde__):'(MZ**2*(ee**2*MZ**2 + (cw**2*ee**2*MZ**2)/(2.*sw**2) + (ee**2*MZ**2*sw**2)/(2.*cw**2)))/(48.*cmath.pi*abs(MZ)**3)',
                                  (P.W__minus__,P.W__plus__):'(((-12*cw**2*ee**2*MW**2)/sw**2 - (17*cw**2*ee**2*MZ**2)/sw**2 + (4*cw**2*ee**2*MZ**4)/(MW**2*sw**2) + (cw**2*ee**2*MZ**6)/(4.*MW**4*sw**2))*cmath.sqrt(-4*MW**2*MZ**2 + MZ**4))/(48.*cmath.pi*abs(MZ)**3)'})

