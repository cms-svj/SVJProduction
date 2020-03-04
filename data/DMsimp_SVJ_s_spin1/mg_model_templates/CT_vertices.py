# This file was automatically created by FeynRules 2.4.46
# Mathematica version: 10.3.0 for Mac OS X x86 (64-bit) (October 9, 2015)
# Date: Thu 27 Oct 2016 23:02:25


from object_library import all_vertices, all_CTvertices, Vertex, CTVertex
import particles as P
import CT_couplings as C
import lorentz as L


V_1 = CTVertex(name = 'V_1',
               type = 'R2',
               particles = [ P.g, P.g, P.g ],
               color = [ 'f(1,2,3)' ],
               lorentz = [ L.VVV3, L.VVV4, L.VVV5, L.VVV6, L.VVV7, L.VVV8 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(0,0,0):C.R2GC_185_96,(0,0,1):C.R2GC_185_97,(0,1,0):C.R2GC_186_98,(0,1,1):C.R2GC_186_99,(0,2,0):C.R2GC_186_98,(0,2,1):C.R2GC_186_99,(0,3,0):C.R2GC_185_96,(0,3,1):C.R2GC_185_97,(0,4,0):C.R2GC_185_96,(0,4,1):C.R2GC_185_97,(0,5,0):C.R2GC_186_98,(0,5,1):C.R2GC_186_99})

V_2 = CTVertex(name = 'V_2',
               type = 'R2',
               particles = [ P.g, P.g, P.g, P.g ],
               color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
               lorentz = [ L.VVVV2, L.VVVV3, L.VVVV4 ],
               loop_particles = [ [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ] ],
               couplings = {(2,0,0):C.R2GC_149_78,(2,0,1):C.R2GC_149_79,(0,0,0):C.R2GC_149_78,(0,0,1):C.R2GC_149_79,(4,0,0):C.R2GC_147_74,(4,0,1):C.R2GC_147_75,(3,0,0):C.R2GC_147_74,(3,0,1):C.R2GC_147_75,(8,0,0):C.R2GC_148_76,(8,0,1):C.R2GC_148_77,(7,0,0):C.R2GC_153_84,(7,0,1):C.R2GC_190_104,(6,0,0):C.R2GC_152_83,(6,0,1):C.R2GC_191_105,(5,0,0):C.R2GC_147_74,(5,0,1):C.R2GC_147_75,(1,0,0):C.R2GC_147_74,(1,0,1):C.R2GC_147_75,(11,0,0):C.R2GC_151_81,(11,0,1):C.R2GC_151_82,(10,0,0):C.R2GC_151_81,(10,0,1):C.R2GC_151_82,(9,0,1):C.R2GC_150_80,(2,1,0):C.R2GC_149_78,(2,1,1):C.R2GC_149_79,(0,1,0):C.R2GC_149_78,(0,1,1):C.R2GC_149_79,(6,1,0):C.R2GC_187_100,(6,1,1):C.R2GC_187_101,(4,1,0):C.R2GC_147_74,(4,1,1):C.R2GC_147_75,(3,1,0):C.R2GC_147_74,(3,1,1):C.R2GC_147_75,(8,1,0):C.R2GC_148_76,(8,1,1):C.R2GC_190_104,(7,1,0):C.R2GC_153_84,(7,1,1):C.R2GC_148_77,(5,1,0):C.R2GC_147_74,(5,1,1):C.R2GC_147_75,(1,1,0):C.R2GC_147_74,(1,1,1):C.R2GC_147_75,(11,1,0):C.R2GC_151_81,(11,1,1):C.R2GC_151_82,(10,1,0):C.R2GC_151_81,(10,1,1):C.R2GC_151_82,(9,1,1):C.R2GC_150_80,(2,2,0):C.R2GC_149_78,(2,2,1):C.R2GC_149_79,(0,2,0):C.R2GC_149_78,(0,2,1):C.R2GC_149_79,(4,2,0):C.R2GC_147_74,(4,2,1):C.R2GC_147_75,(3,2,0):C.R2GC_147_74,(3,2,1):C.R2GC_147_75,(8,2,0):C.R2GC_148_76,(8,2,1):C.R2GC_188_103,(6,2,0):C.R2GC_152_83,(7,2,0):C.R2GC_188_102,(7,2,1):C.R2GC_188_103,(5,2,0):C.R2GC_147_74,(5,2,1):C.R2GC_147_75,(1,2,0):C.R2GC_147_74,(1,2,1):C.R2GC_147_75,(11,2,0):C.R2GC_151_81,(11,2,1):C.R2GC_151_82,(10,2,0):C.R2GC_151_81,(10,2,1):C.R2GC_151_82,(9,2,1):C.R2GC_150_80})

