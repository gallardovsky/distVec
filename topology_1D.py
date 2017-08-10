import numpy as np
from mpi4py import MPI

class topology:
	def __init__(self,noCeldasx, halo):
		global comm
		comm = MPI.COMM_WORLD

		self.noProcs = comm.Get_size()
		self.rank = comm.Get_rank()
		self.offSet = np.zeros(self.noProcs)
		self.bufferComm = np.ones(1)
		self.ownedAll = 0

#		self.owned = np.zeros(1)

# ------------------------------------------------------------
# cantidad de celdas por proc
		if noCeldasx % self.noProcs == 0:
			self.owned = noCeldasx / self.noProcs

		elif (noCeldasx % self.noProcs != 0) and (self.rank < (noCeldasx % self.noProcs)):
			self.owned = noCeldasx / self.noProcs + 1

		else:
			self.owned = noCeldasx / self.noProcs

# ------------------------------------------------------------
# Iteradores y comunicacion
		self.bufferComm[0] = self.owned
		if self.rank == 0:

			self.neighborW = -1
			self.neighborE = self.rank + 1

			self.haloX = halo

			self.vecRange = self.owned + self.haloX

			self.lIterstart = 0
			self.lIterend = self.owned

#			self.offSet = comm.Allgather([self.owned, MPI.INT])
			comm.Allgather([self.bufferComm, MPI.INT],[self.offSet, MPI.INT])
#			comm.Allgather([self.owned, MPI.INT])

# convencion Izquierda-derecha-arriba-abajo-enfrente-atras

			# son iguales para no hay halo en W
			self.hStartW = self.lIterend
			self.hEndW = self.hStartW

			self.hStartE =  self.hEndW
			self.hEndE = self.hStartE + halo

			self.intFstartW =  self.lIterstart
			self.intFendW = self.intFstartW

			self.intFstartE = self.lIterend - halo
			self.intFendE = self.lIterend

# -------------------------------------------
			for i in range(self.rank):
				self.ownedAll += int(self.offSet[i])

			self.globalIterstart = self.lIterstart + self.ownedAll
			self.globalIterend = self.globalIterstart + self.owned



		elif (self.rank != 0) and (self.rank != (self.noProcs - 1)):
			self.neighborW = self.rank - 1
			self.neighborE = self.rank + 1

			self.haloX = 2*halo

			self.vecRange = self.owned + self.haloX

			self.lIterstart = 0
			self.lIterend = self.owned

#			self.offSet = comm.Allgather([self.owned, MPI.INT])
			comm.Allgather([self.bufferComm, MPI.INT],[self.offSet, MPI.INT])
#			comm.Allgather([self.owned, MPI.INT])

			self.hStartW = self.lIterend
			self.hEndW = self.hStartW + halo
			self.hStartE =  self.hEndW
			self.hEndE = self.hStartE + halo

			self.intFstartW =  self.lIterstart
			self.intFendW = self.intFstartW + halo
			self.intFstartE = self.lIterend - halo
			self.intFendE = self.lIterend

			for i in range(self.rank):
				self.ownedAll += int(self.offSet[i])


			self.globalIterstart = self.lIterstart + self.ownedAll
			self.globalIterend = self.globalIterstart + self.owned


		elif self.rank == (self.noProcs - 1):
			self.neighborW = self.rank - 1
			self.neighborE = -1

			self.haloX = halo

			self.vecRange = self.owned + self.haloX

			self.lIterstart = 0
			self.lIterend = self.owned

#			self.offSet = comm.Allgather([self.owned, MPI.INT])
			comm.Allgather([self.bufferComm, MPI.INT],[self.offSet, MPI.INT])
#			comm.Allgather([self.owned, MPI.INT])

			self.hStartW = self.lIterend
			self.hEndW = self.hStartW + halo
			self.hStartE =  self.hEndW
			self.hEndE = self.hStartE

			self.intFstartW =  self.lIterstart
			self.intFendW = self.intFstartW + halo
			self.intFstartE = self.lIterend
			self.intFendE = self.intFstartE

			for i in range(self.rank):
				self.ownedAll += int(self.offSet[i])

			self.globalIterstart = self.lIterstart + self.ownedAll
			self.globalIterend = self.globalIterstart + self.owned

#		print 'offSet = ', self.offSet

	def printTopology(self):
		for i in range(self.noProcs):
			comm.Barrier()
			if self.rank == i:
				print ''
				print '-----Proc = ',self.rank,'----------'
				print 'neighborW = ', self.neighborW
				print 'neighborE = ', self.neighborE
				print 'owned = ', self.owned
				print 'vecRange = ',self.vecRange
				print '--------Iter locales---------'
				print 'lIterstart = ', self.lIterstart
				print 'lIterend = ', self.lIterend
				print '---------Iter Halos--------'
				print 'hStartW = ', self.hStartW
				print 'hEndW = ', self.hEndW
				print 'hStartE =', self.hStartE
				print 'hEndE =', self.hEndE
#				print '---------Interface-----------'
#				print 'intFstartW = ',  self.intFstartW
#				print 'intFendW = ', self.intFendW
#				print 'intFstartE = ', self.intFstartE
#				print 'intFendE = ', self.intFendE
				print '----------Iter Globales --------'
				print 'globalIterstart = ', self.globalIterstart
				print 'globalIterend = ', self.globalIterend
