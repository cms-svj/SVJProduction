# This file was automatically created by FeynRules 2.3.28
# Mathematica version: 11.0.0 for Mac OS X x86 (64-bit) (July 28, 2016)
# Date: Tue 6 Jun 2017 18:37:13
# THE ARGUMENTS PREFIXED WITH A DOLLAR SIGN ARE PLACEHOLDERS FOR PROPER VALUES.
# THESE CAN BE REPLACED IN PYTHON.



from object_library import all_parameters, Parameter


from function_library import complexconjugate, re, im, csc, sec, acsc, asec, cot

# This is a default parameter object representing 0.
ZERO = Parameter(name = 'ZERO',
                 nature = 'internal',
                 type = 'real',
                 value = '0.0',
                 texname = '0')

# User-defined parameters.
aEWM1 = Parameter(name = 'aEWM1',
                  nature = 'external',
                  type = 'real',
                  value = 127.9,
                  texname = '\\text{aEWM1}',
                  lhablock = 'SMINPUTS',
                  lhacode = [ 1 ])

Gf = Parameter(name = 'Gf',
               nature = 'external',
               type = 'real',
               value = 0.0000116637,
               texname = 'G_f',
               lhablock = 'SMINPUTS',
               lhacode = [ 2 ])

aS = Parameter(name = 'aS',
               nature = 'external',
               type = 'real',
               value = 0.1184,
               texname = '\\alpha _s',
               lhablock = 'SMINPUTS',
               lhacode = [ 3 ])

ymb = Parameter(name = 'ymb',
                nature = 'external',
                type = 'real',
                value = 4.7,
                texname = '\\text{ymb}',
                lhablock = 'YUKAWA',
                lhacode = [ 5 ])

ymt = Parameter(name = 'ymt',
                nature = 'external',
                type = 'real',
                value = 172,
                texname = '\\text{ymt}',
                lhablock = 'YUKAWA',
                lhacode = [ 6 ])

ymtau = Parameter(name = 'ymtau',
                  nature = 'external',
                  type = 'real',
                  value = 1.777,
                  texname = '\\text{ymtau}',
                  lhablock = 'YUKAWA',
                  lhacode = [ 15 ])

ls = Parameter(name = 'ls',
               nature = 'external',
               type = 'real',
               value = 1.,
               texname = 'l_s',
               lhablock = 'FRBlock',
               lhacode = [ 1 ])

MZ = Parameter(name = 'MZ',
               nature = 'external',
               type = 'real',
               value = 91.1876,
               texname = '\\text{MZ}',
               lhablock = 'MASS',
               lhacode = [ 23 ])

MTA = Parameter(name = 'MTA',
                nature = 'external',
                type = 'real',
                value = 1.777,
                texname = '\\text{MTA}',
                lhablock = 'MASS',
                lhacode = [ 15 ])

MT = Parameter(name = 'MT',
               nature = 'external',
               type = 'real',
               value = 172,
               texname = '\\text{MT}',
               lhablock = 'MASS',
               lhacode = [ 6 ])

MB = Parameter(name = 'MB',
               nature = 'external',
               type = 'real',
               value = 4.7,
               texname = '\\text{MB}',
               lhablock = 'MASS',
               lhacode = [ 5 ])

MH = Parameter(name = 'MH',
               nature = 'external',
               type = 'real',
               value = 125,
               texname = '\\text{MH}',
               lhablock = 'MASS',
               lhacode = [ 25 ])

Msd11 = Parameter(name = 'Msd11',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msd11}',
                  lhablock = 'MASS',
                  lhacode = [ 9000005 ])

Msd12 = Parameter(name = 'Msd12',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msd12}',
                  lhablock = 'MASS',
                  lhacode = [ 9000006 ])

Msd21 = Parameter(name = 'Msd21',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msd21}',
                  lhablock = 'MASS',
                  lhacode = [ 9000007 ])

Msd22 = Parameter(name = 'Msd22',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msd22}',
                  lhablock = 'MASS',
                  lhacode = [ 9000008 ])

Mss11 = Parameter(name = 'Mss11',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Mss11}',
                  lhablock = 'MASS',
                  lhacode = [ 9000009 ])

Mss12 = Parameter(name = 'Mss12',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Mss12}',
                  lhablock = 'MASS',
                  lhacode = [ 9000010 ])

Mss21 = Parameter(name = 'Mss21',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Mss21}',
                  lhablock = 'MASS',
                  lhacode = [ 9000011 ])

Mss22 = Parameter(name = 'Mss22',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Mss22}',
                  lhablock = 'MASS',
                  lhacode = [ 9000012 ])

