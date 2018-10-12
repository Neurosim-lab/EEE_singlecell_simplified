import os
from neuron import h
import numpy as np


# # Following is code to measure the terminal path lengths of apical tree

# cur_dir = os.getcwd()
# os.chdir('/u/graham/projects/eee/sim/eee_detailed_model/netpyne/batch_comp/')
# execfile('instantiate.py')
# cell = sim.net.cells[0]
# secs = cell.secs
# h.distance(0, 0.5, sec=cell.secs['soma_0']['hSec'])
# term_length = []
# for key, item in secs.iteritems():
#     if "basal" in key:
#         print(key)
#         sec = item['hSec']
#         children = len(sec.children())
#         print(" children: " + str(children))
#         dists = []
#         for seg in sec.allseg():
#             dist = h.distance(seg.x, sec=sec)
#             print("  " + str(dist))
#             dists.append(dist)
#         if children == 0:
#             term_length.append(np.max(dists))
#             print("term_length = " + str(term_length))
# print
# print("##########" * 5)
# print
# print("mean terminal length = " + str(np.mean(term_length)))
# print
# print("##########" * 5)



# Following is code to count total nsegs in cells


cur_dir = os.getcwd()
os.chdir('/u/graham/projects/eee/sim/eee_detailed_model/netpyne/batch_rearr/')
execfile('instantiate.py')
eeeD = sim.net.cells[0]
eeeS = sim.net.cells[1]

Dsecs = eeeD.secs 
Dnsegs = []
Dsecnames = []

print
print("eeeD")
print("======================")
for key, item in Dsecs.iteritems():
    print(str(item['hSec'].nseg) + '\t cmps in: ' + key)
    Dsecnames.append(key)
    Dnsegs.append(item['hSec'].nseg)

print
print("======================")
print(" Num secs = " + str(len(Dsecnames)))
print(" Num cmps = " + str(np.sum(Dnsegs)))
print("======================")


Ssecs = eeeS.secs
Snsegs = []
Ssecnames = []

print
print("eeeS")
print("======================")
for key, item in Ssecs.iteritems():
    print(str(item['hSec'].nseg) + '\t cmps in: ' + key)
    Ssecnames.append(key)
    Snsegs.append(item['hSec'].nseg)

print
print("======================")
print(" Num secs = " + str(len(Ssecnames)))
print(" Num cmps = " + str(np.sum(Snsegs)))
print("======================")



