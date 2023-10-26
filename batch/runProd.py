import os,subprocess,shlex,glob
from copy import deepcopy
from collections import OrderedDict, defaultdict
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, RawTextHelpFormatter, RawDescriptionHelpFormatter, _AppendAction

# convenience definition
# (from ConfigArgParse)
class ArgumentDefaultsRawHelpFormatter(
    ArgumentDefaultsHelpFormatter,
    RawTextHelpFormatter,
    RawDescriptionHelpFormatter):
    """HelpFormatter that adds default values AND doesn't do line-wrapping"""
pass

def parse_pos_name(val):
    try:
        pos_name = int(val)
    except:
        pos_name = str(val)
    return pos_name

class ModifyAction(_AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, None)
        items = self._copy_items(items)
        results = self.parse_local(values) if self.dest=="local" else self.parse_modify(values)
        items.extend(results)
        setattr(namespace, self.dest, items)

    _allowed_ops = OrderedDict([
        ("insert", list.insert),
        ("remove", list.__delitem__),
        ("change", list.__setitem__),
    ])

    def parse_modify(self, args):
        results = []
        counter = 0
        while counter < len(args):
            result = []

            # operation
            op = str(args[counter])
            if op not in self._allowed_ops:
                raise ValueError("Unknown operation: {}".format(op))
            result.append(op)
            counter += 1

            # pos/name
            pos_name = parse_pos_name(args[counter])
            result.append(pos_name)
            counter += 1

            # no third arg for remove
            if op!="remove":
                step = str(args[counter])
                result.append(step)
                counter += 1

            results.append(result)
        return results

    # no loop because fixed nargs=2
    def parse_local(self, args):
        results = []
        counter = 0

        # pos/name
        pos_name = parse_pos_name(args[counter])
        results.append(pos_name)
        counter += 1

        # arguments
        opts = str(args[counter])
        results.append(opts)
        counter += 1

        return [results]

    # from argparse
    def _copy_items(self, items):
        if items is None:
            return []
        # The copy module is used only in the 'append' and 'append_const'
        # actions, and it is needed only when the default value isn't a list.
        # Delay its import for speeding up the common case.
        if type(items) is list:
            return items[:]
        import copy
        return copy.copy(items)

