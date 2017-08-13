import numpy as np
from topology_1D import *
from distvec import *

# --------------- Parametros ---------------
noCeldasx = 11
halo = 1

# se instancia la topologia
topo = topology(noCeldasx, halo)

# imprime la topologia
topo.printTopology()

# si instancia la distribucion del vector
#bla = distvec(topo, vector)

# esta primera llamda del metodo printVec, imprime los vectores distribuidos pero
# sin comunicar los interface con los halos
#bla.printVec(topo)

# updatea los halos
#bla.updateHalo(topo)

# imprime el vector ya updateado
#bla.printVec(topo)
