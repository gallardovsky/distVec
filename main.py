import numpy as np
from topology_1D import *
from distvec import *
from mpi4py import MPI

noCeldasx = 10
halo = 1

topo = topology(noCeldasx,halo)

#topo.printTopology()

vector = np.zeros(10)

bla = distvec(topo, vector)

bla.updateHalo(topo)

bla.printVec()

