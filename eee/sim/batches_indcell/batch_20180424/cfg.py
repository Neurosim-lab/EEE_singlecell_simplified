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
cfg.duration = 1000 
cfg.dt = 0.05
cfg.seeds = {'conn': 4321, 'stim': 1234, 'loc': 4321} 
cfg.hParams = {'celsius': 32}  
cfg.verbose = 0
cfg.cvode_active = False
cfg.printRunTime = 0.1
cfg.printPopAvgRates = True


###############################################################################
# Recording 
###############################################################################
cfg.recordTraces = {'V_soma': {'sec': 'soma_2', 'loc': 0.5, 'var': 'v'}}
cfg.recordTraces['V_axon_S'] = {'sec': 'axon_0', 'loc': 0.5, 'var': 'v'}
cfg.recordTraces['V_axon_D'] = {'sec': 'basal_25', 'loc': 0.5, 'var': 'v'}

cfg.bap = False

if cfg.bap:
    for loc in np.arange(0.0, 1.1, 0.1):
        locstr = str(loc).replace(".","")
        cfg.recordTraces['V_dend_' + locstr] = {'sec': 'basal_8', 'loc': loc, 'var': 'v'}
else:
    cfg.recordTraces['V_dend_25'] = {'sec': 'basal_8', 'loc': 0.25, 'var': 'v'}
    cfg.recordTraces['V_dend_50'] = {'sec': 'basal_8', 'loc': 0.50, 'var': 'v'}
    cfg.recordTraces['V_dend_75'] = {'sec': 'basal_8', 'loc': 0.75, 'var': 'v'}

cfg.recordCells = ['all']
cfg.recordStims = False  
cfg.recordStep = 0.1 


###############################################################################
# Saving
###############################################################################
cfg.simLabel = 'batch_rearr'
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

# Diameter of apical_0 in eeeS
cfg.apicalDiam = 6.0
# Diameter of basal_9 in eeeS
cfg.basalDiam = 6.0

# Sodium, potassium, and calcium conductance scaling
#cfg.dendNaScale = 1.0 # Scales dendritic Na conductance
cfg.dendKScale  = 1.0 # Scales dendritic K  conductance
cfg.dendCaScale = 1.0 # Scales dendritic Ca conductance
cfg.allNaScale  = 0.0 # Scales all Na conductances (overrides dendNaScale if not commented)
#cfg.allKScale   = 1.0 # Scales all K  conductances (overrides dendKScale  if not commented)
#cfg.allCaScale  = 1.0 # Scales all Ca conductances (overrides dendCaScale if not commented)

#cfg.allCaScale  = 1.0 

# DMS NMDA params
cfg.NMDAAlphaScale = 1.0   # Scales original value of 4.0
cfg.NMDABetaScale  = 14.0  # Scales original value of 0.0015
cfg.CdurNMDAScale  = 1.0   # Scales original value of 1.0
cfg.NMDAgmax       = 0.01
cfg.ratioAMPANMDA  = 4.0 

# glutamate stim parameters
cfg.synTime           = 200.0
cfg.numSyns           = 24
cfg.numExSyns         = cfg.numSyns
cfg.glutAmp           = 1.0
cfg.glutAmpExSynScale = 1.0
cfg.glutAmpDecay      = 0.0 # percent/um
cfg.synLocMiddle      = 0.45 
cfg.synLocRadius      = 0.15 
cfg.initDelay         = 10.0
cfg.synDelay          = 2.0 # ms/um
cfg.exSynDelay        = 4.0 # ms/um

# other params
cfg.e_pas         = -80.0 # resting membrane potential
cfg.ihScale       = 0.0   # Scales ih conductance
#cfg.gpasSomaScale = 1.0 # Scales soma g_pas
#cfg.dendRaScale   = 1.0
#cfg.dendRmScale   = 1.0
cfg.RaScale       = 1.0  # Scales axial resistance in all secs
cfg.RmScale       = 1.0  # Scales membrane resistance in all secs

cfg.ampIClamp1    = 5.0 
cfg.durIClamp1    = 0.5 

###############################################################################
# NetStim inputs 
###############################################################################
cfg.addNetStim = True

if cfg.bap:
    cfg.addNetStim = False

cfg.NetStimSyn = {'pop': ['eeeD', 'eeeS'], 'loc': list(np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numSyns)), 'sec': 'basal_8', 'synMech': ['NMDA','AMPA'], 'start': cfg.synTime, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': cfg.glutAmp, 'delay': cfg.synDelay}

cfg.NetStimExSyn = {'pop': ['eeeD', 'eeeS'], 'loc': list(np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numExSyns)), 'sec': 'basal_8', 'synMech': ['NMDA'], 'start': cfg.synTime, 'interval': 1000, 'noise': 0.0, 'number': 1, 'weight': cfg.glutAmp * cfg.glutAmpExSynScale, 'delay': cfg.exSynDelay}


###############################################################################
# Current inputs 
###############################################################################
cfg.addIClamp = False

if cfg.bap:
    cfg.addIClamp = True
    cfg.IClamp1 = {'pop': ['eeeD', 'eeeS'], 'sec': 'soma_2', 'loc': 0.5, 'start': 200, 'dur': cfg.durIClamp1, 'amp': cfg.ampIClamp1}
