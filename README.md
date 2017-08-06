# distVec
Genera un vector distribuido en 1D, mediante particion de dominio, autoescalable

Programado en python 2.7
utiliza los modulos de numpy y mpi4py

genera una topologia para la comunicacion entre los procesadores
y dado un vector geometrico parte el dominio
se tiene que ingresar valores para el halo y el tamaño del vector a distribuir
