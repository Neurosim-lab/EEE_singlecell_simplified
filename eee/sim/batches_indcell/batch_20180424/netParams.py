"""
netParams.py 
Specifications for EEE model using NetPyNE

Originally:
High-level specifications for M1 network model using NetPyNE
Contributors: salvadordura@gmail.com
"""

from netpyne import specs, sim
import os
import numpy as np
from neuron import h
import sys

# Find path to cells directory
curpath = os.getcwd()
while os.path.split(curpath)[1] != "sim":
    oldpath = curpath
    curpath = os.path.split(curpath)[0]
    if oldpath == curpath:
        raise Exception("Couldn't find cells directory. Try running from within eee/sim file tree.")
cellpath = os.path.join(curpath, "cells")

try:
    import batch_utils
except:
    sys.path.append(curpath)
    import batch_utils

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    print("Couldn't import cfg from __main__")
    print("Attempting to import cfg from cfg.")
    try:
        from cfg import cfg  # if no simConfig in parent module, import directly from cfg module
    except:
        print("Couldn't import cfg from cfg")
        cfg, null = sim.readCmdLineArgs()

###############################################################################
#
# NETWORK PARAMETERS
#
###############################################################################

netParams = specs.NetParams()   # object of class NetParams to store the network parameters
netParams.defaultThreshold = -20.0

###############################################################################
# Cell parameters
###############################################################################

# Detailed EEE cell model
eeeD_path = os.path.join(cellpath, 'eeeD.py')
cellRule = netParams.importCellParams(label='eeeD', conds={'cellType': 'eeeD', 'cellModel': 'PFC_full'}, fileName=eeeD_path, cellName='MakeCell')

# Simplified EEE cell model
eeeS_path = os.path.join(cellpath, 'eeeS.py')
cellRule = netParams.importCellParams(label='eeeS', conds={'cellType': 'eeeS', 'cellModel': 'PFC_simp'}, fileName=eeeS_path, cellName='MakeCell')