V_3 = CTVertex(name = 'V_3',
               type = 'R2',
               particles = [ P.t__tilde__, P.b, P.G__plus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               loop_particles = [ [ [P.b, P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_205_112,(0,1,0):C.R2GC_206_113})

V_4 = CTVertex(name = 'V_4',
               type = 'R2',
               particles = [ P.b__tilde__, P.b, P.G0 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS1 ],
               loop_particles = [ [ [P.b, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_183_95})

V_5 = CTVertex(name = 'V_5',
               type = 'R2',
               particles = [ P.b__tilde__, P.b, P.H ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS2 ],
               loop_particles = [ [ [P.b, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_182_94})

V_6 = CTVertex(name = 'V_6',
               type = 'R2',
               particles = [ P.b__tilde__, P.t, P.G__minus__ ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS3, L.FFS5 ],
               loop_particles = [ [ [P.b, P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_207_114,(0,1,0):C.R2GC_204_111})

V_7 = CTVertex(name = 'V_7',
               type = 'R2',
               particles = [ P.t__tilde__, P.t, P.G0 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS1 ],
               loop_particles = [ [ [P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_208_115})

V_8 = CTVertex(name = 'V_8',
               type = 'R2',
               particles = [ P.t__tilde__, P.t, P.H ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFS2 ],
               loop_particles = [ [ [P.g, P.t] ] ],
               couplings = {(0,0,0):C.R2GC_209_116})

V_9 = CTVertex(name = 'V_9',
               type = 'R2',
               particles = [ P.b__tilde__, P.b, P.Y1 ],
               color = [ 'Identity(1,2)' ],
               lorentz = [ L.FFV6, L.FFV7 ],
               loop_particles = [ [ [P.b, P.g] ] ],
               couplings = {(0,0,0):C.R2GC_176_90,(0,1,0):C.R2GC_178_92})

V_10 = CTVertex(name = 'V_10',
                type = 'R2',
                particles = [ P.d__tilde__, P.b, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.b, P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_175_89,(0,1,0):C.R2GC_177_91})

V_11 = CTVertex(name = 'V_11',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_100_1,(0,1,0):C.R2GC_101_2})

V_12 = CTVertex(name = 'V_12',
                type = 'R2',
                particles = [ P.b__tilde__, P.d, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.b, P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_175_89,(0,1,0):C.R2GC_177_91})

V_13 = CTVertex(name = 'V_13',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_105_6,(0,1,0):C.R2GC_106_7})

V_14 = CTVertex(name = 'V_14',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_110_9,(0,1,0):C.R2GC_111_10})

V_15 = CTVertex(name = 'V_15',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_197_107,(0,1,0):C.R2GC_199_109})

V_16 = CTVertex(name = 'V_16',
                type = 'R2',
                particles = [ P.u__tilde__, P.t, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.g, P.t, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_196_106,(0,1,0):C.R2GC_198_108})

V_17 = CTVertex(name = 'V_17',
                type = 'R2',
                particles = [ P.t__tilde__, P.u, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.g, P.t, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_196_106,(0,1,0):C.R2GC_198_108})

V_18 = CTVertex(name = 'V_18',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_115_11,(0,1,0):C.R2GC_116_12})

V_19 = CTVertex(name = 'V_19',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_156_87})

V_20 = CTVertex(name = 'V_20',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_156_87})

V_21 = CTVertex(name = 'V_21',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_156_87})

V_22 = CTVertex(name = 'V_22',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_154_85})

V_23 = CTVertex(name = 'V_23',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_154_85})

V_24 = CTVertex(name = 'V_24',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_154_85})

V_25 = CTVertex(name = 'V_25',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_155_86})

V_26 = CTVertex(name = 'V_26',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_155_86})

V_27 = CTVertex(name = 'V_27',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_155_86})

V_28 = CTVertex(name = 'V_28',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_155_86})

V_29 = CTVertex(name = 'V_29',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_155_86})

V_30 = CTVertex(name = 'V_30',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_155_86})

V_31 = CTVertex(name = 'V_31',
                type = 'R2',
                particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_170_88})

V_32 = CTVertex(name = 'V_32',
                type = 'R2',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.c, P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_170_88})

V_33 = CTVertex(name = 'V_33',
                type = 'R2',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.b, P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_170_88})

V_34 = CTVertex(name = 'V_34',
                type = 'R2',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_170_88})

V_35 = CTVertex(name = 'V_35',
                type = 'R2',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.c, P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_170_88})

V_36 = CTVertex(name = 'V_36',
                type = 'R2',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.b, P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_170_88})

