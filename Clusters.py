from gurobipy import *
from random import randint
from simulacion import *

num_camiones = 8


def opti(estaciones):
    m = Model('cluster')
    m.update()
    excesos = {}
    vars = {}
    demands = {}
    for estacion in estaciones.values():
        excesos[estacion.num] = estacion.inventario - estacion.inv_manana
        vars[estacion.num] = {}
        demands[estacion.num] = {}
        for j in range(num_camiones):
            vars[estacion.num][j] = m.addVar(name='Z_{}_{}'.format(estacion.num, j), vtype=GRB.BINARY)
            m.update()
            demands[estacion.num][j] = m.addVar(name='d_{}_{}'.format(estacion.num, j), vtype=GRB.INTEGER)
            m.update()
    m.addConstrs(quicksum(vars[i][j] * demands[i][j] for i in vars) == 0 for j in vars[1])
    m.update()
    #m.addConstrs(quicksum(abs(demands[i][j]) for j in vars[1]) == abs(excesos[i]) for i in vars)
    m.addConstrs(quicksum(demands[i][j] for j in vars[1]) == excesos[i] for i in vars)
    m.update()
    m.addConstrs(quicksum(vars[i][j] for j in vars[1]) <= 1 for i in vars)
    m.update()
    m.setObjective(quicksum(
        vars[i][j] * vars[k][j] * estaciones['Estación {}'.format(i)].distancias_cuadrado[k] for i
        in vars for k in vars for j in vars[1]), GRB.MINIMIZE)
    m.update()
    m.optimize()
    for v in m.getVars():
        print(v.varName, v.x)


if __name__ == '__main__':
    estaciones = poblar()
    s = Simulador()
    s.estaciones = estaciones
    s.run()
    opti(s.estaciones)
