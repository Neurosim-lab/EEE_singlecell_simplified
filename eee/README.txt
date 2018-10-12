Author:  Joe Graham
E-mail:  joe.w.graham@gmail.com
Project: Embedded Ensemble Encoding (EEE) Model

This is the directory for the EEE project.  The plan is to utilize the NEURON simulator and start with morphologically detailed single cell models and reproduce plateau behavior.  Morphologically simplified cells will then be developed and explored.  Simplified cells will then be utilized in network simulations.

* File Structure

** setup.py                         : set up script for EEE project
** notebook.org                     : lab notebook for EEE project
** gif/                             : figures and attachments from notebook
** data/                            : location for input data
*** BS0284_lstimamp.npy             : pulse stim series amplitudes array
*** BS0284_tracedata_10KHz.npy      : experimental traces for amplitudes
** sim/                             : files for simulation
*** sim/batches_indcell             : code for single cell models
*** sim/batches_network             : code for network models
*** cells/                          : cell model files
**** eeeD.py                        : morphologically detailed cell model
**** eeeS.py                        : morphologically simplified cell model
**** FS3.hoc                        : inhibitory cell used in network model
*** mod/                            : mod files for NEURON simulator



* Setup and Execution

** Get a copy of the EEE directory

    The project lives in Neurosim at /u/graham/projects/eee
    To get an initial copy, run the following where you want the directory:
        % hg clone ssh://no.neurosim.downstate.edu://u/graham/projects/eee

** Set up directory structure and compile mod files

    Change to directory eee/ and enter: 
        % python setup.py

** Run and analyze single cell model batches

    Change to the batch directory of interest (e.g. cd eee/sim/batches_indcell/batch_20180424)
    Execute the following to run batch and analyze results:
        % ./runmybatches ; python analyze.py

    Output will be saved in dirs: `batch_data` and `batch_figs`

** Run and analyze network model batches

    Change to the batch directory of interest (e.g. cd eee/sim/batches_network/batch_20180424)
    Execute the following to run batch and analyze results:
        % ./runsim

    Output will be saved in dirs: `batch_data` and `batch_figs`

