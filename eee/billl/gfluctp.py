"""
checking seeds for Gfluctp.mod
import gfluctp as gp
imp.reload(gp)
"""
from neuron import h
import pylab as plt

h.load_file("stdrun.hoc")
soma = h.Section(name="soma")
soma.insert("pas")

vecl = [h.Vector() for x in range(10)]
vecl[0].record(h._ref_t)
vecl[1].record(soma(0.5)._ref_v)

h.v_init=-70
h.tstop=100
gfl = h.Gfluctp(0.5,sec=soma)
gfl.seed1, gfl.seed2, gfl.seed3 = 18, 27, 44

gfl.std_e = 0.012
gfl.g_e0  = 0.0121
gfl.tau_i = 10.49
gfl.tau_e = 2.728
gfl.std_i = 0.0264
gfl.g_i0  = 0.0573
gfl.E_e   = -40
gfl.E_i   = -80

if __name__ == '__main__':
  h.run()
  plt.plot(vecl[0], vecl[1])
  gfl.seed1, gfl.seed2, gfl.seed3 = 182, 272, 442
  h.run()
  plt.plot(vecl[0], vecl[1])
  gfl.seed1, gfl.seed2, gfl.seed3 = 18, 27, 44
  h.run()
  plt.plot(vecl[0], vecl[1])
  plt.show()
