#signal dictionary used for ProductionV2

flist = [
#baseline
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.2,
    },
#vary mMediator
    {
        "channel": "s",
        "mMediator": 2000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.2,
    },
    {
        "channel": "s",
        "mMediator": 4000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.2,
    },
#vary mDark
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 1,
        "rinv": 0.3,
        "alpha": 0.2,
    },
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 50,
        "rinv": 0.3,
        "alpha": 0.2,
    },
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 100,
        "rinv": 0.3,
        "alpha": 0.2,
    },
#vary rinv
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 20,
        "rinv": 0.1,
        "alpha": 0.2,
    },
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 20,
        "rinv": 0.5,
        "alpha": 0.2,
    },
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 20,
        "rinv": 0.7,
        "alpha": 0.2,
    },
#vary alpha
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.1,
    },
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 0.5,
    },
    {
        "channel": "s",
        "mMediator": 3000,
        "mDark": 20,
        "rinv": 0.3,
        "alpha": 1.0,
    }
]