if __name__=="__main__":
    predefined_chains = OrderedDict([
        ("P8v10",["GEN-SIM","DIGI","RECO","MINIAODv3","NANOAODv10"]),
        ("MGv10",["LHE-GEN-SIM","DIGI","RECO","MINIAODv3","NANOAODv10"]),
        ("P8v11",["GEN-SIM","DIGI","RECO","MINIAODv3","NANOAODv11"]),
        ("MGv11",["LHE-GEN-SIM","DIGI","RECO","MINIAODv3","NANOAODv11"]),
        ("P8v12",["GEN-SIM","DIGI","RECO","MINIAODv4","NANOAODv12"]),
        ("MGv12",["LHE-GEN-SIM","DIGI","RECO","MINIAODv4","NANOAODv12"]),
    ])
    desc = ["runProd.py prepares and executes batch submission for a chain of steps to produce specified signal samples.","Several predefined chains are provided (and can be modified with command-line options):"]
    desc += ["{}: {}".format(key, ", ".join("{}. {}".format(istep, step) for istep, step in enumerate(val))) for key,val in predefined_chains.items()]
    desc = '\n'.join(desc)

    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsRawHelpFormatter,
        description=desc,
    )
    # chain-specific arguments
    group_chain = parser.add_mutually_exclusive_group(required=True)
    group_chain.add_argument("-P", "--predefined", type=str, choices=[key for key in predefined_chains], help="choose predefined chain")
    group_chain.add_argument("-C", "--custom", type=str, nargs='+', help="specify steps for custom chain")
    parser.add_argument("-M", "--modify", metavar=("op pos/name [step]"), action=ModifyAction, nargs='+', default=[],
        help="\n".join([
            "modify predefined chain:",
            "  op = {}".format(', '.join(ModifyAction._allowed_ops)),
            "  pos/name = position (number) or name of step in predefined chain",
            "  [step] = name of step to insert/substitute",
            "multiple ops can be given in one call, or option can be called multiple times",
            "ops will be applied in order provided"
        ])
    )
    parser.add_argument("-S", "--store", metavar="pos/name", type=parse_pos_name, default=["MINIAODv3"], nargs='*', help="store output for intermediate step(s) (position or name) (-1 or all: store all steps' output)")
    parser.add_argument("-G", "--global", dest="global_opts", type=str, default="", help='global arguments for submitJobs (use syntax: -G="...")')
    parser.add_argument("-L", "--local", metavar=("pos/name","LOCAL"), action=ModifyAction, nargs=2, default=[], help='local arguments for submitJobs for a specific step')
    # arguments forward from (or similar to) jobSubmitter or createChain
    parser.add_argument("-n", "--name", dest="name", type=str, required=True, help="base-level name for chain job")
    parser.add_argument("-k", "--keep", default=False, action="store_true", help="keep existing tarball(s) for job submission")
    parser.add_argument("-s", "--submit", default=False, action="store_true", help="submit chain jdl(s)")
    parser.add_argument("-y", "--year", type=str, required=True, help="which year to simulate")
    parser.add_argument("-o", "--output", type=str, required=True, help="base-level output directory")
    parser.add_argument("-t", "--tardir", type=str, required=True, help="xrdcp address for CMSSW tarballs")
    parser.add_argument("-c", "--checkpoint", default=False, action="store_true", help="enable checkpointing (if a job fails, save output files from previous job in chain)")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="print verbose output")
    args = parser.parse_args()

    # clone & apply modifications to predefined chain
    chain = None
    if args.custom is not None:
        if len(args.modify)>0:
            parser.error("-M/--modify should only be used with -p/--predefined.")
        chain = args.custom[:]
    else:
        chain = predefined_chains[args.predefined]
        for mod in args.modify:
            if not isinstance(mod[1],int):
                mod[1] = chain.index(mod[1])
            ModifyAction._allowed_ops[mod[0]](chain, *mod[1:])

    # set up list of intermediate output stores and other options
    if -1 in args.store or "all" in args.store: keep_output = chain[:]
    else: keep_output = [pos_name if isinstance(pos_name,str) else chain[pos_name] for pos_name in args.store]
    local_opts = defaultdict(str)
    for key,val in args.local:
        local_opts[key if isinstance(key,str) else chain[key]] = val

    # list of CMSSW versions for different steps
    env_keys = ["CMSSW_VERSION", "SCRAM_ARCH"]
    this_env = {key:os.getenv(key) for key in env_keys}
    step_versions = {
        "2022": defaultdict(lambda: {"CMSSW_VERSION": "CMSSW_12_4_15"})
    }
    step_versions["2022"]["NANOAODv11"] = {"CMSSW_VERSION": "CMSSW_12_6_5"}
    step_versions["2022"]["MINIAODv4"] = {"CMSSW_VERSION": "CMSSW_13_0_13"}
    step_versions["2022"]["NANOAODv12"] = {"CMSSW_VERSION": "CMSSW_13_0_13"}
    step_versions["2022EE"] = deepcopy(step_versions["2022"])

    # create and copy tarball for other CMSSW versions
    extra_tarballs = []
    for step in chain:
        step_version = step_versions[args.year][step]
        if step_version["CMSSW_VERSION"]==this_env["CMSSW_VERSION"]:
            step_version["SCRAM_ARCH"] = this_env["SCRAM_ARCH"]
        else:
            CMSSW_PATH = os.path.expandvars("$CMSSW_BASE/../{0}".format(step_version["CMSSW_VERSION"]))
            SCRAM_PATH = glob.glob(CMSSW_PATH+"/lib/*")
            if len(SCRAM_PATH)==0:
                raise RuntimeError("Can't find SCRAM_ARCH for dir {}".format(CMSSW_PATH))
            step_version["SCRAM_ARCH"] = SCRAM_PATH[0].split("/")[-1]

            if not args.keep:
                if step_version["CMSSW_VERSION"] not in extra_tarballs:
                    cmd = [
                        "CUR_DIR=$PWD",
                        "cd $CMSSW_BASE/../{0}/src/SVJ/Production/batch",
                        "eval `scramv1 runtime -sh`",
                        "./checkVomsTar.sh -i {1}"
                    ]
                    cmd = '\n'.join(cmd).format(step_version["CMSSW_VERSION"], args.tardir)
                    stdout = None
                    if args.verbose: print(cmd)
                    else: stdout = open(os.devnull, 'w')
                    subprocess.check_call(cmd, shell=True, stdout=stdout, stderr=subprocess.STDOUT)
                    extra_tarballs.append(step_version["CMSSW_VERSION"])

    # create step JDLs (one list per job)
    jdls = []
    # also track logfile names for first jobs
    logs = []
    prepare = False
    for istep,step in enumerate(chain):
        prev_step = chain[istep-1] if istep>0 else ""
        # compose arguments to jobSubmitter
        opts = [
            args.global_opts,
            local_opts[step],
            "--gridpack" if step=="GRIDPACK" else "",
            "--no-queue-arg",
            "--year {}".format(args.year),
            # chain-specific arguments created automatically
            "-t {}".format(args.tardir),
            "--outpre step_{0} --config step_{0} --output {1}/{0}".format(step,args.output),
            "--inpre step_{} --indir {}".format(
                prev_step,
                "../job{}".format(istep-1) if prev_step not in keep_output else "{1}/{0}".format(prev_step,args.output)
            ) if istep>0 else "",
            "--intermediate" if step not in keep_output and istep<len(chain)-1 else "",
            "-k" if args.keep or istep>0 else "",
            "-v" if args.verbose else "",
        ]
        # aggregate then re-split, removing empty entries
        opts = shlex.split(" ".join(opt for opt in opts if len(opt)>0))
        if args.verbose: print(opts)

        # use current jobSubmitterSVJ, but make it specify the correct CMSSW version in JDL
        step_version = step_versions[args.year][step]
        if step_version["CMSSW_VERSION"]!=this_env["CMSSW_VERSION"]:
            for key in env_keys:
                os.environ[key] = step_version[key]

        from jobSubmitterSVJ import jobSubmitterSVJ
        jobSub = jobSubmitterSVJ(argv=opts)
        if jobSub.submit:
            raise RuntimeError("Do not activate jobSubmitter submit mode when creating a production chain")
        # if just running e.g. count mode, no JDLs will be created
        if jobSub.prepare:
            prepare = True
        # -k (keep) is assumed in jobSubmitter for non-submit modes; disable it to generate tarball
        if not args.keep and prepare and istep==0:
            jobSub.keep = False
        jobSub.run()

        # initialize list of lists
        if istep==0: jdls = [[] for _ in range(len(jobSub.protoJobs))]
        # get JDL names
        for ijob,job in enumerate(jobSub.protoJobs):
            jdls[ijob].append(job.jdl)
            if istep==0: logs.append(job.name)

        # revert any env changes
        if step_version["CMSSW_VERSION"]!=this_env["CMSSW_VERSION"]:
            for key in env_keys:
                os.environ[key] = this_env[key]

    # create chain jdl
    if prepare:
        for ijob,job in enumerate(jdls):
            from createChain import createChain
            name = args.name+logs[ijob]
            createChain(job, name, logs[ijob], args.checkpoint)
            chain_jdl = "jobExecCondor_{}.jdl".format(name)
            if args.submit:
                cmd = "condor_submit {}".format(chain_jdl)
                if args.verbose: print(cmd)
                os.system(cmd)