Msb11 = Parameter(name = 'Msb11',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msb11}',
                  lhablock = 'MASS',
                  lhacode = [ 9000013 ])

Msb12 = Parameter(name = 'Msb12',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msb12}',
                  lhablock = 'MASS',
                  lhacode = [ 9000014 ])

Msb21 = Parameter(name = 'Msb21',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msb21}',
                  lhablock = 'MASS',
                  lhacode = [ 9000015 ])

Msb22 = Parameter(name = 'Msb22',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msb22}',
                  lhablock = 'MASS',
                  lhacode = [ 9000016 ])

Msu11 = Parameter(name = 'Msu11',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msu11}',
                  lhablock = 'MASS',
                  lhacode = [ 9000017 ])

Msu12 = Parameter(name = 'Msu12',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msu12}',
                  lhablock = 'MASS',
                  lhacode = [ 9000018 ])

Msu21 = Parameter(name = 'Msu21',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msu21}',
                  lhablock = 'MASS',
                  lhacode = [ 9000019 ])

Msu22 = Parameter(name = 'Msu22',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msu22}',
                  lhablock = 'MASS',
                  lhacode = [ 9000020 ])

Msc11 = Parameter(name = 'Msc11',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msc11}',
                  lhablock = 'MASS',
                  lhacode = [ 9000021 ])

Msc12 = Parameter(name = 'Msc12',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msc12}',
                  lhablock = 'MASS',
                  lhacode = [ 9000022 ])

Msc21 = Parameter(name = 'Msc21',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msc21}',
                  lhablock = 'MASS',
                  lhacode = [ 9000023 ])

Msc22 = Parameter(name = 'Msc22',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Msc22}',
                  lhablock = 'MASS',
                  lhacode = [ 9000024 ])

Mst11 = Parameter(name = 'Mst11',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Mst11}',
                  lhablock = 'MASS',
                  lhacode = [ 9000025 ])

Mst12 = Parameter(name = 'Mst12',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Mst12}',
                  lhablock = 'MASS',
                  lhacode = [ 9000026 ])

Mst21 = Parameter(name = 'Mst21',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Mst21}',
                  lhablock = 'MASS',
                  lhacode = [ 9000027 ])

Mst22 = Parameter(name = 'Mst22',
                  nature = 'external',
                  type = 'real',
                  value = $mediator_mass,
                  texname = '\\text{Mst22}',
                  lhablock = 'MASS',
                  lhacode = [ 9000028 ])

Mgv11 = Parameter(name = 'Mgv11',
                  nature = 'external',
                  type = 'real',
                  value = $dark_quark_mass,
                  texname = '\\text{Mgv11}',
                  lhablock = 'MASS',
                  lhacode = [ 49001011 ])

Mgv12 = Parameter(name = 'Mgv12',
                  nature = 'external',
                  type = 'real',
                  value = $dark_quark_mass,
                  texname = '\\text{Mgv12}',
                  lhablock = 'MASS',
                  lhacode = [ 49001012 ])

Mgv21 = Parameter(name = 'Mgv21',
                  nature = 'external',
                  type = 'real',
                  value = $dark_quark_mass,
                  texname = '\\text{Mgv21}',
                  lhablock = 'MASS',
                  lhacode = [ 49001013 ])

Mgv22 = Parameter(name = 'Mgv22',
                  nature = 'external',
                  type = 'real',
                  value = $dark_quark_mass,
                  texname = '\\text{Mgv22}',
                  lhablock = 'MASS',
                  lhacode = [ 49001014 ])

WZ = Parameter(name = 'WZ',
               nature = 'external',
               type = 'real',
               value = 2.4952,
               texname = '\\text{WZ}',
               lhablock = 'DECAY',
               lhacode = [ 23 ])

WW = Parameter(name = 'WW',
               nature = 'external',
               type = 'real',
               value = 2.085,
               texname = '\\text{WW}',
               lhablock = 'DECAY',
               lhacode = [ 24 ])

WT = Parameter(name = 'WT',
               nature = 'external',
               type = 'real',
               value = 1.50833649,
               texname = '\\text{WT}',
               lhablock = 'DECAY',
               lhacode = [ 6 ])

WH = Parameter(name = 'WH',
               nature = 'external',
               type = 'real',
               value = 0.00407,
               texname = '\\text{WH}',
               lhablock = 'DECAY',
               lhacode = [ 25 ])

MWsd11 = Parameter(name = 'MWsd11',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsd11}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000005 ])

