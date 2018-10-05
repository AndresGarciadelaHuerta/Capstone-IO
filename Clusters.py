from gurobipy import *
from random import randint
from


s = Simulador()
# Estaciones al final del dia
estaciones = s.run()
print(estaciones)
m = Model('verga')
est = {}
vars = {}
for i in range(estaciones - 1):
    ch = randint(-2, 2)
    Estacion.demanda += ch
    est[i] = Estacion(i, randint(0, 100), randint(0, 100), ch)
    vars[i] = {}
    for j in range(8):
        vars[i][j] = m.addVar(name='Z_{}_{}'.format(i, j), vtype=GRB.BINARY)


vars[estaciones - 1] = {}
est[estaciones - 1] = Estacion(estaciones - 1, randint(0, 100), randint(0, 100), -Estacion.demanda)
for j in range(8):
    vars[estaciones -1][j] = m.addVar(name='Z_{}_{}'.format(estaciones - 1, j), vtype=GRB.BINARY)

for i in est.values():
    i.distancias = {j: (est[j].x - i.x) ** 2 + (est[j].y - i.y) ** 2 for j in range(estaciones)}


for j in range(8):
    m.addConstr(quicksum(vars[i][j] for i in vars) == 0)
    #m.addConstr(3 <= quicksum(vars[i][j] for i in vars) <= 8)

for i in vars:
    m.addConstr(quicksum(vars[i][j] for j in range(8)) == 1)

m.setObjective(quicksum(vars[i][j] * vars[m][j] * est[i].distancias[m] for i in est for m in est for j in range(8)))

m.optimize()

for i in est:
    for j in range(8):
        print(vars[i][j].varName)
