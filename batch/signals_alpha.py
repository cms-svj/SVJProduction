flist = []

# vary alpha in steps of 0.05
for x in range(5,105,5):
    alpha = x/100.
    for m in [1,5,10,20,50,75,100]:
        for z in [1000,2000,3000]:
            flist.append({"mZprime": z, "mDark": m, "rinv": 0.3, "alpha": alpha})