V_37 = CTVertex(name = 'V_37',
                type = 'R2',
                particles = [ P.u__tilde__, P.u, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3, L.FFV9 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_102_3,(0,1,0):C.R2GC_103_4})

V_38 = CTVertex(name = 'V_38',
                type = 'R2',
                particles = [ P.c__tilde__, P.c, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3, L.FFV9 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_102_3,(0,1,0):C.R2GC_103_4})

V_39 = CTVertex(name = 'V_39',
                type = 'R2',
                particles = [ P.t__tilde__, P.t, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3, L.FFV9 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_102_3,(0,1,0):C.R2GC_103_4})

V_40 = CTVertex(name = 'V_40',
                type = 'R2',
                particles = [ P.d__tilde__, P.d, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3, L.FFV5 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_107_8,(0,1,0):C.R2GC_103_4})

V_41 = CTVertex(name = 'V_41',
                type = 'R2',
                particles = [ P.s__tilde__, P.s, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3, L.FFV5 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_107_8,(0,1,0):C.R2GC_103_4})

V_42 = CTVertex(name = 'V_42',
                type = 'R2',
                particles = [ P.b__tilde__, P.b, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3, L.FFV5 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_107_8,(0,1,0):C.R2GC_103_4})

V_43 = CTVertex(name = 'V_43',
                type = 'R2',
                particles = [ P.u__tilde__, P.u ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_104_5})

V_44 = CTVertex(name = 'V_44',
                type = 'R2',
                particles = [ P.c__tilde__, P.c ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_104_5})

V_45 = CTVertex(name = 'V_45',
                type = 'R2',
                particles = [ P.t__tilde__, P.t ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2, L.FF3 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_200_110,(0,1,0):C.R2GC_104_5})

V_46 = CTVertex(name = 'V_46',
                type = 'R2',
                particles = [ P.d__tilde__, P.d ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_104_5})

V_47 = CTVertex(name = 'V_47',
                type = 'R2',
                particles = [ P.s__tilde__, P.s ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF1 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.R2GC_104_5})

V_48 = CTVertex(name = 'V_48',
                type = 'R2',
                particles = [ P.b__tilde__, P.b ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FF2, L.FF3 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.R2GC_179_93,(0,1,0):C.R2GC_104_5})

V_49 = CTVertex(name = 'V_49',
                type = 'R2',
                particles = [ P.g, P.g ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VV2, L.VV3, L.VV4 ],
                loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.g] ], [ [P.t] ] ],
                couplings = {(0,2,2):C.R2GC_98_117,(0,0,0):C.R2GC_119_13,(0,0,3):C.R2GC_119_14,(0,1,1):C.R2GC_122_19})

V_50 = CTVertex(name = 'V_50',
                type = 'R2',
                particles = [ P.g, P.g, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVV2 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_125_24,(0,0,1):C.R2GC_125_25,(0,0,2):C.R2GC_125_26,(0,0,3):C.R2GC_125_27,(0,0,4):C.R2GC_125_28,(0,0,5):C.R2GC_125_29})

V_51 = CTVertex(name = 'V_51',
                type = 'R2',
                particles = [ P.g, P.g, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVV1 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_129_48,(0,0,1):C.R2GC_129_49})

V_52 = CTVertex(name = 'V_52',
                type = 'R2',
                particles = [ P.g, P.g, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVS1 ],
                loop_particles = [ [ [P.b] ], [ [P.t] ] ],
                couplings = {(0,0,0):C.R2GC_120_15,(0,0,1):C.R2GC_120_16})

V_53 = CTVertex(name = 'V_53',
                type = 'R2',
                particles = [ P.g, P.g, P.Y1, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b] ], [ [P.b, P.d] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.t, P.u] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_137_66,(0,0,2):C.R2GC_137_67,(0,0,3):C.R2GC_137_68,(0,0,4):C.R2GC_137_69,(0,0,5):C.R2GC_137_70,(0,0,7):C.R2GC_137_71,(0,0,1):C.R2GC_137_72,(0,0,6):C.R2GC_137_73})

