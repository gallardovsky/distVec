from topology_1D import *
from mpi4py import MPI
import numpy as np

class distvec:
	def __init__(self, ptrTopo, vector):
		comm = MPI.COMM_WORLD
		global comm

		self.vecPart = np.zeros(ptrTopo.vecRange)

# reparte el vector ingresado en los procesadores
		i = 0
		for j in range(ptrTopo.globalIterstart, ptrTopo.globalIterend):
			self.vecPart[i] = j
			i += 1

	def updateHalo(self, ptrTopo):
		comm = MPI.COMM_WORLD
		if ptrTopo.neighborW != -1:
# si tiene vecino W entonces envia la parte Interface hacia el vecino y espera recibir el interface del vecino
			comm.send(self.vecPart[ptrTopo.intFstartW:ptrTopo.intFendW], dest = ptrTopo.neighborW)
			self.vecPart[ptrTopo.hStartW:ptrTopo.hEndW] = comm.recv(source = ptrTopo.neighborW)
# si tiene vecino E entonces envia la parte Interface hacia el vecino
		if ptrTopo.neighborE != -1:
# pero primero recibe del vecino E (si tiene) y despues envia hacia el vecino (esto para evitar bloqueo)
			self.vecPart[ptrTopo.hStartE:ptrTopo.hEndE] = comm.recv(source = ptrTopo.neighborE)
			comm.send(self.vecPart[ptrTopo.intFstartE:ptrTopo.intFendE], dest = ptrTopo.neighborE)

	def printVec(self,ptrTopo):
		for i in range(ptrTopo.noProcs):
			comm.Barrier()
# -----------------------------imprime los vecPart de cada procesador
			if i == ptrTopo.rank:
				print 'Proc = ', ptrTopo.rank, ' vectorPartido = ', self.vecPart
