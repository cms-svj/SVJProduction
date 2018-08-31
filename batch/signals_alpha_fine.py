flist = []

eps=1e-10
for m, alphamin in zip([1,5,10,20,50,75,100],[0.15,0.2,0.225,0.275,0.35,0.4,0.45]):
#    print "m = "+str(m)
    # vary alpha in steps of 0.005
    for x in range(0,21,1):
        delta = x/200.
        alpha = round(alphamin + delta,3)
        # skip the existing ones
        if (alpha*100)%5<eps: continue
#        print str(alpha)+" "+str((alpha*100)%5)
        for z in [1000,2000,3000]:
            flist.append({"mZprime": z, "mDark": m, "rinv": 0.3, "alpha": alpha})
