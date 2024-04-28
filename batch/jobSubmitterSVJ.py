from Condor.Production.jobSubmitter import *
from SVJ.Production.svjHelper import svjHelper
from SVJ.Production.suepHelper import suepHelper
from SVJ.Production.emjHelper import emjHelper

def makeNameSVJ(self,num,useFolders=False):
    return self.name+("/" if useFolders else "_")+"part-"+str(num)

protoJob.makeName = makeNameSVJ

class jobSubmitterSVJ(jobSubmitter):
    def __init__(self,argv=None,parser=None):
        super(jobSubmitterSVJ,self).__init__(argv,parser)

        if self.model=="svj":
            self.helper = svjHelper()
        elif self.model=="suep":
            self.helper = suepHelper()
        elif self.model=="emj":
            self.helper = emjHelper()

    def addDefaultOptions(self,parser):
        super(jobSubmitterSVJ,self).addDefaultOptions(parser)
        parser.add_option("-y", "--getpy", dest="getpy", default=False, action="store_true", help="make python file list for ntuple production (default = %default)")
        parser.add_option("--actualEvents", dest="actualEvents", default=False, action="store_true", help="count actual number of events from each input file (for python file list) (default = %default)")
        self.modes.update({
            "getpy": 1,
        })

    def addExtraOptions(self,parser):
        super(jobSubmitterSVJ,self).addExtraOptions(parser)

        parser.add_option("-d", "--dicts", dest="dicts", default="", help="file with list of input dicts; each dict contains signal parameters (required) (default = %default)")
        parser.add_option("-o", "--output", dest="output", default="", help="path to output directory in which root files will be stored (required) (default = %default)")
        parser.add_option("-E", "--maxEvents", dest="maxEvents", default=1, help="number of events to process per job (default = %default)")
        parser.add_option("-I", "--maxEventsIn", dest="maxEventsIn", default=-1, help="number of events from input file (if different from -E) (default = %default)")
        parser.add_option("-F", "--firstPart", dest="firstPart", default=1, help="first part to process, in case extending a sample (default = %default)")
        parser.add_option("-N", "--nParts", dest="nParts", default=1, help="number of parts to process (default = %default)")
        parser.add_option("-K", "--skipParts", dest="skipParts", default="", help="comma-separated list of parts to skip, or auto (default = %default)")
        parser.add_option("-f", "--use-folders", dest="useFolders", default=False, action="store_true", help="store the output in a folder for each sample (default = %default)")
        parser.add_option("--indir", dest="indir", default="", help="input file directory (LFN) (default = %default)")
        parser.add_option("--redir", dest="redir", default="root://cmseos.fnal.gov/", help="input file redirector (default = %default)")
        parser.add_option("--inpre", dest="inpre", default="", help="input file prefix (default = %default)")
        parser.add_option("--outpre", dest="outpre", default="", help="output file prefix (required) (default = %default)")
        parser.add_option("--year", dest="year", default=0, help="which year to simulate (default = %default)")
        parser.add_option("--config", dest="config", default="", help="CMSSW config to run (required unless madgraph) (default = %default)")
        parser.add_option("--gridpack", dest="gridpack", default=False, action="store_true", help="gridpack production (default = %default)")
        parser.add_option("--madgraph", dest="madgraph", default=False, action="store_true", help="sample generated w/ madgraph (rather than pythia) (default = %default)")
        parser.add_option("--model", dest="model", default="svj", choices=["svj","suep","emj"], help="model to simulate (default = %default)")
        parser.add_option("-A", "--args", dest="args", default="", help="additional common args to use for all jobs (default = %default)")
        parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="enable verbose output (default = %default)")
        parser.add_option("--chain-name", dest="chainName", default="", help="value for job.chainName (default = %default)")

    def runPerJob(self,job):
        super(jobSubmitterSVJ,self).runPerJob(job)
        if self.getpy:
            self.doPy(job)

    def checkDefaultOptions(self,options,parser):
        super(jobSubmitterSVJ,self).checkDefaultOptions(options,parser)
        if (options.actualEvents and not options.getpy):
            parser.error("Option --actualEvents only allowed for -y mode")
        if (options.actualEvents and options.skipParts!="auto"):
            parser.error("Option --actualEvents requires auto skipParts")

    def checkExtraOptions(self,options,parser):
        super(jobSubmitterSVJ,self).checkExtraOptions(options,parser)

        if options.dicts is None or len(options.dicts)==0:
            parser.error("Required option: --dicts [dict]")

        if options.prepare or not options.count:
            if len(options.outpre)==0:
                parser.error("Required option: --outpre [str]")
        if options.prepare or not (options.count or options.getpy):
            if len(options.output)==0:
                parser.error("Required option: --output [directory]")
            if len(options.config)==0 and not options.gridpack:
                parser.error("Required option: --config [str]")

        if options.skipParts=="auto" and (len(options.inpre)==0 or len(options.indir)==0 or (options.indir.startswith("/store/") and len(options.redir)==0)):
            parser.error("Option auto skipParts requires inpre, indir, (redir)")

        if len(options.skipParts)>0 and options.skipParts!="auto":
            options.skipParts = {int(x) for x in options.skipParts.split(',')}

        self.getpy_weights = "weights_"+options.dicts.replace(".py","")+".txt"
        if options.getpy and os.path.isfile(self.getpy_weights):
            os.remove(self.getpy_weights)

        options.maxEvents = int(options.maxEvents)
        options.maxEventsIn = int(options.maxEventsIn)

    def generateExtra(self,job):
        super(jobSubmitterSVJ,self).generateExtra(job)
        job.patterns.update([
            ("JOBNAME",job.name+"_part-$(Process)_$(Cluster)"),
            ("EXTRAINPUTS","input/args_"+job.name+".txt"),
            ("EXTRAARGS","-j "+job.name+" -p $(Process) -o "+self.output+(" -m madgraph" if self.gridpack else "")+(" -f " if self.useFolders else "")),
        ])
        if "cmslpc" in os.uname()[1]:
            job.appends.append(
                'ONE_DAY = 86400\n'
                'periodic_hold = (\\\n'
                '    ( JobUniverse == 5 && JobStatus == 2 && CurrentTime - EnteredCurrentStatus > $(ONE_DAY) * 1.75 ) || \\\n'
                '    ( JobRunCount > 8 ) || \\\n'
                '    ( JobStatus == 5 && CurrentTime - EnteredCurrentStatus > $(ONE_DAY) * 6 ) || \\\n'
                '    ( DiskUsage > 38000000 ) || \\\n'
                '    ( ifthenelse(ResidentSetSize isnt undefined, ResidentSetSize > RequestMemory * 950, false) ) )\n'
                'periodic_hold_reason = strcat("Job held by PERIODIC_HOLD due to ", \\\n'
                '    ifThenElse(( JobUniverse == 5 && JobStatus == 2 && CurrentTime - EnteredCurrentStatus > $(ONE_DAY) * 1.75 ), "runtime longer than 1.75 days", \\\n'
                '    ifThenElse(( JobRunCount > 8 ), "JobRunCount greater than 8", \\\n'
                '    ifThenElse(( JobStatus == 5 && CurrentTime - EnteredCurrentStatus > $(ONE_DAY) * 6 ), "hold time longer than 6 days", \\\n'
                '    ifThenElse(( DiskUsage > 38000000 ), "disk usage greater than 38GB", \\\n'
                '                strcat("memory usage ",ResidentSetSize," greater than requested ",RequestMemory*1000))))), ".")'
            )

    def generateSubmission(self):
        # get dicts
        flist = __import__(self.dicts.replace(".py","")).flist
        # loop over dicts
        svj_extras = ["boost","boostvar","yukawa","nMediator","sepproc"]
        for pdict in flist:
            # create protojob
            job = protoJob()
            # extra attribute to store max events (in case of pseudo-scan)
            job.maxEvents = self.maxEvents
            if "maxEvents" in pdict: job.maxEvents = pdict["maxEvents"]
            # extra attribute to store actual events
            if self.actualEvents: job.actualEvents = 0
            # make name from params or scan/fragment
            if "fragment" in pdict:
                self.helper.generate = True
                outpre = self.outpre+"_"+pdict["fragment"]
                inpre = self.inpre+"_"+pdict["fragment"]
                signal = False
            elif "scan" in pdict:
                outpre = self.outpre+"_"+pdict["scan"]
                inpre = self.inpre+"_"+pdict["scan"]
                signal = False
            else:
                if self.model=="svj":
                    model_args = [pdict["channel"],pdict["mMediator"],pdict["mDark"],pdict["rinv"],pdict["alpha"]]
                    model_kwargs = {}
                    for key in svj_extras:
                        if key in pdict: model_kwargs[key] = pdict[key]
                    model_kwargs["generate"] = not (self.madgraph or self.gridpack)
                    self.helper.setModel(*model_args,**model_kwargs)
                elif self.model=="suep":
                    self.helper.setModel(pdict["channel"],pdict["mMediator"],pdict["mDark"],pdict["temperature"],pdict["decay"])
                elif self.model=="emj":
                    self.helper.setModel(pdict["mMediator"],pdict["mDark"],pdict["kappa"],pdict["mode"],pdict["type"],pdict["channel"])
                outpre = self.outpre
                inpre = self.inpre
                signal = True
            job.name = self.helper.getOutName(events=job.maxEvents,outpre=outpre,signal=signal,gridpack=self.gridpack)
            if len(self.chainName)>0: job.chainName = self.chainName
            if self.verbose:
                print("Creating job: "+job.name)
            self.generatePerJob(job)

            # for auto skipping
            if self.skipParts=="auto":
                injob = protoJob()
                injob.name = self.helper.getOutName(events=self.maxEventsIn if self.maxEventsIn>0 else job.maxEvents,outpre=inpre,signal=signal)
                injobdir = self.indir
                if self.useFolders: injobdir += "/"+injob.name
                infiles = {self.finishedToJobName(x if injob.name in x else injob.name+"_"+x) for x in generalized_ls(self.redir,injobdir)}

            # set this after making name to avoid duplicating pythia8 in name
            if "scan" in pdict:
                self.helper.generate = True

            # write job options to file - will be transferred with job
            if self.prepare:
                with open("input/args_"+job.name+".txt",'w') as argfile:
                    arglist = []
                    if "fragment" in pdict:
                        arglist = [
                            "fragment="+str(pdict["fragment"]),
                        ]
                    elif "scan" in pdict:
                        arglist = [
                            "scan="+str(pdict["scan"]),
                        ]
                    elif self.model=="svj":
                        arglist = [
                            "model=svj",
                            "channel="+str(pdict["channel"]),
                            "mMediator="+str(pdict["mMediator"]),
                            "mDark="+str(pdict["mDark"]),
                            "rinv="+str(pdict["rinv"]),
                            "alpha="+str(pdict["alpha"]),
                        ]
                        for extra in svj_extras+["filterZ2"]:
                            if extra in pdict: arglist.append("{}={}".format(extra,str(pdict[extra])))
                    elif self.model=="suep":
                        arglist = [
                            "model=suep",
                            "channel="+str(pdict["channel"]),
                            "mMediator="+str(pdict["mMediator"]),
                            "mDark="+str(pdict["mDark"]),
                            "temperature="+str(pdict["temperature"]),
                            "decay="+str(pdict["decay"]),
                        ]
                        if "filterHT" in pdict:
                            if pdict["filterHT"] > 0:
                                arglist.append("filterHT=%1.3f"%pdict["filterHT"])
                    elif self.model=="emj":
                        arglist = [
                            "model=emj",
                            "channel="+str(pdict["channel"]),
                            "mMediator="+str(pdict["mMediator"]),
                            "mDark="+str(pdict["mDark"]),
                            "kappa="+str(pdict["kappa"]),
                            "mode="+str(pdict["mode"]),
                            "type="+str(pdict["type"]),
                        ]
                    if "scout" in pdict:
                        arglist.append("scout="+str(pdict["scout"]))
                    arglist.extend([
                        "maxEvents="+str(job.maxEvents),
                        "outpre="+self.outpre,
                        "year="+str(self.year),
                    ])
                    if not self.gridpack:
                        arglist.append("config="+self.config)
                    if self.madgraph or self.gridpack:
                        arglist.append("madgraph=1")
                    if len(self.indir)>0:
                        arglist.append("indir="+self.indir)
                    if len(self.inpre)>0:
                        arglist.append("inpre="+self.inpre)
                    if len(self.args)>0:
                        arglist.insert(0,self.args)
                    if int(self.cpus)>1:
                        arglist.append("threads="+str(self.cpus))
                    if len(self.redir)>1:
                        arglist.append("redir="+self.redir)
                    if self.maxEventsIn>0:
                        arglist.append("maxEventsIn="+str(self.maxEventsIn))
                    argfile.write(" ".join(arglist))

            # start loop over N jobs
            for iJob in six.moves.range(int(self.nParts)):
                # get real part number
                iActualJob = iJob+int(self.firstPart)

                if (self.skipParts=="auto" and injob.makeName(iActualJob) not in infiles) or (type(self.skipParts)==set and iActualJob in self.skipParts):
                    if self.verbose: print("  skipping part "+str(iActualJob)+" ("+injob.makeName(iActualJob)+")")
                    continue

                if self.actualEvents:
                    from ROOT import TFile,TTree
                    iFile = TFile.Open(self.redir+self.indir+"/"+injob.makeName(iActualJob,self.useFolders)+".root")
                    iTree = iFile.Get("Events")
                    job.actualEvents += iTree.GetEntries()

                job.njobs += 1
                if self.count and not self.prepare:
                    continue

                job.nums.append(iActualJob)

            # append queue comment
            job.queue = '-queue Process in '+','.join(map(str,job.nums))

            # store protojob
            self.protoJobs.append(job)

    def doPy(self,job):
        with open(job.name.replace('.','p')+"_cff.py",'w') as outfile:
            outfile.write("import FWCore.ParameterSet.Config as cms\n\n")
            outfile.write("maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )\n")
            outfile.write("readFiles = cms.untracked.vstring()\n")
            outfile.write("secFiles = cms.untracked.vstring()\n")
            outfile.write("source = cms.Source (\"PoolSource\",fileNames = readFiles, secondaryFileNames = secFiles)\n")
            counter = 0
            # swap outpre with inpre - list of input files
            job.name = job.name.replace(self.outpre,self.inpre)
            # split into chunks of 255
            for ijob in job.nums:
                iname = job.makeName(ijob,self.useFolders)
                if counter==0: outfile.write("readFiles.extend( [\n")
                outfile.write("       '"+("file:" if not self.indir.startswith("/store/") else "")+self.indir+"/"+iname+".root',\n")
                if counter==254 or ijob==job.nums[-1]:
                    outfile.write("] )\n")
                    counter = 0
                else:
                    counter += 1

        with open(self.getpy_weights,'a') as wfile:
            nEvents = job.actualEvents if self.actualEvents else int(job.maxEvents)*len(job.nums)
            line = '    MCSample("'+job.name+'", "", "", "Constant", '+str(nEvents)+'),';
            wfile.write(line+"\n")

    def findFinishedJob(self,job):
        if not hasattr(self,"checkedDirectories"):
            setattr(self,"checkedDirectories",set())

        if hasattr(self,"output"):
            bottomDir = self.output + "/" + job.name
            if bottomDir not in self.checkedDirectories:
                finishedFilesPerJob = {self.finishedToJobName(finished) for finished in generalized_ls(bottomDir,"",self.minDate,self.maxDate)}
                self.filesSet |= set(finishedFilesPerJob)
                self.checkedDirectories.add(bottomDir)

    def doMissing(self,job):
        # add to finished files in case the files are folderized
        if self.useFolders:
            self.findFinishedJob(job)

        # now do the rest of missing mode
        super(jobSubmitterSVJ,self).doMissing(job)

    def doClean(self,job):
        # add to finished files in case the files are folderized
        if self.useFolders:
            self.findFinishedJob(job)

        # now do the rest of clean mode
        super(jobSubmitterSVJ,self).doClean(job)

    def finishedToJobName(self,val):
        if self.useFolders:
            subval = "_".join(val.split("/")[-2:])
        else:
            subval = val.split("/")[-1]
        return subval.replace(".root","")
