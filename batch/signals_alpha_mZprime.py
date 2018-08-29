flist = []

alpha = 0.5
for z in [1000,1500,2000,2500,3000,3500,4000]:
    for m in [5,10,20,50,75,100]:
        flist.append({"mZprime": z, "mDark": m, "rinv": 0.3, "alpha": alpha})

