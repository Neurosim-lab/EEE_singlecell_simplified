"""
batches.py 
Batch simulations for EEE project
contact: joe.w.graham@gmail.com
"""

from collections import OrderedDict
from batch_utils import *
import os
from cfg import cfg

batchoutputdir = "batch_data"
if not os.path.exists(batchoutputdir):
	os.mkdir(batchoutputdir)


###############################################################################
# Batches 
# -------
# 
###############################################################################

batches = {}

# # Batch template
# batch = {}
# batch["label"] = "my_batch"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["param1_name"] = [0.0, 0.10, 0.50, 1.0, 10.0]
# params["param2_name"] = [0.0, 0.10, 0.50, 1.0, 10.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# Varying dendNa (gNa in dendrites) against a series of current pulses
batch = {}
batch["label"] = "dendNa_stimamp"
batch["cfgFile"] = "/u/graham/projects/eee/sim/batches/cfg.py"
batch["netParamsFile"] = "/u/graham/projects/eee/sim/batches/netParams.py"
params = OrderedDict()
params["dendNa"] = list(np.array([0.0, 0.10, 0.50, 1.0, 10.0])*cfg.dendNa)
params[("IClamp1", "amp")] = list(np.arange(-2.0, 8.0, 1.0)/10.0)
batch["params"] = params
batches[batch["label"]] = batch

# Varying NMDA Tau2 and glutamate stim
batch = {}
batch["label"] = "NMDATau2_synweight"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["tau2NMDA"] = [75, 150, 300, 600, 1200]
params[('NetStim1', 'weight', 0)] = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
batch["params"] = params
batches[batch["label"]] = batch

# Varying AMPA weight and NMDA weight
batch = {}
batch["label"] = "AMPAw_NMDAw"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams_AMPAw_NMDAw.py"
params = OrderedDict()
# AMPA weight
params[('NetStim1', 'weight', 1)] = [0.0, 0.01, 0.05, 0.1, 1.0]
# NMDA weight
params[('NetStim1', 'weight', 0)] = [0.01, 0.03, 0.05, 0.07, 0.09]
batch["params"] = params
batches[batch["label"]] = batch

# Varying AMPA beta and glut stim -- doesn't seem to work...
batch = {}
batch["label"] = "AMPAbeta"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["betaAMPA"] = [0.0, 0.2, 0.5, 1.0, 10.0]
params[('NetStim1', 'weight', 0)] = [0.01, 0.03, 0.05, 0.07, 0.09]
batch["params"] = params
batches[batch["label"]] = batch

# Varying AMPA/NMDA ratio and glutamate stim
batch = {}
batch["label"] = "ratioAMPANMDA"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["ratioAMPANMDA"] = [0, 1, 10, 25, 50]
params[('NetStim1', 'weight', 0)] = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
batch["params"] = params
batches[batch["label"]] = batch

# Varying synaptic location ratio and glutamate stim
batch = {}
batch["label"] = "synloc"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params[('NetStim1', 'loc')] = [0.1, 0.3, 0.5, 0.7, 0.9]
params[('NetStim1', 'weight', 0)] = [0.04, 0.05, 0.06, 0.07, 0.08]
batch["params"] = params
batches[batch["label"]] = batch

# A range of "glutamate" stimulation amplitudes
batch = {}
batch["label"] = "glut_stim_range"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params[('NetStim1', 'weight', 0)] = list([0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1])
batch["params"] = params
batches[batch["label"]] = batch

# Batch template
batch = {}
batch["label"] = "dendNa_dendK_block_bAP"
batch["cfgFile"] = "cfg_bAP.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params[('dendNa')] = list(np.array([0.0, 1.0])*cfg.dendNa)
params[('dendK')] = list(np.array([0.0, 1.0])*cfg.dendK)
batch["params"] = params
batches[batch["label"]] = batch



###############################################################################
# Main code: runs all batches
###############################################################################

if __name__ == '__main__':
	
	import time
	start = time.time()

	# Run all batches
	for label, batch in batches.items():
		print("Running batch with label: " + label)
		print
		run_batch(**batch)

	stop = time.time()
	print
	print("Completed /u/graham/projects/eee/sim/batches/my_batches.py")
	print("Duration (s): " + str(stop-start))