V_54 = CTVertex(name = 'V_54',
                type = 'R2',
                particles = [ P.a, P.g, P.g, P.Y1 ],
                color = [ 'Identity(2,3)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_127_36,(0,0,1):C.R2GC_127_37,(0,0,2):C.R2GC_127_38,(0,0,3):C.R2GC_127_39,(0,0,4):C.R2GC_127_40,(0,0,5):C.R2GC_127_41})

V_55 = CTVertex(name = 'V_55',
                type = 'R2',
                particles = [ P.g, P.g, P.Y1, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_133_56,(0,0,1):C.R2GC_133_57,(0,0,2):C.R2GC_133_58,(0,0,3):C.R2GC_133_59,(0,0,4):C.R2GC_133_60,(0,0,5):C.R2GC_133_61})

V_56 = CTVertex(name = 'V_56',
                type = 'R2',
                particles = [ P.g, P.g, P.g, P.Y1 ],
                color = [ 'd(1,2,3)', 'f(1,2,3)' ],
                lorentz = [ L.VVVV1, L.VVVV7 ],
                loop_particles = [ [ [P.b] ], [ [P.c] ], [ [P.d] ], [ [P.s] ], [ [P.t] ], [ [P.u] ] ],
                couplings = {(1,0,0):C.R2GC_126_30,(1,0,1):C.R2GC_126_31,(1,0,2):C.R2GC_126_32,(1,0,3):C.R2GC_126_33,(1,0,4):C.R2GC_126_34,(1,0,5):C.R2GC_126_35,(0,1,0):C.R2GC_128_42,(0,1,1):C.R2GC_128_43,(0,1,2):C.R2GC_128_44,(0,1,3):C.R2GC_128_45,(0,1,4):C.R2GC_128_46,(0,1,5):C.R2GC_128_47})

V_57 = CTVertex(name = 'V_57',
                type = 'R2',
                particles = [ P.g, P.g, P.W__minus__, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b, P.t], [P.c, P.s], [P.d, P.u] ] ],
                couplings = {(0,0,0):C.R2GC_136_65})

V_58 = CTVertex(name = 'V_58',
                type = 'R2',
                particles = [ P.a, P.g, P.g, P.Z ],
                color = [ 'Identity(2,3)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_130_50,(0,0,1):C.R2GC_130_51})

V_59 = CTVertex(name = 'V_59',
                type = 'R2',
                particles = [ P.g, P.g, P.Z, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_134_62,(0,0,1):C.R2GC_134_63})

V_60 = CTVertex(name = 'V_60',
                type = 'R2',
                particles = [ P.a, P.a, P.g, P.g ],
                color = [ 'Identity(3,4)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_123_20,(0,0,1):C.R2GC_123_21})

V_61 = CTVertex(name = 'V_61',
                type = 'R2',
                particles = [ P.g, P.g, P.g, P.Z ],
                color = [ 'd(1,2,3)', 'f(1,2,3)' ],
                lorentz = [ L.VVVV1, L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(1,0,0):C.R2GC_132_54,(1,0,1):C.R2GC_132_55,(0,1,0):C.R2GC_131_52,(0,1,1):C.R2GC_131_53})

V_62 = CTVertex(name = 'V_62',
                type = 'R2',
                particles = [ P.a, P.g, P.g, P.g ],
                color = [ 'd(2,3,4)' ],
                lorentz = [ L.VVVV7 ],
                loop_particles = [ [ [P.b], [P.d], [P.s] ], [ [P.c], [P.t], [P.u] ] ],
                couplings = {(0,0,0):C.R2GC_124_22,(0,0,1):C.R2GC_124_23})

V_63 = CTVertex(name = 'V_63',
                type = 'R2',
                particles = [ P.g, P.g, P.H, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.t] ] ],
                couplings = {(0,0,0):C.R2GC_121_17,(0,0,1):C.R2GC_121_18})

V_64 = CTVertex(name = 'V_64',
                type = 'R2',
                particles = [ P.g, P.g, P.G0, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b] ], [ [P.t] ] ],
                couplings = {(0,0,0):C.R2GC_121_17,(0,0,1):C.R2GC_121_18})

V_65 = CTVertex(name = 'V_65',
                type = 'R2',
                particles = [ P.g, P.g, P.G__minus__, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.VVSS1 ],
                loop_particles = [ [ [P.b, P.t] ] ],
                couplings = {(0,0,0):C.R2GC_135_64})

V_66 = CTVertex(name = 'V_66',
                type = 'UV',
                particles = [ P.g, P.g, P.g ],
                color = [ 'f(1,2,3)' ],
                lorentz = [ L.VVV3, L.VVV4, L.VVV5, L.VVV6, L.VVV7, L.VVV8 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(0,0,0):C.UVGC_185_44,(0,0,1):C.UVGC_185_45,(0,0,2):C.UVGC_185_46,(0,0,3):C.UVGC_185_47,(0,0,4):C.UVGC_185_48,(0,1,0):C.UVGC_186_49,(0,1,1):C.UVGC_186_50,(0,1,2):C.UVGC_186_51,(0,1,3):C.UVGC_186_52,(0,1,4):C.UVGC_186_53,(0,2,0):C.UVGC_186_49,(0,2,1):C.UVGC_186_50,(0,2,2):C.UVGC_186_51,(0,2,3):C.UVGC_186_52,(0,2,4):C.UVGC_186_53,(0,3,0):C.UVGC_185_44,(0,3,1):C.UVGC_185_45,(0,3,2):C.UVGC_185_46,(0,3,3):C.UVGC_185_47,(0,3,4):C.UVGC_185_48,(0,4,0):C.UVGC_185_44,(0,4,1):C.UVGC_185_45,(0,4,2):C.UVGC_185_46,(0,4,3):C.UVGC_185_47,(0,4,4):C.UVGC_185_48,(0,5,0):C.UVGC_186_49,(0,5,1):C.UVGC_186_50,(0,5,2):C.UVGC_186_51,(0,5,3):C.UVGC_186_52,(0,5,4):C.UVGC_186_53})

