"""
cfg.py 

Simulation configuration 

Contributors: salvadordura@gmail.com
"""

from netpyne import specs
import numpy as np

cfg = specs.SimConfig()  

###############################################################################
#
# SIMULATION CONFIGURATION
#
###############################################################################

cfg.checkErrors = True

###############################################################################
# Run parameters
###############################################################################
cfg.duration = 1200 
cfg.dt = 0.05
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 34, 'v_init': -80}  
cfg.verbose = 0
cfg.cvode_active = False
cfg.printRunTime = 0.1
cfg.printPopAvgRates = True


###############################################################################
# Recording 
###############################################################################
cfg.recordTraces = {'V_soma': {'sec': 'soma', 'loc': 0.5, 'var': 'v'}}
cfg.recordTraces['V_Bdend1'] = {'sec': 'Bdend1', 'loc': 0.5, 'var': 'v'}
cfg.recordTraces['V_Bdend2'] = {'sec': 'Bdend2', 'loc': 0.5, 'var': 'v'}
cfg.recordCells = ['e2s', 'dms']
cfg.recordStims = False  
cfg.recordStep = 0.1 


###############################################################################
# Saving
###############################################################################
cfg.simLabel = 'spillover'
cfg.saveFolder = 'batch_data'
cfg.savePickle = False
cfg.saveJson = True
cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']


###############################################################################
# Analysis and plotting 
###############################################################################
cfg.analysis['plotTraces'] = {'include': ['all'], 'oneFigPer': 'cell', 'saveFig': True, 
                              'showFig': False, 'figSize': (10,8), 'timeRange': [0,cfg.duration]}


###############################################################################
# Parameters
###############################################################################

# Exp2Syn NMDA params
cfg.tau1NMDAscale = 1.0 # Scales original value of 15 ms to 15 ms
cfg.tau2NMDAscale = 4.0 # Scales original value of 150 ms to 600 ms

cfg.NMDAAlphaScale = 1.0 # Scales original value of 4.0 to 4.0
cfg.NMDABetaScale  = 0.15 # Scales original value of 0.01 to 0.0015

# DMS NMDA params
cfg.CdurNMDAScale = 40.0   # Scales original value of 1.0
cfg.CdurNMDAesScale = 1.0 # Scales original value of 1.0

cfg.CmaxNMDAScale = 1.0
cfg.CmaxNMDAesScale = 1.0

# Other params
cfg.ratioAMPANMDA = 0.2
cfg.glutAmp = 0.1 

# glutLoc should be a spine number (0 to 255)
# glutSpread should be the number of spines to spread to 
#  (starts at glutLoc spine and increases; shouldn't come to > spine 255)
cfg.glutSpine     = 50
cfg.glutSpread    = 1

cfg.recordTraces['V_spine'] = {'sec': 'head_'+str(cfg.glutSpine), 'loc': 0.5, 'var': 'v'}

# spillDelay is time to reach dendritic shaft in ms
# spillFraction is the percentage of weight reaching the dendritic shaft
cfg.spillDelay    = 10.0
cfg.spillFraction = 0.0



###############################################################################
# NetStim inputs 
###############################################################################
cfg.addNetStim = 1

cfg.NetStim1 = {'pop': ['dms'], 'loc': 0.99999, 'sec': 'spineheads', 'synMech': ['NMDA','AMPA'], 'start': 200, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': [cfg.glutAmp/cfg.glutSpread, cfg.glutAmp*cfg.ratioAMPANMDA/cfg.glutSpread], 'delay': 1.0}

cfg.NetStim2 = {'pop': ['e2s'], 'loc': 0.99999, 'sec': 'spineheads', 'synMech': ['NMDAe2s','AMPA'], 'start': 200, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': [cfg.glutAmp/cfg.glutSpread, cfg.glutAmp*cfg.ratioAMPANMDA/cfg.glutSpread], 'delay': 1.0}

