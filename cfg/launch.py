import imp, os, sys
from optparse import OptionParser
import re

# 2016 FastSim
from Samples.miniAOD.Spring16_miniAODv2 import allSamples as Spring16_miniAODv2
# 2016 FullSim
from Samples.miniAOD.Summer16_miniAODv2 import allSamples as Summer16_miniAODv2
from Samples.miniAOD.Summer16_miniAODv3 import allSamples as Summer16_miniAODv3
# 2017 FullSim
from Samples.miniAOD.Fall17_miniAODv2   import allSamples as Fall17_miniAODv2
# 2018 FullSim
from Samples.miniAOD.Autumn18_miniAODv1 import allSamples as Autumn18_miniAODv1
# 2016 Data
from Samples.miniAOD.Run2016_17Jul2018  import allSamples as Run2016_17Jul2018
# 2017 Data
from Samples.miniAOD.Run2017_31Mar2018  import allSamples as Run2017_31Mar2018
# 2018 special HEM Data
from Samples.miniAOD.Run2018_26Sep2018  import allSamples as Run2018_26Sep2018
# 2018 prompt Data (in the end only for D!)
from Samples.miniAOD.Run2018_promptReco import allSamples as Run2018_promptReco
# 2018 rereco Data (for A->C)
from Samples.miniAOD.Run2018_17Sep2018  import allSamples as Run2018_17Sep2018

allSamples  = Spring16_miniAODv2 + Summer16_miniAODv2 + Summer16_miniAODv3 + Fall17_miniAODv2 + Autumn18_miniAODv1
allSamples += Run2016_17Jul2018 + Run2017_31Mar2018 + Run2018_26Sep2018 + Run2018_promptReco + Run2018_17Sep2018

parser = OptionParser(usage="python launch.py [options] component1 [ component2 ...]", \
                          description="Launch heppy jobs with CRAB3. Components correspond to the variables defined in heppy_samples.py (their name attributes)")
parser.add_option("--production_label", dest="production_label",        help="production label", default="heppy")
parser.add_option("--remoteDir",        dest="remoteDir",               help="remote subdirectory", default="")
parser.add_option("--unitsPerJob",      dest="unitsPerJob",             help="Nr. of units (files) / crab job", type="int", default=1)
parser.add_option("--totalUnits",       dest="totalUnits",              help="Total nr. of units (files)", type="int", default=None)
parser.add_option("--era",              dest="era",                     help="Which era?")
parser.add_option("--sample",           dest="sample",                  help="Which sample?")
parser.add_option("--publish",          action='store_true',            help="Publish on dbs?", default=False)
( options, args ) = parser.parse_args()

dataset = None
for sample in allSamples:
    if sample.name == options.sample:
        dataset = sample.DASname

if dataset is None:
    raise NotImplementedError

os.system("scram runtime -sh")
os.system("source /cvmfs/cms.cern.ch/crab3/crab.sh")

#os.environ["CMG_REMOTE_DIR"]  = options.remoteDir
os.environ["CRAB_UNITS_PER_JOB"] = str(options.unitsPerJob)
if options.totalUnits:
    os.environ["CRAB_TOTAL_UNITS"] = str(options.totalUnits)

m=re.match("\/(.*)\/(.*)\/(.*)",dataset)

os.environ["CRAB_PROD_LABEL"]  = m.group(2) + "_" + options.production_label

os.environ["MAOD_SAMPLE_M1"]    = m.group(1)
os.environ["MAOD_SAMPLE_M2"]    = m.group(2)
os.environ["ORIG_PROD_LABEL"]   = options.production_label
os.environ["MAOD_SAMPLE_NAME"]  = m.group(1)+"_"+m.group(2)

os.environ["CRAB_PUBLISH"]      = 'True' if options.publish else 'False'
os.environ["CRAB_DATASET"]      = dataset

print "### Publication is set to", os.environ["CRAB_PUBLISH"]

## Config selection

# fullsim configs
if options.era == 'mc_80X_Summer16':
    os.environ["CMSRUN_CFG"] = "nano_mc_80X_Summer16.py"
elif options.era == 'mc_94X_Summer16_miniAODv3':
    os.environ["CMSRUN_CFG"] = "nano_mc_94X_Summer16_miniAODv3.py"
elif options.era == 'mc_94X_Fall17_miniAODv2':
    os.environ["CMSRUN_CFG"] = "nano_mc_94X_Fall17_miniAODv2.py"
elif options.era == 'mc_102X_Autumn18_miniAODv1':
    os.environ["CMSRUN_CFG"] = "nano_mc_102X_Autumn18_miniAODv1.py"
# fastsim configs
elif options.era == 'mc_80X_fast':
    os.environ["CMSRUN_CFG"] = "nano_mc_fast_80X_Summer16.py"
# data configs
elif options.era == 'data_94X_Run2016':
    os.environ["CMSRUN_CFG"] = "nano_data_94X_Run2016.py"
elif options.era == 'data_94X_Run2017':
    os.environ["CMSRUN_CFG"] = "nano_data_94X_Run2017.py"
elif options.era == 'data_102X_Run2018_promptReco':
    os.environ["CMSRUN_CFG"] = "nano_data_102X_Run2018_promptReco.py"
elif options.era == 'data_102X_Run2018_17Sep2018':
    os.environ["CMSRUN_CFG"] = "nano_data_102X_Run2018_17Sep2018.py"

else:
    raise NotImplementedError

os.system("which crab")
os.system("crab submit -c crabConfig.py")