V_67 = CTVertex(name = 'V_67',
                type = 'UV',
                particles = [ P.g, P.g, P.g, P.g ],
                color = [ 'd(-1,1,3)*d(-1,2,4)', 'd(-1,1,3)*f(-1,2,4)', 'd(-1,1,4)*d(-1,2,3)', 'd(-1,1,4)*f(-1,2,3)', 'd(-1,2,3)*f(-1,1,4)', 'd(-1,2,4)*f(-1,1,3)', 'f(-1,1,2)*f(-1,3,4)', 'f(-1,1,3)*f(-1,2,4)', 'f(-1,1,4)*f(-1,2,3)', 'Identity(1,2)*Identity(3,4)', 'Identity(1,3)*Identity(2,4)', 'Identity(1,4)*Identity(2,3)' ],
                lorentz = [ L.VVVV2, L.VVVV3, L.VVVV4 ],
                loop_particles = [ [ [P.b] ], [ [P.b], [P.c], [P.d], [P.s], [P.t], [P.u] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                couplings = {(2,0,3):C.UVGC_148_9,(2,0,4):C.UVGC_148_8,(0,0,3):C.UVGC_148_9,(0,0,4):C.UVGC_148_8,(4,0,3):C.UVGC_147_6,(4,0,4):C.UVGC_147_7,(3,0,3):C.UVGC_147_6,(3,0,4):C.UVGC_147_7,(8,0,3):C.UVGC_148_8,(8,0,4):C.UVGC_148_9,(7,0,0):C.UVGC_190_64,(7,0,2):C.UVGC_190_65,(7,0,3):C.UVGC_190_66,(7,0,4):C.UVGC_190_67,(7,0,5):C.UVGC_190_68,(6,0,0):C.UVGC_190_64,(6,0,2):C.UVGC_190_65,(6,0,3):C.UVGC_191_69,(6,0,4):C.UVGC_191_70,(6,0,5):C.UVGC_190_68,(5,0,3):C.UVGC_147_6,(5,0,4):C.UVGC_147_7,(1,0,3):C.UVGC_147_6,(1,0,4):C.UVGC_147_7,(11,0,3):C.UVGC_151_12,(11,0,4):C.UVGC_151_13,(10,0,3):C.UVGC_151_12,(10,0,4):C.UVGC_151_13,(9,0,3):C.UVGC_150_10,(9,0,4):C.UVGC_150_11,(2,1,3):C.UVGC_148_9,(2,1,4):C.UVGC_148_8,(0,1,3):C.UVGC_148_9,(0,1,4):C.UVGC_148_8,(6,1,0):C.UVGC_187_54,(6,1,3):C.UVGC_187_55,(6,1,4):C.UVGC_187_56,(6,1,5):C.UVGC_187_57,(4,1,3):C.UVGC_147_6,(4,1,4):C.UVGC_147_7,(3,1,3):C.UVGC_147_6,(3,1,4):C.UVGC_147_7,(8,1,0):C.UVGC_192_71,(8,1,2):C.UVGC_192_72,(8,1,3):C.UVGC_190_66,(8,1,4):C.UVGC_192_73,(8,1,5):C.UVGC_192_74,(7,1,1):C.UVGC_152_14,(7,1,3):C.UVGC_148_8,(7,1,4):C.UVGC_153_15,(5,1,3):C.UVGC_147_6,(5,1,4):C.UVGC_147_7,(1,1,3):C.UVGC_147_6,(1,1,4):C.UVGC_147_7,(11,1,3):C.UVGC_151_12,(11,1,4):C.UVGC_151_13,(10,1,3):C.UVGC_151_12,(10,1,4):C.UVGC_151_13,(9,1,3):C.UVGC_150_10,(9,1,4):C.UVGC_150_11,(2,2,3):C.UVGC_148_9,(2,2,4):C.UVGC_148_8,(0,2,3):C.UVGC_148_9,(0,2,4):C.UVGC_148_8,(4,2,3):C.UVGC_147_6,(4,2,4):C.UVGC_147_7,(3,2,3):C.UVGC_147_6,(3,2,4):C.UVGC_147_7,(8,2,0):C.UVGC_189_60,(8,2,2):C.UVGC_189_61,(8,2,3):C.UVGC_188_58,(8,2,4):C.UVGC_189_62,(8,2,5):C.UVGC_189_63,(6,2,1):C.UVGC_152_14,(6,2,4):C.UVGC_150_10,(7,2,0):C.UVGC_187_54,(7,2,3):C.UVGC_188_58,(7,2,4):C.UVGC_188_59,(7,2,5):C.UVGC_187_57,(5,2,3):C.UVGC_147_6,(5,2,4):C.UVGC_147_7,(1,2,3):C.UVGC_147_6,(1,2,4):C.UVGC_147_7,(11,2,3):C.UVGC_151_12,(11,2,4):C.UVGC_151_13,(10,2,3):C.UVGC_151_12,(10,2,4):C.UVGC_151_13,(9,2,3):C.UVGC_150_10,(9,2,4):C.UVGC_150_11})

V_68 = CTVertex(name = 'V_68',
                type = 'UV',
                particles = [ P.t__tilde__, P.b, P.G__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS5 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_205_94,(0,0,2):C.UVGC_205_95,(0,0,1):C.UVGC_205_96,(0,1,0):C.UVGC_206_97,(0,1,2):C.UVGC_206_98,(0,1,1):C.UVGC_206_99})

V_69 = CTVertex(name = 'V_69',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_183_41})

V_70 = CTVertex(name = 'V_70',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_182_40})

