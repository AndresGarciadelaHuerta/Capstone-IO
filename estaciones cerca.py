from gurobipy import *
from simulacion import *

num_camiones = 2
M = 3000


def opti(estaciones):
    m = Model('cluster')
    m.update()
    vars = {}
    distancias = {}
    for estacion in estaciones.values():
        vars[estacion.num] = {}
        distancias[estacion.num] = {}
        for j in range(num_camiones):
            vars[estacion.num][j] = m.addVar(name='Z_{}_{}'.format(estacion.num, j), vtype=GRB.BINARY)
            m.update()
    for estacion in estaciones.values():
        for est in estaciones.values():
            distancias[estacion.num][est.num] = {}
            for cam in range(num_camiones):
                distancias[estacion.num][est.num][cam] = m.addVar(
                    name='dist_{}_{}_{}'.format(estacion.num, est.num, cam))

    for estacion in estaciones.values():
        lista_ordenada = sorted(estacion.distancias_cuadrado.values())
        valor = lista_ordenada[50]
        # for est in estaciones.values():
        #     if estacion.distancias_cuadrado[est.num] > valor:
        #         m.addConstrs(vars[estacion.num][j] + vars[est.num][j] <= 1 for j in vars[1])

    m.addConstrs(quicksum(vars[i][j] for j in vars[1]) >= 1 for i in vars)

    m.addConstrs(distancias[i][j][cam] >= 0 for i in vars for j in vars for cam in vars[1])
    m.addConstrs(
        distancias[est.num][est2.num][cam] >= vars[est.num][cam] * est.distancias_cuadrado[est2.num] - (
                1 - vars[est2.num][cam]) * est.distancias_cuadrado[est2.num] for est in
        estaciones.values() for est2 in estaciones.values() for cam in range(num_camiones))
    #m.addConstrs(quicksum(vars[i][j] for i in vars) <= 12 for j in range(num_camiones))
    #m.addConstrs(quicksum(vars[i][j] for i in vars) >= 11 for j in range(num_camiones))

    m.update()
    m.setObjective(quicksum(
        distancias[est.num][est2.num][cam] for est in estaciones.values() for est2 in estaciones.values() for cam in
        vars[1]), GRB.MINIMIZE)
    m.update()
    m.Params.timeLimit = 120
    m.optimize()
    resultados = {i: {} for i in range(num_camiones)}
    for z in m.getVars():
        if z.X > 0 and 'Z' in z.varName:
            lista = z.varName.split('_')
            est = int(lista[1])
            cam = int(lista[2])
            resultados[cam][est] = 1

    for grupo in resultados:
        dist = 0
        print('*' * 20)
        print('GRUPO {}'.format(grupo))
        for estacion in resultados[grupo]:
            print('Estacion {}'.format(estacion))


if __name__ == '__main__':
    estaciones = poblar()
    opti(estaciones)
