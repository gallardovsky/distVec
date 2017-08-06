from topology_1D import *
from mpi4py import MPI
import numpy as np

class distvec:
	def __init__(self, ptrTopo, vector):
		comm = MPI.COMM_WORLD
		self.vecPart = np.zeros(ptrTopo.vecRange)

		i = 0
		for j in range(ptrTopo.globalIterstart, ptrTopo.globalIterend):
			self.vecPart[i] = j
			i += 1
#		self.localIterstart = ptrTopo.localIterstart


#		for iterator in range(ptrTopo.globalIterstart, ptrTopo.globalIterend):
#			self.vecPart[self.localIterstart] = vector[iterator]

#			self.localIterstart += 1

#		if ptrTopo.haloW != 0:
#			for iterator in range(ptrTopo.haloW):
#				self.vecPart[iterator] = self.vecPart[ptrTopo.localIterstart + iterator]

#		if ptrTopo.haloE != 0:
#			for iterator in range(ptrTopo.haloE):
#				self.vecPart[ptrTopo.localIterend + iterator] = self.vecPart[(ptrTopo.localIterend - 1) + iterator]

#		print 'Proc = ', ptrTopo.rank, ' vectorPartido = ', self.vecPart
#		print self.vecPart

	def updateHalo(self, ptrTopo):
		comm = MPI.COMM_WORLD
		stat = 0

		self.hRecvW = np.zeros(1)
		self.hRecvE = np.zeros(1)

		self.iSendW = np.zeros(1)
		self.iSendE = np.zeros(1)

		self.iSendW[0] = self.vecPart[ptrTopo.intFstartW] 
		self.iSendE[0] = self.vecPart[ptrTopo.intFstartE]


		if ptrTopo.neighborW != -1:
			# si tiene vecino W entonces envia la parte Interface hacia el vecino y espera recibir el interface del vecino
			comm.send([self.iSendW, MPI.DOUBLE], dest = ptrTopo.neighborW)
			comm.recv([self.hRecvE, MPI.DOUBLE], source = ptrTopo.neighborW)
			# si tiene vecino E entonces envia la parte Interface hacia el vecino
		if ptrTopo.neighborE != -1:
			# pero primero recibe del vecino E (si tiene) y despues envia hacia el vecino (esto para evitar bloqueo)
			comm.recv([self.hRecvW, MPI.DOUBLE], source = ptrTopo.neighborE)			
			comm.send([self.iSendE, MPI.DOUBLE], dest = ptrTopo.neighborE)


	def printVec(self):
		print self.vecPart		

