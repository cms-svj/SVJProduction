from collections import OrderedDict

params = OrderedDict([
("mZprime", (3000,[1000, 1500, 2000, 2500, 3000, 3500, 4000])),
("mDark", (20,[5, 20, 50])),
("rinv", (0.3,[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])),
("alpha", ("peak",["peak", "high", "low"])),
])

sigs = []

# make default sample
stmp = ()
for p in params:
    stmp += (params[p][0],)
sigs.append(stmp)

# vary one at a time
for i, (p, vals) in enumerate(params.iteritems()):
    for v in vals[1]:
        tmp = list(stmp)
        tmp[i] = v
        tmp = tuple(tmp)
        if tmp!=stmp: sigs.append(tmp)

#print '\n'.join([str(s) for s in sigs])
#print len(sigs)

flist = [{"mZprime": x[0], "mDark": x[1], "rinv": x[2], "alpha": x[3]} for x in sigs]

#print flist