V_71 = CTVertex(name = 'V_71',
                type = 'UV',
                particles = [ P.b__tilde__, P.t, P.G__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS3, L.FFS5 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_207_100,(0,0,2):C.UVGC_207_101,(0,0,1):C.UVGC_207_102,(0,1,0):C.UVGC_204_91,(0,1,2):C.UVGC_204_92,(0,1,1):C.UVGC_204_93})

V_72 = CTVertex(name = 'V_72',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.G0 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS1 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_208_103})

V_73 = CTVertex(name = 'V_73',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.H ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFS2 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_209_104})

V_74 = CTVertex(name = 'V_74',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_176_32,(0,1,0):C.UVGC_178_36})

V_75 = CTVertex(name = 'V_75',
                type = 'UV',
                particles = [ P.d__tilde__, P.b, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.b, P.d, P.g] ], [ [P.b, P.g] ], [ [P.d, P.g] ] ],
                couplings = {(0,0,1):C.UVGC_175_29,(0,0,2):C.UVGC_175_30,(0,0,0):C.UVGC_175_31,(0,1,1):C.UVGC_177_33,(0,1,2):C.UVGC_177_34,(0,1,0):C.UVGC_177_35})

V_76 = CTVertex(name = 'V_76',
                type = 'UV',
                particles = [ P.b__tilde__, P.d, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.b, P.d, P.g] ], [ [P.b, P.g] ], [ [P.d, P.g] ] ],
                couplings = {(0,0,1):C.UVGC_175_29,(0,0,2):C.UVGC_175_30,(0,0,0):C.UVGC_175_31,(0,1,1):C.UVGC_177_33,(0,1,2):C.UVGC_177_34,(0,1,0):C.UVGC_177_35})

V_77 = CTVertex(name = 'V_77',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_197_81,(0,1,0):C.UVGC_199_85})

V_78 = CTVertex(name = 'V_78',
                type = 'UV',
                particles = [ P.u__tilde__, P.t, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.g, P.t] ], [ [P.g, P.t, P.u] ], [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_196_78,(0,0,2):C.UVGC_196_79,(0,0,1):C.UVGC_196_80,(0,1,0):C.UVGC_198_82,(0,1,2):C.UVGC_198_83,(0,1,1):C.UVGC_198_84})

V_79 = CTVertex(name = 'V_79',
                type = 'UV',
                particles = [ P.t__tilde__, P.u, P.Y1 ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV6, L.FFV7 ],
                loop_particles = [ [ [P.g, P.t] ], [ [P.g, P.t, P.u] ], [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_196_78,(0,0,2):C.UVGC_196_79,(0,0,1):C.UVGC_196_80,(0,1,0):C.UVGC_198_82,(0,1,2):C.UVGC_198_83,(0,1,1):C.UVGC_198_84})

V_80 = CTVertex(name = 'V_80',
                type = 'UV',
                particles = [ P.u__tilde__, P.u, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_156_18,(0,1,0):C.UVGC_139_2,(0,2,0):C.UVGC_139_2})

V_81 = CTVertex(name = 'V_81',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.c, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_156_18,(0,1,0):C.UVGC_139_2,(0,2,0):C.UVGC_139_2})

