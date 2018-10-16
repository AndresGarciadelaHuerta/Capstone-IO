from gurobipy import *
from simulacion import *
# import numpy as np
# import matplotlib.pyplot as plt

num_camiones = 2
M = 3000


def opti(estaciones):
    m = Model('cluster')
    m.update()
    N = {}
    S = {}
    vars = {}
    n = {}
    s = {}
    distancias = {}
    for estacion in estaciones.values():
        valor = estacion.inv_manana - estacion.inventario
        N[estacion.num] = valor if valor > 0 else 0
        S[estacion.num] = -valor if valor < 0 else 0
        vars[estacion.num] = {}
        n[estacion.num] = {}
        s[estacion.num] = {}
        distancias[estacion.num] = {}
        for j in range(num_camiones):
            vars[estacion.num][j] = m.addVar(name='Z_{}_{}'.format(estacion.num, j), vtype=GRB.BINARY)
            m.update()
            n[estacion.num][j] = m.addVar(name='n_{}_{}'.format(estacion.num, j), vtype=GRB.INTEGER)
            s[estacion.num][j] = m.addVar(name='s_{}_{}'.format(estacion.num, j), vtype=GRB.INTEGER)
            m.update()
    # for estacion in estaciones.values():
    #     for est in estaciones.values():
    #         distancias[estacion.num][est.num] = {}
    #         for cam in range(num_camiones):
    #             distancias[estacion.num][est.num][cam] = m.addVar(
    #                 name='dist_{}_{}_{}'.format(estacion.num, est.num, cam))

    # m.addConstrs(distancias[i][j][cam] >= 0 for i in vars for j in vars for cam in vars[1])
    # m.addConstrs(
    #     distancias[est.num][est2.num][cam] >= vars[est.num][cam] * est.distancias_cuadrado[est2.num] - (
    #             1 - vars[est2.num][cam]) * est.distancias_cuadrado[est2.num] for est in
    #     estaciones.values() for est2 in estaciones.values() for cam in range(num_camiones))

    m.addConstrs(quicksum((n[i][j] - s[i][j]) for i in vars) == 0 for j in vars[1])
    m.update()
    m.addConstrs(M * vars[i][j] >= n[i][j] + s[i][j] for i in vars for j in vars[1])
    m.update()
    m.addConstrs(quicksum(n[i][j] for j in vars[1]) == N[i] for i in vars)
    m.update()
    m.addConstrs(quicksum(s[i][j] for j in vars[1]) == S[i] for i in vars)
    m.update()
    m.addConstrs(quicksum(vars[i][j] for i in vars) <= 50 for j in vars[1])
    m.update()
    m.addConstrs(s[i][j] >= 0 for i in vars for j in vars[1])
    m.update()
    m.addConstrs(n[i][j] >= 0 for i in vars for j in vars[1])
    m.update()
    # m.setObjective(quicksum(
    #     vars[i][j] * vars[k][j] * estaciones['Estación {}'.format(i)].distancias_cuadrado[k] for i
    #     in vars for k in vars for j in vars[1]), GRB.MINIMIZE)
    # m.setObjective(quicksum(quicksum(vars[i][j] for j in vars[1]) for i in vars), GRB.MINIMIZE)
    # m.setObjective(quicksum(
    #     distancias[est.num][est2.num][cam] for est in estaciones.values() for est2 in estaciones.values() for cam in
    #     vars[1]), GRB.MINIMIZE)

    m.setObjective(quicksum(
        vars[i][j] * vars[k][j] * estaciones['Estación {}'.format(i)].distancias_cuadrado[k] for i in vars for k in vars
        for j in vars[1]))
    m.update()
    m.Params.MIPGap = .05
    m.Params.timeLimit = 2 * 60
    m.optimize()
    resultados = {i: {} for i in range(num_camiones)}
    for z in m.getVars():
        if z.X > 0 and 'Z' in z.varName:
            lista = z.varName.split('_')
            est = int(lista[1])
            cam = int(lista[2])
            if est not in resultados[cam]:
                resultados[cam][est] = {}
            resultados[cam][est]['n'] = n[est][cam].X
            resultados[cam][est]['s'] = s[est][cam].X
            # print('{}->{}; necesidad {}; sobra {}'.format(z.varName, z.X, n[est][cam].X, s[est][cam].X))

    for grupo in resultados:
        print('*' * 20)
        print('GRUPO {}'.format(grupo))
        n = 0
        s = 0
        dist = 0
        x = []
        y = []
        for estacion in resultados[grupo]:
            print('Estacion {}; necesidad {}; sobra {}'.format(estacion, resultados[grupo][estacion]['n'],
                                                               resultados[grupo][estacion]['s']))
            n += resultados[grupo][estacion]['n']
            s += resultados[grupo][estacion]['s']
            # for est in resultados[grupo]:
            #     dist += distancias[estacion][est][grupo].X
            x.append(int(estaciones['Estación {}'.format(estacion)].x))
            y.append(int(estaciones['Estación {}'.format(estacion)].y))

        # x = np.array(x)
        # y = np.array(y)
        #
        # plt.scatter(x, y, s, c="y", alpha=.5,
        #             label="Luck")
        # plt.xlabel("Leprechauns")
        # plt.ylabel("Gold")
        # plt.legend(loc='upper left')
        # plt.show()

        print('Balance: {}'.format(n - s))
        print('Dist: {}'.format(dist))


if __name__ == '__main__':
    estaciones = poblar()
    s = Simulador()
    s.estaciones = estaciones
    s.run()
    opti(s.estaciones)
