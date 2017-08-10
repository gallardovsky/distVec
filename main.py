import numpy as np
from topology_1D import *
from distvec import *

topo = topology(noCeldasx=10,halo=1)

#topo.printTopology()

vector = np.zeros(10)

bla = distvec(topo, vector)

bla.printVec(topo)

bla.updateHalo(topo)

bla.printVec(topo)
