import os
import subprocess

class PythiaInfoObject:
    def __init__(self):
        self.version = int(next(l for l in subprocess.check_output(['scram', 'tool', 'info', 'pythia8'], cwd=os.getenv('CMSSW_BASE')).decode('utf-8').split('\n') if l.startswith("Ver")).split(" : ")[1].split("-")[0])

    def useSetLambda(self):
        return self.version >= 309

    # EMJ flavored related settings
    def _emjFlavorExternalPatch(self):
        return self.version < 309

    def emjFlavoredFlagname(self)->str:
        return 'altHadronSpecies' if self._emjFlavorExternalPatch() else 'separateFlav'


# provide an instance of info object with version already found (to avoid repeated scram calls)
pythiaInfo = PythiaInfoObject()
