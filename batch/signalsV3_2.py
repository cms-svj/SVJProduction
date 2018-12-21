from collections import OrderedDict

params = OrderedDict([
("mZprime", (3000,range(500,4600,100))),
("mDark", (20,[1]+range(10,110,10))),
("rinv", (0.3,[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])),
("alpha", ("peak",["peak", "high", "low"])),
])

sigs = set()

# make default sample
stmp = ()
for p in params:
    stmp += (params[p][0],)
sigs.add(stmp)

# vary one at a time
for i, (p, vals) in enumerate(params.iteritems()):
    for v in vals[1]:
        tmp = list(stmp)
        tmp[i] = v
        tmp = tuple(tmp)
        if tmp!=stmp: sigs.add(tmp)

from signalsV3_1 import sigs as sigs1
sigs = sigs - sigs1
print len(sigs)

flist = [OrderedDict([("mZprime", x[0]), ("mDark", x[1]), ("rinv", x[2]), ("alpha", x[3])]) for x in sorted(sigs)]

#print flist