V_82 = CTVertex(name = 'V_82',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_156_18,(0,1,0):C.UVGC_194_76,(0,2,0):C.UVGC_194_76})

V_83 = CTVertex(name = 'V_83',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.d, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_154_16,(0,1,0):C.UVGC_141_3,(0,2,0):C.UVGC_141_3})

V_84 = CTVertex(name = 'V_84',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_154_16,(0,1,0):C.UVGC_141_3,(0,2,0):C.UVGC_141_3})

V_85 = CTVertex(name = 'V_85',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.a ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_154_16,(0,1,0):C.UVGC_173_27,(0,2,0):C.UVGC_173_27})

V_86 = CTVertex(name = 'V_86',
                type = 'UV',
                particles = [ P.u__tilde__, P.u, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.u] ] ],
                couplings = {(0,0,4):C.UVGC_155_17,(0,1,0):C.UVGC_157_19,(0,1,1):C.UVGC_157_20,(0,1,2):C.UVGC_157_21,(0,1,3):C.UVGC_157_22,(0,1,4):C.UVGC_157_23,(0,2,0):C.UVGC_157_19,(0,2,1):C.UVGC_157_20,(0,2,2):C.UVGC_157_21,(0,2,3):C.UVGC_157_22,(0,2,4):C.UVGC_157_23})

V_87 = CTVertex(name = 'V_87',
                type = 'UV',
                particles = [ P.c__tilde__, P.c, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.c, P.g] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,2):C.UVGC_155_17,(0,1,0):C.UVGC_157_19,(0,1,1):C.UVGC_157_20,(0,1,3):C.UVGC_157_21,(0,1,4):C.UVGC_157_22,(0,1,2):C.UVGC_157_23,(0,2,0):C.UVGC_157_19,(0,2,1):C.UVGC_157_20,(0,2,3):C.UVGC_157_21,(0,2,4):C.UVGC_157_22,(0,2,2):C.UVGC_157_23})

V_88 = CTVertex(name = 'V_88',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,4):C.UVGC_155_17,(0,1,0):C.UVGC_157_19,(0,1,1):C.UVGC_157_20,(0,1,2):C.UVGC_157_21,(0,1,3):C.UVGC_157_22,(0,1,4):C.UVGC_195_77,(0,2,0):C.UVGC_157_19,(0,2,1):C.UVGC_157_20,(0,2,2):C.UVGC_157_21,(0,2,3):C.UVGC_157_22,(0,2,4):C.UVGC_195_77})

V_89 = CTVertex(name = 'V_89',
                type = 'UV',
                particles = [ P.d__tilde__, P.d, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.d, P.g] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,2):C.UVGC_155_17,(0,1,0):C.UVGC_157_19,(0,1,1):C.UVGC_157_20,(0,1,3):C.UVGC_157_21,(0,1,4):C.UVGC_157_22,(0,1,2):C.UVGC_157_23,(0,2,0):C.UVGC_157_19,(0,2,1):C.UVGC_157_20,(0,2,3):C.UVGC_157_21,(0,2,4):C.UVGC_157_22,(0,2,2):C.UVGC_157_23})

V_90 = CTVertex(name = 'V_90',
                type = 'UV',
                particles = [ P.s__tilde__, P.s, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.b] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ], [ [P.g, P.s] ] ],
                couplings = {(0,0,4):C.UVGC_155_17,(0,1,0):C.UVGC_157_19,(0,1,1):C.UVGC_157_20,(0,1,2):C.UVGC_157_21,(0,1,3):C.UVGC_157_22,(0,1,4):C.UVGC_157_23,(0,2,0):C.UVGC_157_19,(0,2,1):C.UVGC_157_20,(0,2,2):C.UVGC_157_21,(0,2,3):C.UVGC_157_22,(0,2,4):C.UVGC_157_23})

V_91 = CTVertex(name = 'V_91',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.g ],
                color = [ 'T(3,2,1)' ],
                lorentz = [ L.FFV1, L.FFV3, L.FFV4 ],
                loop_particles = [ [ [P.b] ], [ [P.b, P.g] ], [ [P.c], [P.d], [P.s], [P.u] ], [ [P.g] ], [ [P.ghG] ] ],
                couplings = {(0,0,1):C.UVGC_155_17,(0,1,0):C.UVGC_157_19,(0,1,2):C.UVGC_157_20,(0,1,3):C.UVGC_157_21,(0,1,4):C.UVGC_157_22,(0,1,1):C.UVGC_174_28,(0,2,0):C.UVGC_157_19,(0,2,2):C.UVGC_157_20,(0,2,3):C.UVGC_157_21,(0,2,4):C.UVGC_157_22,(0,2,1):C.UVGC_174_28})

