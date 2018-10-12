"""
analyze.py 
Batch analysis for EEE project
contact: joe.w.graham@gmail.com
"""

import os
import sys
import matplotlib.pyplot as plt

try: 
    import batch_analysis
except:
    curpath = os.getcwd()
    while os.path.split(curpath)[1] != "sim":
        curpath = os.path.split(curpath)[0]
    sys.path.append(curpath)
    import batch_analysis


outputdir = "batch_figs"
if not os.path.exists(outputdir):
    os.mkdir(outputdir)

makepdf   = False

bap_branch = "basal_34"  #Bdend1

plt.ion()

batches = [dir for dir in os.listdir('batch_data') if os.path.isdir(os.path.join('batch_data', dir))]

batchfigs = os.listdir(outputdir)

batches1D = []
batches2D = []

for batch in batches:
    
    analyze_batch = True
    for batchfig in batchfigs:
        if batch in batchfig:
            analyze_batch = False

    if analyze_batch:
        
        batch_files = os.listdir(os.path.join('batch_data', batch))
        batch_files.sort()
        numunderscores = batch_files[0].split(batch)[-1].count("_") 
        # counts number of underscores in first Netpyne file, excluding those in batch name
        # pretty hacky, feel free to improve 
        if numunderscores == 1:
            batches1D.append(batch)
        elif numunderscores == 2:
            batches2D.append(batch)
        else:
            print("Batch '%s' is not 1D or 2D.  See eee/sim/batches/analyze.py." % (batch))
    else:
        print("Skipping batch : " + batch)



def plot_all():

    for batch in batches1D:
        print("Analyzing 1D batch: " + batch)
        batch_analysis.plot_vtraces_multicell(batch, celllabel="pop")
        try:
            #batch_analysis.plot_plat_comps(batch, cellIDs=None, expdata=True)
            batch_analysis.plot_plat_comps(batch, cellIDs="all", expdata=True)
        except:
            print("There was an error executing plot_plat_comps on batch: " + batch)
        if "glutAmp" in batch:
            batch_analysis.plot_antic_plateaus(batch)

    for batch in batches2D:
        print("Analyzing 2D batch: " + batch)
        batch_analysis.plot_vtraces(batch)
        if "bap" in batch:
            batch_analysis.plot_baps(batch, section=bap_branch)



if __name__ == '__main__':

    import time
    start = time.time()
    
    plot_all()

    if makepdf:
        import matplotlib.backends.backend_pdf
        pdf = matplotlib.backends.backend_pdf.PdfPages(os.path.join(outputdir, "batch_figures.pdf"))
        for i in plt.get_fignums():
            fig = plt.figure(i)
            pdf.savefig(fig)
        pdf.close()

    stop = time.time()
    print
    print("Completed eee/sim/batches/analyze.py")
    print("Duration (s): " + str(stop-start))