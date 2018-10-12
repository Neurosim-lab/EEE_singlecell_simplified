"""
my_batches.py 
Batch simulations for EEE project
contact: joe.w.graham@gmail.com
"""

from neuron import h
from collections import OrderedDict
import numpy as np
import os
from cfg import cfg
from inspect import getsourcefile
import sys

try: 
	import batch_utils
except:
	curpath = os.getcwd()
	while os.path.split(curpath)[1] != "sim":
		curpath = os.path.split(curpath)[0]
	sys.path.append(curpath)
	import batch_utils
	
batchoutputdir = "batch_data"
if not os.path.exists(batchoutputdir):
	os.mkdir(batchoutputdir)



###############################################################################
# Batches 
# ------- 
# 
###############################################################################

batches = {}

# Varying synLocMiddle
batch = {}
batch["label"] = "synLocMiddle_ttx"
batch["cfgFile"] = "cfg.py"
batch["netParamsFile"] = "netParams.py"
params = OrderedDict()
params["synLocMiddle"] = [0.2, 0.4, 0.6, 0.8]
batch["params"] = params
batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmpAxon"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = [0.25, 0.75, 1.25, 1.75, 2.25]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp50"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0., 5.0, 10).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp5000"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0., 500.0, 10).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# #cfg.NMDABetaScale  = 14.0
# batch = {}
# batch["label"] = "NMDABetaScale"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["NMDABetaScale"] = [3.5, 7.0, 14.0, 28.0, 56.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# #cfg.glutAmpDecay      = 0.0 # percent/um
# batch = {}
# batch["label"] = "glutAmpDecay"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmpDecay"] = [0.0, 1.0, 5.0, 10.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# #cfg.synLocMiddle      = 0.45 
# batch = {}
# batch["label"] = "synLocMiddle"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["synLocMiddle"] = [0.3, 0.4, 0.5, 0.6, 0.7]
# batch["params"] = params
# batches[batch["label"]] = batch

# #cfg.CdurNMDAScale  = 1.0   # Scales original value of 1.0
# batch = {}
# batch["label"] = "CdurNMDAScale"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["CdurNMDAScale"] = [0.01, 0.1, 1.0, 10.0, 100.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# #cfg.e_pas         = -80.0 # resting membrane potential
# batch = {}
# batch["label"] = "e_pas"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["e_pas"] = [-70.0, -75.0, -80.0, -85.0, -90.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp
# batch = {}
# batch["label"] = "glutAmp2020"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0., 2.0, 20).round(2))
# batch["params"] = params
# batches[batch["label"]] = batch

# # Turning dendritic Na and K on and off for bAPs
# batch = {}
# batch["label"] = "bap"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params[('dendNaScale')] = [0.0, 1.0] 
# params[('dendKScale')]  = [0.0, 1.0] 
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying eeeS apical diam
# batch = {}
# batch["label"] = "basalDiam02"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["basalDiam"] = [5.0, 6.0, 7.0, 8.0, 9.0]
# batch["params"] = params
# batches[batch["label"]] = batch

# # Varying glutAmp and allNaScale (TTX)
# batch = {}
# batch["label"] = "glutAmp_allNaScale"
# batch["cfgFile"] = "cfg.py"
# batch["netParamsFile"] = "netParams.py"
# params = OrderedDict()
# params["glutAmp"] = list(np.linspace(0.1, 1.2, 10).round(2))
# params["allNaScale"] = [0.0, 1.0]
# batch["params"] = params
# batches[batch["label"]] = batch


###############################################################################
# Main code: runs all batches
###############################################################################

if __name__ == '__main__':
	
	import time
	start = time.time()

	# Run all batches
	for label, batch in batches.items():
		print("Running batch with label: " + label)
		batch_utils.run_batch(**batch)

	stop = time.time()
	print
	print("Completed my_batches.py")
	print("Duration (s): " + str(stop-start))
	print
	
	import psutil
	print("Current process:")
	print(psutil.Process())
	
	if 'python' not in psutil.Process().name():
		print("Parent process:")
		print(psutil.Process().parent())
		print("Attempting to terminate grandparent process:")
		print(psutil.Process().parent().parent())
		psutil.Process().parent().parent().terminate()


