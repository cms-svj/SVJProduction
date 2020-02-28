# This file was automatically created by FeynRules 2.3.28
# Mathematica version: 11.0.0 for Mac OS X x86 (64-bit) (July 28, 2016)
# Date: Tue 6 Jun 2017 18:37:13


from __future__ import division
from object_library import all_particles, Particle
import parameters as Param

import propagators as Prop

a = Particle(pdg_code = 22,
             name = 'a',
             antiname = 'a',
             spin = 3,
             color = 1,
             mass = Param.ZERO,
             width = Param.ZERO,
             texname = 'a',
             antitexname = 'a',
             charge = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

Z = Particle(pdg_code = 23,
             name = 'Z',
             antiname = 'Z',
             spin = 3,
             color = 1,
             mass = Param.MZ,
             width = Param.WZ,
             texname = 'Z',
             antitexname = 'Z',
             charge = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

W__plus__ = Particle(pdg_code = 24,
                     name = 'W+',
                     antiname = 'W-',
                     spin = 3,
                     color = 1,
                     mass = Param.MW,
                     width = Param.WW,
                     texname = 'W+',
                     antitexname = 'W-',
                     charge = 1,
                     GhostNumber = 0,
                     LeptonNumber = 0,
                     Y = 0)

W__minus__ = W__plus__.anti()

g = Particle(pdg_code = 21,
             name = 'g',
             antiname = 'g',
             spin = 3,
             color = 8,
             mass = Param.ZERO,
             width = Param.ZERO,
             texname = 'g',
             antitexname = 'g',
             charge = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

ghA = Particle(pdg_code = 9000001,
               name = 'ghA',
               antiname = 'ghA~',
               spin = -1,
               color = 1,
               mass = Param.ZERO,
               width = Param.ZERO,
               texname = 'ghA',
               antitexname = 'ghA~',
               charge = 0,
               GhostNumber = 1,
               LeptonNumber = 0,
               Y = 0)

ghA__tilde__ = ghA.anti()

ghZ = Particle(pdg_code = 9000002,
               name = 'ghZ',
               antiname = 'ghZ~',
               spin = -1,
               color = 1,
               mass = Param.MZ,
               width = Param.WZ,
               texname = 'ghZ',
               antitexname = 'ghZ~',
               charge = 0,
               GhostNumber = 1,
               LeptonNumber = 0,
               Y = 0)

ghZ__tilde__ = ghZ.anti()

ghWp = Particle(pdg_code = 9000003,
                name = 'ghWp',
                antiname = 'ghWp~',
                spin = -1,
                color = 1,
                mass = Param.MW,
                width = Param.WW,
                texname = 'ghWp',
                antitexname = 'ghWp~',
                charge = 1,
                GhostNumber = 1,
                LeptonNumber = 0,
                Y = 0)

ghWp__tilde__ = ghWp.anti()

ghWm = Particle(pdg_code = 9000004,
                name = 'ghWm',
                antiname = 'ghWm~',
                spin = -1,
                color = 1,
                mass = Param.MW,
                width = Param.WW,
                texname = 'ghWm',
                antitexname = 'ghWm~',
                charge = -1,
                GhostNumber = 1,
                LeptonNumber = 0,
                Y = 0)

ghWm__tilde__ = ghWm.anti()

ghG = Particle(pdg_code = 82,
               name = 'ghG',
               antiname = 'ghG~',
               spin = -1,
               color = 8,
               mass = Param.ZERO,
               width = Param.ZERO,
               texname = 'ghG',
               antitexname = 'ghG~',
               charge = 0,
               GhostNumber = 1,
               LeptonNumber = 0,
               Y = 0)

ghG__tilde__ = ghG.anti()

ve = Particle(pdg_code = 12,
              name = 've',
              antiname = 've~',
              spin = 2,
              color = 1,
              mass = Param.ZERO,
              width = Param.ZERO,
              texname = 've',
              antitexname = 've~',
              charge = 0,
              GhostNumber = 0,
              LeptonNumber = 1,
              Y = 0)

ve__tilde__ = ve.anti()

vm = Particle(pdg_code = 14,
              name = 'vm',
              antiname = 'vm~',
              spin = 2,
              color = 1,
              mass = Param.ZERO,
              width = Param.ZERO,
              texname = 'vm',
              antitexname = 'vm~',
              charge = 0,
              GhostNumber = 0,
              LeptonNumber = 1,
              Y = 0)

vm__tilde__ = vm.anti()

vt = Particle(pdg_code = 16,
              name = 'vt',
              antiname = 'vt~',
              spin = 2,
              color = 1,
              mass = Param.ZERO,
              width = Param.ZERO,
              texname = 'vt',
              antitexname = 'vt~',
              charge = 0,
              GhostNumber = 0,
              LeptonNumber = 1,
              Y = 0)

vt__tilde__ = vt.anti()

e__minus__ = Particle(pdg_code = 11,
                      name = 'e-',
                      antiname = 'e+',
                      spin = 2,
                      color = 1,
                      mass = Param.ZERO,
                      width = Param.ZERO,
                      texname = 'e-',
                      antitexname = 'e+',
                      charge = -1,
                      GhostNumber = 0,
                      LeptonNumber = 1,
                      Y = 0)

e__plus__ = e__minus__.anti()

mu__minus__ = Particle(pdg_code = 13,
                       name = 'mu-',
                       antiname = 'mu+',
                       spin = 2,
                       color = 1,
                       mass = Param.ZERO,
                       width = Param.ZERO,
                       texname = 'mu-',
                       antitexname = 'mu+',
                       charge = -1,
                       GhostNumber = 0,
                       LeptonNumber = 1,
                       Y = 0)

mu__plus__ = mu__minus__.anti()

ta__minus__ = Particle(pdg_code = 15,
                       name = 'ta-',
                       antiname = 'ta+',
                       spin = 2,
                       color = 1,
                       mass = Param.MTA,
                       width = Param.ZERO,
                       texname = 'ta-',
                       antitexname = 'ta+',
                       charge = -1,
                       GhostNumber = 0,
                       LeptonNumber = 1,
                       Y = 0)

ta__plus__ = ta__minus__.anti()

u = Particle(pdg_code = 2,
             name = 'u',
             antiname = 'u~',
             spin = 2,
             color = 3,
             mass = Param.ZERO,
             width = Param.ZERO,
             texname = 'u',
             antitexname = 'u~',
             charge = 2/3,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

u__tilde__ = u.anti()

c = Particle(pdg_code = 4,
             name = 'c',
             antiname = 'c~',
             spin = 2,
             color = 3,
             mass = Param.ZERO,
             width = Param.ZERO,
             texname = 'c',
             antitexname = 'c~',
             charge = 2/3,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

c__tilde__ = c.anti()

t = Particle(pdg_code = 6,
             name = 't',
             antiname = 't~',
             spin = 2,
             color = 3,
             mass = Param.MT,
             width = Param.WT,
             texname = 't',
             antitexname = 't~',
             charge = 2/3,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

t__tilde__ = t.anti()

d = Particle(pdg_code = 1,
             name = 'd',
             antiname = 'd~',
             spin = 2,
             color = 3,
             mass = Param.ZERO,
             width = Param.ZERO,
             texname = 'd',
             antitexname = 'd~',
             charge = -1/3,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

d__tilde__ = d.anti()

s = Particle(pdg_code = 3,
             name = 's',
             antiname = 's~',
             spin = 2,
             color = 3,
             mass = Param.ZERO,
             width = Param.ZERO,
             texname = 's',
             antitexname = 's~',
             charge = -1/3,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

s__tilde__ = s.anti()

b = Particle(pdg_code = 5,
             name = 'b',
             antiname = 'b~',
             spin = 2,
             color = 3,
             mass = Param.MB,
             width = Param.ZERO,
             texname = 'b',
             antitexname = 'b~',
             charge = -1/3,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

b__tilde__ = b.anti()

H = Particle(pdg_code = 25,
             name = 'H',
             antiname = 'H',
             spin = 1,
             color = 1,
             mass = Param.MH,
             width = Param.WH,
             texname = 'H',
             antitexname = 'H',
             charge = 0,
             GhostNumber = 0,
             LeptonNumber = 0,
             Y = 0)

G0 = Particle(pdg_code = 250,
              name = 'G0',
              antiname = 'G0',
              spin = 1,
              color = 1,
              mass = Param.MZ,
              width = Param.WZ,
              texname = 'G0',
              antitexname = 'G0',
              goldstone = True,
              charge = 0,
              GhostNumber = 0,
              LeptonNumber = 0,
              Y = 0)

G__plus__ = Particle(pdg_code = 251,
                     name = 'G+',
                     antiname = 'G-',
                     spin = 1,
                     color = 1,
                     mass = Param.MW,
                     width = Param.WW,
                     texname = 'G+',
                     antitexname = 'G-',
                     goldstone = True,
                     charge = 1,
                     GhostNumber = 0,
                     LeptonNumber = 0,
                     Y = 0)

G__minus__ = G__plus__.anti()

sd11 = Particle(pdg_code = 9000005,
                name = 'sd11',
                antiname = 'sd11~',
                spin = 1,
                color = 3,
                mass = Param.Msd11,
                width = Param.MWsd11,
                texname = 'sd11',
                antitexname = 'sd11~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sd11__tilde__ = sd11.anti()

sd12 = Particle(pdg_code = 9000006,
                name = 'sd12',
                antiname = 'sd12~',
                spin = 1,
                color = 3,
                mass = Param.Msd12,
                width = Param.MWsd12,
                texname = 'sd12',
                antitexname = 'sd12~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sd12__tilde__ = sd12.anti()

sd21 = Particle(pdg_code = 9000007,
                name = 'sd21',
                antiname = 'sd21~',
                spin = 1,
                color = 3,
                mass = Param.Msd21,
                width = Param.MWsd21,
                texname = 'sd21',
                antitexname = 'sd21~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sd21__tilde__ = sd21.anti()

sd22 = Particle(pdg_code = 9000008,
                name = 'sd22',
                antiname = 'sd22~',
                spin = 1,
                color = 3,
                mass = Param.Msd22,
                width = Param.MWsd22,
                texname = 'sd22',
                antitexname = 'sd22~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sd22__tilde__ = sd22.anti()

ss11 = Particle(pdg_code = 9000009,
                name = 'ss11',
                antiname = 'ss11~',
                spin = 1,
                color = 3,
                mass = Param.Mss11,
                width = Param.MWss11,
                texname = 'ss11',
                antitexname = 'ss11~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

ss11__tilde__ = ss11.anti()

ss12 = Particle(pdg_code = 9000010,
                name = 'ss12',
                antiname = 'ss12~',
                spin = 1,
                color = 3,
                mass = Param.Mss12,
                width = Param.MWss12,
                texname = 'ss12',
                antitexname = 'ss12~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

ss12__tilde__ = ss12.anti()

ss21 = Particle(pdg_code = 9000011,
                name = 'ss21',
                antiname = 'ss21~',
                spin = 1,
                color = 3,
                mass = Param.Mss21,
                width = Param.MWss21,
                texname = 'ss21',
                antitexname = 'ss21~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

ss21__tilde__ = ss21.anti()

ss22 = Particle(pdg_code = 9000012,
                name = 'ss22',
                antiname = 'ss22~',
                spin = 1,
                color = 3,
                mass = Param.Mss22,
                width = Param.MWss22,
                texname = 'ss22',
                antitexname = 'ss22~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

ss22__tilde__ = ss22.anti()

sb11 = Particle(pdg_code = 9000013,
                name = 'sb11',
                antiname = 'sb11~',
                spin = 1,
                color = 3,
                mass = Param.Msb11,
                width = Param.MWsb11,
                texname = 'sb11',
                antitexname = 'sb11~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sb11__tilde__ = sb11.anti()

sb12 = Particle(pdg_code = 9000014,
                name = 'sb12',
                antiname = 'sb12~',
                spin = 1,
                color = 3,
                mass = Param.Msb12,
                width = Param.MWsb12,
                texname = 'sb12',
                antitexname = 'sb12~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sb12__tilde__ = sb12.anti()

sb21 = Particle(pdg_code = 9000015,
                name = 'sb21',
                antiname = 'sb21~',
                spin = 1,
                color = 3,
                mass = Param.Msb21,
                width = Param.MWsb21,
                texname = 'sb21',
                antitexname = 'sb21~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sb21__tilde__ = sb21.anti()

sb22 = Particle(pdg_code = 9000016,
                name = 'sb22',
                antiname = 'sb22~',
                spin = 1,
                color = 3,
                mass = Param.Msb22,
                width = Param.MWsb22,
                texname = 'sb22',
                antitexname = 'sb22~',
                charge = -1/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sb22__tilde__ = sb22.anti()

su11 = Particle(pdg_code = 9000017,
                name = 'su11',
                antiname = 'su11~',
                spin = 1,
                color = 3,
                mass = Param.Msu11,
                width = Param.MWsu11,
                texname = 'su11',
                antitexname = 'su11~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

su11__tilde__ = su11.anti()

su12 = Particle(pdg_code = 9000018,
                name = 'su12',
                antiname = 'su12~',
                spin = 1,
                color = 3,
                mass = Param.Msu12,
                width = Param.MWsu12,
                texname = 'su12',
                antitexname = 'su12~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

su12__tilde__ = su12.anti()

su21 = Particle(pdg_code = 9000019,
                name = 'su21',
                antiname = 'su21~',
                spin = 1,
                color = 3,
                mass = Param.Msu21,
                width = Param.MWsu21,
                texname = 'su21',
                antitexname = 'su21~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

su21__tilde__ = su21.anti()

su22 = Particle(pdg_code = 9000020,
                name = 'su22',
                antiname = 'su22~',
                spin = 1,
                color = 3,
                mass = Param.Msu22,
                width = Param.MWsu22,
                texname = 'su22',
                antitexname = 'su22~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

su22__tilde__ = su22.anti()

sc11 = Particle(pdg_code = 9000021,
                name = 'sc11',
                antiname = 'sc11~',
                spin = 1,
                color = 3,
                mass = Param.Msc11,
                width = Param.MWsc11,
                texname = 'sc11',
                antitexname = 'sc11~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sc11__tilde__ = sc11.anti()

sc12 = Particle(pdg_code = 9000022,
                name = 'sc12',
                antiname = 'sc12~',
                spin = 1,
                color = 3,
                mass = Param.Msc12,
                width = Param.MWsc12,
                texname = 'sc12',
                antitexname = 'sc12~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sc12__tilde__ = sc12.anti()

sc21 = Particle(pdg_code = 9000023,
                name = 'sc21',
                antiname = 'sc21~',
                spin = 1,
                color = 3,
                mass = Param.Msc21,
                width = Param.MWsc21,
                texname = 'sc21',
                antitexname = 'sc21~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sc21__tilde__ = sc21.anti()

sc22 = Particle(pdg_code = 9000024,
                name = 'sc22',
                antiname = 'sc22~',
                spin = 1,
                color = 3,
                mass = Param.Msc22,
                width = Param.MWsc22,
                texname = 'sc22',
                antitexname = 'sc22~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

sc22__tilde__ = sc22.anti()

st11 = Particle(pdg_code = 9000025,
                name = 'st11',
                antiname = 'st11~',
                spin = 1,
                color = 3,
                mass = Param.Mst11,
                width = Param.MWst11,
                texname = 'st11',
                antitexname = 'st11~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

st11__tilde__ = st11.anti()

st12 = Particle(pdg_code = 9000026,
                name = 'st12',
                antiname = 'st12~',
                spin = 1,
                color = 3,
                mass = Param.Mst12,
                width = Param.MWst12,
                texname = 'st12',
                antitexname = 'st12~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

st12__tilde__ = st12.anti()

st21 = Particle(pdg_code = 9000027,
                name = 'st21',
                antiname = 'st21~',
                spin = 1,
                color = 3,
                mass = Param.Mst21,
                width = Param.MWst21,
                texname = 'st21',
                antitexname = 'st21~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

st21__tilde__ = st21.anti()

st22 = Particle(pdg_code = 9000028,
                name = 'st22',
                antiname = 'st22~',
                spin = 1,
                color = 3,
                mass = Param.Mst22,
                width = Param.MWst22,
                texname = 'st22',
                antitexname = 'st22~',
                charge = 2/3,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

st22__tilde__ = st22.anti()

gv11 = Particle(pdg_code = 49001011,
                name = 'gv11',
                antiname = 'gv11~',
                spin = 2,
                color = 1,
                mass = Param.Mgv11,
                width = Param.ZERO,
                texname = 'gv11',
                antitexname = 'gv11~',
                charge = 0,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

gv11__tilde__ = gv11.anti()

gv12 = Particle(pdg_code = 49001012,
                name = 'gv12',
                antiname = 'gv12~',
                spin = 2,
                color = 1,
                mass = Param.Mgv12,
                width = Param.ZERO,
                texname = 'gv12',
                antitexname = 'gv12~',
                charge = 0,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

gv12__tilde__ = gv12.anti()

gv21 = Particle(pdg_code = 49001013,
                name = 'gv21',
                antiname = 'gv21~',
                spin = 2,
                color = 1,
                mass = Param.Mgv21,
                width = Param.ZERO,
                texname = 'gv21',
                antitexname = 'gv21~',
                charge = 0,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

gv21__tilde__ = gv21.anti()

gv22 = Particle(pdg_code = 49001014,
                name = 'gv22',
                antiname = 'gv22~',
                spin = 2,
                color = 1,
                mass = Param.Mgv22,
                width = Param.ZERO,
                texname = 'gv22',
                antitexname = 'gv22~',
                charge = 0,
                GhostNumber = 0,
                LeptonNumber = 0,
                Y = 0)

gv22__tilde__ = gv22.anti()

