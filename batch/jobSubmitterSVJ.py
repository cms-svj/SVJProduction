from Condor.Production.jobSubmitter import *
from SVJ.Production.svjHelper import svjHelper

def makeNameSVJ(self,num):
    return self.name+"_part-"+str(num)

protoJob.makeName = makeNameSVJ

class jobSubmitterSVJ(jobSubmitter):
    def __init__(self):
        super(jobSubmitterSVJ,self).__init__()
        
        self.helper = svjHelper()

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
        parser.add_option("-F", "--firstPart", dest="firstPart", default=1, help="first part to process, in case extending a sample (default = %default)")
        parser.add_option("-N", "--nParts", dest="nParts", default=1, help="number of parts to process (default = %default)")
        parser.add_option("-K", "--skipParts", dest="skipParts", default="", help="comma-separated list of parts to skip, or auto (default = %default)")
        parser.add_option("--indir", dest="indir", default="", help="input file directory (LFN) (default = %default)")
        parser.add_option("--redir", dest="redir", default="root://cmseos.fnal.gov/", help="input file redirector (default = %default)")
        parser.add_option("--inpre", dest="inpre", default="", help="input file prefix (default = %default)")
        parser.add_option("--outpre", dest="outpre", default="", help="output file prefix (required) (default = %default)")
        parser.add_option("--config", dest="config", default="", help="CMSSW config to run (required) (default = %default)")
        parser.add_option("-A", "--args", dest="args", default="", help="additional common args to use for all jobs (default = %default)")
        parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true", help="enable verbose output (default = %default)")

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
            if len(options.config)==0:
                parser.error("Required option: --config [str]")

        if options.skipParts=="auto" and (len(options.inpre)==0 or len(options.indir)==0 or len(options.redir)==0):
            parser.error("Option auto skipParts requires inpre, indir, redir")

        if len(options.skipParts)>0 and options.skipParts!="auto":
            options.skipParts = {int(x) for x in options.skipParts.split(',')}

        self.getpy_weights = "weights_"+options.dicts.replace(".py","")+".txt"
        if options.getpy and os.path.isfile(self.getpy_weights):
            os.remove(self.getpy_weights)
            
    def generateExtra(self,job):
        super(jobSubmitterSVJ,self).generateExtra(job)
        job.patterns.update([
            ("JOBNAME",job.name+"_part-$(Process)_$(Cluster)"),
            ("EXTRAINPUTS","input/args_"+job.name+".txt"),
            ("EXTRAARGS","-j "+job.name+" -p $(Process) -o "+self.output),
        ])
        if "cmslpc" in os.uname()[1]:
            job.appends.append(
                'ONE_DAY = 86400\n'
                'periodic_hold = (\\\n'
                '    ( JobUniverse == 5 && JobStatus == 2 && CurrentTime - EnteredCurrentStatus > $(ONE_DAY) * 1.75 ) || \\\n'
                '    ( JobRunCount > 8 ) || \\\n'
                '    ( JobStatus == 5 && CurrentTime - EnteredCurrentStatus > $(ONE_DAY) * 6 ) || \\\n'
                '    ( DiskUsage > 38000000 ) || \\\n'
                '    ( ResidentSetSize > RequestMemory * 950 ) )\n'
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
        for pdict in flist:
            # create protojob
            job = protoJob()
            # extra attribute to store actual events
            if self.actualEvents: job.actualEvents = 0
            # make name from params
            self.helper.setModel(pdict["mZprime"],pdict["mDark"],pdict["rinv"],pdict["alpha"])
            job.name = self.helper.getOutName(int(self.maxEvents),outpre=self.outpre)
            if self.verbose:
                print "Creating job: "+job.name
            self.generatePerJob(job)

            # for auto skipping
            if self.skipParts=="auto":
                injob = protoJob()
                injob.name = self.helper.getOutName(int(self.maxEvents),outpre=self.inpre)
                infiles = {x.split('/')[-1].replace(".root","") for x in filter(None,os.popen("xrdfs "+self.redir+" ls "+self.indir).read().split('\n'))}

            # write job options to file - will be transferred with job
            if self.prepare:
                with open("input/args_"+job.name+".txt",'w') as argfile:
                    arglist = [
                        "mZprime="+str(pdict["mZprime"]),
                        "mDark="+str(pdict["mDark"]),
                        "rinv="+str(pdict["rinv"]),
                        "alpha="+str(pdict["alpha"]),
                        "maxEvents="+str(self.maxEvents),
                        "outpre="+self.outpre,
                        "config="+self.config,
                    ]
                    if len(self.indir)>0:
                        arglist.append("indir="+self.indir)
                    if len(self.inpre)>0:
                        arglist.append("inpre="+self.inpre)
                    if len(self.args)>0:
                        arglist.insert(0,self.args)
                    if self.cpus>1:
                        arglist.append("threads="+str(self.cpus))
                    if len(self.redir)>1:
                        arglist.append("redir="+self.redir)
                    argfile.write(" ".join(arglist))
            
            # start loop over N jobs
            for iJob in xrange(int(self.nParts)):
                # get real part number
                iActualJob = iJob+self.firstPart

                if (self.skipParts=="auto" and injob.makeName(iActualJob) not in infiles) or (type(self.skipParts)==set and iActualJob in self.skipParts):
                    if self.verbose: print "  skipping part "+str(iActualJob)
                    continue

                if self.actualEvents:
                    from ROOT import TFile,TTree
                    iFile = TFile.Open(self.redir+self.indir+"/"+injob.makeName(iActualJob)+".root")
                    iTree = iFile.Get("Events")
                    job.actualEvents += iTree.GetEntries()

                job.njobs += 1
                if self.count and not self.prepare:
                    continue

                job.nums.append(iActualJob)
            
            # append queue comment
            job.queue = "-queue Process in "+','.join(map(str,job.nums))

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
                iname = job.makeName(ijob)
                if counter==0: outfile.write("readFiles.extend( [\n")
                outfile.write("       '"+self.indir+"/"+iname+".root',\n")
                if counter==254 or ijob==job.nums[-1]:
                    outfile.write("] )\n")
                    counter = 0
                else:
                    counter += 1

        with open(self.getpy_weights,'a') as wfile:
            nEvents = job.actualEvents if self.actualEvents else int(self.maxEvents)*len(job.nums)
            line = '        MCSample("'+job.name+'", "", "", "Constant", '+str(nEvents)+'),';
            wfile.write(line+"\n")
