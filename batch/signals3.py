#signal dictionary used for ProductionV2

flist = [
#baseline
    {
        "mZprime": 3000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.2,
    },
#vary mZprime
#    { RUN THIS SAMPLE WITH 200 JOBS INSTEAD OF 100 BECAUSE OF LOW STATISTICS
#       "mZprime": 1000,
#        "mDark": 20,
#        "rinv": 0.3,
#        "alpha": 0.2,
#    },
    {
        "mZprime": 2000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.2,
    },
    {
        "mZprime": 4000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.2,
    },
#Vary mDark
    {
        "mZprime": 3000,
        "mDark": 1,
        "rinv": 0.3,
        "alpha": 0.2,
    },
    {
        "mZprime": 3000,
        "mDark": 50,
        "rinv": 0.3,
        "alpha": 0.2,
    },
    {
        "mZprime": 3000,
        "mDark": 100,
        "rinv": 0.3,
        "alpha": 0.2,
    },
# Vary rinv
    {
        "mZprime": 3000,
        "mDark": 20,
        "rinv": 0.1,
        "alpha": 0.2,
    },
    {
        "mZprime": 3000,
        "mDark": 20,
        "rinv": 0.5,
        "alpha": 0.2,
    },
    {
        "mZprime": 3000,
        "mDark": 20,
        "rinv": 0.7,
        "alpha": 0.2,
    },
#vary alpha
    {
        "mZprime": 3000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.1,
    },
    {
        "mZprime": 3000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.5,
    },
    {
        "mZprime": 3000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 1.0,
    }
]