MWsd12 = Parameter(name = 'MWsd12',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsd12}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000006 ])

MWsd21 = Parameter(name = 'MWsd21',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsd21}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000007 ])

MWsd22 = Parameter(name = 'MWsd22',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsd22}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000008 ])

MWss11 = Parameter(name = 'MWss11',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWss11}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000009 ])

MWss12 = Parameter(name = 'MWss12',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWss12}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000010 ])

MWss21 = Parameter(name = 'MWss21',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWss21}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000011 ])

MWss22 = Parameter(name = 'MWss22',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWss22}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000012 ])

MWsb11 = Parameter(name = 'MWsb11',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsb11}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000013 ])

MWsb12 = Parameter(name = 'MWsb12',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsb12}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000014 ])

MWsb21 = Parameter(name = 'MWsb21',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsb21}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000015 ])

MWsb22 = Parameter(name = 'MWsb22',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsb22}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000016 ])

MWsu11 = Parameter(name = 'MWsu11',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsu11}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000017 ])

MWsu12 = Parameter(name = 'MWsu12',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsu12}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000018 ])

MWsu21 = Parameter(name = 'MWsu21',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsu21}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000019 ])

MWsu22 = Parameter(name = 'MWsu22',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsu22}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000020 ])

MWsc11 = Parameter(name = 'MWsc11',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsc11}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000021 ])

MWsc12 = Parameter(name = 'MWsc12',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsc12}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000022 ])

MWsc21 = Parameter(name = 'MWsc21',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsc21}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000023 ])

MWsc22 = Parameter(name = 'MWsc22',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWsc22}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000024 ])

MWst11 = Parameter(name = 'MWst11',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWst11}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000025 ])

MWst12 = Parameter(name = 'MWst12',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWst12}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000026 ])

MWst21 = Parameter(name = 'MWst21',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWst21}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000027 ])

MWst22 = Parameter(name = 'MWst22',
                   nature = 'external',
                   type = 'real',
                   value = 1,
                   texname = '\\text{MWst22}',
                   lhablock = 'DECAY',
                   lhacode = [ 9000028 ])

aEW = Parameter(name = 'aEW',
                nature = 'internal',
                type = 'real',
                value = '1/aEWM1',
                texname = '\\alpha _{\\text{EW}}')

G = Parameter(name = 'G',
              nature = 'internal',
              type = 'real',
              value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)',
              texname = 'G')

MW = Parameter(name = 'MW',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(MZ**2/2. + cmath.sqrt(MZ**4/4. - (aEW*cmath.pi*MZ**2)/(Gf*cmath.sqrt(2))))',
               texname = 'M_W')

ee = Parameter(name = 'ee',
               nature = 'internal',
               type = 'real',
               value = '2*cmath.sqrt(aEW)*cmath.sqrt(cmath.pi)',
               texname = 'e')

sw2 = Parameter(name = 'sw2',
                nature = 'internal',
                type = 'real',
                value = '1 - MW**2/MZ**2',
                texname = '\\text{sw2}')

cw = Parameter(name = 'cw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(1 - sw2)',
               texname = 'c_w')

sw = Parameter(name = 'sw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(sw2)',
               texname = 's_w')

g1 = Parameter(name = 'g1',
               nature = 'internal',
               type = 'real',
               value = 'ee/cw',
               texname = 'g_1')

gw = Parameter(name = 'gw',
               nature = 'internal',
               type = 'real',
               value = 'ee/sw',
               texname = 'g_w')

vev = Parameter(name = 'vev',
                nature = 'internal',
                type = 'real',
                value = '(2*MW*sw)/ee',
                texname = '\\text{vev}')

lam = Parameter(name = 'lam',
                nature = 'internal',
                type = 'real',
                value = 'MH**2/(2.*vev**2)',
                texname = '\\text{lam}')

yb = Parameter(name = 'yb',
               nature = 'internal',
               type = 'real',
               value = '(ymb*cmath.sqrt(2))/vev',
               texname = '\\text{yb}')

yt = Parameter(name = 'yt',
               nature = 'internal',
               type = 'real',
               value = '(ymt*cmath.sqrt(2))/vev',
               texname = '\\text{yt}')

ytau = Parameter(name = 'ytau',
                 nature = 'internal',
                 type = 'real',
                 value = '(ymtau*cmath.sqrt(2))/vev',
                 texname = '\\text{ytau}')

muH = Parameter(name = 'muH',
                nature = 'internal',
                type = 'real',
                value = 'cmath.sqrt(lam*vev**2)',
                texname = '\\mu')

