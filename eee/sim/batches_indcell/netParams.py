
"""
netParams.py 
Specifications for EEE model using NetPyNE


Originally:
High-level specifications for M1 network model using NetPyNE
Contributors: salvadordura@gmail.com
"""

from netpyne import specs

try:
	from __main__ import cfg  # import SimConfig object with params from parent module
except:
	from cfg import cfg  # if no simConfig in parent module, import directly from cfg module

###############################################################################
#
# NETWORK PARAMETERS
#
###############################################################################

netParams = specs.NetParams()   # object of class NetParams to store the network parameters

###############################################################################
# Cell parameters
###############################################################################

# PT cell params (6-comp)
cellRule = netParams.importCellParams(label='EEE_SPI7', conds={'cellType': 'PT', 'cellModel': 'HH_reduced'}, fileName='../cells/SPI7.py', cellName='SPI7')

# define section lists
cellRule['secLists']['alldend'] = ['Bdend1', 'Bdend2', 'Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['apicdend'] = ['Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['basaldend'] = ['Bdend1', 'Bdend2']

for secName,sec in cellRule['secs'].iteritems(): 
	sec['vinit'] = -75.0413649414  # set vinit for all secs
	if secName in cellRule['secLists']['alldend']:  
		sec['mechs']['nax']['gbar'] = cfg.dendNa  # set dend Na gmax for all dends
		sec['mechs']['kdr']['gbar'] = cfg.dendK * sec['mechs']['kdr']['gbar'] 
		sec['mechs']['kap']['gbar'] = cfg.dendK * sec['mechs']['kap']['gbar']  
	if secName in cellRule['secLists']['basaldend']:
		sec["geom"]["Ra"] = cfg.BdendRa

# if cfg.reduced3DGeom: # set 3D pt geom
# 	offset, prevL = 0, 0
# 	for secName, sec in netParams.cellParams[label]['secs'].iteritems():
# 		sec['geom']['pt3d'] = []
# 		if secName in ['soma', 'Adend1', 'Adend2', 'Adend3']:  # set 3d geom of soma and Adends
# 			sec['geom']['pt3d'].append([offset+0, prevL, 0, sec['geom']['diam']])
# 			prevL = float(prevL + sec['geom']['L'])
# 			sec['geom']['pt3d'].append([offset+0, prevL, 0, sec['geom']['diam']])
# 		if secName in ['Bdend']:  # set 3d geom of Bdend
# 			sec['geom']['pt3d'].append([offset+0, 0, 0, sec['geom']['diam']])
# 			sec['geom']['pt3d'].append([offset+sec['geom']['L'], 0, 0, sec['geom']['diam']])
# 			if secName in ['axon']:  # set 3d geom of axon
# 				sec['geom']['pt3d'].append([offset+0, 0, 0, sec['geom']['diam']])
# 			sec['geom']['pt3d'].append([offset+0, -sec['geom']['L'], 0, sec['geom']['diam']])


###############################################################################
# Population parameters
###############################################################################
netParams.popParams['PT5B'] =	{'cellModel': 'HH_reduced', 'cellType': 'PT', 'numCells': 1}


###############################################################################
# Synaptic mechanism parameters
###############################################################################
netParams.synMechParams['NMDA'] = {'mod': 'MyExp2SynNMDABB', 'tau1NMDA': cfg.tau1NMDA, 'tau2NMDA': cfg.tau2NMDA, 'e': 0}
netParams.synMechParams['AMPA'] = {'mod': 'AMPA', 'Alpha': cfg.alphaAMPA, 'Beta': cfg.betaAMPA}


###############################################################################
# Current inputs (IClamp)
###############################################################################
if cfg.addIClamp:	
 	for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
 		ic = getattr(cfg, iclabel, None)  # get dict with params

		# add stim source
		netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'delay': ic['start'], 'dur': ic['dur'], 'amp': ic['amp']}
		
		# connect stim source to target
		netParams.stimTargetParams[iclabel+'_'+ic['pop']] = \
			{'source': iclabel, 'conds': {'popLabel': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}


###############################################################################
# NetStim inputs
###############################################################################
if cfg.addNetStim:
	for nslabel in [k for k in dir(cfg) if k.startswith('NetStim')]:
		ns = getattr(cfg, nslabel, None)

		# add stim source
		netParams.stimSourceParams[nslabel] = {'type': 'NetStim', 'start': ns['start'], 'interval': ns['interval'], 'noise': ns['noise'], 'number': ns['number']}

		# connect stim source to target
		for i in range(len(ns['synMech'])):
			if ns['synMech'][i] == 'AMPA': 
				ns['weight'][i] = ns['weight'][0] * cfg.ratioAMPANMDA
			netParams.stimTargetParams[nslabel+'_'+ns['pop']+'_'+ns['synMech'][i]] = \
                {'source': nslabel, 'conds': {'popLabel': ns['pop']}, 'sec': ns['sec'], 'loc': ns['loc'], 'synMech': ns['synMech'][i], 'weight': ns['weight'][i], 'delay': ns['delay']}


