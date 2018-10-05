from gurobipy import *
from clases import *
from parametros import *
from random import randint

m = Model('verga')
est = {}

for i in range(estaciones):
    est[i] = Estacion(i, randint(0, 100), randint(0, 100))