# define section lists
cellRule['secLists']['alldend'] = ['Bdend1', 'Bdend2', 'Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['apicdend'] = ['Adend1', 'Adend2', 'Adend3']
cellRule['secLists']['basaldend'] = ['Bdend1', 'Bdend2']

# apply values to parameters
for cell_label, cell_params in netParams.cellParams.iteritems():

    for secName,sec in cell_params['secs'].iteritems(): 
        sec['vinit'] = cfg.e_pas  # set vinit for all secs

        #if cell_label == "eeeS":

        if secName == "apical_0":
            if hasattr(cfg, 'apicalDiam'):
                orig_diam = sec['geom']['diam']
                print("eeeS original apical diam = " + str(orig_diam))
                sec['geom']['diam'] = cfg.apicalDiam
                print("eeeS new apical diam      = " + str(sec['geom']['diam']))
        if secName == "basal_9":
            if hasattr(cfg, 'basalDiam'):
                orig_diam = sec['geom']['diam']
                print("eeeS original basal_9 diam = " + str(orig_diam))
                sec['geom']['diam'] = cfg.basalDiam
                print("eeeS new basal_9 diam      = " + str(sec['geom']['diam']))


        if hasattr(cfg, 'allNaScale') or hasattr(cfg, 'dendNaScale'):
            if 'na' in sec['mechs']:
                orig_na = sec['mechs']['na']['gbar']
                if hasattr(cfg, 'dendNaScale') and (("basal" in secName) or ("axon" in secName)) and (cfg.dendNaScale != 1.0):
                    sec['mechs']['na']['gbar'] = list(np.array(orig_na, ndmin=1) * cfg.dendNaScale) 
                    print("Scaling (dend) gbar Na in %s by %s" % (secName, str(cfg.dendNaScale)))
                if hasattr(cfg, 'allNaScale') and (cfg.allNaScale != 1.0):
                    sec['mechs']['na']['gbar'] = list(np.array(orig_na, ndmin=1) * cfg.allNaScale)
                    print("Scaling (all)  gbar Na in %s by %s" % (secName, str(cfg.allNaScale)))
        
        if hasattr(cfg, 'allKScale') or hasattr(cfg, 'dendKScale'):
            
            if 'kv' in sec['mechs']:
                orig_kv = sec['mechs']['kv']['gbar']
                if hasattr(cfg, 'dendKScale') and (("basal" in secName)  or ("axon" in secName)) and (cfg.dendKScale != 1.0):
                    sec['mechs']['kv']['gbar'] = list(np.array(orig_kv, ndmin=1) * cfg.dendKScale)
                    print("Scaling (dend) gbar kv in %s by %s" % (secName, str(cfg.dendKScale)))
                if hasattr(cfg, 'allKScale') and (cfg.allKScale != 1.0):
                    sec['mechs']['kv']['gbar'] = list(np.array(orig_kv, ndmin=1) * cfg.allKScale)
                    print("Scaling (all) gbar kv in %s by %s" % (secName, str(cfg.allKScale))) 

            if 'kap' in sec['mechs']:
                orig_kap = sec['mechs']['kap']['gkabar']
                if hasattr(cfg, 'dendKScale') and (("basal" in secName) or ("axon" in secName)) and (cfg.dendKScale != 1.0):
                    sec['mechs']['kap']['gkabar'] = list(np.array(orig_kap, ndmin=1) * cfg.dendKScale)
                    print("Scaling (dend) gkabar kap in %s by %s" % (secName, str(cfg.dendKScale)))
                if hasattr(cfg, 'allKScale') and (cfg.allKScale != 1.0):
                    sec['mechs']['kap']['gkabar'] = list(np.array(orig_kap, ndmin=1) * cfg.allKScale)
                    print("Scaling (all) gbar kap in %s by %s" % (secName, str(cfg.allKScale)))

            if 'kad' in sec['mechs']:
                orig_kad = sec['mechs']['kad']['gkabar']
                if hasattr(cfg, 'dendKScale') and (("basal" in secName) or ("axon" in secName)) and (cfg.dendKScale != 1.0):
                    sec['mechs']['kad']['gkabar'] = list(np.array(orig_kad, ndmin=1) * cfg.dendKScale)
                    print("Scaling (dend) gkabar kad in %s by %s" % (secName, str(cfg.dendKScale)))
                if hasattr(cfg, 'allKScale') and (cfg.allKScale != 1.0):
                    sec['mechs']['kad']['gkabar'] = list(np.array(orig_kad, ndmin=1) * cfg.allKScale)
                    print("Scaling (all) gbar kad in %s by %s" % (secName, str(cfg.allKScale)))

            if 'kBK' in sec['mechs']:
                orig_kBK = sec['mechs']['kBK']['gpeak']
                if hasattr(cfg, 'dendKScale') and (("basal" in secName) or ("axon" in secName)) and (cfg.dendKScale != 1.0):
                    sec['mechs']['kBK']['gpeak'] = list(np.array(orig_kBK, ndmin=1) * cfg.dendKScale)
                    print("Scaling (dend) gpeak kBK in %s by %s" % (secName, str(cfg.dendKScale)))
                if hasattr(cfg, 'allKScale') and (cfg.allKScale != 1.0):
                    sec['mechs']['kBK']['gpeak'] = list(np.array(orig_kBK, ndmin=1) * cfg.allKScale)
                    print("Scaling (all) gpeak kBK in %s by %s" % (secName, str(cfg.allKScale)))

        if hasattr(cfg, 'allCaScale') or hasattr(cfg, 'dendCaScale'):

            if 'ca' in sec['mechs']:
                orig_ca = sec['mechs']['ca']['gbar']
                if hasattr(cfg, 'dendCaScale') and (("basal" in secName) or ("axon" in secName)) and (cfg.dendCaScale != 1.0):
                    sec['mechs']['ca']['gbar'] = list(np.array(orig_ca, ndmin=1) * cfg.dendCaScale)
                    print ("Scalling (dend) gbar ca in %s by %s" % (secName, str(cfg.dendCaScale)))
                if hasattr(cfg, 'allCaScale') and (cfg.allCaScale != 1.0):
                    sec['mechs']['ca']['gbar'] = list(np.array(orig_ca, ndmin=1) * cfg.allCaScale)
                    print("Scaling (all) gbar ca in %s by %s" % (secName, str(cfg.allCaScale)))

            if 'it' in sec['mechs']:
                orig_it = sec['mechs']['it']['gbar']
                if hasattr(cfg, 'dendCaScale') and (("basal" in secName) or ("axon" in secName)) and (cfg.dendCaScale != 1.0):
                    sec['mechs']['it']['gbar'] = list(np.array(orig_it, ndmin=1) * cfg.dendCaScale)
                    print ("Scalling (dend) gbar it in %s by %s" % (secName, str(cfg.dendCaScale)))
                if hasattr(cfg, 'allCaScale') and (cfg.allCaScale != 1.0):
                    sec['mechs']['it']['gbar'] = list(np.array(orig_it, ndmin=1) * cfg.allCaScale)
                    print("Scaling (all) gbar it in %s by %s" % (secName, str(cfg.allCaScale)))


        #end of if cell_label == "eeeS":

        if hasattr(cfg, 'ihScale'):
            if 'ih' in sec['mechs']:
                sec['mechs']['ih']['gbar'] = cfg.ihScale * sec['mechs']['ih']['gbar']

        if hasattr(cfg, 'RmScale'):
            if type(sec['mechs']['pas']['g']) == list:
                sec['mechs']['pas']['g'] = list((1.0/cfg.RmScale) * np.array(sec['mechs']['pas']['g']))
            elif type(sec['mechs']['pas']['g']) == float:
                sec['mechs']['pas']['g'] = (1.0/cfg.RmScale) * sec['mechs']['pas']['g']
            else:
                raise Exception("Error occurred adjusting RmScale in " + cell_label + ", " + secName)

        if hasattr(cfg, 'RaScale'):
            orig_ra = sec['geom']['Ra']
            sec['geom']['Ra'] = cfg.RaScale * sec['geom']['Ra']

        if hasattr(cfg, 'e_pas'):
            if 'pas' in sec['mechs']:
                sec['mechs']['pas']['e'] = cfg.e_pas

        if "soma" in secName:
            if hasattr(cfg, 'gpasSomaScale'):
                orig_gpas = sec['mechs']['pas']['g']
                sec['mechs']['pas']['g'] = cfg.gpasSomaScale * orig_gpas

        if hasattr(cfg, 'dendRaScale'):
            if "dend" in secName:
                orig_ra = sec['geom']['Ra']
                sec['geom']['Ra'] = cfg.dendRaScale * sec['geom']['Ra']

        if hasattr(cfg, 'dendRmScale'):
            if "dend" in secName:
                orig_gpas = sec['mechs']['pas']['g']
                sec['mechs']['pas']['g'] = (1/cfg.dendRmScale) * orig_gpas
                



###############################################################################
# Population parameters
###############################################################################

netParams.popParams['eeeD']= {'cellModel':'PFC_full', 'cellType':'eeeD', 'numCells':1}
netParams.popParams['eeeS']= {'cellModel':'PFC_simp', 'cellType':'eeeS', 'numCells':1}


###############################################################################
# Synaptic mechanism parameters
###############################################################################

netParams.synMechParams['NMDA'] = {'mod': 'NMDAeee', 'Cdur': cfg.CdurNMDAScale * 1.0, 'Alpha': cfg.NMDAAlphaScale * 4.0, 'Beta': cfg.NMDABetaScale * 0.0015, 'gmax': cfg.NMDAgmax}

netParams.synMechParams['AMPA'] = {'mod': 'AMPA', 'gmax': cfg.ratioAMPANMDA * cfg.NMDAgmax}

#h.gmax_NMDAeee = cfg.NMDAgmax 
#h.gmax_AMPA = cfg.ratioAMPANMDA * cfg.NMDAgmax

###############################################################################
# NetStim inputs
###############################################################################
if cfg.addNetStim:
    
    for nslabel in [k for k in dir(cfg) if k.startswith('NetStim')]:
        ns = getattr(cfg, nslabel, None)

        for cur_pop in ns['pop']:

            branch_length = netParams.cellParams[cur_pop]['secs'][ns['sec']]['geom']['L']
                
            if "ExSyn" in nslabel:
                cur_locs = np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numExSyns)
                cur_dists = branch_length * np.abs(cur_locs - cfg.synLocMiddle)
                cur_weights = (cfg.glutAmp * cfg.glutAmpExSynScale) * (1 - cur_dists * cfg.glutAmpDecay/100)
                cur_weights = [weight if weight > 0.0 else 0.0 for weight in cur_weights]
                cur_delays = cfg.initDelay + (cfg.exSynDelay * cur_dists)
                # print
                # print("ExSyn")
                # print("locs")
                # print(cur_locs)
                # print("dists")
                # print(cur_dists)
                # print("delays:")
                # print(cur_delays)
                # print("weights:")
                # print(cur_weights)
            
            elif "Syn" in nslabel:
                cur_locs = np.linspace(cfg.synLocMiddle-cfg.synLocRadius, cfg.synLocMiddle+cfg.synLocRadius, cfg.numSyns)
                cur_dists = branch_length * np.abs(cur_locs - cfg.synLocMiddle)
                cur_weights = cfg.glutAmp * (1 - cur_dists * cfg.glutAmpDecay/100)
                cur_weights = [weight if weight > 0.0 else 0.0 for weight in cur_weights]
                cur_delays = cfg.initDelay + (cfg.synDelay * cur_dists)
                # print
                # print("Syn")
                # print("locs")
                # print(cur_locs)
                # print("dists")
                # print(cur_dists)
                # print("delays:")
                # print(cur_delays)
                # print("weights:")
                # print(cur_weights)
            
            else:
                raise Exception("NetStim must have Syn or ExSyn in name")

            # add stim source
            netParams.stimSourceParams[nslabel] = {'type': 'NetStim', 'start': ns['start'], 'interval': ns['interval'], 'noise': ns['noise'], 'number': ns['number']}

            # connect stim source to target
            for i in range(len(ns['synMech'])):
                netParams.stimTargetParams[nslabel+'_'+cur_pop+'_'+ns['synMech'][i]] = \
                    {'source': nslabel, 'conds': {'pop': cur_pop}, 'sec': ns['sec'], 'synsPerConn': cfg.numSyns, 'loc': list(cur_locs), 'synMech': ns['synMech'][i], 'weight': list(cur_weights), 'delay': list(cur_delays)}

            
###############################################################################
# Current inputs (IClamp)
###############################################################################

if cfg.addIClamp:   
    for iclabel in [k for k in dir(cfg) if k.startswith('IClamp')]:
        ic = getattr(cfg, iclabel, None)  # get dict with params

        # add stim source
        netParams.stimSourceParams[iclabel] = {'type': 'IClamp', 'del': ic['start'], 'dur': cfg.durIClamp1, 'amp': cfg.ampIClamp1}
        
        for curpop in ic['pop']:
            netParams.stimTargetParams[iclabel+'_'+curpop] = \
                {'source': iclabel, 'conds': {'popLabel': ic['pop']}, 'sec': ic['sec'], 'loc': ic['loc']}