V_92 = CTVertex(name = 'V_92',
                type = 'UV',
                particles = [ P.d__tilde__, P.u, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.d, P.g], [P.g, P.u] ], [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_170_24,(0,0,1):C.UVGC_170_25})

V_93 = CTVertex(name = 'V_93',
                type = 'UV',
                particles = [ P.s__tilde__, P.c, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.c, P.g], [P.g, P.s] ], [ [P.c, P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_170_24,(0,0,1):C.UVGC_170_25})

V_94 = CTVertex(name = 'V_94',
                type = 'UV',
                particles = [ P.b__tilde__, P.t, P.W__minus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_201_87,(0,0,2):C.UVGC_201_88,(0,0,1):C.UVGC_170_25})

V_95 = CTVertex(name = 'V_95',
                type = 'UV',
                particles = [ P.u__tilde__, P.d, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.d, P.g], [P.g, P.u] ], [ [P.d, P.g, P.u] ] ],
                couplings = {(0,0,0):C.UVGC_170_24,(0,0,1):C.UVGC_170_25})

V_96 = CTVertex(name = 'V_96',
                type = 'UV',
                particles = [ P.c__tilde__, P.s, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.c, P.g], [P.g, P.s] ], [ [P.c, P.g, P.s] ] ],
                couplings = {(0,0,0):C.UVGC_170_24,(0,0,1):C.UVGC_170_25})

V_97 = CTVertex(name = 'V_97',
                type = 'UV',
                particles = [ P.t__tilde__, P.b, P.W__plus__ ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3 ],
                loop_particles = [ [ [P.b, P.g] ], [ [P.b, P.g, P.t] ], [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_201_87,(0,0,2):C.UVGC_201_88,(0,0,1):C.UVGC_170_25})

V_98 = CTVertex(name = 'V_98',
                type = 'UV',
                particles = [ P.t__tilde__, P.t, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3, L.FFV9 ],
                loop_particles = [ [ [P.g, P.t] ] ],
                couplings = {(0,0,0):C.UVGC_202_89,(0,1,0):C.UVGC_203_90})

V_99 = CTVertex(name = 'V_99',
                type = 'UV',
                particles = [ P.b__tilde__, P.b, P.Z ],
                color = [ 'Identity(1,2)' ],
                lorentz = [ L.FFV3, L.FFV5 ],
                loop_particles = [ [ [P.b, P.g] ] ],
                couplings = {(0,0,0):C.UVGC_180_38,(0,1,0):C.UVGC_181_39})

V_100 = CTVertex(name = 'V_100',
                 type = 'UV',
                 particles = [ P.u__tilde__, P.u ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.g, P.u] ] ],
                 couplings = {(0,0,0):C.UVGC_138_1})

V_101 = CTVertex(name = 'V_101',
                 type = 'UV',
                 particles = [ P.c__tilde__, P.c ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.c, P.g] ] ],
                 couplings = {(0,0,0):C.UVGC_138_1})

V_102 = CTVertex(name = 'V_102',
                 type = 'UV',
                 particles = [ P.t__tilde__, P.t ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3 ],
                 loop_particles = [ [ [P.g, P.t] ] ],
                 couplings = {(0,0,0):C.UVGC_200_86,(0,1,0):C.UVGC_193_75})

V_103 = CTVertex(name = 'V_103',
                 type = 'UV',
                 particles = [ P.d__tilde__, P.d ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.d, P.g] ] ],
                 couplings = {(0,0,0):C.UVGC_138_1})

V_104 = CTVertex(name = 'V_104',
                 type = 'UV',
                 particles = [ P.s__tilde__, P.s ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF4 ],
                 loop_particles = [ [ [P.g, P.s] ] ],
                 couplings = {(0,0,0):C.UVGC_138_1})

V_105 = CTVertex(name = 'V_105',
                 type = 'UV',
                 particles = [ P.b__tilde__, P.b ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.FF2, L.FF3 ],
                 loop_particles = [ [ [P.b, P.g] ] ],
                 couplings = {(0,0,0):C.UVGC_179_37,(0,1,0):C.UVGC_172_26})

V_106 = CTVertex(name = 'V_106',
                 type = 'UV',
                 particles = [ P.g, P.g ],
                 color = [ 'Identity(1,2)' ],
                 lorentz = [ L.VV1, L.VV5 ],
                 loop_particles = [ [ [P.b] ], [ [P.g] ], [ [P.ghG] ], [ [P.t] ] ],
                 couplings = {(0,1,0):C.UVGC_184_42,(0,1,3):C.UVGC_184_43,(0,0,1):C.UVGC_146_4,(0,0,2):C.UVGC_146_5})

