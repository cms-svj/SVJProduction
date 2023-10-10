#signal dictionary used for SUEP production v0.0 

#"cmsRun runSVJ.py model=suep year=2018 config=step1_GEN outpre=step1 mMediator={} mDark={:.1f} temperature={:.1f} decay='{}' part=1 maxEvents={}".format(med_mass,dark_mes_mass,temp,decay_mode,nevents) 

flist = [
#filtered, example
    {
        "mMediator": 125,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPho",
        "filterHT": 1000.,
    },

#baseline
    {
        "mMediator": 1000,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPho",
    },
    {
        "mMediator": 750,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPho",
    },
    {
        "mMediator": 400,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPho",
    },
    {
        "mMediator": 125,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPho",
    },
    {
        "mMediator": 1000,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPhoHad",
    },
    {
        "mMediator": 750,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPhoHad",
    },
    {
        "mMediator": 400,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPhoHad",
    },
    {
        "mMediator": 125,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "darkPhoHad",
    },
    {
        "mMediator": 1000,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "generic",
    },
    {
        "mMediator": 750,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "generic",
    },
    {
        "mMediator": 400,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "generic",
    },
    {
        "mMediator": 125,
        "mDark": 2.0,
        "temperature": 2.0,
        "decay": "generic",
    }
]
